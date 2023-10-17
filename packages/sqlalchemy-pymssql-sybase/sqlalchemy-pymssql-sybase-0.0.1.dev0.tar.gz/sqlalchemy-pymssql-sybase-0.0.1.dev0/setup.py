from os.path import dirname, join
import re

from setuptools import setup, find_packages


basepath = dirname(__file__)

with open(join(basepath, "sqlalchemy_pymssql_sybase", "__init__.py")) as finp:
    VERSION = re.match(r'.*__version__ = "(.*?)"', finp.read(), re.S).group(1)

with open(join(basepath, "requirements.txt")) as finp:
    REQUIREMENTS = [pkg for pkg in (line.split("#")[0].strip() for line in finp) if pkg]

with open(join(basepath, "README.rst")) as finp:
    README = finp.read()


setup(
    name="sqlalchemy-pymssql-sybase",
    version=VERSION,
    description="SAP ASE (Sybase) Connector for SQLAlchemy using PyMsSql",
    long_description=README,
    url="https://github.com/gordthompson/sqlalchemy-pymssql-sybase",
    author="Giovany Vega",
    author_email="aleph.omega@gmail.com",
    license="MIT",
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # "Development Status :: 2 - Pre-Alpha",
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Database :: Front-Ends",
        "Operating System :: OS Independent",
    ],
    keywords="ASE SAP SQLAlchemy Sybase PyMSSql",
    project_urls={
        "Documentation": "https://github.com/gordthompson/sqlalchemy-pymssql-sybase/wiki",
        "Source": "https://github.com/gordthompson/sqlalchemy-pymssql-sybase",
        "Tracker": "https://github.com/gordthompson/sqlalchemy-pymssql-sybase/issues",
    },
    packages=find_packages(include=["sqlalchemy_pymssql_sybase"]),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    zip_safe=False,
    entry_points={
        "sqlalchemy.dialects": [
            "sybase.pymssql = sqlalchemy_pymssql_sybase.pymssql:SybaseDialect_pymssql",
        ]
    },
)
