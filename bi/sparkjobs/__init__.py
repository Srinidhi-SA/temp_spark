from bi import master
from sparkjobserver.api import SparkJob, build_problems


'''
class WordCountSparkJob(SparkJob):

    def validate(self, context, runtime, config):
        if config.get('input.strings', None):
            return config.get('input.strings')
        else:
            return build_problems(['config input.strings not found'])

    def run_job(self, context, runtime, data):
        return context.parallelize(data).countByValue()


class FailingSparkJob(SparkJob):
    """
    Simple example of a SparkContext job that fails
    with an exception for use in tests
    """

    def validate(self, context, runtime, config):
        if config.get('input.strings', None):
            return config.get('input.strings')
        else:
            return build_problems(['config input.strings not found'])

    def run_job(self, context, runtime, data):
        raise ValueError('Deliberate failure')

'''

class JobScript(SparkJob):
    def validate(self, context, runtime, config):
        job_data = None
        problems = []
        if config.get('cfgpath', None):
            job_data = config.get('cfgpath')
        else:
            problems.append('Missing cfgpath data')
	    if len(problems) == 0:
            return job_data
        else:
            return build_problems(problems)

    def run_job(self, context, runtime, data):
        print data
        configJson = data[0]
        print 'configJson', configJson
        master.main(configJson)
        return "Done the regression job"
