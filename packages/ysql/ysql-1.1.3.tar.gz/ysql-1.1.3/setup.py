import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="ysql",
    version="1.1.3",
    author="dfqxhhh",
    author_email="dfqxhhh@163.com",
    description="based on android room, developed a better sqlite frame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/darlingxyz/ysql",
    packages=['ysql'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

