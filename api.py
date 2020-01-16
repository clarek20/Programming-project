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
    # The URL to make the request to
    request_url = "https://openprescribing.net/api/1.0/spending_by_ccg/"
    # Paramaters to include in the request
    params = {
        "org": org,
        "code": code,
        "format": "json"
    }
    op_request = requests.get(request_url, params=params)
    op_request_dict = json.loads(op_request.text) 
    return op_request_dict

def practice_no_of_items(org, code):
    """
    Specify a organisation code e.g 14L for Manchester CCG and a BNF code
    e.g 5.1 for Antibacterials. Will request the data in JSON format and return
    the data converted to a dictionary. Will return the total spend and total
    items prescribed for given months within a pratcice. 

    Returns a dictionary of values
    """

    # The URL to make the request to
    request_url = "https://openprescribing.net/api/1.0/spending_by_practice/"

    # Parameters to include in the request
    params = {
        "org": org,
        "code": code,
        "format": "json"
    }
    op_request = requests.get(request_url, params=params)
    op_request_dict = json.loads(op_request.text) 
    return op_request_dict

def get_list_size(org):
    """Get's the number of patients (the list size) from a practice when given
    the practice code
    
    Arguments:
        org {string} -- The organisation code for a practice
    
    Returns:
        dict -- a dictionary of values pertaining to the list size of that practice
        on a given date
    """
    
    # Define the API endpoint URL
    request_url = "https://openprescribing.net/api/1.0/org_details/"

    # Specify the parameter dictionary
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
    """Function that will return a merged dataframe of the no of items and cost
    of a specific BNF code and the list size for a specific organisation.
    Useful for calculating per patient spend.
    
    Arguments:
        org {string} -- the organisation code
        code {string} -- the bnf code of the desired group
    
    Returns:
        pd.DataFrame -- a dataframe of columns of the practice names, n items 
        prescribed, and n of patients.
    """    

    # Get the number of items sold for a group
    n_items_df = op_request_to_dataframe(practice_no_of_items(org, code))
    # Get the number of patients for a group
    list_size_df = op_request_to_dataframe(get_list_size(org))
    # Merge the dataframe and return it
    result = pd.merge(n_items_df, list_size_df)
    result['items_per_patient'] = result['items'] / result['total_list_size']
    return result

def get_practice_info(query):
    """Function that will get practice code and other information given a query
    such as a practice name e.g "fallowfield medical centre"

    Arguments:
        query {string} -- a query to search the practice database with could be
         a partial name or a code
    
    Raises:
        Exception: If the result is empty throw an error
    
    Returns:
        dict -- Dictionary of practice information inlcuding code, name, postcode
        etc
    """    
    # Url to make a request to
    request_url = "https://openprescribing.net/api/1.0/org_code/"
    # Params to include in request
    params = {
        "org_type": "practice",
        "q": query,
        "format": "json"
    }

    op_request = requests.get(request_url, params=params)

    # Convert the request from a json object into a dictionary.
    op_request_dict = json.loads(op_request.text)


    # If the length of a result is greater than one, let the user know the first
    # result was selected
    if len(op_request_dict) > 1:
        print(f"The query returned more than 1 practice, automatically choosing\
 the first practice which is {op_request_dict[0]['name']}")
        op_request_dict = op_request_dict[0]
    # Likewise, if the result is empty, let the user known and thrown an error
    elif len(op_request_dict) == 0:
        raise Exception(f"Query {query} returned no results, perhaps the query \
was missspelled.")
    else:
        #  if query only returns one result, return that result
        op_request_dict = op_request_dict[0]

    return op_request_dict

def get_ccg_info(query):
    """When provided with a query e.g a code or place will search for the corresponding
    ccg information.
    
    Arguments:
        query {string} -- A query string, typically a place name e.g 'Sheffield'
        or a code 
    
    Raises:
        Exception: If the result is empty throw an error 
    
    Returns:
        dict -- A dict of the ccg name and code aong other details
    """    
    # Request url and associated parameters
    request_url = "https://openprescribing.net/api/1.0/org_code/"
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
    """Same as the other get_*_info functions, provide a query such as a 
    drug group e.g "Antibacterial" or a code such as "5.1"
    
    Arguments:
        query {string} -- bnf code or drug group
    
    Raises:
        Exception: If no results throw an error
    
    Returns:
        dict -- dictionary of BNF section including id code and name of section
    """    
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


