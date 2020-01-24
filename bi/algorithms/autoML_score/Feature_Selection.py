#!/usr/bin/env python
# coding: utf-8

# # FeatureSelection

import warnings

warnings.filterwarnings("ignore")

import pandas as pd

"""Tree_fea_sel_tech class libraries"""

from sklearn.ensemble import ExtraTreesClassifier

from sklearn.ensemble import ExtraTreesRegressor

""" Linear_fea_sel_tech class libraries """

from scipy.stats import chi2_contingency

from sklearn.feature_selection import f_classif,f_regression

import statsmodels.api as sm

from statsmodels.formula.api import ols

""" Utils class libraries """

from sklearn.preprocessing import LabelEncoder,OneHotEncoder





"""Feature Selection Techniques w.r.t Linear based models"""

class Linear_fea_sel_tech(object):

    def __init__(self,Dataframe,target,cat_col,num_col):

        self.Dataframe = Dataframe

        self.target = target

        self.cat_col = cat_col

        self.num_col = num_col

    """one way anova or two way anova depends on categorical columns(categorical vs continous)"""

    def anova(self):

        if len(self.cat_col)>1:

            individual = ' + '.join(self.cat_col)

            String = str(self.target)+ ' ~ ' '+'+individual

            mod = ols(String, data = self.Dataframe).fit()

            aov_table = sm.stats.anova_lm(mod, typ=2)

            anova_fea_imp = []

            for idx,col_name in enumerate(self.cat_col):

                anova_fea_imp.append([col_name, round(aov_table['PR(>F)'][idx],3)])

            return dict(anova_fea_imp)

        else:

            String = self.target+ ' ~ ' +self.cat_col[0]

            mod = ols(String, data = self.Dataframe).fit()

            aov_table = sm.stats.anova_lm(ols(self.target+ ' ~ ' +self.cat_col[0], data = self.Dataframe).fit(), typ=1)

            anova_fea_imp = zip(self.cat_col,[round(aov_table['PR(>F)'][0],3)])

            return dict(anova_fea_imp)

    """f_regression(continous vs continous)"""

    def f_regress(self):

        X = self.Dataframe[self.num_col]

        Y = self.Dataframe[self.target]

        f_p_values = f_regression(X,Y)

        p_values = []

        for idx, col_name in enumerate(X.columns):

            p_values.append([col_name,round(f_p_values[1][idx],3)])

        return dict(p_values)

    """chi2(categorical vs categorical)"""

    def chi2(self):

        p_values = []

        for idx,col_name in enumerate(self.cat_col):

            chi2, p_value, dof, expected = chi2_contingency(pd.crosstab(self.Dataframe[col_name],self.Dataframe[self.target]))

            p_values.append([col_name,round(p_value,3)])

        return dict(p_values)

    """f_classifier(continous vs categorical)"""

    def f_class(self):

        X = self.Dataframe[self.num_col]

        Y = self.Dataframe[self.target]

        f_p_values = f_classif(X,Y)

        p_values = []

        for idx, col_name in enumerate(X.columns):

            p_values.append([col_name,round(f_p_values[1][idx],3)])

        return dict(p_values)

    """Filtering the columns based on p-values"""

    def pvalue_significance(self,p_values_dict):

        fea_sel = [key for key,value in p_values_dict.items() if value <= 0.05 ]

        return fea_sel



""" Feature Selection Techniques w.r.t Tree based models """

class Tree_fea_sel_tech(object):

    def __init__(self,X,Y,cat_col,Dataframe):

        self.X = X

        self.Y = Y

        self.cat_col = cat_col

        self.Dataframe = Dataframe

        self.Pattern_col,self.veri_col,self.Tree_fea_sel = [],[],[]

    """ExtraTreesRegressor for regression"""

    def Tree_Regressor(self):

        clf = ExtraTreesRegressor()

        clf = clf.fit(self.X,self.Y)

        return clf

    """ExtraTreesClassifier for Classification"""

    def Tree_Classifier(self):

        clf = ExtraTreesClassifier()

        clf = clf.fit(self.X,self.Y)

        return clf

    """Feature Selection for Tree Based Models"""

    def Fea_imp(self,model,dum_col):

        """Feature selection is based on feature importances of a model

              which is not equal to 0.0 after rounding to 3 decimals"""

        Tree_fea_imp = []

        for idx, col_name in enumerate(self.X.columns):

            Tree_fea_imp.append([col_name, round(model.feature_importances_[idx],3)])

        Tree_fea_imp_dict = dict(Tree_fea_imp)

        self.Tree_fea_sel = [key for key,value in Tree_fea_imp_dict.items() if value != 0.0 ]

        if self.Tree_fea_sel != []:

            """All respectives dummy features will be replaced as respective columns in feature selection list"""

            if dum_col != []:

                for col in dum_col:

                    labels = list(self.Dataframe[col].value_counts().index)

                    labels.sort()

                    labels.pop(0)

                    for label in labels:

                        Pattern = col+label

                        if Pattern in self.Tree_fea_sel:

                            self.Pattern_col.append(Pattern)

                            self.veri_col.append(col)

                self.Tree_fea_sel = set(self.Tree_fea_sel)-set(self.Pattern_col)

                self.Tree_fea_sel = set(self.Tree_fea_sel) | set(self.veri_col)

                return list(self.Tree_fea_sel)

            else:

                return list(self.Tree_fea_sel)
        else:

            return self.Tree_fea_sel


