from bi.common.decorators import accepts
import numpy as np


class AlgorithmParameters:

    def __init__(self):
        self.name = None
        self.description = None
        self.displayName = None
        self.paramType = None
        self.defaultValue = None
        self.acceptedValue = None
        self.valueRange = None
        self.uiElemType = None
        self.diplay = None
        self.hyperpatameterTuningCandidate = None


    def set_params(self,algoParamObj):
        if "name" in algoParamObj:
            self.name = algoParamObj["name"]
        if "description" in algoParamObj:
            self.description = algoParamObj["description"]
        if "displayName" in algoParamObj:
            self.displayName = algoParamObj["displayName"]
        if "paramType" in algoParamObj:
            self.paramType = algoParamObj["paramType"]
        if "defaultValue" in algoParamObj:
            self.defaultValue = algoParamObj["defaultValue"]
        if "acceptedValue" in algoParamObj:
            if algoParamObj["acceptedValue"] != None:
                # self.acceptedValue = float(algoParamObj["acceptedValue"])
                self.acceptedValue = algoParamObj["acceptedValue"]

        if "valueRange" in algoParamObj:
            self.valueRange = algoParamObj["valueRange"]
        if "uiElemType" in algoParamObj:
            self.uiElemType = algoParamObj["uiElemType"]
        if "diplay" in algoParamObj:
            self.diplay = algoParamObj["diplay"]
        if "hyperpatameterTuningCandidate" in algoParamObj:
            self.hyperpatameterTuningCandidate = algoParamObj["hyperpatameterTuningCandidate"]

    def get_name(self):
        return self.name
    def get_param_type(self):
        return self.paramType
    def get_uielem_type(self):
        return self.uiElemType
    def get_value_range(self):
        return self.valueRange
    def check_for_tuning(self):
        return self.hyperpatameterTuningCandidate
    def get_accepted_value(self):
        return self.acceptedValue
    def get_default_value(self):
        if type(self.defaultValue) == list:
            filteredVal = filter(lambda x:x["selected"] == True,self.defaultValue)[0]["name"]
            if filteredVal not in ["True","False"]:
                return  filteredVal
            else:
                if filteredVal == "True":
                    return True
                else:
                    return False
        else:
            if self.defaultValue != None:
                # return float(self.defaultValue)
                return self.defaultValue

            else:
                return self.defaultValue

    def hyperParameterInputParser(self,stringObj):
        out = []
        blocks =  stringObj.split(",")
        for val in blocks:
            subBlocks = val.split("-")
            if len(subBlocks) == 1:
                if "." in subBlocks[0]:
                    out += [float(subBlocks[0])]
                else:
                    out += [int(subBlocks[0])]
            elif len(subBlocks) == 2:
                startVal = subBlocks[0]
                endVal = subBlocks[1]
                startValPrecision,endValPrecision = 0,0
                floatType = False
                if "." in startVal:
                    floatType = True
                    startValPrecision = len(startVal.split(".")[1])
                if "." in endVal:
                    floatType = True
                    endValPrecision = len(endVal.split(".")[1])
                precision = max(endValPrecision,startValPrecision)
                if precision > 0:
                    valRange = list(np.arange(float(startVal),float(endVal),1.0/(10**precision)))
                else:
                    valRange = range(int(startVal),int(endVal))
                out += valRange
        return out


    def get_param_value(self,hyperParams=True):
        defaultValue = self.get_default_value()
        if hyperParams:
            if self.hyperpatameterTuningCandidate != True:
                if self.acceptedValue != None:
                    if self.name != "tol":
                        return {self.name:self.acceptedValue}
                    else:
                        return {self.name:1.0/10**self.acceptedValue}
                else:
                    if self.name != "tol":
                        return {self.name:defaultValue}
                    else:
                        return {self.name:1.0/10**self.defaultValue}
            else:
                if self.paramType != "list":
                    if self.acceptedValue == None:
                        self.acceptedValue = self.defaultValue
                    outRange = self.hyperParameterInputParser(str(self.acceptedValue))
                    if self.name != "tol":
                        return {self.name:outRange}
                    else:
                        return {self.name:[1.0/10**x for x in outRange]}
                else:
                    filteredVal = filter(lambda x:x["selected"] == True,self.defaultValue)
                    outList = [x["name"] for x in filteredVal]
                    outListMod = []
                    for x in outList:
                        if x not in ["True","False"]:
                            outListMod.append(x)
                        else:
                            if x == "True":
                                outListMod.append(True)
                            else:
                                outListMod.append(False)
                    return {self.name:outListMod}
        else:
            if self.acceptedValue != None:
                if self.name != "tol":
                    return {self.name:self.acceptedValue}
                else:
                    return {self.name:1.0/10**self.acceptedValue}
            else:
                if self.name != "tol":
                    return {self.name:defaultValue}
                else:
                    return {self.name:1.0/10**self.defaultValue}



