import pendulum

from hawa.common.query import DataQuery
from hawa.config import project
from test.mock import prepare_test

prepare_test()

dq = DataQuery()


def test_query_unit():
    rows = [
        ['school', 1101019055], ["district", 110101], ["city", 331100],
        ["province", 110000], ["country", 0]]
    for r in rows:
        res = dq.query_unit(*r)
        assert res.id == r[1]


def test_query_schools():
    rows = [[1101019055], [1101019055, 1101019056]]
    for r in rows:
        res = dq.query_schools_by_ids(r)
        assert len(res) >= 1

    startwith = 110101
    res = dq.query_schools_by_startwith(startwith)
    assert len(res) >= 1

    res = dq.query_schools_all()
    assert len(res) >= 1


def test_query_papers():
    conditions = [
        {'test_type': 'mht'}, {'test_type': 'psychological'},
        {'test_types': ['publicWelfare', 'ZjpublicWelfare']}
    ]
    for c in conditions:
        res = dq.query_papers(**c)
        assert len(res) >= 1


def test_query_cases():
    target_year = 2021
    start_stamp = pendulum.datetime(target_year, 1, 1)
    end_stamp = pendulum.datetime(target_year + 1, 1, 1)
    start_stamp_str = start_stamp.format(project.format)
    end_stamp_str = end_stamp.format(project.format)

    papers = dq.query_papers(test_types=['publicWelfare', 'ZjpublicWelfare'])
    paper_ids = [i[1]['id'] for i in papers.iterrows()]

    school_ids = [3707850002, 3707030003]
    res = dq.query_cases(school_ids, paper_ids, start_stamp_str, end_stamp_str, is_cleared=True)
    assert len(res) >= 1
    res = dq.query_cases(school_ids[:1], paper_ids, start_stamp_str, end_stamp_str, is_cleared=True)
    assert len(res) >= 1


def test_query_answers():
    conditions = [
        [2209250708],
        [2209250708, 2209250803]
    ]
    for c in conditions:
        res = dq.query_answers(c)
        assert len(res) >= 1


def test_query_students():
    case_ids = 2210240104
    answers = dq.query_answers([case_ids])
    res = dq.query_students(answers.student_id.tolist())
    assert len(res) >= 1


def test_query_items():
    res = dq.query_items([1, 401])
    assert len(res) >= 1


def test_query_item_codes():
    res = dq.query_item_codes([1, 401], categories=['dimension', 'field'])
    assert len(res) >= 1
