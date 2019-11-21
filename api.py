import pandas as pd
import requests, json
import matplotlib.pyplot

def get_no_of_items_by_org(org, code):
    """
    Specify a organisation code e.g 14L for Manchester CCG and a BNF code
    e.g 5.1 for Antibacterials. Will request the data in JSON format and return
    the data converted to a dictionary. Will return the total spend and total
    items prescribed for given months. 
    """
    request_url = "https://openprescribing.net/api/1.0/spending_by_ccg/"
    params = {
        "org": org,
        "code": code,
        "format": "json"
    }
    op_request = requests.get(request_url, params=params)
    op_request_dict = json.loads(op_request.text) 
    return op_request_dict

def practice_no_of_items(org, code):
    request_url = "https://openprescribing.net/api/1.0/spending_by_practice/"
    params = {
        "org": org,
        "code": code,
        "format": "json"
    }
    op_request = requests.get(request_url, params=params)
    op_request_dict = json.loads(op_request.text) 
    return op_request_dict

def get_list_size(org):
    request_url = "https://openprescribing.net/api/1.0/org_details/"
    # GET /api/1.0/org_details/?org_type=practice&org=99H&keys=total_list_size
    params = {
        "org_type": "practice",
        "org": org,
        "keys": "total_list_size",
        "format": "json"
    }
    op_request = requests.get(request_url, params=params)
    op_request_dict = json.loads(op_request.text)
    return op_request_dict

def get_merged_dataframe(org, code):
    n_items_df = op_request_to_dataframe(practice_no_of_items(org, code))
    list_size_df = op_request_to_dataframe(get_list_size(org))
    result = pd.merge(n_items_df, list_size_df)
    return result


def op_request_to_dataframe(dictionary):
    df = pd.DataFrame.from_dict(dictionary)
    return df

def plot_ccg_trends(df):
    plot = df.plot(x = 'date', y = 'items')
    return plot