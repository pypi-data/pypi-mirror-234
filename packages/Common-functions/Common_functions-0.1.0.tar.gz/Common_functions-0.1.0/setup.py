from setuptools import setup,find_packages
from typing import List
REQUIREMENT_FILE_NAME="requirements.txt"
Project_Name="Common_functions"
Version="0.1.0"
AUTHOR="Jyoti"
DESCRIPTION="Mini Project on creating a library for all the program in 5 syllabus"







setup(

    name=Project_Name,
    version=Version,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),

    long_description="This is simple project to create a library",
    requires=["pandas","numpy","ctypes","sklearn","playsound","gtts","torch"],
    url="https://github.com/Jyotijaladi/Common_functions",

    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
)

