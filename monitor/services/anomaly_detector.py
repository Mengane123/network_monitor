#It is an anomaly detection system for network traffic using Isolation Forest (a machine learning model for anomaly detection)

from sklearn.ensemble import IsolationForest 
from ..models import NetworkConnection , SecurityAlert 
import pandas as pd #used to process network traffic data in tabular form 
import numpy as np #used for data processing 


#AnomalyDetector class , trains the Isolation Forest model based on past network connection data 
                        # based on the trained model , it will detects anomalies in incomming network traffic 
                        # creates security alerts for suspicious connection and stores it into the SecurityAlert model 
# this class will provide 4 methods 
# prepare_data 
# train_model 
# detect_anomalies 
# prepare_data_for_prediction 

class AnomalyDetector:

    def __init__(self):
        self.model = IsolationForest(contamination=0.1 , random_state=42) 
        #here we are initializing the model , 0.1 means , it will assume 10% data contains anomalies 
        #random_state=42 ensures consistent results accross run , because when we split the data , we want consistence in the result of the dataset every time 

    def prepare_data(self):
        # prepare_data only returns only features [] as a dataframe
        #getting recent connection 
        connections = NetworkConnection.objects.all().order_by('-timestamp')[:10000]

        #convert to dataframe (table format)
        df = pd.DataFrame.from_records(connections.values())

        #feature engineering (means only extracting the relevant features for anomaly detection)
        features =[
            'bytes_tranferred', #amount of data sent in a connection 
            'source_port', #port used by the sender
            'destination_port' #port receiving the data(load)
        ]

        return df[features]
    

    def train_model(self):
        data = self.prepare_data() #calling prepare_data() to get the training dataset 
        self.model.fit(data) #trains isolationForest model on this dataset 



    
    def detect_anomalies(self , new_connections):

        #converting new_connections in feature format 
        features = self.prepare_data_for_prediction(new_connections)

        #predicting anomalies 
        prediction = self.model.predict(features)

        #creating alerts for anomalies 
        for i,pred in enumerate(prediction):
            if pred == -1: #means anomaly detected
                SecurityAlert.objects.create(
                    title="Anomalous Network Activity Detected",
                    description=f"Unusual traffic pattern detected for connection {new_connections[i]}",
                    severity="MEDIUM",
                    source_ip = new_connections[i].source_ip
                )





    def prepare_data_for_prediction(self , connections):
        features =[]
        for conn in connections:
            features.append([
                conn.bytes_tranferred,
                conn.source_port,
                conn.destination_port,
            ])
        return np.array(features)
        


