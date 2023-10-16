from setuptools import setup, find_packages

REQUIRED = ["PyQt5", "pyquery", "qasync", "jinja2"]
setup(
    name = "mvvmQt" ,
    version = "0.35.4" ,
    description = "write qt like html" ,
    author = "Norman",
    author_email = "332535694@qq.com",
    url = "https://gitee.com/zhiyang/py-qt-dom",
    packages = find_packages(),
    python_requires = '>=3.8.10',
    install_requires = REQUIRED
)