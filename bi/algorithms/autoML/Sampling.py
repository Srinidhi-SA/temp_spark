import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from imblearn.over_sampling import SMOTE, SMOTENC
from collections import Counter
import math
import pandas as pd

class Sampling:
    
    '''  

        Docstring:

        "Class to handle Class Imbalanced Problems"

        Techniques Used: Over-sample using SMOTE for for dataset containing only continuous or SMOTE-NC for dataset containing continuous and categorical features(Date columns also included).

        Parameters
        ----------
        
        dataset : DataFrame
            DataFrame to be sampled

        target : str
            string containing Target column name

    '''
    
    
    def __init__(self, dataset, target):
        
        self.dataset = dataset
        self.target = target
        self.cat_col_names = None

    def OverSampling(self):
        
        '''  function to sample the dataset '''
        
        # getting Independent Variables and Dependent Variable
        X_train, y_train = self.dataset.drop(self.target, inplace=False,axis = 1), self.dataset[self.target]
        
        # getting the Categorical Column names (if any)
        self.cat_col_names = list(X_train.select_dtypes(include=['object','datetime64']).columns)
        
        # no. of classes limit for sampling # constraint is adjustable
        multiclass_limit = 5
        
        # Min No. of observations for each class # constraint is adjustable
        min_class_value_count = 10
        
        # counts of each class
        class_value_counts = y_train.value_counts() 
        
        # number of classes 
        num_classes = len(class_value_counts)
        
        # first check for sampling
        if num_classes <= multiclass_limit and min(Counter(y_train).values()) >= min_class_value_count:
                
            # Size constraints are adjustable
            binary = 2

            # size of the dataset
            dataset_size = len(y_train) 

            # constraint is adjustable
            if num_classes == binary:
                big_data = 75000
            else:
                big_data = 25000
            
            # second check for sampling
            if  dataset_size <= big_data:

                # percentages of each class in the target variable
                percentage =[(i*100)/dataset_size for i in list(class_value_counts)] 

                # threshold for class imbalance problem
                threshold = 1/(2*float(num_classes))                             

                # minority Classes to over-sample
                to_oversample_classes = [class_value_counts.index[i] for i,d in enumerate(percentage) if d < (threshold*100)] 

                # third check for sampling
                if len(to_oversample_classes)>0:
                    
                    # for Binary 
                    if num_classes == binary:
                        
                        # size of majority class
                        majority_class_size = class_value_counts[0]
                        
                        threshold_count = math.ceil((majority_class_size*threshold)/(1-threshold))
                        ratio = {to_oversample_classes[i]: math.ceil(threshold_count) for i in range(len(to_oversample_classes))}
                    
                    # for Multi-class 
                    else: 
                        threshold_count = math.ceil(threshold*dataset_size) 
                        ratio = {to_oversample_classes[i]: threshold_count for i in range(len(to_oversample_classes))}

                    # Over-sample using SMOTE-NC for dataset containing continuous and categorical features(Date columns also included).
                    if len(self.cat_col_names) != 0:
                        
                        # getting the categorical column index
                        cat_cols_index = []
                        for i in self.cat_col_names:
                            cat_col_index = X_train.columns.get_loc(i)
                            cat_cols_index.append(cat_col_index)

                        X_train_sampled, y_train_sampled = SMOTENC(random_state = 1, sampling_strategy  = ratio, categorical_features = cat_cols_index).fit_sample(X_train,y_train)

                    # Over-sample using SMOTE for for dataset containing only continuous. 
                    else:

                        X_train_sampled, y_train_sampled = SMOTE(random_state = 1, sampling_strategy  = ratio).fit_sample(X_train,y_train) 
                        
                    X_train_sampled = pd.DataFrame(X_train_sampled)
                    
                    # updating the dataset with sampled dataset 
                    self.dataset = pd.concat([X_train_sampled, y_train_sampled], axis = 1) 
                    
                    print("*"*10 + "SAMPLING SUCCESSFUL" + "*"*10)
                
                else:
                    print("*"*10 + "SAMPLING NOT REQUIRED" + "*"*10)
            else:
                print("*"*10 + "DATASET TOO BIG FOR SAMPLING" + "*"*10)
    
        else:
            print("*"*10 + "DATASET NOT ELIGIBLE FOR SAMPLING" + "*"*10)