import openai
import os
from langchain.llms import AzureOpenAI
import pyspark.pandas as ps
import json
from langchain.agents import create_pandas_dataframe_agent


class BusinessContext:
    def __init__(self,spark,api_key,api_base,api_version,deployment_model,model_name):
                
        
        """ Initialize the class
            Params:
            agent: Langchain agent which can be use to get the result from ai model using prompt as input.
        """
        self.spark=spark
        self.api_key=api_key
        self.api_base=api_base
        self.api_version=api_version
        self.deployment_model=deployment_model
        self.model_name=model_name


    def initiate_langchainFN(self):
            os.environ["OPENAI_API_TYPE"] = "azure"

            os.environ["OPENAI_API_KEY"] = self.api_key

            os.environ["OPENAI_API_BASE"] = self.api_base

            os.environ["OPENAI_API_VERSION"] = self.api_version


            llm = AzureOpenAI(

                    openai_api_type="azure",

                    deployment_name=self.deployment_model,

                    model_name=self.model_name,

                    temperature=0)

            #agent = create_pandas_dataframe_agent(llm, df, verbose=False, max_iterations=10)
            return llm

    def business_contextFN(self,df):
        llm=self.initiate_langchainFN()
        #agent = create_pandas_dataframe_agent(llm,df, verbose=False, max_iterations=10)
        agent=create_pandas_dataframe_agent(llm,df,verbose=False, max_iterations=10)
        prompt = """Understand the given dataset and generate the business context of the data.
            The Business context of the data will include the name, description, the domain of data and the entities or attributes associated with the data.
            The output should be in json structure with above mentioned points as keys. Please give a little detailed explanation in values and explain the attributes. 
            Return the final answer in json format.
            """
        llm=self.initiate_langchainFN()
        agent = create_pandas_dataframe_agent(llm, df, verbose=False, max_iterations=10)
        business_context=agent.run(prompt)

        #business_context = ps.DataFrame([business_context], columns=['Business_Context'])
        business_context=self.spark.createDataFrame([(business_context,)], ["Business_Context"])
        return business_context
    
    def dq_rulesFN(self,df):
        prompt="""
        Understand the given dataset and generate a set of data quality checks which can be applied on the dataset. The information about the checks is as following-
        Null check- If the value of the column should not be Null for a record. Example of null check- for a policy data, Null check can be applied for the policy id and name but cannot be applied for duration.
        Unique check- If the value of the column should be Unique for a record. For Example for a employee data, unique check can be applied for -employeeid  but not for name and salary.
        Pattern check- If some regex pattern is supposed to be checked for the record. Example of pattern check- a regex for Checking if first alphabet of a Name column value is capital, regex to check if a phone number column has all digits, similarly for gender and date columns.
        The result should be a json with below structure-
        {
        "Null check": ["Column1", "Column2", ...],
        "Unique check": ["Column3", "Column4", ...],
        "Pattern check":{"Column1":"pattern1","Column2":"pattern2",...}
        }
        """
        llm=self.initiate_langchainFN()
        agent = create_pandas_dataframe_agent(llm, df, verbose=False, max_iterations=10)
        dq_rules=agent.run(prompt)
        #df = ps.DataFrame([dq_rules],columns=['Data_Quality_Rules'])
        df=self.spark.createDataFrame([(dq_rules,)],['Data_Quality_Rules'])
        return dq_rules