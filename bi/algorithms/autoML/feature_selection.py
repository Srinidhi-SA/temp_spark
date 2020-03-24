import pandas as pd
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier

class FeatureSelection():

    def __init__(self, data_frame, target, data_change_dict, numeric_cols, dimension_cols, datetime_cols,problem_type):
        self.data_frame = data_frame
        self.target = target
        self.problem_type = problem_type
        self.numeric_cols = numeric_cols
        self.dimension_cols = dimension_cols
        self.datetime_cols = datetime_cols
        self.data_change_dict = data_change_dict
        self.data_change_dict['SelectedColsTree'] = []
        self.data_change_dict['SelectedColsLinear'] = []

    def feat_importance(self):
        model = ExtraTreesClassifier()
        X_train = self.data_frame.drop(self.target, axis=1)
        X_train = X_train[X_train._get_numeric_data().columns]
        Y_train = self.data_frame[self.target]
        # print (list(training_set))
        model.fit(X_train, Y_train)
        feat_importances = pd.Series(model.feature_importances_, index=X_train.columns)
        number_of_cols_to_consider = int(len(X_train.columns)*0.7)
        # print (feat_importances.nlargest(number_of_cols_to_consider))
        cols_considered = []
        for i, v in feat_importances.items():
            if v > 0:
                cols_considered.append(i)
        self.data_change_dict['SelectedColsTree'] = cols_considered
        return cols_considered
