from setuptools import setup, find_packages

from pkg_resources import parse_requirements
from pathlib import Path

requirements_path = str(Path(__file__).resolve().parent / 'promptmanager/requirements.txt')
with open(requirements_path, encoding="utf-8") as fp:
    install_requires = [str(requirement) for requirement in parse_requirements(fp)]

setup(
    name='PromptManager',
    version='0.0.10',
    author='zhangdi',
    author_email='zhangdi@zetyun.com',
    description='',
    url='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': ['pmctl=promptmanager.pmctl.main:main'],
    }

)
