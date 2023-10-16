from setuptools import setup, find_packages

setup(
    name="sqlite_dao_ext",
    version="0.1.5",
    description="Sqlite3 Dao",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["dataclasses", "typing"],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