"""Commonly repeated or general functions in this module"""

class Utils(object):

    """Encoding Rule - sqrt(n,2)>=p based on this,dummy or label encoding is decided"""

    def cat_en_rule(self,Dataframe,cat_col):

        labels_count = [[len(Dataframe[col].value_counts().index)-1,col]for col in cat_col]

        labels_count.sort()

        dum_col = []

        n,p = Dataframe.shape[0],Dataframe.shape[1]

        for i in range(len(labels_count)):

            p = p+labels_count[i][0]

            if round(n**(1/2)) >= p:

                dum_col.append(labels_count[i][1])

        return dum_col

    """Label encoding"""

    def label_en(self,Dataframe,col):

        for col_name in col:

            Dataframe[col_name] = LabelEncoder().fit_transform(Dataframe[col_name].astype(str))

        return Dataframe

    """Categorical columns extraction excluding target"""

    def cat_col_f(self,Dataframe,target):

        #cat_col = [col for col in list(Dataframe) if Dataframe[col].dtype == "O"]
        #cat_col = cat_col+[col for col in list(Dataframe) if Dataframe[col].dtype == "category"]
        #cat_col = list(set(cat_col))

        cat_col = list(Dataframe.select_dtypes(include=['object','category']).columns)

        try:
            cat_col.remove(target)

            return cat_col

        except:

            return cat_col

    """Categorical columns extraction excluding target"""

    def num_col_f(self,Dataframe,target):

        col1 = [col for col in list(Dataframe) if str(Dataframe[col].dtype).startswith("int")]

        col2 = [col for col in list(Dataframe) if str(Dataframe[col].dtype).startswith("float")]

        num_col = col1 + col2

        try:
            num_col.remove(target)

            return num_col

        except:

            return num_col

    """Date datatype columns removals"""

    def date_remove(self,Dataframe):

        Date = [col for col in list(Dataframe) if Dataframe[col].dtype == '<M8[ns]']

        col = list(Dataframe)

        if Date !=[]:

            for i in Date:

                col.remove(i)

            return col

        else:

            return col

    """Restoring dummies of respective feature selection"""

    def label_form(self,Dataframe,dum_veri_col,Tree_fea_sel):

        veri_col = list(set(dum_veri_col))

        Pattern = []

        for col in veri_col:

            labels = list(Dataframe[col].value_counts().index)

            labels.sort()

            labels.pop(0)

            for label in labels:

                Pattern.append(col+label)

        Pattern = list((set(Tree_fea_sel)-set(veri_col))|set(Pattern))

        return Pattern

    """merging independent and dependent columns"""

    def merge_split(self,X,Y):

        target = list(Y)

        X[target] = Y[target]

        return X

    """splitting independent and dependent columns"""

    def dataframe_split(self,Dataframe,target):

        X = Dataframe.drop(target, axis=1)

        Y = Dataframe[[target]]

        return X,Y

    """ Sklearn Onehotencoder drop first """

    def Onehotencoder(self,X,col):

        temp = X[[col]]

        enc = OneHotEncoder(drop='first')

        k = enc.fit_transform(temp).toarray()

        temp = pd.DataFrame(k,columns=list(enc.get_feature_names()))

        feature_names = list(enc.get_feature_names())

        temp.set_index(X.index,inplace = True)

        for col_name in feature_names:

            X[col+col_name.partition('_')[2]] = temp[col_name]

        X.drop(col,axis = 1,inplace = True)

        return X



"""Feature Selection Main Code """

class Main(object):

    def __init__(self,Dataframe,data_dict,pass_2):

        self.info = {'linear_features': [],

                     'tree_features'  : [],

                     'dummy'          :{'linear':[],

                                        'tree'  :[]},

                    'labelencoder'    :{'linear':[],

                                        'tree'  :[]}}

        self.Dataframe = Dataframe

#         self.Dataframe.reset_index(inplace = True)

