CHISQUARELEVELLIMIT = 10
CHISQUARESIGNIFICANTDIMENSIONTOSHOW = 2

DECISIONTREERKMEANSTARGETNAME = ['Low','Medium','High']
HDFS_SECRET_KEY = "xfBmEcr_hFHGqVrTo2gMFpER3ks9x841UcvJbEQJesI="
ALGORITHMRANDOMSLUG = "f77631ce2ab24cf78c55bb6a5fce4db8"
ANOVAMAXLEVEL = 200
BLOCKSPLITTER = "|~NEWBLOCK~|"
BASEFOLDERNAME_MODELS = "mAdvisorModels"
BASEFOLDERNAME_SCORES = "mAdvisorScores"
PROBABILITY_RANGE_FOR_DONUT_CHART = {"50-60%":(50,60),"60-70%":(60,70),"70-80%":(70,80),"80-90%":(80,90),"90-100%":(90,100)}

APPS_ID_NAME_MAP = {
    "1":"Automated Prediction",
    "2":"Opportunity Scoring",
    "3":"Churn Prediction",
    "4":"Re-admission Prediction",
    "5":"Physician Attrition",
    "6":"Credit Card Fraud",
    "7":"Claims Prediction",
    "8":"Asset health Prediction",
    "9":"Employee Attrition"
}
APPS_ID_HEADING_MAP = {
    "1":"Feature Importance",
    "2":"Factors influencing Opportunity Score",
    "3":"Factors influencing Churn",
    "4":"Factors influencing Re-admission",
    "5":"Factors influencing Attrition",
    "6":"Factors influencing Fraud",
    "7":"Factors influencing Claims",
    "8":"Factors influencing Asset health",
    "9":"Factors influencing Attrition"
}

SLUG_MODEL_MAPPING = {
            ALGORITHMRANDOMSLUG+"rf":"randomforest",
            ALGORITHMRANDOMSLUG+"lr":"logisticregression",
            ALGORITHMRANDOMSLUG+"xgb":"xgboost",
            ALGORITHMRANDOMSLUG+"svm":"svm"
            }
MODEL_SLUG_MAPPING = {
            "randomforest":ALGORITHMRANDOMSLUG+"rf",
            "logisticregression":ALGORITHMRANDOMSLUG+"lr",
            "xgboost":ALGORITHMRANDOMSLUG+"xgb",
            "svm":ALGORITHMRANDOMSLUG+"svm"
            }

scriptsMapping = {
    "overview" : "Descriptive analysis",
    "performance" : "Measure vs. Dimension",
    "influencer" : "Measure vs. Measure",
    "prediction" : "Predictive modeling",
    "trend" : "Trend",
    "association" : "Dimension vs. Dimension"
}
measureAnalysisRelativeWeight = {
    "initialization":0.25,
    "Descriptive analysis":1,
    "Measure vs. Dimension":3,
    "Measure vs. Measure":3,
    "Trend":1.5,
    "Predictive modeling":1.5
}
dimensionAnalysisRelativeWeight = {
    "initialization":0.25,
    "Descriptive analysis":1,
    "Dimension vs. Dimension":4,
    "Trend":2.5,
    "Predictive modeling":2.5
}
mlModelTrainingWeight = {
    "initialization":{"total":10,"script":10,"narratives":10},
    "randomForest":{"total":30,"script":30,"narratives":30},
    "logisticRegression":{"total":30,"script":30,"narratives":30},
    "xgboost":{"total":30,"script":30,"narratives":30},
    "svm":{"total":30,"script":30,"narratives":30}
}
mlModelPredictionWeight = {
    "initialization":{"total":10,"script":10,"narratives":10},
    "randomForest":{"total":20,"script":20,"narratives":20},
    "logisticRegression":{"total":20,"script":20,"narratives":20},
    "xgboost":{"total":20,"script":20,"narratives":20},
    "svm":{"total":20,"script":20,"narratives":20},
    "Descriptive analysis":{"total":10,"script":10,"narratives":10},
    "Dimension vs. Dimension":{"total":10,"script":5,"narratives":5},
    "Predictive modeling":{"total":10,"script":5,"narratives":5}
}
metadataScriptWeight = {
    "initialization":{"total":3,"script":2,"narratives":1},
}
subsettingScriptWeight = {
    "initialization":{"total":3,"script":2,"narratives":1},
}