def get_practice_prescriptions_by_time(practice, ccg='auto', bnf='5.1'):
    """A function that will get the practice prescriptions for a particular bnf 
    group over a period of time. 
    
    Arguments:
        practice {string} -- A string to search for a practice using 
    
    Keyword Arguments:
        ccg {str} -- A ccg code, defaults to auto so will automatically choose
        a CCG code based on the practice name (default: {'auto'})
        bnf {str} -- bnf section code e.g 5.1 fro Antibacterials
         (default: {'5.1'})
    
    Returns:
        pd.DataFrame -- a dataframe of prescription quantity of a speicifc bnf
        group over time
    """    
    practice = get_practice_info(practice)['code']
    if ccg == 'auto':
        ccg = get_practice_info(practice)['ccg']
    df = get_merged_dataframe(ccg, bnf)
    # Filter the dataframe by the practice name
    filtered_df = df[df.row_id == practice].reset_index()
    return filtered_df

def plot_practice_prescriptions_by_time(practice, ccg='14L', bnf='5.1'):
    """Plots a grap of practice prescriptions over time 
    
    Arguments:
        practice {string} -- [name of a practice]
    
    Keyword Arguments:
        ccg {str} -- [ccg code] (default: {'14L'})
        bnf {str} -- [bnf code] (default: {'5.1'})
    
    Returns:
        [plot] -- [a matplotlib object of prescriptions over time]
    """    
    df = get_practice_prescriptions_by_time(practice, ccg, bnf)
    # Add function later to get name of bnf paragraph or section
    practice_name = get_practice_info(practice)['name']
    title = f"Number of prescriptions by {practice_name} over time"
    plot = df.plot(x = 'date', y = 'items', title=title)
    plot.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))
    return plot

# unfinished
# def month_practice_stats(practice, month, year, org = '14L'):
#     df = get

def op_request_to_dataframe(dictionary):
    """converts a dictionary to a dataframe
    
    Arguments:
        dictionary {dict} -- A dictionary to be convered to a dataframe
    
    Returns:
        [pd.DataFrame] -- [a pandas Dataframe of the dictionary]
    """    
    df = pd.DataFrame.from_dict(dictionary)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df

def plot_ccg_trends(df):
    """Basically just plots a given dataframe of date against item
    
    Arguments:
        df {DataFrame} -- A dataframe containing columns date and items
    
    Returns:
        [plot] -- [a matplotlib plot]
    """    
    plot = df.plot(x = 'date', y = 'items')
    return plot

def get_heatmap_df(org, code, year):
    """Function to generate a heatmap compatible dataframe
    
    Arguments:
        org {string} -- an organisation CCG code
        code {string} -- a bnf code to search for
        year {int} -- a year to filter the dataframe with
    
    Returns:
        [type] -- [description]
    """    
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
    # Pivot the dataframe to get it in a heatmappable form
    df = df.pivot(index = "row_name", columns='month', values='items_per_patient')

    return df

def plot_heatmap(df, year):
    """Plot the dataframe retrieved using the get_merged_dataframe function

    Arguments:
        df {pandas.DataFrame} -- A pandas dataframe retrieved using get_merged_dataframe
        year {int} -- A year
    
    Returns:
        seaborn plot -- A seaborn heatmap plot
    """    
    fig, ax = plt.subplots(figsize=(10,30))  
    plot = sns.heatmap(df, cmap="coolwarm", ax=ax, linewidths=.5)
    ax.set_title(f"Heatmap of prescriptions normalised to patient numbers from \
practices in the Manchester CCG in {year}")
    ax.set(ylabel = "Practice", xlabel = "Month")
    return plot
    
