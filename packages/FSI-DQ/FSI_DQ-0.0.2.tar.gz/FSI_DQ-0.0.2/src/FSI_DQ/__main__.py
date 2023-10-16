import logging
import os
import json
import pandas as pd
import io
import pyspark.pandas as ps
from FSI_DQ.business_contextNB import BusinessContext
from FSI_DQ.AnomalyDetectionNB import AnomalyDetection
from FSI_DQ.StandardizationNB import Standardization
import findspark
from pyspark.sql import SparkSession

from azure.storage.blob import BlobServiceClient

class DataQuality:
    def __init__(self,storage_account_name,connection_string, input_container_name,output_container_name, location_name, file_name,catalog_name,schema,choice,api_key=None,api_base=None,api_version=None,model_name=None,deployment_name=None,standardization_columns=None,inputfile=None, outputfile=None, column_types=None, columns_and_contamination=None,columns_and_null_handling=None, columns_and_dbscan_params=None):
        self.catalog_name=catalog_name
        self.schema=schema
        # self.input_table=input_table


        self.api_key=api_key
        self.api_base=api_base
        self.api_version=api_version
        self.deployment_model=deployment_name
        self.model_name=model_name
        self.choice=choice

        self.standardization_columns=standardization_columns

        self.inputfile=inputfile
        self.outputfile=outputfile
        self.column_types=column_types
        self.columns_and_contamination=columns_and_contamination
        self.columns_and_null_handling=columns_and_null_handling
        self.columns_and_dbscan_params=columns_and_dbscan_params
        self.connection_string=connection_string
        self.input_container_name=input_container_name
        self.output_container_name=output_container_name
        self.location_name=location_name
        self.file_name=file_name

        self.storage_account_name=storage_account_name

    

    #Function to get connection client for ADLS Blob
    def azure_blob_connection(self,connection_string,container_name):
       
        service_client = BlobServiceClient.from_connection_string(connection_string)
        client = service_client.get_container_client(container_name)
        
        return client
    
    def write_dqresult_in_adls(self,df,folderName):
        container_name='dataquality'
        blob_name=f'DQ_result/{folderName}'

        csv_data = df.to_csv(index=False)

        container_name='dataquality'
        client=self.azure_blob_connection(self.connection_string,container_name)
        client.upload_blob(blob_name, csv_data, overwrite=True)



    def main(self):

        spark = SparkSession.builder \
                    .appName("AppName") \
                    .config("spark.sql.catalogDatabase", self.catalog_name) \
                    .config("spark.sql.catalogSchema", self.schema) \
                    .getOrCreate()
        # table_name = self.catalog_name+'.'+self.schema+'.'+self.input_table
        # df = spark.sql(f"SELECT * FROM {table_name}")
        # df= df.toPandas()

        # Reading the input file from ADLS
        client=DataQuality.azure_blob_connection(self,self.connection_string,self.input_container_name)
        file_path=self.location_name+self.file_name
        blob_client = client.get_blob_client(blob=file_path)
        blob_content = blob_client.download_blob().readall()
        csv_io = io.BytesIO(blob_content)
        df = pd.read_csv(csv_io)


        if self.choice['BusinessContext']==1:
            bc_df=df.head(10)
            businessContext= BusinessContext(spark,self.api_key,self.api_base,self.api_version,self.deployment_model,self.model_name)
            result_bc= businessContext.business_contextFN(bc_df)
            final_table=f"{self.schema}.BusinessContext" #{self.catalog_name}.
            print(final_table)
            
            self.write_dqresult_in_adls(self,result_bc,'business_context')


            logging.info(final_table)
            result_bc.write.option("catalog", self.catalog_name).option("name", final_table).mode('overwrite').saveAsTable(final_table)
            #result_bc.to_table(final_table, overwriteSchema=True)
        if self.choice['DQRules']==1:
            businessContext= BusinessContext(spark,self.api_key,self.api_base,self.api_version,self.deployment_model,self.model_name)
            result_dq= businessContext.dq_rulesFN(df)
            final_table=f"{self.schema}.DQRules" #{self.catalog_name}.
            result_dq.write.option("catalog", self.catalog_name).option("name", final_table).mode('overwrite').saveAsTable(final_table)
            # result_dq.to_table(final_table, overwriteSchema=True)

            self.write_dqresult_in_adls(self,df,'DQRules')

        if self.choice['AnomalyDetection']==1:
            result=AnomalyDetection(self.inputfile, self.outputfile, self.column_types, self.columns_and_contamination,
                 self.columns_and_null_handling, self.columns_and_dbscan_params).run_anomaly_detection(df)
            final_table=f"{self.schema}.AnomalyDetectionResult"#{self.catalog_name}.
            result=spark.createDataFrame(result)
            result.write.option("catalog", self.catalog_name).option("name", final_table).mode('overwrite').saveAsTable(final_table)
            #result.to_table(final_table, overwriteSchema=True)

            self.write_dqresult_in_adls(self,df,'AnomalyDetectionResult')
        if self.choice['Standardization']==1:
            result=Standardization(spark,self.standardization_columns,df,self.api_key,self.api_base,self.api_version,self.deployment_model,self.model_name).format_issue_detection()
            final_table=f"{self.schema}.StandardizationResult"#{self.catalog_name}.
            result.write.option("catalog", self.catalog_name).option("name", final_table).mode('overwrite').saveAsTable(final_table)
            # result.to_table(final_table, overwriteSchema=True)
            self.write_dqresult_in_adls(self,df,'StandadrizationREsult')
