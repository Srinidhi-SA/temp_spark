############################      Regression      ###############################
SKLEARN_ML_LINEAR_REGRESSION_PARAMS = [
            {
                "name":"n_jobs",
                "displayName":"No Of Jobs",
                "defaultValue":1,
                "acceptedValue":None,
                "valueRange":[-1,4],
                "paramType":"number",
                "uiElemType":"slider",
                "display":True,
                "hyperpatameterTuningCandidate":False,
                "expectedDataType": ["int"]
            },
            {
                 "name":"fit_intercept",
                 "displayName":"Fit Intercept",
                 "defaultValue":[
                     {
                         "name":"false",
                         "selected":False,
                         "displayName":"False"
                     },
                     {
                         "name":"true",
                         "selected":True,
                         "displayName":"True"
                     }
                    ],
                "paramType":"list",
                "uiElemType":"checkbox",
                "display":True,
                "hyperpatameterTuningCandidate":True,
                "expectedDataType": ["bool"]
             },
             {
                 "name":"normalize",
                 "displayName":"Normalize",
                 "defaultValue":[
                     {
                         "name":"false",
                         "selected":True,
                         "displayName":"False"
                     },
                     {
                         "name":"true",
                         "selected":False,
                         "displayName":"True"
                     }
                    ],
                "paramType":"list",
                "uiElemType":"checkbox",
                "display":True,
                "hyperpatameterTuningCandidate":True,
                "expectedDataType": ["bool"]
             },
             {
                 "name":"copy_X",
                 "displayName":"Copy X",
                 "defaultValue":[
                     {
                         "name":"false",
                         "selected":False,
                         "displayName":"False"
                     },
                     {
                         "name":"true",
                         "selected":True,
                         "displayName":"True"
                     }
                    ],
                "paramType":"list",
                "uiElemType":"checkbox",
                "display":True,
                "hyperpatameterTuningCandidate":True,
                "expectedDataType": ["bool"]
             }
]

SKLEARN_ML_GENERALIZED_LINEAR_REGRESSION_PARAMS = [

]

SKLEARN_ML_SUPPORTED_LOSS = [
    {"name":"ls","selected":True,"displayName":"Least Squares Regression"},
    {"name":"lad","selected":False,"displayName":"Least Absolute Deviation"},
    {"name":"huber","selected":False,"displayName":"Huber"},
    {"name":"quantile","selected":False,"displayName":"Quantile Regression"},
]
SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_REGRESSION = [
    {"name":"friedman_mse","selected":True,"displayName":"Friedman Mse"},
    {"name":"mse","selected":False,"displayName":"Mean Squared Error"},
    {"name":"mae","selected":False,"displayName":"Mean Absolute Error"},
]