class HyperParameterSetting:
    def __init__(self):
        self.selected = None
        self.name = None
        self.displayName = None
        self.params = []
    def set_params(self,hyperParameterObj):
        if "name" in hyperParameterObj:
            self.name = hyperParameterObj["name"]
        if "selected" in hyperParameterObj:
            self.selected = hyperParameterObj["selected"]
        if "displayName" in hyperParameterObj:
            self.displayName = hyperParameterObj["displayName"]
        if "params" in hyperParameterObj:
            paramsArr = hyperParameterObj["params"]
            outArray = []
            if paramsArr != None:
                for paramObj in paramsArr:
                    algoParamsInstance = AlgorithmParameters()
                    algoParamsInstance.set_params(paramObj)
                    outArray.append(algoParamsInstance)
                self.params = outArray

    def get_name(self):
        return self.name
    def is_selected(self):
        return self.selected
    def get_params(self):
        return self.params



class AlgorithmParameterConfig:
    def __init__(self):
        self.description = None
        self.selected = None
        self.algorithmSlug = None
        self.algorithmName = None
        self.hyperParameterSetting = []
        self.parameters = []

    def set_params(self,algoParamObj):
        if "description" in algoParamObj:
            self.description = algoParamObj["description"]
        if "selected" in algoParamObj:
            self.selected = algoParamObj["selected"]
        if "algorithmSlug" in algoParamObj:
            self.algorithmSlug = algoParamObj["algorithmSlug"]
        if "algorithmName" in algoParamObj:
            self.algorithmName = algoParamObj["algorithmName"]
        if "hyperParameterSetting" in algoParamObj:
            hyperSettingArr = []
            hyperParamArray = algoParamObj["hyperParameterSetting"]
            for hyperParamObj in hyperParamArray:
                hyperParameterSettingInstance = HyperParameterSetting()
                hyperParameterSettingInstance.set_params(hyperParamObj)
                hyperSettingArr.append(hyperParameterSettingInstance)

            self.hyperParameterSetting = hyperSettingArr

        if "parameters" in algoParamObj:
            paramArr = []
            paramArrInput = algoParamObj["parameters"]
            for paramObj in paramArrInput:
                algoParamsInstance = AlgorithmParameters()
                algoParamsInstance.set_params(paramObj)
                paramArr.append(algoParamsInstance)
            self.parameters = paramArr

    def is_selected(self):
        return self.selected

    def get_algorithm_name(self):
        return self.algorithmName

    def get_algorithm_slug(self):
        return self.algorithmSlug

    def is_hyperparameter_tuning_enabled(self):
        hyperCheckArr = [obj.is_selected() & len(obj.get_params()) > 0  for obj in self.hyperParameterSetting]
        if True in hyperCheckArr:
            return True
        else:
            return False

    def get_hyperparameter_params(self):
        hyperParamsObj = [obj for obj in self.hyperParameterSetting if (obj.is_selected() & len(obj.get_params()) > 0) == True][0]
        hyperParamsArray = hyperParamsObj.get_params()
        params_dict = {}
        for obj in hyperParamsArray:
            params_dict.update(obj.get_param_value(hyperParams=False))
        return params_dict

    def get_hyperparameter_algo_name(self):
        hyperParamsObj = [obj for obj in self.hyperParameterSetting if (obj.is_selected() & len(obj.get_params()) > 0) == True][0]
        return hyperParamsObj.get_name()

    def get_params_dict(self):
        params_dict = {}
        for obj in self.parameters:
            params_dict.update(obj.get_param_value(hyperParams=False))
        return params_dict

    def get_params_dict_hyperparameter(self):
        params_dict = {}
        for obj in self.parameters:
            if obj.check_for_tuning():
                params_dict.update(obj.get_param_value())
        return params_dict
