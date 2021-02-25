PYSPARK_ML_REGRESSION_PARAMS = [
    {
        "name": "maxIter",
        "displayName": "Maximum Iteration",
        "defaultValue": 100,
        "acceptedValue": None,
        "valueRange": [1, 200],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": False,
    },
    {
        "name": "regParam",
        "displayName": "Regularization parameter",
        "defaultValue": 0.0,
        "acceptedValue": None,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
    },
    {
        "name": "tol",
        "displayName": "Convergence tolerance of iterations(e^-n)",
        "defaultValue": 6,
        "acceptedValue": None,
        "valueRange": [3, 10],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
    },
    {
        "name": "fitIntercept",
        "displayName": "Fit Intercept",
        "defaultValue": True,
        "acceptedValue": None,
        "paramType": "boolean",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
    },
    {
        "name": "weightCol",
        "displayName": "Weight Column",
        "defaultValue": None,
        "acceptedValue": None,
        "paramType": "string",
        "uiElemType": "dropDown",
        "display": False,
        "hyperpatameterTuningCandidate": False,
    }
]
PYSPARK_ML_LINEAR_REGRESSION_PARAMS = PYSPARK_ML_REGRESSION_PARAMS + [
    {
        "name": "elasticNetParam",
        "displayName": "Elastic Net Param",
        "defaultValue": 0.0,
        "acceptedValue": None,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
    },
    {
        "name": "standardization",
        "displayName": "Standardization",
        "defaultValue": True,
        "acceptedValue": None,
        "paramType": "boolean",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
    },
    {
        "name": "solver",
        "displayName": "Solver",
        "defaultValue": [
            {
                "name": "l-bfgs",
                "selected": False,
                "displayName": "Limited-memory BFGS"
            },
            {
                "name": "auto",
                "selected": False,
                "displayName": "Automatic Selection"
            },
            {
                "name": "normal",
                "selected": False,
                "displayName": "Normal"
            }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
    },
    {
        "name": "loss",
        "displayName": "Loss Function",
        "defaultValue": [
            {
                "name": "huber",
                "selected": False,
                "displayName": "Huber"
            },
            {
                "name": "squaredError",
                "selected": True,
                "displayName": "Squared Error"
            }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
    },
    {
        "name": "epsilon",
        "displayName": "Learning Rate",
        "defaultValue": 1.35,
        "acceptedValue": None,
        "valueRange": [1.0, 5.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": False,
    },
    {
        "name": "aggregationDepth",
        "displayName": "Aggregation Depth",
        "defaultValue": 2,
        "acceptedValue": None,
        "valueRange": [2, 5],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": False,
    }
]
GLM_FAMILY_LINK_MAPPING = {
    "gaussian": ["identity", "log", "inverse"],
    "poisson": ["logit", "probit", "cloglog"],
    "gamma": ["inverse", "identity", "log"],
    "binomial": ["logit", "probit", "cloglog"],
}
TWEEDIE_LINK_VARIANCE_POWER = {
                                  "name": "variancePower",
                                  "displayName": "Tweedie Distribution Variance Power",
                                  "defaultValue": 0.0,
                                  "acceptedValue": None,
                                  "valueRange": [0.0, 1000.0],
                                  "paramType": "number",
                                  "uiElemType": "slider",
                                  "display": True
                              },
TWEEDIE_LINK_POWER = {
                         "name": "linkPower",
                         "displayName": "Tweedie Distribution Link Power",
                         "defaultValue": 0.0,
                         "acceptedValue": None,
                         "valueRange": [0.0, 1000.0],
                         "paramType": "number",
                         "uiElemType": "slider",
                         "display": False
                     },
PYSPARK_ML_GENERALIZED_LINEAR_REGRESSION_PARAMS = PYSPARK_ML_REGRESSION_PARAMS + [
    {
        "name": "solver",
        "displayName": "Solver",
        "defaultValue": [
            {
                "name": "irls",
                "selected": True,
                "displayName": "Iteratively Reweighted Least Square"
            },
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": False
    },
    {
        "name": "family",
        "displayName": "Error Distribution",
        "defaultValue": [
            {
                "name": "gaussian",
                "selected": True,
                "displayName": "Gaussian",
                "display": True
            },
            {
                "name": "binomial",
                "selected": False,
                "displayName": "Binomial",
                "display": True
            },
            {
                "name": "poisson",
                "selected": False,
                "displayName": "Poisson",
                "display": True
            },
            {
                "name": "gamma",
                "selected": False,
                "displayName": "Gamma",
                "display": True
            },
            {
                "name": "tweedie",
                "selected": False,
                "displayName": "Tweedie",
                "display": False
            }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True
    },
    {
        "name": "link",
        "displayName": "Link Function",
        "defaultValue": [
            {
                "name": "identity",
                "selected": False,
                "displayName": "Identity",
                "display": False
            },
            {
                "name": "log",
                "selected": False,
                "displayName": "Log",
                "display": False
            },
            {
                "name": "inverse",
                "selected": False,
                "displayName": "Inverse",
                "display": False
            },
            {
                "name": "logit",
                "selected": False,
                "displayName": "Logit",
                "display": False
            },
            {
                "name": "probit",
                "selected": False,
                "displayName": "Probit",
                "display": False
            },
            {
                "name": "cloglog",
                "selected": False,
                "displayName": "Cloglog",
                "display": False
            },
            {
                "name": "sqrt",
                "selected": False,
                "displayName": "Sqrt",
                "display": False
            }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": False
    },
    {
        "name": "linkPredictionCol",
        "displayName": "Link Prediction Column",
        "defaultValue": None,
        "acceptedValue": None,
        "paramType": "string",
        "uiElemType": "dropDown",
        "display": False
    },
    {
        "name": "offsetCol",
        "displayName": "Offset Column",
        "defaultValue": None,
        "acceptedValue": None,
        "paramType": "string",
        "uiElemType": "dropDown",
        "display": False
    }

]
PYSPARK_ML_SUPPORTED_IMPURITIES = [{"name": "variance", "selected": True, "displayName": "Variance"}]
PYSPARK_ML_TREE_BASED_REGRESSION_COMMON_PARAMS = [
    {
        "name": "maxDepth",
        "displayName": "Depth Of Trees",
        "defaultValue": 5,
        "acceptedValue": None,
        "valueRange": [2, 20],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
    },
    {
        "name": "maxBins",
        "displayName": "Maximum Number Of Bins",
        "defaultValue": 32,
        "acceptedValue": None,
        "valueRange": [16, 128],
        "paramType": "number",
        "uiElemType": "slider",
        "powerOf2": True,
        "display": True,
        "hyperpatameterTuningCandidate": True,
    },
    {
        "name": "checkpointInterval",
        "displayName": "Check Point Interval",
        "defaultValue": 10,
        "acceptedValue": None,
        "valueRange": [10, 20],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
    },
    {
        "name": "minInstancesPerNode",
        "displayName": "Minimum Instances Per Node",
        "defaultValue": 1,
        "acceptedValue": None,
        "valueRange": [1, 10],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
    },
    {
        "name": "subsamplingRate",
        "displayName": "Sub Sampling Rate",
        "defaultValue": 1.0,
        "acceptedValue": None,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": False,
    },
    {
        "name": "minInfoGain",
        "displayName": "Minimum Info Gain",
        "defaultValue": 0.0,
        "acceptedValue": None,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
    },
    {
        "name": "maxMemoryInMB",
        "displayName": "Maximum Memory Available",
        "defaultValue": 256,
        "acceptedValue": None,
        "valueRange": [128, 10240],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": False,
    },
    {
        "name": "cacheNodeIds",
        "displayName": "Cache Node Ids",
        "defaultValue": False,
        "acceptedValue": None,
        "paramType": "boolean",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
    },
    {
        "name": "impuriy",
        "displayName": "Impurity Index",
        "defaultValue": [{"name": obj["name"], "selected": obj["selected"], "displayName": obj["displayName"]} for obj
                         in PYSPARK_ML_SUPPORTED_IMPURITIES],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
    },
    {
        "name": "seed",
        "displayName": "Random Seed",
        "defaultValue": None,
        "acceptedValue": None,
        "valueRange": [],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
    }
]
PYSPARK_ML_GBT_REGRESSION_PARAMS = PYSPARK_ML_TREE_BASED_REGRESSION_COMMON_PARAMS + [
    {
        "name": "maxIter",
        "displayName": "Maximum Iteration",
        "defaultValue": 20,
        "acceptedValue": None,
        "valueRange": [1, 100],
        "paramType": "number",
        "uiElemType": "slider",
        "hyperpatameterTuningCandidate": True,
    },
    {
        "name": "stepSize",
        "displayName": "Step Size",
        "defaultValue": 0.1,
        "acceptedValue": None,
        "valueRange": [0.1, 1.0],
        "paramType": "number",
        "uiElemType": "slider",
        "hyperpatameterTuningCandidate": True,
    },
    {
        "name": "lossType",
        "displayName": "Loss Type",
        "defaultValue": [
            {
                "name": "squared",
                "selected": True,
                "displayName": "Squared Loss"
            },
            {
                "name": "absolute",
                "selected": False,
                "displayName": "Huber Loss"
            }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "hyperpatameterTuningCandidate": False,
    },
]
PYSPARK_ML_DTREE_REGRESSION_PARAMS = PYSPARK_ML_TREE_BASED_REGRESSION_COMMON_PARAMS + [
    {
        "name": "varianceCol",
        "displayName": "Variance Column Name",
        "defaultValue": None,
        "acceptedValue": None,
        "paramType": "string",
        "uiElemType": "dropDown",
        "display": False,
        "hyperpatameterTuningCandidate": False,
    },

]
PYSPARK_ML_RF_REGRESSION_PARAMS = PYSPARK_ML_TREE_BASED_REGRESSION_COMMON_PARAMS + [
    {
        "name": "numTrees",
        "displayName": "Number of Trees",
        "defaultValue": 20,
        "acceptedValue": None,
        "valueRange": [1, 1000],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
    },
    {
        "name": "featureSubsetStrategy",
        "displayName": "Feature Subset Strategy",
        "defaultValue": [
            {
                "name": "auto",
                "selected": True,
                "displayName": "Automatic"
            },
            {
                "name": "all",
                "selected": False,
                "displayName": "All"
            },
            {
                "name": "all",
                "selected": False,
                "displayName": "All"
            },
            {
                "name": "onethird",
                "selected": False,
                "displayName": "One-Third"
            },
            {
                "name": "sqrt",
                "selected": False,
                "displayName": "Squared Root"
            },
            {
                "name": "log2",
                "selected": False,
                "displayName": "Log2"
            },
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
    },
]

PYSPARK_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION = [
    {"name": "Variance", "selected": True, "displayName": "Variance"},
]

# Updated Pyspark Regression Config changes

PYSPARK_LINEAR_REGRESSION_PARAMS = [
    {
        "name": "regParam",
        "displayName": "Regularisation parameter",
        "className": "regParam",
        "description": "Regularisation parameter.",
        "defaultValue": 0.0,
        "acceptedValue": None,
        "valueRange": [0.00001, 0.5],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "fitIntercept",
        "displayName": "fitIntercept",
        "description": "Fit an intercept terms.",
        "defaultValue": [
            {
                "name": "false",
                "selected": False,
                "displayName": "False"
            },
            {
                "name": "true",
                "selected": True,
                "displayName": "True"
            }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "elasticNetParam",
        "displayName": "elasticNetParam",
        "className": "elasticNetParam",
        "description": "Elastic Net mixing parameter in the given range.",
        "defaultValue": 0.0,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]

PYSPARK_GBT_REGRESSION_PARAMS = [
    {
        "name": "maxDepth",
        "displayName": "Max Depth Of Trees",
        "description": "The maximum depth of the tree",
        "defaultValue": 5,
        "acceptedValue": None,
        "valueRange": [2, 20],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int", None],
        "allowedDataType": ["int", None]
    },
    {
        "name": "impurity",
        "displayName": "Criterion",
        "description": "Criterion used for information gain calculation.",
        "defaultValue": [obj for obj in PYSPARK_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "maxBins",
        "displayName": "maxBins",
        "description": "Maximum number of bins used for discretizing continuous features and for choosing how to split on features at each node.",
        "defaultValue": 32,
        "acceptedValue": None,
        "valueRange": [40, 300],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "minInstancesPerNode",
        "displayName": "Minimum instance for split",
        "description": "Minimum number of instances each child must have after split.",
        "defaultValue": 1,
        "acceptedValue": None,
        "valueRange": [1, 100],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "minInfoGain",
        "className": "minInfoGain",
        "displayName": "minInfoGain",
        "description": "Minimum information gain for a split to be considered at a tree node.",
        "defaultValue": 0.0,
        "acceptedValue": None,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "lossType",
        "displayName": "Loss Type",
        "className": "lossType",
        "description": "Loss function which GBT tries to minimize.",
        "defaultValue": [
            {
                "name": "squared",
                "selected": True,
                "displayName": "Squared Loss"
            },
            {
                "name": "absolute",
                "selected": False,
                "displayName": "Huber Loss"
            }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "maxIter",
        "displayName": "Maximum Solver Iterations",
        "className": "maxIter",
        "description": "Maximum number of iterations to be attempted for solver operations",
        "defaultValue": 100,
        "acceptedValue": None,
        "valueRange": [10, 400],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "stepSize",
        "displayName": "Step Size",
        "className": "stepSize",
        "description": "Learning rate in interval",
        "defaultValue": 0.1,
        "acceptedValue": None,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]

PYSPARK_DTREE_REGRESSION_PARAMS = [
    {
        "name": "maxDepth",
        "displayName": "Max Depth Of Trees",
        "description": "The maximum depth of the tree",
        "defaultValue": 5,
        "acceptedValue": None,
        "valueRange": [2, 20],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int", None],
        "allowedDataType": ["int", None]

    },
    {
        "name": "minInfoGain",
        "className": "minInfoGain",
        "displayName": "minInfoGain",
        "description": "Minimum information gain for a split to be considered at a tree node.",
        "defaultValue": 0.0,
        "acceptedValue": None,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "maxBins",
        "displayName": "maxBins",
        "description": "Maximum number of bins used for discretizing continuous features and for choosing how to split on features at each node.",
        "defaultValue": 32,
        "acceptedValue": None,
        "valueRange": [40, 300],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    }
]

PYSPARK_RF_REGRESSION_PARAMS = [
    {
        "name": "maxDepth",
        "displayName": "Max Depth",
        "description": "Max number of levels in each decision tree.",
        "defaultValue": 5,
        "acceptedValue": None,
        "valueRange": [2, 20],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int", None],
        "allowedDataType": ["int", None]
    },
    {
        "name": "maxBins",
        "displayName": "No of Bins",
        "description": "Maximum number of bins used for discretizing continuous features and for choosing how to split on features at each node.",
        "defaultValue": 32,
        "acceptedValue": None,
        "valueRange": [40, 300],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "minInstancesPerNode",
        "displayName": "Minimum instance for split",
        "description": "Minimum number of instances each child must have after split.",
        "defaultValue": 1,
        "acceptedValue": None,
        "valueRange": [1, 100],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "minInfoGain",
        "className": "minInfoGain",
        "displayName": "minInfoGain",
        "description": "Minimum information gain for a split to be considered at a tree node.",
        "defaultValue": 0.0,
        "acceptedValue": None,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "impurity",
        "displayName": "Criterion",
        "description": "Criterion used for information gain calculation.",
        "defaultValue": [obj for obj in PYSPARK_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "numTrees",
        "displayName": "No of Estimators",
        "description": "Number of trees in the forest.",
        "defaultValue": 10,
        "acceptedValue": None,
        "valueRange": [10, 1000],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
]
