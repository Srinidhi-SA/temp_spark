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

SKLEARN_ML_REGRESSION_PARAMS = [
            {
                "name":"n_jobs",
                "displayName":"No Of Jobs",
                "defaultValue":1,
                "acceptedValue":None,
                "valueRange":[-1,4],
                "paramType":"number",
                "uiElemType":"slider",
                "display":True
            },
            {
                 "name":"fit_intercept",
                 "displayName":"Fit Intercept",
                 "defaultValue":True,
                 "acceptedValue":None,
                 "paramType":"boolean",
                 "uiElemType":"checkbox",
                 "display":True
             },
             {
                 "name":"normalize",
                 "displayName":"Normalize",
                 "defaultValue":False,
                 "acceptedValue":None,
                 "paramType":"boolean",
                 "uiElemType":"checkbox",
                 "display":True
             },
             {
                 "name":"copy_X",
                 "displayName":"Copy X",
                 "defaultValue":True,
                 "acceptedValue":None,
                 "paramType":"boolean",
                 "uiElemType":"checkbox",
                 "display":True
             }
]

SKLEARN_ML_SUPPORTED_LOSS = [
    {"name":"ls","selected":True,"displayName":"Least Squares Regression"},
    {"name":"lad","selected":False,"displayName":"Least Absolute Deviation"},
    {"name":"huber","selected":False,"displayName":"Huber"},
    {"name":"quantile","selected":False,"displayName":"Quantile Regression"},
]
SKLEARN_ML_SUPPORTED_SPLIT_CRITERION = [
    {"name":"friedman_mse","selected":True,"displayName":"Friedman Mse"},
    {"name":"mse","selected":False,"displayName":"Mean Squared Error"},
    {"name":"mae","selected":False,"displayName":"Mean Absolute Error"},
]

