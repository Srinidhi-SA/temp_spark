#! /bin/sh
python3 setup.py bdist_egg
rm SPARK_DOCKER/marlabs_bi_jobs-0.0.0-py3.6.egg
cp -r dist/marlabs_bi_jobs-0.0.0-py3.6.egg SPARK_DOCKER/
ls -l SPARK_DOCKER/
cd API-CODE
rm -r mAdvisor-api
git clone -b main --single-branch https://Srinidhi-SA:Sri160293@github.com/Srinidhi-SA/temp_api
cd mAdvisor-api
rsync -r * ../../SPARK_DOCKER/code/mAdvisor-api/ --exclude API_DOCKER --exclude copyApiFolder.sh --exclude buildspec.yml --exclude hadoop_docker --exclude NGINX_DOCKER --exclude copyHadoopImage.sh --exclude requirements
cp -r requirements ../../SPARK_DOCKER/requirements/
cp -r static/ ../../SPARK_DOCKER/code/mAdvisor-api/
cd ../../
