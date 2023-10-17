"""通用的 report data 构造器，支持 校、区、市、省、全国级别的通用报告数据构造"""
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Optional, ClassVar, Any, Set

import pandas as pd
import pendulum

from hawa.base.db import DbUtil, RedisUtil
from hawa.base.decos import log_func_time
from hawa.base.errors import NoCasesError
from hawa.common.query import DataQuery
from hawa.common.utils import GradeData, CaseData, Measurement, Util
from hawa.config import project


class MetaCommomData(type):
    def __new__(cls, name, bases, attrs):
        attrs['db'] = DbUtil()
        attrs['redis'] = RedisUtil()
        attrs['query'] = DataQuery()
        return super().__new__(cls, name, bases, attrs)


@dataclass
class CommonData(metaclass=MetaCommomData):
    # 构造单位
    meta_unit_type: Optional[str] = ''  # class/school/group/district/city/province/country
    meta_unit_id: Optional[int] = None
    meta_unit: Optional[Any] = None
    grade: Optional[int] = None  # 必填

    different_mode: Optional[str] = 'default'  # 用于区分数据的不同模式 default默认/xx新乡

    # 时间目标
    target_year: Optional[int] = None
    last_year_num: Optional[int] = None
    is_load_last: bool = True  # 仅计算往年数据时 为 False

    is_load_all: bool = True  # 加载全部数据

    # 卷子
    test_type: str = ''
    test_types: list = field(default_factory=list)
    code_word_list: Set[str] = field(default=set)  # 卷子使用指标的词表，详见继承

    # meta class tool
    db: ClassVar[DbUtil] = None
    redis: ClassVar[RedisUtil] = None
    query: ClassVar[DataQuery] = None

    # 原始数据

    school_ids: list[int] = field(default_factory=list)
    schools: pd.DataFrame = field(default_factory=pd.DataFrame)

    codebook: pd.DataFrame = field(default_factory=pd.DataFrame)

    cases: pd.DataFrame = field(default_factory=pd.DataFrame)
    case_ids: list[int] = field(default_factory=list)
    case_project_ids: Counter = field(default_factory=Counter)

    answers: pd.DataFrame = field(default_factory=pd.DataFrame)
    item_codes: pd.DataFrame = field(default_factory=pd.DataFrame)

    students: pd.DataFrame = field(default_factory=pd.DataFrame)
    student_ids: list[int] = field(default_factory=list)
    student_count: Optional[int] = None

    item_ids: Optional[set[int]] = None
    items: Optional[pd.DataFrame] = None

    # 辅助工具
    grade_util: Optional[GradeData] = None
    case_util: Optional[CaseData] = None
    rank_names = ['待提高', '中等', '良好', '优秀']
    measurement = Measurement()

    # 计算数据
    final_answers: pd.DataFrame = field(default_factory=pd.DataFrame)
    final_scores: pd.DataFrame = field(default_factory=pd.DataFrame)
    grade_final_scores: pd.DataFrame = field(default_factory=pd.DataFrame)

    # 去年全国数据
    last_year = None
    last_year_code_scores: Optional[pd.DataFrame] = field(default_factory=pd.DataFrame)

    def __post_init__(self):
        # 初始化数据
        if self.is_load_all:
            self.load_all_data()

            # 构建辅助工具
            self._to_build_helper()

            # 计算数据
            count_functions = [i for i in dir(self) if i.startswith('_to_count_')]
            for func in count_functions:
                getattr(self, func)()
                project.logger.info(f'count {func} success')

        else:
            self.load_less_data()
            self._to_build_helper()

    def _to_init_a_meta_unit(self):
        try:
            self.meta_unit = self.query.query_unit(self.meta_unit_type, str(self.meta_unit_id))
        except TypeError as e:
            project.logger.warning(f'query_unit error: {e}')
            self.__class__.query = DataQuery()
            self.meta_unit = self.query.query_unit(self.meta_unit_type, str(self.meta_unit_id))
        if '百万' in self.meta_unit.name:
            self.different_mode = 'xx'

    def _to_init_b_time(self):
        if not self.target_year:
            self.target_year = pendulum.now().year
        self.last_year_num = self.target_year - 1
        project.logger.info(f'target_year: {self.target_year}')

    def _to_init_c_schools(self):
        if self.school_ids:
            self.schools = self.query.query_schools_by_ids(self.school_ids)
        else:
            match self.meta_unit_type:
                case 'country':
                    self.schools = self.query.query_schools_all()
                case 'province':
                    self.schools = self.query.query_schools_by_startwith(self.meta_unit_id // 10000)
                case 'city':
                    self.schools = self.query.query_schools_by_startwith(self.meta_unit_id // 100)
                case 'district':
                    self.schools = self.query.query_schools_by_startwith(self.meta_unit_id)
                case 'school' | 'class' | 'student':
                    self.schools = self.query.query_schools_by_ids([self.meta_unit_id])
                case 'group':
                    self.schools = self.query.query_schools_by_group_id(group_id=self.meta_unit_id)
                case _:
                    raise ValueError(f'unknown meta_unit_type: {self.meta_unit_type}')
            self.school_ids = self.schools['id'].tolist()
        project.logger.debug(f'schools: {len(self.schools)}')

    def _to_init_d_cases(self, is_cleared: bool = True):
        start_stamp = pendulum.datetime(self.target_year, 1, 1)
        end_stamp = pendulum.datetime(self.target_year + 1, 1, 1)
        start_stamp_str = start_stamp.format(project.format)
        end_stamp_str = end_stamp.format(project.format)

        papers = self.query.query_papers(test_types=self.test_types, test_type=self.test_type)
        paper_ids = papers['id'].tolist()

        self.cases = self.query.query_cases(
            school_ids=self.school_ids,
            paper_ids=paper_ids,
            valid_to_start=start_stamp_str,
            valid_to_end=end_stamp_str,
            is_cleared=is_cleared
        )
        if self.cases.empty:
            raise NoCasesError(f'no cases:{self.meta_unit} {self.school_ids}')
        self.case_ids = self.cases['id'].tolist()
        self.case_project_ids = Counter(self.cases['project_id'].tolist())
        self.school_ids = self.cases['school_id'].unique().tolist()
        project.logger.debug(f'cases: {len(self.cases)}')

        if self.grade:
            self.cases = self.cases.loc[self.cases['id'] % 100 == self.grade, :]
            self.case_ids = self.cases['id'].tolist()
            self.case_project_ids = Counter(self.cases['project_id'].tolist())
            project.logger.debug(f'cases: {len(self.cases)}')
        if len(self.cases) == 0:
            raise NoCasesError(f'grade {self.grade} cases is empty')

    @log_func_time
    def _to_init_e_answers(self):
        self.answers = self.query.query_answers(case_ids=self.case_ids)
        project.logger.debug(f'answers: {len(self.answers)}')

    def _to_init_f_students(self):
        self.student_ids = set(self.answers['student_id'].tolist())
        student_id_list = list(self.student_ids)
        self.students = self.query.query_students(student_id_list, mode=self.different_mode)
        self.student_count = len(self.students)
        project.logger.debug(f'students: {self.student_count}')

    def _to_init_g_items(self):
        self.item_ids = set(self.answers['item_id'].drop_duplicates())
        self.items = self.query.query_items(self.item_ids)
        project.logger.debug(f'items: {len(self.items)}')

    def _to_init_y_item_codes(self):
        word_list = self.code_word_list | {'other'} if len(self.code_word_list) == 1 else self.code_word_list
        self.item_codes = self.query.query_item_codes(self.item_ids, categories=word_list)

    def _to_init_z_dim_field(self):
        cache_key = f"{project.PROJECT}:codebook"
        if data := self.redis.conn.get(cache_key):
            self.codebook = pd.DataFrame.from_records(json.loads(data))
        else:
            self.codebook = self.query.query_codebook()
            cache_data = self.codebook.to_json(orient='records', force_ascii=False)
            self.redis.conn.set(cache_key, cache_data, ex=60 * 60 * 24 * 7)

    def _to_build_helper(self):
        self.grade = GradeData(case_ids=self.case_ids)
        self.case = CaseData(cases=self.cases)
        self.grade_util = GradeData(case_ids=self.case_ids)
        self.case_util = CaseData(cases=self.cases)

    @log_func_time
    def _to_count_a_final_answers(self):
        items = {k: {} for k in self.code_word_list}
        # code-dimension/field  ~  item_id  ~ code   name
        project.logger.debug(f"{self.code_word_list=}")
        for (item_id, category), codes in self.item_codes.groupby(['item_id', 'category']):
            if category in self.code_word_list:
                for _, code_data in codes.iterrows():
                    items[category][item_id] = code_data['name']

        data = pd.merge(
            self.answers, self.students.loc[:, ['id', 'gender', 'nickname']],
            left_on='student_id', right_on='id'
        )
        project.logger.debug(f"ans merge students {len(data)}")
        # inner 时，final_answers 和 answers 数目不等：final_answers 过滤掉了 没有 code_word_list（维度领域或其他）的题目
        # outer 时，数目相等，不过滤任何题目
        data = pd.merge(data, self.item_codes, left_on='item_id', right_on='item_id', how='inner')

        project.logger.debug(f'merge success {data.shape}')

        self.set_data_extra(d=data, set_grade=True, set_class=True)

        data['username'] = data['nickname']
        for code_word in self.code_word_list:
            data[code_word] = data.item_id.apply(lambda x: items[code_word][x])
        self.final_answers = data.drop_duplicates(subset=['case_id', 'student_id', 'item_id'])
        project.logger.debug(f'final_answers: {len(self.final_answers)}')

    @log_func_time
    def _to_count_b_final_scores(self):
        self.final_scores = self.count_final_score(answers=self.final_answers)
        project.logger.debug(f'final_scores: {len(self.final_scores)}')

    @staticmethod
    def count_level(score, mode: str = 'f'):
        assert mode in ('f', 'r'), 'only support feedback or report'
        if score >= 90:
            a = 'A'
        elif score >= 80:
            a = 'B'
        elif score >= 60:
            a = 'C'
        else:
            a = 'D'
        key = "RANK_LABEL" if mode == 'r' else 'FEEDBACK_LEVEL'
        return project.ranks[key][a]

    def count_final_score(self, answers: pd.DataFrame):
        records = []
        for student_id, group in answers.groupby('student_id'):
            score = group.score.mean() * 100
            record = {
                "student_id": student_id,
                "username": group['username'].tolist()[0],
                "grade": group['grade'].tolist()[0],
                "gender": group['gender'].tolist()[0],
                "score": score,
                "level": self.count_level(score),
            }
            records.append(record)
        return pd.DataFrame.from_records(records)

    def get_last_year_miss(self, grade: int):
        key = f'{project.REDIS_PREFIX}{self.last_year_num}:data'
        data = json.loads(self.redis.conn.get(key))
        try:
            grade_data = data[str(grade)]
        except KeyError:
            for i in range(1, grade):
                temp_grade = grade - i
                grade_data = data.get(str(temp_grade))
                if grade_data:
                    break
            else:
                grade_data = data[str(3)]

        grade_data['people']['grade'] = f"{grade}年级"
        for k, v in grade_data['code'].items():
            grade_data['code'][k]['grade'] = grade
        return grade_data

    def sort_rank(self, name: str) -> int:
        order_map = dict(zip(self.rank_names, range(0, 4)))
        return order_map[name]

    def count_dim_field_ranks(self, item_code: str):
        """
        计算维度、领域的 ranks 分级比例
        :param item_code:dimision or field
        """
        r = defaultdict(list)
        codes = set()
        for (s, c), student_code_group in self.final_answers.groupby(['student_id', item_code]):
            s_c_score = Util.format_num(student_code_group.score.mean() * 100, project.precision)
            codes.add(c)
            r[c].append(s_c_score)
        codes = list(codes)
        df = pd.DataFrame.from_records(r)
        res = {}
        for c in codes:
            row = df[c]
            base_row_ranks = {k: 0 for k in self.rank_names}
            count_row_ranks = pd.cut(
                row, bins=[0, 60, 80, 90, 100], labels=self.rank_names,
                right=False, include_lowest=True,
            ).value_counts().to_dict()
            sum_value = sum(count_row_ranks.values())
            row_ranks = {k: Util.format_num(v / sum_value * 100, project.precision) for k, v in
                         (base_row_ranks | count_row_ranks).items()}
            res[c] = row_ranks
        code_map = self.get_dim_field_order(key=item_code)
        return {
            "data": res, "codes": sorted(codes, key=lambda x: code_map[x]),
            "legend": self.rank_names,
        }

    def count_sub_units(self, target_level: str = 'school'):
        """查询下辖单位"""
        match target_level:
            case 'school':
                return self.school_ids
            case 'district':
                return {i // (10 ** 4) for i in self.school_ids}
            case _:
                raise ValueError(f"target_level: {target_level} not support")

    def get_cascade_students(self):
        """年级/班级/学生嵌套"""
        data = self.final_scores
        self.set_data_extra(d=data, set_grade=False, set_class=True)
        res = []
        for grade, grade_group in data.groupby('grade'):
            grade_row = {
                'label': f'{grade}年级', 'value': grade,
                'children': [], "is_leaf": False
            }
            for cls, cls_group in grade_group.groupby('cls'):
                cls_row = {
                    'label': f'{cls}班', 'value': int(cls),
                    'children': [], "is_leaf": False
                }
                for _, student_g_row in cls_group.iterrows():
                    student_row = {
                        'label': student_g_row['username'],
                        'value': str(student_g_row['student_id']),
                        "is_leaf": True
                    }
                    cls_row['children'].append(student_row)
                if not cls_row['children']:
                    cls_row['is_leaf'] = True
                grade_row['children'].append(cls_row)
            if not grade_row['children']:
                grade_row['is_leaf'] = True
            res.append(grade_row)
        return res

    def get_cascade_schools_from_province(self):
        """省-市-区县-学校的 cascade 数据"""
        sch_ids = self.school_ids
        province_ids = {i // (10 ** 8) * 10000 for i in sch_ids}
        city_ids = {i // (10 ** 6) * 100 for i in sch_ids}
        district_ids = {i // (10 ** 4) for i in sch_ids}
        location_ids = province_ids | city_ids | district_ids
        locations = self.query.query_locations(list(location_ids))
        schools = self.schools
        location_map = {lo['id']: lo for _, lo in locations.iterrows()}
        school_map = {sch['id']: sch for _, sch in schools.iterrows()}
        res = []
        for p_id in province_ids:
            p = location_map[p_id]
            p_row = {
                'label': p['name'], 'value': p['id'], 'children': [], "is_leaf": False
            }
            if p_id not in project.municipality_ids:
                for c_id in city_ids:
                    if c_id // 10000 * 10000 != p_id:
                        continue
                    c = location_map[c_id]
                    c_row = {
                        'label': c['name'], 'value': c['id'], 'children': [], "is_leaf": False
                    }
                    for d_id in district_ids:
                        if d_id // 100 * 100 != c_id:
                            continue
                        d = location_map[d_id]
                        d_row = {
                            'label': d['name'], 'value': d['id'], 'children': [], "is_leaf": False
                        }
                        for s_id in sch_ids:
                            if s_id // 10000 != d_id:
                                continue
                            s = school_map[s_id]
                            s_row = {
                                'label': s['name'], 'value': s['id'], "is_leaf": True
                            }
                            d_row['children'].append(s_row)
                        c_row['children'].append(d_row)
                    p_row['children'].append(c_row)
                res.append(p_row)
            else:
                for d_id in district_ids:
                    if d_id // 10000 * 10000 != p_id:
                        continue
                    d = location_map[d_id]
                    d_row = {
                        'label': d['name'], 'value': d['id'], 'children': [], "is_leaf": False
                    }
                    for s_id in sch_ids:
                        if s_id // 10000 != d_id:
                            continue
                        s = school_map[s_id]
                        s_row = {
                            'label': s['name'], 'value': s['id'], "is_leaf": True
                        }
                        d_row['children'].append(s_row)
                    p_row['children'].append(d_row)
                res.append(p_row)
        return res

    def get_dim_field_order(self, key: str):
        """获取维度/领域顺序的映射
        :param key: dimension/field
        """
        data = self.codebook.loc[self.codebook['category'] == key, :]
        order_map = {i['name']: i['order'] for _, i in data.iterrows()}
        if '其他' in order_map.keys():
            del order_map['其他']
        return order_map

    def load_less_data(self):
        init_functions = [i for i in dir(self) if i.startswith('_to_init_')]
        for func in init_functions:
            if '_to_init_e_' in func:
                break
            getattr(self, func)()

    def load_all_data(self):
        init_functions = [i for i in dir(self) if i.startswith('_to_init_')]
        for func in init_functions:
            getattr(self, func)()
            project.logger.info(f'load data {func} success')

    def set_data_extra(self, d: pd.DataFrame, set_grade: bool = True, set_class: bool = True):
        """为 数据 设置不同模式下的 extra 字段"""
        if self.different_mode == 'xx':
            user_classes = {}
            user_grades = {}
            for _, row in self.students.iterrows():
                extra = json.loads(row['extra'])
                user_grades[row['id']] = extra.get('grade', 0)
                user_classes[row['id']] = extra.get('class', 0)
            if set_grade:
                d['grade'] = d['student_id'].apply(lambda x: user_grades.get(x, ''))
            if set_class:
                d['cls'] = d['student_id'].apply(lambda x: user_classes.get(x, ''))
        else:
            if set_grade:
                d['grade'] = d['case_id'].apply(lambda x: x % 100)
            if set_class:
                d['cls'] = d['student_id'].apply(lambda x: int(str(x)[13:15]))
