import setuptools

from verion_text import text

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()
    for version, description in text:
        long_description += f"\n- {version} {description}"

with open("requirements.txt", "r", encoding='utf8') as fh:
    requires = fh.read().replace('==', '>=')

setuptools.setup(
    name="HawaData",
    version=text[-1][0],
    author="Steven Wang",
    author_email="brightstar8284@icloud.com",
    description="Use For Unified Hawa Data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StevenLianaL/HawaData",
    # packages=setuptools.find_packages(exclude=["tests*"]),
    # install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
