import os

from setuptools import setup, find_packages

setup(
        name='marlabs-bi-jobs',
        version=os.getenv('SJS_VERSION', '0.0.0'),
        description='Marlabs BI jobs for Spark Job Server',
        #url='https://github.com/spark-jobserver/spark-jobserver',
        #license='Apache License 2.0',
        packages=find_packages(exclude=['test*','example*','config*','doc*','spark-ware*']),
	#install_requires=['numpy','scipy','pyhocon', 'py4j','pandas','statsmodels','jinja2','pattern']
	install_requires=['numpy','scipy','pyhocon','pandas','statsmodels','jinja2','pattern']
)