SKLEARN_ML_TREE_BASED_REGRESSION_COMMON_PARAMS = [
                {
                    "name":"n_estimators",
                    "displayName":"Learning Rate",
                    "defaultValue":10,
                    "acceptedValue":None,
                    "valueRange":[10,1000],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["int"]
                },
                {
                    "name":"max_depth",
                    "displayName":"Max Depth Of Trees",
                    "defaultValue":3,
                    "acceptedValue":None,
                    "valueRange":[2,20],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["int", None]
                },

                {
                    "name":"criterion",
                    "displayName":"Measure For quality of a split",
                    "defaultValue":[{"name":obj["name"],"selected":obj["selected"],"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_REGRESSION],
                    "paramType":"list",
                    "uiElemType":"checkbox",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["string"]
                },
                {
                    "name":"min_samples_split",
                    "displayName":"Minimum Instances For Split",
                    "defaultValue":2,
                    "acceptedValue":None,
                    "valueRange":[2,10],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["int", "float"]
                },
                {
                    "name":"min_samples_leaf",
                    "displayName":"Minimum Instances For Leaf Node",
                    "defaultValue":1,
                    "acceptedValue":None,
                    "valueRange":[1,100],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["int", "float"]
                },
                {
                    "name":"subsample",
                    "displayName":"Sub Sampling Rate",
                    "defaultValue":1.0,
                    "acceptedValue":None,
                    "valueRange":[0.1,1.0],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["float"]
                },
                {
                    "name":"max_features",
                    "displayName":"Maximum Features for Split",
                    "defaultValue":None,
                    "acceptedValue":None,
                    "valueRange":[0.1,1.0],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["int", "float", "string", None]
                },
                {
                    "name":"max_leaf_nodes",
                    "displayName":"Maximum Number of Leaf Nodes",
                    "defaultValue":None,
                    "acceptedValue":None,
                    "valueRange":[],
                    "paramType":"number",
                    "uiElemType":"textBox",
                    "display":True,
                    "hyperpatameterTuningCandidate":False,
                    "expectedDataType": ["int", None]
                },
                {
                    "name":"min_impurity_decrease",
                    "displayName":"Impurity Decrease cutoff for Split",
                    "defaultValue":0.0,
                    "acceptedValue":None,
                    "valueRange":[0.0,1.0],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":False,
                    "expectedDataType": ["float"]
                },
                 {
                 "name":"random_state",
                 "displayName":"Random Seed",
                 "defaultValue":None,
                 "acceptedValue":None,
                 "valueRange":[1,100],
                 "paramType":"number",
                 "uiElemType":"textBox",
                 "display":True,
                 "hyperpatameterTuningCandidate":False,
                 "expectedDataType": ["int", None]
                 }
]

SKLEARN_ML_GBT_REGRESSION_PARAMS = [
        {
            "name":"loss",
            "displayName":"Loss Function",
            "defaultValue":[{"name":obj["name"],"selected":obj["selected"],"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_LOSS],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":True,
            "expectedDataType": ["string"]
        },
        {
            "name":"alpha",
            "displayName":"alpha-quantile for huber and quantile loss",
            "defaultValue":0.9,
            "acceptedValue":None,
            "valueRange":[0.1,1.0],
            "paramType":"number",
            "uiElemType":"slider",
            "display":False,
            "dependentOnDict":{"loss":["huber","quantile"]},
            "hyperpatameterTuningCandidate":False,
            "expectedDataType": ["float"]
        },
        {
            "name":"learning_rate",
            "displayName":"Learning Rate",
            "defaultValue":0.1,
            "acceptedValue":None,
            "valueRange":[0.1,1.0],
            "paramType":"number",
            "uiElemType":"slider",
            "display":True,
            "hyperpatameterTuningCandidate":True,
            "expectedDataType": ["float"]

        },
        {
            "name":"warm_start",
            "displayName":"Warm Start",
            "defaultValue":[
             {
                 "name":"false",
                 "selected":True,
                 "displayName":"False"
             },
             {
                 "name":"true",
                 "selected":False,
                 "displayName":"True"
             }
            ],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
            "expectedDataType": ["bool"]

        },

]

SKLEARN_ML_RF_REGRESSION_PARAMS = SKLEARN_ML_TREE_BASED_REGRESSION_COMMON_PARAMS + [
    {
        "name":"bootstrap",
        "displayName":"Bootstrap Sampling",
        "defaultValue":[
             {
                 "name":"false",
                 "selected":False,
                 "displayName":"False"
             },
             {
                 "name":"true",
                 "selected":True,
                 "displayName":"True"
             }
            ],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":True,
        "expectedDataType": ["bool"]

    },
    {
        "name":"oob_score",
        "displayName":"use out-of-bag samples",
        "defaultValue":[
             {
                 "name":"false",
                 "selected":False,
                 "displayName":"False"
             },
             {
                 "name":"true",
                 "selected":True,
                 "displayName":"True"
             }
            ],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":True,
        "expectedDataType": ["bool"]

    },
    {
        "name":"n_jobs",
        "displayName":"No Of Jobs",
        "defaultValue":1,
        "acceptedValue":None,
        "valueRange":[-1,4],
        "paramType":"number",
        "uiElemType":"slider",
        "display":True,
        "hyperpatameterTuningCandidate":False,
        "expectedDataType": ["int"]

    },
    {
        "name":"warm_start",
        "displayName":"Warm Start",
        "defaultValue":[
             {
                 "name":"false",
                 "selected":True,
                 "displayName":"False"
             },
             {
                 "name":"true",
                 "selected":False,
                 "displayName":"True"
             }
            ],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
        "expectedDataType": ["bool"]

    },
]

SKLEARN_ML_DTREE_REGRESSION_PARAMS = SKLEARN_ML_TREE_BASED_REGRESSION_COMMON_PARAMS + [
        {
            "name":"splitter",
            "displayName":"Node Split Strategy",
            "defaultValue":[
             {
                 "name":"best",
                 "selected":True,
                 "displayName":"Best split"
             },
             {
                 "name":"randome",
                 "selected":True,
                 "displayName":"Best random split"
             }
            ],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":True,
            "expectedDataType": ["string"]

        },

]
