from configs.localConfigs import *
def get_test_configs(jobType):
    testConfigs = {
        "story"        : get_story_config(),
        "metaData"     : get_metadata_config(),
        "training"     : get_training_config(),
        "prediction"   : get_prediction_config(),
        "subSetting"   : get_subsetting_config(),
        "stockAdvisor" : get_stockadvisor_config()
    }
    return testConfigs[jobType]
