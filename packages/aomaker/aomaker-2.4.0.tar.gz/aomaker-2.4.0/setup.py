# --coding:utf-8--
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="aomaker",
    version="2.4.0",
    author="ancientone",
    author_email="listeningsss@163.com",
    description="An api testing framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ae86sen/aomaker",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Jinja2',
        'jsonpath',
        'loguru',
        'PyMySQL',
        'pytest',
        'PyYAML',
        'requests',
        'allure-pytest==2.8.24',
        'pydantic==1.10.2',
        'mitmproxy',
        'colorlog',
        'jsonschema',
        'genson',
        'click==8.1.3',
        'emoji==2.2.0',
        'click-help-colors==0.9.1',
        'tenacity==8.2.3'

    ],
    entry_points={
        'console_scripts': [
            'amake=aomaker.cli:main_make_alias',
            'arun=aomaker.cli:main_arun_alias',
            'arec=aomaker.cli:main_record_alias',
            'aomaker=aomaker.cli:main',
        ]
    }
)