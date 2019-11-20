import pandas as pd
import requests, json
import matplotlib.pyploy
from io import StringIO
from pprint import pprint

def get_spending_by_org_dict(org, code):
    """
    Specify a organisation code e.g 14L for Manchester CCG and a BNF code
    e.g 5.1 for Antibacterials
    """
    request_url = "https://openprescribing.net/api/1.0/spending_by_ccg/"
    params = {
        "org": org,
        "code": code,
        "format": "json",
    }
    op_request = requests.get(request_url, params=params)
    op_request_dict = json.loads(op_request.text) 
    pprint(op_request_dict)
    return op_request_dict

def get_list_size_dict(org):
    request_url = "https://openprescribing.net/api/1.0/org_details/"
    params
def op_request_to_dataframe(dictionary):

    df = pd.DataFrame.from_dict(dictionary)
    return df

def plot_ccg_trends(df):
    plot = df.plot(x = 'date', y = 'items')
    return plot


op_dict = get_spending_by_org_dict('14L', '5.1')
op_df = op_request_to_dataframe(op_dict)
plot = plot_ccg_trends(op_df)
plot.figure.show()