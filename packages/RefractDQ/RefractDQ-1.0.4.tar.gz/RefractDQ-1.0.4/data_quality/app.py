## Importing libraries
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
import os,json
from utility.connector import connector_factory

#update alert info
def update_alert_info(alert_data):
    model_name = None; model_id = None; version_no = None ; version_no = None ; version_id = None
    plugin_id = None ; workflow_id = None
    temp = alert_data["alert_data"]

    try:
        model_config = json.loads(os.getenv("model_configuration"))
        refract_source = model_config[0]["refract_source"]
        if refract_source == "model":
            model_name = [item["field_value"] for item in model_config if item['field_id']=="model_name"][0]
            model_id = [item["field_value"] for item in model_config if item['field_id']=="model_id"][0]
            version_no = [item["field_value"] for item in model_config if item['field_id']=="version_no"][0]
            version_id = [item["field_value"] for item in model_config if item['field_id']=="version_id"][0]
            temp_data = {
                    "description": {
                            "version": str(version_no)
                        },
                    "name": str(model_name),
                    "id": '_'.join([model_id,version_id]),
                    "type" : "MODEL"
                }
        elif refract_source == "workflow":
            workflow_id = [item["field_value"] for item in model_config if item['field_id']=="workflow_id"][0]
            plugin_id = [item["field_value"] for item in model_config if item['field_id']=="plugin_id"][0]
            temp_data = {
                    "description": {
                            "version": str(plugin_id)
                        },
                    "name": temp['recipe'],
                    "id": '_'.join([workflow_id,plugin_id]),
                    "type" : "WORKFLOW"
                }
    except Exception as msg:
        raise Exception("Unable to load model_configurations - error :",msg)



    temp.update({"object_metadata":temp_data})

    alert_data["alert_data"] =  temp

    print("Alert Info : \n",alert_data)
    
    return alert_data

# get outliers count for datetime type dataframe
def get_outliers_datetime_df(datetime_df):
    total_outliers = 0
    outlier_columns = []
    for col in datetime_df.columns:
        Q1 = datetime_df[col].quantile(0.25)
        Q3 = datetime_df[col].quantile(0.75)
        IQR = (Q3 - Q1).total_seconds()

        # calculate the upper and lower bounds for outliers using the IQR method
        lower_bound = Q1 - pd.Timedelta(1.5 * IQR, unit='s')
        upper_bound = Q3 + pd.Timedelta(1.5 * IQR, unit='s')

        # identify outliers in the 'date' column based on the bounds
        outliers = datetime_df.loc[(df[col] < lower_bound) | (datetime_df[col] > upper_bound)]
        if len(outliers) > 0:
            outlier_columns.append(col)
        total_outliers += len(outliers)
        
    return total_outliers , datetime_df.size , outlier_columns
    
# get outliers count for dataframe other than datetime dtype
def get_outliers_others_df(other_df):
    # Calculate outlier percentage using the Z-score method
    z_scores = np.abs((other_df - other_df.mean()) / other_df.std())
    outlier_columns = z_scores.columns[(z_scores > 3).any()].to_list()
    outlier_fraction = (z_scores > 3).sum().sum()
    
    return outlier_fraction,other_df.size,outlier_columns

def validate_inputs(temp):
    for item in temp:
        if not all([any([
                        isinstance(item[0],int),
                        isinstance(item[0],float),
                        ]),
                    any([
                        isinstance(item[1],int),
                        isinstance(item[1],float),
                        ])
                    ]
                    ):
            raise Exception("Alert thresholds should of type int or float")
        
        if not all([0 <= item[0] <= 1,0 <= item[1] <= 1]):
            raise Exception("threshold input range should be between 0 and 1")
        
