from bi import master
from sparkjobserver.api import SparkJob, build_problems



class JobScript(SparkJob):

    def validate(self, context, runtime, config):
        return config["job_config"]

    def run_job(self, context, runtime, data):
	return master.main(data)
