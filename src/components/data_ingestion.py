import os
import sys
from src.logger import logging # custom logging
from src.exception import CustomException # custom exception handling

# First read dataset
import pandas as pd
from sklearn.model_selection import train_test_split # for splitting dataset

from dataclasses import dataclass # it is special placeholder

# Initialize the Data ingestiomn configurations

@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join('artifacts','train.csv')  # path to save train data
    test_data_path:str=os.path.join('artifacts','test.csv')    # path to save test data
    raw_data_path:str=os.path.join('artifacts','data.csv')     # path to save raw data

# Data ingestion class
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Data Ingestion Method Starts')

        try:
            df=pd.read_csv(os.path.join('notebooks/data','gemstone.csv')) # read the dataset
            logging.info('Dataset read as pandas DataFrame')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True) # create directory if not exists
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True) # save the dataset to csv file

            logging.info('Raw data is Created')

            train_set,test_set=train_test_split(df, test_size=0.3,random_state=42) # split the dataset into train and test set

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True) # save the train set to csv file
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True) # save the test set to csv file

            logging.info('Ingestion of data is completed')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )



        except Exception as e:
            logging.info('Exception occurred in data ingestion method')
            raise CustomException(e,sys)