#         self.Dataframe.drop(self.Dataframe.columns[[0]],axis=1,inplace = True)

        self.data_dict = data_dict

        self.pass_2 = pass_2

        self.target = self.data_dict['target']

        self.apptype = self.data_dict['app_type'].lower()

        self.utils = Utils()

    """ feature selection are converted to dummies and label encoded"""

    def empty_feature(self,linear_col,key):

        X,Y = self.utils.dataframe_split(self.Dataframe,self.target)

        X = X[linear_col]

        cat_col_l = self.utils.cat_col_f(X[linear_col],self.target)

        dum_col_l = self.utils.cat_en_rule(X,cat_col_l)

        self.info['dummy'][key] = dum_col_l

        en_label_l = list(set(cat_col_l)-set(dum_col_l))

        self.info['labelencoder'][key] = en_label_l

        X = self.utils.label_en(X,en_label_l)

        if dum_col_l != []:

            for col in dum_col_l:

                X = self.utils.Onehotencoder(X,col)

        linear_col_en = self.utils.merge_split(X,Y)

        return linear_col,linear_col_en

    """This is the main function of a linear based  feature selection"""

    def linear_run(self,cat_col,num_col,col):

        cat,num = [],[]

        Linear_fea = Linear_fea_sel_tech(self.Dataframe,self.target,cat_col,num_col)

        if self.apptype == "classification":

            if cat_col != []:

                cat = Linear_fea.chi2()

                cat = Linear_fea.pvalue_significance(cat)

            if num_col != []:

                num = Linear_fea.f_class()

                num = Linear_fea.pvalue_significance(num)

            linear_col = list(set(cat)|set(num))

        else:

            if cat_col != []:

                cat = Linear_fea.anova()

                cat = Linear_fea.pvalue_significance(cat)

            if num_col != []:

                num = Linear_fea.f_regress()

                num = Linear_fea.pvalue_significance(num)

            linear_col = list(set(cat)|set(num))

        if linear_col == []:

            linear_col = col

        linear_col,linear_col_en = self.empty_feature(linear_col,'linear')

        return linear_col,linear_col_en

    """This is the main function of a tree based  feature selection"""

    def tree_run(self,cat_col,col,num_col):

        X,Y = self.utils.dataframe_split(self.Dataframe,self.target)

        dum_col = self.utils.cat_en_rule(X,cat_col)

        en_label = list(set(cat_col)-set(dum_col))

        X = self.utils.label_en(X,en_label)

        if dum_col != []:

            for col in dum_col:

                X = self.utils.Onehotencoder(X,col)

        Tree_fea = Tree_fea_sel_tech(X,Y,cat_col,self.Dataframe)

        if self.apptype == "classification":

            model = Tree_fea.Tree_Classifier()

            tree_col = Tree_fea.Fea_imp(model,dum_col)

        else :

            model = Tree_fea.Tree_Regressor()

            tree_col = Tree_fea.Fea_imp(model,dum_col)

        if tree_col == []:

            tree_col = col

            tree_col,tree_col_en = self.empty_feature(tree_col,'tree')

            return tree_col,tree_col_en

        else:

            self.info['dummy']['tree'] = list(set(Tree_fea.veri_col))

            temp = list(set(self.utils.cat_col_f(self.Dataframe[tree_col],self.target))-set(Tree_fea.veri_col))

            self.info['labelencoder']['tree'] = temp

            tree_col_en = self.utils.label_form(self.Dataframe,Tree_fea.veri_col,tree_col)

            tree_col_en = self.utils.merge_split(X[tree_col_en],Y)

            return tree_col,tree_col_en

    """This is the main function of a feature selection"""

    def run(self):

        if self.apptype == "classification":

            if str(self.Dataframe[self.target].dtype).startswith('float') :

                self.Dataframe[self.target] = self.Dataframe[self.target].astype('int')

        cat_col = self.utils.cat_col_f(self.Dataframe,self.target)

        num_col = self.utils.num_col_f(self.Dataframe,self.target)

        col = self.utils.date_remove(self.Dataframe)

        self.Dataframe = self.Dataframe[col]

        col = list(set(col)-set([self.target]))

        self.info['linear_features'],linear_col_en = self.linear_run(cat_col,num_col,col)

        self.info['tree_features'],tree_col_en = self.tree_run(cat_col,col,num_col)

        """ Saving the Dataframe as CSV file """

        linear_col_en.to_csv('linear.csv')

        tree_col_en.to_csv('tree.csv')


        """ Selected flag is created and updated flag in two dictionaries """

        li = list(set(self.info['linear_features']+self.info['tree_features']))


        for idx in range(len(self.data_dict['Column_settings'])):

            if self.data_dict['Column_settings'][idx]['re_column_name'] in li:

                self.data_dict['Column_settings'][idx]['selected'] = True

            else:

                self.data_dict['Column_settings'][idx]['selected'] = False


        for idx in range(len(self.pass_2['Column_settings'])):

            if self.pass_2['Column_settings'][idx]['re_column_name'] in li:

                self.pass_2['Column_settings'][idx]['selected'] = True

            else:

                self.pass_2['Column_settings'][idx]['selected'] = False



        """One click dictinary is updating """

        self.data_dict['pass_2'] = self.pass_2

        self.data_dict.update(self.info)

        return linear_col_en,tree_col_en
