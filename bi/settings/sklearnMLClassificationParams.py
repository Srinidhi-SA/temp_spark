
############################    Classification    ###############################
SKLEARN_ML_SUPPORTED_PENALTY_CLASSIFICATION = [
    {"name":"gini","selected":False,"displayName":"Gini Impurity"},
    {"name":"entropy","selected":False,"displayName":"Entropy"},
]
SKLEARN_ML_SUPPORTED_MULTICLASS_OPTION = [
    {"name":"ovr","selected":False,"displayName":"One Vs Rest"},
    {"name":"multinomial","selected":False,"displayName":"Multinomial"}
]
SKLEARN_ML_SUPPORTED_SOLVER_CLASSIFICATION = [
    {"name":"newton-cg","selected":False,"displayName":"newton-cg","penalty":"l2"},
    {"name":"lbfgs","selected":False,"displayName":"lbfgs","penalty":"l2"},
    {"name":"sag","selected":False,"displayName":"sag","penalty":"l2"},
    {"name":"liblinear","selected":False,"displayName":"liblinear","penalty":"l1"},
    {"name":"saga","selected":False,"displayName":"saga","penalty":"l1"},

]
SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION = [
    {"name":"gini","selected":False,"displayName":"Gini Impurity"},
    {"name":"entropy","selected":False,"displayName":"Entropy"},
]

SKLEARN_ML_SUPPORTED_MAX_FEATURES = [
    {"name":"auto","selected":False,"displayName":"sqrt(n_features)"},
    {"name":"sqrt","selected":False,"displayName":"sqrt(n_features)"},
    {"name":"log2","selected":False,"displayName":"log2(n_features)"},
    {"name":None,"selected":False,"displayName":"n_features"}
]


SKLEARN_ML_TREE_BASED_CLASSIFICATION_COMMON_PARAMS = [
                {
                    "name":"criterion",
                    "displayName":"Measure For quality of a split",
                    "defaultValue":[obj if obj["name"] != "gini" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION],
                    "paramType":"list",
                    "uiElemType":"checkbox",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                },
                {
                    "name":"max_depth",
                    "displayName":"Max Depth Of Trees",
                    "defaultValue":None,
                    "acceptedValue":None,
                    "valueRange":[2,20],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                },
                {
                    "name":"min_samples_split",
                    "displayName":"Minimum Instances For Split",
                    "defaultValue":2,
                    "acceptedValue":None,
                    "valueRange":[1,100],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,

                },
                {
                    "name":"min_samples_leaf",
                    "displayName":"Minimum Instances For Leaf Node",
                    "defaultValue":1,
                    "acceptedValue":None,
                    "valueRange":[1,1000],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,

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
                    "hyperpatameterTuningCandidate":True,

                },
                 {
                 "name":"random_state",
                 "displayName":"Random Seed",
                 "defaultValue":None,
                 "acceptedValue":None,
                 "valueRange":[],
                 "paramType":"number",
                 "uiElemType":"textBox",
                 "display":True,
                "hyperpatameterTuningCandidate":False,

                 }
]

SKLEARN_ML_DTREE_CLASSIFICATION_PARAMS = SKLEARN_ML_TREE_BASED_CLASSIFICATION_COMMON_PARAMS + [
        {
            "name":"max_features",
            "displayName":"Maximum Features for Split",
            "defaultValue":[obj if obj["name"] != None else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_MAX_FEATURES],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
        },
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
                 "name":"random",
                 "selected":True,
                 "displayName":"Best random split"
             }
            ],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
        },
        {
             "name":"presort",
             "displayName":"Pre Sort",
             "defaultValue":False,
             "acceptedValue":None,
             "paramType":"boolean",
             "uiElemType":"checkbox",
             "display":True,
             "hyperpatameterTuningCandidate":False,
         },


]

SKLEANR_ML_RF_CLASSIFICATION_PARAMS = SKLEARN_ML_TREE_BASED_CLASSIFICATION_COMMON_PARAMS + [
        {
            "name":"n_estimators",
            "displayName":"No of Estimators",
            "defaultValue":10,
            "acceptedValue":None,
            "valueRange":[1,1000],
            "paramType":"number",
            "uiElemType":"slider",
            "display":True,
            "hyperpatameterTuningCandidate":True,
        },
        {
            "name":"bootstrap",
            "displayName":"Bootstrap Sampling",
            "defaultValue":True,
            "acceptedValue":None,
            "paramType":"boolean",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
        },
        {
            "name":"oob_score",
            "displayName":"use out-of-bag samples",
            "defaultValue":False,
            "acceptedValue":None,
            "paramType":"boolean",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
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
        },
        {
            "name":"warm_start",
            "displayName":"Warm Start",
            "defaultValue":False,
            "acceptedValue":None,
            "paramType":"boolean",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
        },
]