def check_metric_status(alert_info,metric_value,parameter):
    metric_status = None 
    serverity_maps = []; alert_list = []; alert_map = []

    for item in alert_info:
        if item['severity'] == "Red" and item['parameter'] == parameter:
            serverity_maps.append([float(item["max_value"]),float(item["min_value"]),"Poor"])
        if item['severity'] == "Amber" and item['parameter'] == parameter:
            serverity_maps.append([float(item["max_value"]),float(item["min_value"]),"Moderate"])
        if item['severity'] == "Green" and item['parameter'] == parameter:
            serverity_maps.append([float(item["max_value"]),float(item["min_value"]),"Good"])
    
    validate_inputs(serverity_maps)
    
    for map_obj in serverity_maps:
        if map_obj[1] <= metric_value <= map_obj[0] :
                print(f"Threshold range for {parameter}: {map_obj}, Status: {map_obj[2]}")
                return map_obj[2]
        else:
            alert_list.append(float(map_obj[0]))
            alert_list.append(float(map_obj[1]))
            alert_map.append((float(map_obj[1]),float(map_obj[0])))

    
    for item in alert_info:
        if item['parameter'] == parameter:
            metric_status = "Good" if metric_value > max(alert_list)  else "Poor" if metric_value < min(alert_list) else "Moderate"
    
    print(f"Thresholds provided for {parameter}: {alert_map}, Status : {metric_status}")
    return metric_status

def final_recipe_status(alert_list):
    temp_info = set([st for st in alert_list if st])
    if len(temp_info)==1 and "Good" in temp_info:
        return "Good"
    elif len(temp_info) >= 1 and "Poor" in temp_info:
        return "Poor"
    else:
        return "Moderate"


def get_alert_configurations(recipe_name):
    alert_configuration = []
    alert_info = json.loads(os.getenv("alert_configuration").replace("'", '"'))
    for metric_info in alert_info:

        parameter_name = [item["field_value"] for item in metric_info if item["field_id"]=="parameter"][0]
        max_value = [item["field_value"] for item in metric_info if item["field_id"]=="max_threshold"][0]
        min_value = [item["field_value"] for item in metric_info if item["field_id"]=="min_threshold"][0]
        severity = [item["field_value"] for item in metric_info if item["field_id"]=="severity"][0]
        temp_dict = {
                "parameter": parameter_name,
                "max_value": max_value,
                "min_value": min_value,
                "severity": severity
            }
        alert_configuration.append(temp_dict)

    return alert_configuration

def get_pandas_profile(df=None):
    profile = ProfileReport(df, title="Data Profiling",explorative=True,html={
            'style':{
                'padding': '400px',
                'theme' : 'flatly',
                'full_width' : True
            }
    })
    return profile

def get_plugin_name():
    try:
        plugin_info = json.loads(os.getenv("plugin"))
        plugin_name = [item["field_value"] for item in plugin_info  if item['field_id']=="plugin_type"][0]
    except Exception as msg:
        print("Unable to load plugin name - error :",msg)
        raise Exception("Failed to load plugin env")
    
    return plugin_name

def edit_html(file_path):
    from bs4 import BeautifulSoup
    html_content = None
    try:
        file = open(file_path,'r')
        html_content = file.read()
        file.close()
    except Exception as msg:
        print(msg)
    
    soup = BeautifulSoup(html_content,"html.parser")

    # print(soup.prettify())
    select_elements = soup.find_all("select",attrs={'id':'variables-dropdown'})
    for select_element in select_elements:
        select_element.extract()
    soup.find('h1').extract()
    
    try:
        file = open(file_path,'w',encoding="utf-8")
        file.write(str(soup))
        file.close()
    except Exception as msg:
        print(msg)

    return None

def update_metrics_json(metric_info,plugin_name):
    try:
        fh = open(os.getenv("output_path")+ "/metrics.json","w")
        metrics_info = {
            plugin_name : metric_info
        }
        json.dump(metrics_info,fh)
        fh.close()
    except Exception as msg:
        print("Unable to create alert_data.json")

