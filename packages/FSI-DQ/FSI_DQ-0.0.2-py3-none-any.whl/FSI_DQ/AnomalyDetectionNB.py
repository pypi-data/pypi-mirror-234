import pyspark.pandas as ps
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN

class AnomalyDetection:

    def __init__(self, column_types, columns_and_contamination,columns_and_null_handling,columns_and_dbscan_params):
            self.column_types = column_types
            self.columns_and_contamination = columns_and_contamination
            self.columns_and_null_handling = columns_and_null_handling
            self.columns_and_dbscan_params = columns_and_dbscan_params
    # def load_dataset(self):
    #     try:
    #         dataset = pd.read_csv(self.inputfile)
    #         return dataset
    #     except Exception as e:
    #         print(f"Error loading dataset: {str(e)}")
    #         return None

    def select_columns(self, dataset, columns_to_use):
        selected_data = dataset[columns_to_use]
        return selected_data

    def replace_null_with_mean(self, data):
        return data.fillna(data.mean())

    def replace_null_with_zero(self, data):
        return data.fillna(0)

    def apply_scaling(self, data):
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        return pd.DataFrame(scaled_data, columns=data.columns)

    def apply_isolation_forest(self, data, contamination):
        isolation_forest = IsolationForest(contamination=contamination)
        data['IFanomaly'] = isolation_forest.fit_predict(data)
        return data

    def apply_dbscan(self, data, eps, min_samples):
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        data['DBSCAN_Labels'] = dbscan.fit_predict(data)
        return data

    def preprocess_data(self, data, target_column):
        label_encoder = LabelEncoder()
        data[target_column] = label_encoder.fit_transform(data[target_column])
        return data
    
    
    def run_anomaly_detection(self,df):
            #dataset = self.load_dataset()
            dataset=df
            output_data = dataset.copy()
            #output_data = dataset.select(*dataset.columns)


            for column, column_type in self.column_types.items():
                if column_type == 'numeric':
                    contamination_factor = self.columns_and_contamination.get(column, 0.1)
                    selected_data = self.select_columns(dataset, [column])
                    null_handling_method = self.columns_and_null_handling.get(column, 'mean')

                    if null_handling_method == 'mean':
                        selected_data = self.replace_null_with_mean(selected_data)
                    elif null_handling_method == 'zero':
                        selected_data = self.replace_null_with_zero(selected_data)
                    else:
                        print(f"Invalid null handling method for column '{column}'. Using 'mean' as default.")
                        selected_data = self.replace_null_with_mean(selected_data)

                    scaled_data = self.apply_scaling(selected_data)
                    data_with_if_anomaly = self.apply_isolation_forest(scaled_data, contamination_factor)
                    dbscan_params = self.columns_and_dbscan_params.get(column, {'eps': 0.5, 'min_samples': 5})
                    data_with_dbscan = self.apply_dbscan(scaled_data, eps=dbscan_params['eps'], min_samples=dbscan_params['min_samples'])

                    output_data[f'{column}_IFanomaly'] = data_with_if_anomaly['IFanomaly']
                    output_data[f'{column}_DBSCAN_Labels'] = data_with_dbscan['DBSCAN_Labels']

                elif column_type == 'non-numeric':
                    print(f"Processing non-numeric column '{column}'")
                    selected_data = self.select_columns(output_data, [column])
                    selected_data = self.preprocess_data(selected_data, column)
                    dbscan_params = self.columns_and_dbscan_params.get(column, {'eps': 0.5, 'min_samples': 5})
                    data_with_dbscan = self.apply_dbscan(selected_data, eps=dbscan_params['eps'], min_samples=dbscan_params['min_samples'])
                    output_data[f'{column}_DBSCAN_Labels'] = data_with_dbscan['DBSCAN_Labels']

            return output_data
        