SKLEARN_ML_LOGISTIC_REGRESSION_PARAMS = [
        {
             "name":"fit_intercept",
             "displayName":"Fit Intercept",
             "defaultValue":True,
             "acceptedValue":None,
             "paramType":"boolean",
             "uiElemType":"checkbox",
             "display":True,
             "hyperpatameterTuningCandidate":False,
         },
        {
            "name":"solver",
            "displayName":"Solver Used",
            "defaultValue":[obj if obj["name"] != "liblinear" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_SOLVER_CLASSIFICATION],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":True,
        },
        {
            "name":"multi_class",
            "displayName":"Multiclass Option",
            "defaultValue":[obj if obj["name"] != "ovr" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_MULTICLASS_OPTION],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
        },
        {
            "name":"max_iter",
            "displayName":"Maximum Solver Iterations",
            "defaultValue":100,
            "acceptedValue":None,
            "valueRange":[10,400],
            "paramType":"number",
            "uiElemType":"slider",
            "display":True,
            "hyperpatameterTuningCandidate":True,
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
        },
        {
            "name":"warm_start",
            "displayName":"Warm Start",
            "defaultValue":False,
            "acceptedValue":None,
            "paramType":"boolean",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
        },
         {
             "name":"random_state",
             "displayName":"Random Seed",
             "defaultValue":None,
             "acceptedValue":None,
             "valueRange":[],
             "paramType":"number",
             "uiElemType":"textBox",
             "display":True,
             "hyperpatameterTuningCandidate":False,
         },
         {
             "name":"tol",
             "displayName":"Convergence tolerance of iterations(e^-n)",
             "defaultValue":4,
             "acceptedValue":None,
             "valueRange":[3,10],
             "paramType":"number",
             "uiElemType":"slider",
             "display":True,
             "hyperpatameterTuningCandidate":True,
         },
         {
             "name":"C",
             "displayName":"Inverse of regularization strength",
             "defaultValue":1.0,
             "acceptedValue":None,
             "valueRange":[0.1,20.0],
             "paramType":"number",
             "uiElemType":"textBox",
             "display":True,
             "hyperpatameterTuningCandidate":True,
         },
]

SKLEARN_ML_SUPPORTED_XGB_BOOSTER = [
    {"name":"gbtree","selected":False,"displayName":"gbtree"},
    {"name":"dart","selected":False,"displayName":"dart"},
    {"name":"gblinear","selected":False,"displayName":"gblinear"},
]

SKLEARN_ML_SUPPORTED_XGB_TREE_ALGORITHMS = [
    {"name":"auto","selected":False,"displayName":"auto"},
    {"name":"exact","selected":False,"displayName":"exact"},
    {"name":"approx","selected":False,"displayName":"approx"},
    {"name":"hist","selected":False,"displayName":"hist"},
    {"name":"gpu_exact","selected":False,"displayName":"gpu_exact"},
    {"name":"gpu_hist","selected":False,"displayName":"gpu_hist"},

]

SKLEARN_ML_XGBOOST_CLASSIFICATION_PARAMS = [
    {
        "name":"booster",
        "displayName":"Booster Function",
        "defaultValue":[obj if obj["name"] != "gbtree" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_XGB_BOOSTER],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":True,
        "hyperpatameterTuningCandidate":True,
    },
    {
        "name":"silent",
        "displayName":"Print Messages on Console",
        "defaultValue":[{"name":0,"selected":False,"displayName":"True"},{"name":1,"selected":True,"displayName":"False"}],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":True,
        "hyperpatameterTuningCandidate":False,
    },
    {
        "name":"eta",
        "displayName":"Learning Rate",
        "defaultValue":0.3,
        "acceptedValue":None,
        "valueRange":[0.0,1.0],
        "paramType":"number",
        "uiElemType":"slider",
        "display":True,
        "hyperpatameterTuningCandidate":True,
    },
    {
        "name":"gamma",
        "displayName":"Minimum Loss Reduction",
        "defaultValue":0,
        "acceptedValue":None,
        "valueRange":[0,100],
        "paramType":"number",
        "uiElemType":"slider",
        "display":True,
        "hyperpatameterTuningCandidate":False
    },
    {
        "name":"max_depth",
        "displayName":"Maximum Depth of Tree",
        "defaultValue":6,
        "acceptedValue":None,
        "valueRange":[0,100],
        "paramType":"number",
        "uiElemType":"slider",
        "display":True,
        "hyperpatameterTuningCandidate":True
    },
    {
        "name":"min_child_weight",
        "displayName":"Maximum Depth of Tree",
        "defaultValue":6,
        "acceptedValue":None,
        "valueRange":[0,100],
        "paramType":"number",
        "uiElemType":"slider",
        "display":True,
        "hyperpatameterTuningCandidate":False,
    },
    {
        "name":"subsample",
        "displayName":"Subsampling Ratio",
        "defaultValue":1,
        "acceptedValue":None,
        "valueRange":[0.1,1],
        "paramType":"number",
        "uiElemType":"slider",
        "display":True,
        "hyperpatameterTuningCandidate":False,
    },
    {
        "name":"colsample_bytree",
        "displayName":"subsample ratio of columns for each tree",
        "defaultValue":1,
        "acceptedValue":None,
        "valueRange":[0.1,1],
        "paramType":"number",
        "uiElemType":"slider",
        "display":True,
        "hyperpatameterTuningCandidate":False,
    },
    {
        "name":"colsample_bylevel",
        "displayName":"subsample ratio of columns for each split",
        "defaultValue":1,
        "acceptedValue":None,
        "valueRange":[0.1,1],
        "paramType":"number",
        "uiElemType":"slider",
        "display":True,
        "hyperpatameterTuningCandidate":False,
    },
    {
        "name":"tree_method",
        "displayName":"Tree Construction Algorithm",
        "defaultValue":[obj if obj["name"] != "auto" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_XGB_TREE_ALGORITHMS],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":True,
        "hyperpatameterTuningCandidate":False,
    },
    {
        "name":"predictor",
        "displayName":"Type of Predictor Algorithm",
        "defaultValue":[{"name":"cpu_predictor","selected":True,"displayName":"Multicore CPU prediction algorithm"},
                {"name":"gpu_predictor","selected":True,"displayName":"Prediction using GPU"}
            ],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":True,
        "hyperpatameterTuningCandidate":False,
    },
    {
        "name":"process_type",
        "displayName":"Boosting process to run",
        "defaultValue":[{"name":"default","selected":True,"displayName":"Create New Trees"},
                {"name":"update","selected":True,"displayName":"Update Trees"}
            ],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":True,
        "hyperpatameterTuningCandidate":False,
    },



]