SKLEARN_ML_TREE_BASED_REGRESSION_COMMON_PARAMS = [
                {
                    "name":"max_depth",
                    "displayName":"Depth Of Trees",
                    "defaultValue":3,
                    "acceptedValue":None,
                    "valueRange":[2,20],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },
                {
                    "name":"learning_rate",
                    "displayName":"Learning Rate",
                    "defaultValue":0.1,
                    "acceptedValue":None,
                    "valueRange":[0.1,1.0],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },
                {
                    "name":"criterion",
                    "displayName":"Measure For quality of a split",
                    "defaultValue":[{"name":obj["name"],"selected":obj["selected"],"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_SPLIT_CRITERION],
                    "paramType":"list",
                    "uiElemType":"checkbox",
                    "display":True
                },
                {
                    "name":"min_samples_leaf",
                    "displayName":"Minimum Instances For Leaf Node",
                    "defaultValue":1,
                    "acceptedValue":None,
                    "valueRange":[1,1000],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },

                {
                    "name":"min_samples_split",
                    "displayName":"Minimum Instances For Split",
                    "defaultValue":2,
                    "acceptedValue":None,
                    "valueRange":[1,100],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },
                {
                    "name":"subsample",
                    "displayName":"Sub Sampling Rate",
                    "defaultValue":1.0,
                    "acceptedValue":None,
                    "valueRange":[0.0,1.0],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },
                {
                    "name":"max_features",
                    "displayName":"Maximum Features for Split",
                    "defaultValue":0.0,
                    "acceptedValue":None,
                    "valueRange":[0.0,1.0],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },
                {
                    "name":"maxMemoryInMB",
                    "displayName":"Maximum Memory Available",
                    "defaultValue":256,
                    "acceptedValue":None,
                    "valueRange":[128,10240],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },
                {
                     "name":"cacheNodeIds",
                     "displayName":"Cache Node Ids",
                     "defaultValue":False,
                     "acceptedValue":None,
                     "paramType":"boolean",
                     "uiElemType":"checkbox",
                     "display":True
                 },
                 {
                     "name":"loss",
                     "displayName":"Loss Function",
                     "defaultValue":[{"name":obj["name"],"selected":obj["selected"],"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_LOSS],
                     "paramType":"list",
                     "uiElemType":"checkbox",
                     "display":True
                 },
                 {
                 "name":"seed",
                 "displayName":"Random Seed",
                 "defaultValue":None,
                 "acceptedValue":None,
                 "valueRange":[],
                 "paramType":"number",
                 "uiElemType":"textBox",
                 "display":True
                 }
]

PYSPARK_ML_REGRESSION_PARAMS = [
            {
                "name":"maxIter",
                "displayName":"Maximum Iteration",
                "defaultValue":100,
                "acceptedValue":None,
                "valueRange":[1,200],
                "paramType":"number",
                "uiElemType":"slider",
                "display":True
            },
            {
                "name":"regParam",
                "displayName":"Regularization parameter",
                "defaultValue":0.0,
                "acceptedValue":None,
                "valueRange":[0.0,1.0],
                "paramType":"number",
                "uiElemType":"slider",
                "display":True
            },
            {
                "name":"tol",
                "displayName":"Convergence tolerance of iterations(e^-n)",
                "defaultValue":6,
                "acceptedValue":None,
                "valueRange":[3,10],
                "paramType":"number",
                "uiElemType":"slider",
                "display":True
            },
            {
                 "name":"fitIntercept",
                 "displayName":"Fit Intercept",
                 "defaultValue":True,
                 "acceptedValue":None,
                 "paramType":"boolean",
                 "uiElemType":"checkbox",
                 "display":True
             },
             {
                 "name":"weightCol",
                 "displayName":"Weight Column",
                 "defaultValue":None,
                 "acceptedValue":None,
                 "paramType":"string",
                 "uiElemType":"dropDown",
                 "display":False
             }
]
PYSPARK_ML_LINEAR_REGRESSION_PARAMS = PYSPARK_ML_REGRESSION_PARAMS + [
                {
                    "name":"elasticNetParam",
                    "displayName":"Elastic Net Param",
                    "defaultValue":0.0,
                    "acceptedValue":None,
                    "valueRange":[0.0,1.0],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },
                 {
                      "name":"standardization",
                      "displayName":"Standardization",
                      "defaultValue":True,
                      "acceptedValue":None,
                      "paramType":"boolean",
                      "uiElemType":"checkbox",
                      "display":True
                  },
                   {
                       "name":"solver",
                       "displayName":"Solver",
                       "defaultValue":[
                        {
                            "name":"l-bfgs",
                            "selected":False,
                            "displayName":"Limited-memory BFGS"
                        },
                        {
                            "name":"auto",
                            "selected":True,
                            "displayName":"Automatic Selection"
                        },
                        {
                            "name":"normal",
                            "selected":False,
                            "displayName":"Normal"
                        }
                       ],
                       "paramType":"list",
                       "uiElemType":"checkbox",
                       "display":True
                   },
                   {
                       "name":"loss",
                       "displayName":"Loss Function",
                       "defaultValue":[
                        {
                            "name":"huber",
                            "selected":False,
                            "displayName":"Huber"
                        },
                        {
                            "name":"squaredError",
                            "selected":True,
                            "displayName":"Squared Error"
                        }
                       ],
                       "paramType":"list",
                       "uiElemType":"checkbox",
                       "display":True
                   },
                   {
                       "name":"epsilon",
                       "displayName":"Learning Rate",
                       "defaultValue":1.35,
                       "acceptedValue":None,
                       "valueRange":[1.0,5.0],
                       "paramType":"number",
                       "uiElemType":"slider",
                       "display":True
                   },
                {
                    "name":"aggregationDepth",
                    "displayName":"Aggregation Depth",
                    "defaultValue":2,
                    "acceptedValue":None,
                    "valueRange":[2,5],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                }
]
GLM_FAMILY_LINK_MAPPING = {
    "gaussian":["identity", "log", "inverse"],
    "poisson":["logit", "probit", "cloglog"],
    "gamma":["inverse", "identity", "log"],
    "binomial":["logit", "probit", "cloglog"],
}
TWEEDIE_LINK_VARIANCE_POWER = {
    "name":"variancePower",
    "displayName":"Tweedie Distribution Variance Power",
    "defaultValue":0.0,
    "acceptedValue":None,
    "valueRange":[0.0,1000.0],
    "paramType":"number",
    "uiElemType":"slider",
    "display":True
},
TWEEDIE_LINK_POWER = {
    "name":"linkPower",
    "displayName":"Tweedie Distribution Link Power",
    "defaultValue":0.0,
    "acceptedValue":None,
    "valueRange":[0.0,1000.0],
    "paramType":"number",
    "uiElemType":"slider",
    "display":False
},
PYSPARK_ML_GENERALIZED_LINEAR_REGRESSION_PARAMS = PYSPARK_ML_REGRESSION_PARAMS + [
    {
        "name":"solver",
        "displayName":"Solver",
        "defaultValue":[
         {
             "name":"irls",
             "selected":True,
             "displayName":"Iteratively Reweighted Least Square"
         },
        ],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":False
    },
    {
        "name":"family",
        "displayName":"Error Distribution",
        "defaultValue":[
         {
             "name":"gaussian",
             "selected":True,
             "displayName":"Gaussian",
             "display":True
         },
         {
             "name":"binomial",
             "selected":False,
             "displayName":"Binomial",
             "display":True
         },
         {
             "name":"poisson",
             "selected":False,
             "displayName":"Poisson",
             "display":True
         },
         {
             "name":"gamma",
             "selected":False,
             "displayName":"Gamma",
             "display":True
         },
         {
             "name":"tweedie",
             "selected":False,
             "displayName":"Tweedie",
             "display":False
         }
        ],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":True
    },
    {
        "name":"link",
        "displayName":"Link Function",
        "defaultValue":[
         {
             "name":"identity",
             "selected":False,
             "displayName":"Identity",
             "display":False
         },
         {
             "name":"log",
             "selected":False,
             "displayName":"Log",
             "display":False
         },
         {
             "name":"inverse",
             "selected":False,
             "displayName":"Inverse",
             "display":False
         },
         {
             "name":"logit",
             "selected":False,
             "displayName":"Logit",
             "display":False
         },
         {
             "name":"probit",
             "selected":False,
             "displayName":"Probit",
             "display":False
         },
         {
             "name":"cloglog",
             "selected":False,
             "displayName":"Cloglog",
             "display":False
         },
         {
             "name":"sqrt",
             "selected":False,
             "displayName":"Sqrt",
             "display":False
         }
        ],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":False
    },
    {
        "name":"linkPredictionCol",
        "displayName":"Link Prediction Column",
        "defaultValue":None,
        "acceptedValue":None,
        "paramType":"string",
        "uiElemType":"dropDown",
        "display":False
    },
    {
        "name":"offsetCol",
        "displayName":"Offset Column",
        "defaultValue":None,
        "acceptedValue":None,
        "paramType":"string",
        "uiElemType":"dropDown",
        "display":False
    }

]
PYSPARK_ML_SUPPORTED_IMPURITIES = [{"name":"variance","selected":True,"displayName":"Variance"}]
PYSPARK_ML_TREE_BASED_REGRESSION_COMMON_PARAMS = [
                {
                    "name":"maxDepth",
                    "displayName":"Depth Of Trees",
                    "defaultValue":5,
                    "acceptedValue":None,
                    "valueRange":[2,20],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },
                {
                    "name":"maxBins",
                    "displayName":"Maximum Number Of Bins",
                    "defaultValue":32,
                    "acceptedValue":None,
                    "valueRange":[16,128],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "powerOf2":True,
                    "display":True
                },
                {
                    "name":"checkpointInterval",
                    "displayName":"Check Point Interval",
                    "defaultValue":10,
                    "acceptedValue":None,
                    "valueRange":[10,20],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },
                {
                    "name":"minInstancesPerNode",
                    "displayName":"Minimum Instances Per Node",
                    "defaultValue":1,
                    "acceptedValue":None,
                    "valueRange":[1,10],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },
                {
                    "name":"subsamplingRate",
                    "displayName":"Sub Sampling Rate",
                    "defaultValue":1.0,
                    "acceptedValue":None,
                    "valueRange":[0.0,1.0],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },
                {
                    "name":"minInfoGain",
                    "displayName":"Minimum Info Gain",
                    "defaultValue":0.0,
                    "acceptedValue":None,
                    "valueRange":[0.0,1.0],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },
                {
                    "name":"maxMemoryInMB",
                    "displayName":"Maximum Memory Available",
                    "defaultValue":256,
                    "acceptedValue":None,
                    "valueRange":[128,10240],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True
                },
                {
                     "name":"cacheNodeIds",
                     "displayName":"Cache Node Ids",
                     "defaultValue":False,
                     "acceptedValue":None,
                     "paramType":"boolean",
                     "uiElemType":"checkbox",
                     "display":True
                 },
                 {
                     "name":"impuriy",
                     "displayName":"Impurity Index",
                     "defaultValue":[{"name":obj["name"],"selected":obj["selected"],"displayName":obj["displayName"]} for obj in PYSPARK_ML_SUPPORTED_IMPURITIES],
                     "paramType":"list",
                     "uiElemType":"checkbox",
                     "display":True
                 },
                 {
                 "name":"seed",
                 "displayName":"Random Seed",
                 "defaultValue":None,
                 "acceptedValue":None,
                 "valueRange":[],
                 "paramType":"number",
                 "uiElemType":"textBox",
                 "display":True
                 }
]
PYSPARK_ML_GBT_REGRESSION_PARAMS = PYSPARK_ML_TREE_BASED_REGRESSION_COMMON_PARAMS +[
                {
                    "name":"maxIter",
                    "displayName":"Maximum Iteration",
                    "defaultValue":20,
                    "acceptedValue":None,
                    "valueRange":[1,100],
                    "paramType":"number",
                    "uiElemType":"slider"
                },
                {
                    "name":"stepSize",
                    "displayName":"Step Size",
                    "defaultValue":0.1,
                    "acceptedValue":None,
                    "valueRange":[0.1,1.0],
                    "paramType":"number",
                    "uiElemType":"slider"
                },
               {
                   "name":"lossType",
                   "displayName":"Loss Type",
                   "defaultValue":[
                    {
                        "name":"squared",
                        "selected":True,
                        "displayName":"Squared Loss"
                    },
                    {
                        "name":"absolute",
                        "selected":False,
                        "displayName":"Huber Loss"
                    }
                   ],
                   "paramType":"list",
                   "uiElemType":"checkbox"
               },
            ]
PYSPARK_ML_DTREE_REGRESSION_PARAMS = PYSPARK_ML_TREE_BASED_REGRESSION_COMMON_PARAMS +[
        {
            "name":"varianceCol",
            "displayName":"Variance Column Name",
            "defaultValue":None,
            "acceptedValue":None,
            "paramType":"string",
            "uiElemType":"dropDown",
            "display":False
        },

    ]
PYSPARK_ML_RF_REGRESSION_PARAMS = PYSPARK_ML_TREE_BASED_REGRESSION_COMMON_PARAMS +[
        {
            "name":"numTrees",
            "displayName":"Number of Trees",
            "defaultValue":20,
            "acceptedValue":None,
            "valueRange":[1,1000],
            "paramType":"number",
            "uiElemType":"slider",
            "display":True
        },
        {
            "name":"featureSubsetStrategy",
            "displayName":"Feature Subset Strategy",
            "defaultValue":[
             {
                 "name":"auto",
                 "selected":True,
                 "displayName":"Automatic"
             },
             {
                 "name":"all",
                 "selected":False,
                 "displayName":"All"
             },
             {
                 "name":"all",
                 "selected":False,
                 "displayName":"All"
             },
             {
                 "name":"onethird",
                 "selected":False,
                 "displayName":"One-Third"
             },
             {
                 "name":"sqrt",
                 "selected":False,
                 "displayName":"Squared Root"
             },
             {
                 "name":"log2",
                 "selected":False,
                 "displayName":"Log2"
             },
            ],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True
        },
    ]

DEFAULT_VALIDATION_OBJECT = {
         "name":"trainAndtest",
         "displayName":"Train and Test",
         "value":0.7
       }

APPS_ID_MAP = {
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
  '1': {
    'displayName': 'Opportunity Scoring',
    'type': 'CLASSIFICATION',
    'name': 'opportunity_scoring',
    'heading': 'Factors influencing Opportunity Score'
  },
  '3': {
    'displayName': 'Robo Advisor',
    'type': 'ROBO',
    'name': 'robo_advisor_insights',
    'heading': None
  },
  '2': {
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
  }
}


SLUG_MODEL_MAPPING = {
            ALGORITHMRANDOMSLUG+"rf":"randomforest",
            ALGORITHMRANDOMSLUG+"lr":"logisticregression",
            ALGORITHMRANDOMSLUG+"xgb":"xgboost",
            ALGORITHMRANDOMSLUG+"svm":"svm",
            ALGORITHMRANDOMSLUG+"linr":"linearregression",
            ALGORITHMRANDOMSLUG+"glinr":"generalizedlinearregression",
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
            "generalizedlinearregression":ALGORITHMRANDOMSLUG+"glinr",
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