if __name__ == "__main__":
    # Get DataFrame
    # from test import set_env_configs
    # set_env_configs()
    if not "data_source" in os.environ:
        raise Exception("data_source env is not found.")
    data_source = os.getenv("data_source")

    connection = connector_factory.ConnectorFactory.getConnector(data_source)

    df = connection.load_data()

    # Create profile
    profile = get_pandas_profile(df)
        
    alert_messages = ""
    data_quality_status = None

    #Completeness
    null_fraction = df.isnull().sum().sum()/df.size
    completeness = 1 - null_fraction

    ## Finding percentage of duplicates and outliers
    # Calculate duplicate row percentage
    duplicate_fraction = df.duplicated().sum() / len(df)


    ## Checking whether dataset has valid numeric data
    # select columns with numeric data types
    numeric_cols = df.select_dtypes(include=['int', 'float','object']).columns.tolist()
    # check if all values in the numeric columns are numeric
    is_numeric = df[numeric_cols].apply(lambda x: pd.to_numeric(x, errors='coerce').notnull().all())
    # get the column names that have non-numeric values
    non_numeric_cols = is_numeric[is_numeric == False].index.tolist()
    no_numeric_alert_msg = "non numeric data found in columns "+",".join(non_numeric_cols) if non_numeric_cols else "" 
    # alert_messages+=no_numeric_alert_msg

    #Select dataframe for outliers
    df_outliers = df.drop(non_numeric_cols, axis=1) 

    # select columns where data type is datetime64[ns]
    datetime_df = df_outliers.select_dtypes(include=['datetime64[ns]'])
    outliers_dtime,size_dtime,columns_date = get_outliers_datetime_df(datetime_df)

    # select columns where data type is not datetime64[ns]
    other_df =  df_outliers.select_dtypes(exclude=['datetime64[ns]'])
    outliers_others,size_others,columns_others = get_outliers_others_df(other_df)

    outlier_fraction = (outliers_dtime+outliers_others)/(size_dtime+size_others)
    outlier_columns = columns_date + columns_others

    consistency = 1 - (duplicate_fraction+outlier_fraction)
    alert_messages += f"Dataset has {round(null_fraction*100,2)}% of null values, {round(duplicate_fraction*100,2)}% of duplicate rows and Outliers of {round(outlier_fraction*100,2)}% found in columns {','.join(outlier_columns)}. "
    alert_messages+=no_numeric_alert_msg

    recipe_name = get_plugin_name()

    alerts  = None ; alert_data = None
    try:
        #Alert Configs
        alert_data = get_alert_configurations('data_quality')
        alerts = True
    except Exception as msg:
        alerts = False
        print("Alerts configs not found")
    
    metric_info = {
        "COMPLETENESS" : completeness,
        "CONSISTENCY" : consistency,
    }
    
    update_metrics_json(metric_info,recipe_name)
    
    if alert_data:
        # Seviority Check
        status_completeness = check_metric_status(alert_data,completeness,"Completeness")
        status_consistency = check_metric_status(alert_data,consistency,"Consistency")

        data_quality_status  = final_recipe_status([status_completeness,status_consistency])

        #Alert Data 
        alert_data = {
            "alert_data": {
                "recipe" : recipe_name,
                "metrics" :{
                    "completeness" : round(completeness,4),
                    "consistency" : round(consistency,4)
                },
                "status" : data_quality_status,
                "message" : alert_messages,
                "ui_value" : data_quality_status
            },
            "ai-backend-metadata" : {
                "data_quality_flag": data_quality_status
            }
        }

        alert_data = update_alert_info(alert_data)


        # if not data_quality_status == "Good":
        try:
            fh = open(os.getenv("output_path")+ "/alert_data.json","w")
            json.dump(alert_data,fh)
            fh.close()
        except Exception as msg:
            print("Unable to create alert_data.json")

    #Saving Data
    output_dir = os.getenv("output_path",default="/output")
    profile.to_file(f"{output_dir}/{recipe_name}.html")
    edit_html(f"{output_dir}/{recipe_name}.html")
    profile_data = json.loads(profile.to_json())
    
    try:
        fh = open(os.getenv("output_path")+f"/{recipe_name}.json","w")
        profile_data = json.dump(profile_data,fh)
        fh.close()
    except Exception as msg:
        print("Unable to create recipe.json")
    



