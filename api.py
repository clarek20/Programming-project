import pandas as pd
import requests, json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

def get_no_of_items_by_org(org, code):
    """
    Specify a organisation code e.g 14L for Manchester CCG and a BNF code
    e.g 5.1 for Antibacterials. Will request the data in JSON format and return
    the data converted to a dictionary. Will return the total spend and total
    items prescribed for given months. 

    Returns a dictionary of values
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

def get_practice_info(query):
    request_url = "https://openprescribing.net/api/1.0/org_code/"
    # GET /api/1.0/org_details/?org_type=practice&org=99H&keys=total_list_size
    params = {
        "org_type": "practice",
        "q": query,
        "format": "json"
    }
    op_request = requests.get(request_url, params=params)
    op_request_dict = json.loads(op_request.text)
    if len(op_request_dict) > 1:
        print(f"The query returned more than 1 practice, automatically choosing the first practice which is {op_request_dict[0]['name']}")
        op_request_dict = op_request_dict[0]
    elif len(op_request_dict) == 0:
        raise Exception(f"Query {query} returned no results, perhaps the query was missspelled.")
    else:
        # if query only returns one result, return that result
        op_request_dict = op_request_dict[0]

    return op_request_dict

def get_ccg_info(query):
    request_url = "https://openprescribing.net/api/1.0/org_code/"
    # GET /api/1.0/org_details/?org_type=practice&org=99H&keys=total_list_size
    params = {
        "org_type": "ccg",
        "q": query,
        "format": "json"
    }
    op_request = requests.get(request_url, params=params)
    op_request_dict = json.loads(op_request.text)
    if len(op_request_dict) > 1:
        print(f"The query returned more than 1 ccg, automatically choosing the first ccg which is {op_request_dict[0]['name']}")
        op_request_dict = op_request_dict[0]
    elif len(op_request_dict) == 0:
        raise Exception(f"Query {query} returned no results, perhaps the query was missspelled.")
    else:
        # if query only returns one result, return that result
        op_request_dict = op_request_dict[0]

    return op_request_dict

def get_bnf_info(query):
    request_url = "https://openprescribing.net/api/1.0/bnf_code/"
    # GET /api/1.0/org_details/?org_type=practice&org=99H&keys=total_list_size
    params = {
        "q": query,
        "format": "json"
    }
    op_request = requests.get(request_url, params=params)
    op_request_dict = json.loads(op_request.text)
    if len(op_request_dict) > 1:
        print(f"The query returned more than 1 bnf, automatically choosing the first bnf which is {op_request_dict[0]['name']}")
        op_request_dict = op_request_dict[0]
    elif len(op_request_dict) == 0:
        raise Exception(f"Query {query} returned no results, perhaps the query was missspelled.")
    else:
        # if query only returns one result, return that result
        op_request_dict = op_request_dict[0]

    return op_request_dict


def get_practice_prescriptions_by_time(practice, ccg='14L', bnf='5.1'):
    df = get_merged_dataframe(ccg, bnf)
    practice = get_practice_info(practice)['code']
    filtered_df = df[df.row_id == practice].reset_index()
    return filtered_df

def plot_practice_prescriptions_by_time(practice, ccg='14L', bnf='5.1'):
    df = get_practice_prescriptions_by_time(practice, ccg, bnf)
    # Add function later to get name of bnf paragraph or section
    title = f"Number of prescriptions by {practice} over time"
    plot = df.plot(x = 'date', y = 'items', title=title)
    plot.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))
    return plot

def month_practice_stats(practice, month, year, org = '14L'):
    df = get

def op_request_to_dataframe(dictionary):
    df = pd.DataFrame.from_dict(dictionary)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df

def plot_ccg_trends(df):
    plot = df.plot(x = 'date', y = 'items')
    return plot

def get_heatmap_df(org, code, year):
    # Get the dataframe 
    df = get_merged_dataframe(org, code)
    # Make a new column for the year from the date column
    df['year'] = [d.year for d in df['date']]
    # Make a new column for the month from the date column
    df['month'] = [d.month for d in df['date']]
    # Filter dataframe based on year
    df = df[df.year == year]
    # Make a new column normalising number of items prescribed for patient 
    # numbers
    df['items_per_patient'] = df['items'] / df['total_list_size']
    # Pivot the dataframe to get it in a heatmappable 
    df = df.pivot(index = "row_name", columns='month', values='items_per_patient')

    return df

def plot_heatmap(df, year):
    fig, ax = plt.subplots(figsize=(10,30))  
    plot = sns.heatmap(df, cmap="coolwarm", ax=ax, linewidths=.5)
    ax.set_title(f"Heatmap of prescriptions normalised to patient numbers from practices in the Manchester CCG in {year}")
    ax.set(ylabel = "Practice", xlabel = "Month")
    return plot
    



