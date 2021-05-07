import os
import pandas as pd
import plotly.express as px
import pymongo as pm
import datetime

HOST = 'mongodb://localhost:27017/'
DATABASE = 'inter_test'
COLLECTION = 'bookings_per_hour'

def set_path():
    ROOT_DIR = os.path.abspath(os.curdir) 
    root_data_path = os.path.join(
	    ROOT_DIR,
        "odysseus",
        "city_data_manager/"
	    "data"
    )
    return root_data_path
    
def initialize_mongoDB(host=HOST,database=DATABASE,collection=COLLECTION):
    client = pm.MongoClient(host)
    db = client[database]
    col = db[collection]
    return db,col

def insert_documents_db(collection,dict_object):
    print(dict_object)
    id_object = collection.insert_one(dict_object)
    return id_object

class DataTransformer:
    def __init__(self,host=HOST,database=DATABASE,DEBUG =False):
        self.data_path = set_path()
        self.db = initialize_mongoDB(host,database)
        self.DEBUG=DEBUG

    def makeitjson(self,usually_a_df): # can also be a series
        result = usually_a_df.to_json(orient="index")
        return result

    def to_dictionary_timeseries(self,usually_a_df):
        final_dict = {}
        start_dict = usually_a_df.to_dict()
        for key in start_dict.keys():
            list_values=list(start_dict[key].values())
            final_dict[key] = list_values
        return final_dict
            
    def transform_cdm(self,city, data_steps_id, data_type_id, data_source, year, month, filetype, *args, **kwargs):
        transformed={}
        if kwargs.get('filter_type', None):
            filter_type = kwargs.get('filter_type', None)

        path_to__data_city_norm_trips_source_year_month_filetype = os.path.join(
            self.data_path, city, data_steps_id, data_type_id, data_source, year+"_"+month + filetype
        )
        if filetype==".csv":
            df = pd.read_csv(path_to__data_city_norm_trips_source_year_month_filetype)
        elif filetype==".pickle":
            with open(path_to__data_city_norm_trips_source_year_month_filetype,"rb") as f:
                df = pickle.load(f)
        # the csv file has been saved with the index, which i do not want
        df = df.drop(df.columns[0], axis=1)
        print(df)
        if filter_type == "most_used_cars":
            df_plates = df.filter(["plate"], axis=1)
            df_plates["occurance"] = 1
            most_used = df_plates.groupby(by="plate").sum(["occurance"]).sort_values(by=["occurance"], ascending=[True])
            most_used = most_used.reset_index()
            print(most_used.head())
            #transformed = self.makeitjson(most_used)
            transformed = self.to_dictionary_timeseries(most_used)

        elif filter_type == "busy_hours":
            df_busy = df.filter(["start_hour"], axis=1)
            df_busy["occurance"] = 1
            most_busy_hour = df_busy.groupby(by="start_hour").sum(["occurance"]).sort_values(by=["occurance"], ascending=[True])
            most_busy_hour = most_busy_hour.reset_index()

            #transformed = self.makeitjson(most_busy_hour)
            transformed = self.to_dictionary_timeseries(most_busy_hour)

        elif filter_type == "avg_duration":
            df_duration = df.filter(["start_hour","duration"], axis=1)
            avg_duration = df_duration.groupby(by="start_hour").mean(["duration"]).sort_values(by=["start_hour"], ascending=[True])
            avg_duration = avg_duration.reset_index()

        elif filter_type == "general_sum":
            generaldf = df.filter(["start_time"],axis=1)
            print (generaldf)
            generaldf['starting_date'] = generaldf['start_time'].apply(lambda x:  datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S%z'))
            self.sim_booking_requests = generaldf.fillna(0).set_index("starting_date").iloc[:, 0].resample("60Min").count()
            #if self.DEBUG:
            print(self.sim_booking_requests)
            transformed =  self.sim_booking_requests.to_json()
        #print(transformed)
        return transformed

    def save_to_db (self,city,data_source, year, month, data_type_id="trips",filetype=".csv",data_steps_id="norm",filter_list = ["general_sum","most_used_cars","busy_hours","avg_duration"]):
        print("start data transformer")
        db,col = initialize_mongoDB()
        dt = DataTransformer()
        data_collected = {}
        for f in filter_list:
            print(f)
            results = dt.transform_cdm(city, data_steps_id, data_type_id, data_source, str(year), str(month), filetype, filter_type=f)
            data_collected[f] = results

        insert_documents_db(col,data_collected)