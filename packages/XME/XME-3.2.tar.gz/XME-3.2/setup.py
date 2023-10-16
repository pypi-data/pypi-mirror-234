import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="XME",
    version="3.2",
    author="Junxiang Huang & Weihui Li",
    author_email="huangjunxiang@mail.ynu.edu.cn",
    description="This is a Python interface for process pool establishment, and result collection based on the Multiprocessing module.",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    url="https://github.com/wacmkxiaoyi/Xenon-Multiprocessing-Engine", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)