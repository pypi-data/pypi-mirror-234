from setuptools import setup, find_packages

setup(
	name="py-dbclients",
	version="0.1.1",
	packages=find_packages(),
    install_requires=[

    ],
    extras_require={
        "all": ["redis[hiredis]", "pymysql", "aiomysql"],
        "redis": ["redis[hiredis]"],
        "pymysql": ["pymysql"],
        "aiomysql": ["aiomysql"],
    }
)