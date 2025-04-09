from sklearn.impute import SimpleImputer  # handling missing values
from sklearn.preprocessing import StandardScaler  # scaling numerical variables
from sklearn.preprocessing import OrdinalEncoder  # encoding categorical variables
# Pipelines
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logging
import sys
import os
from dataclasses import dataclass

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl') # path to save the preprocessor object

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            logging.info("Data Transformation started")

            # Categorical and Numerical Variables
            categorical_cols=['cut','color','clarity']
            numerical_cols=['carat','depth','table','x','y','z']

            # define ranking for each ordinal/categorical variable
            cut_categories=['Fair','Good','Very Good','Premium','Ideal']
            color_categories=['D','E','F','G','H','I','J']
            clarity_categories=['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            logging.info('Data Transformation Pipeline Initiated')

            # Numerical Pipeline
            num_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),  # handling missing values
                    ('scaler',StandardScaler())  # scaling numerical variables

                ]
            )

            # Categorical Pipeline
            cat_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy="most_frequent")),  # handling missing values
                    ('encoder',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),  # encoding categorical variables
                    ('scaler',StandardScaler())  # scaling variables
                ]
            )

            preprocessor=ColumnTransformer([
                ('num_pipeline',num_pipeline,numerical_cols),
                ('cat_pipeline',cat_pipeline,categorical_cols)  # applying categorical pipeline to categorical variables
            ]
            )
            logging.info("Data Transformation Pipeline Completed")

            return preprocessor

        except Exception as e:
            logging.info("Exceptiuon occured in data transformation")
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):

        try:
            # Read the data
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info('Read train and test data completed')
            logging.info(f'Train Dataframe head:\n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe head:\n{test_df.head().to_string()}')

            logging.info('Obtaining preprocessor object')
            preprocessing_obj=self.get_data_transformation_object()

            target_column='price'
            drop_columns=[target_column,'id']

           # Splitting the data into input and target features
            # for train dataframes
            input_feature_train_df=train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column]

            # for test dataframes
            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column]

            # Data Transformation

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_array=np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_array=np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return(
                train_array,
                test_array,
                self.data_transformation_config.preprocessor_obj_file_path
            )

            logging.info('Data Transformation completed')




        except Exception as e:
            raise CustomException(e, sys)