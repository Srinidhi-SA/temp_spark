from pySparkMlParams import *
from sklernMlParams import *

CHISQUARELEVELLIMIT = 10
CHISQUARESIGNIFICANTDIMENSIONTOSHOW = 8

DECISIONTREERKMEANSTARGETNAME = ['Low','Medium','High']
MAPEBINS = [0,5,15,25,100]
HDFS_SECRET_KEY = "xfBmEcr_hFHGqVrTo2gMFpER3ks9x841UcvJbEQJesI="
ALGORITHMRANDOMSLUG = "f77631ce2ab24cf78c55bb6a5fce4db8"
ANOVAMAXLEVEL = 200
BLOCKSPLITTER = "|~NEWBLOCK~|"
BASEFOLDERNAME_MODELS = "mAdvisorModels"
BASEFOLDERNAME_SCORES = "mAdvisorScores"
PROBABILITY_RANGE_FOR_DONUT_CHART = {"50-60%":(50,60),"60-70%":(60,70),"70-80%":(70,80),"80-90%":(80,90),"90-100%":(90,100)}

DEFAULT_VALIDATION_OBJECT = {
         "name":"trainAndtest",
         "displayName":"Train and Test",
         "value":0.8
       }

APPS_ID_MAP = {
    '1': {
      'displayName': 'Opportunity Scoring',
      'type': 'CLASSIFICATION',
      'name': 'opportunity_scoring',
      'heading': 'Factors influencing Opportunity Score'
    },
    '2': {
      'displayName': 'Opportunity Scoring',
      'type': 'CLASSIFICATION',
      'name': 'opportunity_scoring',
      'heading': 'Factors influencing Opportunity Score'
    },
    '14': {
      'displayName': 'Robo Advisor',
      'type': 'ROBO',
      'name': 'robo_advisor_insights',
      'heading': None
    },
    '3': {
      'displayName': 'Automated Prediction',
      'type': 'CLASSIFICATION',
      'name': 'automated_prediction',
      'heading': 'Feature Importance'
    },
    '5': {
      'displayName': 'Stock Sense',
      'type': 'STOCK_SENSE',
      'name': 'stock_sense',
      'heading': None
    },
    '4': {
      'displayName': 'Speech Analytics',
      'type': 'SPEECH',
      'name': 'speech_analytics',
      'heading': None
    },
    '7': {
      'displayName': 'Re-admission Prediction',
      'type': 'CLASSIFICATION',
      'name': 're_admission_prediction',
      'heading': 'Factors influencing Re-admission'
    },
    '6': {
      'displayName': 'Churn Prediction',
      'type': 'CLASSIFICATION',
      'name': 'churn_prediction',
      'heading': 'Factors influencing Churn'
    },
    '9': {
      'displayName': 'Credit Card Fraud',
      'type': 'CLASSIFICATION',
      'name': 'credit_card_fraud',
      'heading': 'Factors influencing Fraud'
    },
    '8': {
      'displayName': 'Physician Attrition',
      'type': 'CLASSIFICATION',
      'name': 'physician_attrition',
      'heading': 'Factors influencing Attrition'
    },
  '11': {
    'displayName': 'Asset Health Prediction',
    'type': 'CLASSIFICATION',
    'name': 'asset_health_prediction',
    'heading': 'Factors influencing Asset Health'
  },
  '10': {
    'displayName': 'Claims Prediction',
    'type': 'CLASSIFICATION',
    'name': 'claims_prediction',
    'heading': 'Factors influencing Claims'
  },
  '13': {
    'displayName': 'Automated Prediction',
    'type': 'REGRESSION',
    'name': 'regression_app',
    'heading': 'Feature Importance'
  },
  '12': {
    'displayName': 'Employee Attrition',
    'type': 'CLASSIFICATION',
    'name': 'employee_attrition',
    'heading': 'Factors influencing Attrition'
  },

}


SLUG_MODEL_MAPPING = {
            ALGORITHMRANDOMSLUG+"rf":"randomforest",
            ALGORITHMRANDOMSLUG+"lr":"logisticregression",
            ALGORITHMRANDOMSLUG+"xgb":"xgboost",
            ALGORITHMRANDOMSLUG+"svm":"svm",
            ALGORITHMRANDOMSLUG+"linr":"linearregression",
            ALGORITHMRANDOMSLUG+"linr":"generalizedlinearregression",
            ALGORITHMRANDOMSLUG+"gbtr":"gbtregression",
            ALGORITHMRANDOMSLUG+"dtreer":"dtreeregression",
            ALGORITHMRANDOMSLUG+"rfr":"rfregression"
            }
MODEL_SLUG_MAPPING = {
            "randomforest":ALGORITHMRANDOMSLUG+"rf",
            "logisticregression":ALGORITHMRANDOMSLUG+"lr",
            "xgboost":ALGORITHMRANDOMSLUG+"xgb",
            "svm":ALGORITHMRANDOMSLUG+"svm",
            "linearregression":ALGORITHMRANDOMSLUG+"linr",
            "generalizedlinearregression":ALGORITHMRANDOMSLUG+"linr",
            "gbtregression":ALGORITHMRANDOMSLUG+"gbtr",
            "dtreeregression":ALGORITHMRANDOMSLUG+"dtreer",
            "rfregression":ALGORITHMRANDOMSLUG+"rfr"
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



classificationInitialScriptWeight = {"initialization":{"total":10}}
regressionInitialScriptWeight = {"initialization":{"total":10}}

regressionAlgoRelativeWeight = {
    ALGORITHMRANDOMSLUG+"linr"  : 1,
    ALGORITHMRANDOMSLUG+"gbtr" : 1,
    ALGORITHMRANDOMSLUG+"rfr"  : 1,
    ALGORITHMRANDOMSLUG+"dtreer" : 1
}

classificationAlgoRelativeWeight = {
    ALGORITHMRANDOMSLUG+"rf"  : 1,
    ALGORITHMRANDOMSLUG+"xgb" : 1,
    ALGORITHMRANDOMSLUG+"lr"  : 1,
    ALGORITHMRANDOMSLUG+"svm" : 2
}
classificationAlgorithmsToRunTemp = [ALGORITHMRANDOMSLUG+"rf",ALGORITHMRANDOMSLUG+"xgb",ALGORITHMRANDOMSLUG+"lr"]


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
regressionModelPredictionWeight = {
    "initialization":{"total":10,"script":5,"narratives":5},
    "linearRegression":{"total":10,"script":5,"narratives":5},
    "gbtRegression":{"total":10,"script":5,"narratives":5},
    "rfRegression":{"total":10,"script":5,"narratives":5},
    "dtreeRegression":{"total":10,"script":5,"narratives":5},
    "Descriptive analysis":{"total":10,"script":5,"narratives":5},
    "Measure vs. Dimension":{"total":20,"script":15,"narratives":5},
    "Predictive modeling":{"total":20,"script":15,"narratives":5}
}
metadataScriptWeight = {
    "initialization":{"total":3,"script":2,"narratives":1},
}
subsettingScriptWeight = {
    "initialization":{"total":3,"script":2,"narratives":1},
}
