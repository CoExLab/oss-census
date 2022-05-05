
import math
import os, webbrowser
import numpy as np
import pandas as pd
import json



import math
import os, webbrowser
import numpy as np
import pandas as pd
import json

def load_contributor(lang, dat_path, store_path):
    """
    Stores formatted JavaScript variables for graph from:
    All active contributor by gender by window: './contributor/all/'
    Core active contributor by gender by window: './contributor/core/'

    :string lang: programming language
    :string dat_path: CSV pandas data
    :string store_path: path to Contributor graph settings
    :return: None
    """ 
    dat = pd.read_csv(dat_path, error_bad_lines=False, warn_bad_lines=False, index_col=False)
    max_win = 45
    dat = dat[dat['win']<=max_win]

    # Format column data of contributors by gender
    all_female = {}
    all_female["name"] = "All women"
    all_female["type"] = "column"
    all_female["data"] = list(dat["female_all"] / 1000)
    all_female["color"] = "#de2d26"

    all_male = {}
    all_male["name"] = "All Men"
    all_male["type"] = "column"
    all_male["data"] = list((dat["female_all"] + dat["male_all"]) / 1000)
    all_male["color"] = "#f29d4b"

    all_unknown = {}
    all_unknown["name"] = "All Unknown"
    all_unknown["type"] = "column"
    all_unknown["data"] = list(dat["all_all"] / 1000)
    all_unknown["color"] = "blanchedalmond"

    # Plot ratio line for female in all contributor
    male = dat["male_all"].replace(0, 1)
    ratio_all = dat["female_all"] / (dat["female_all"] + male)
    for win in dat["win"]:
        win = win - 1
        if dat["female_all"][win] + male[win] <= 5:
            ratio_all[win] = 0

    # Plot ratio line for female in core contributor
    male = dat["male_core"].replace(0, 1)
    ratio_core = dat["female_core"] / (dat["female_core"] + male)
    for win in dat["win"]:
        win = win - 1
        if dat["female_core"][win] + male[win] <= 10:
            ratio_core[win] = 0

    # Format line data of contributors
    among_all = {}
    among_all["name"] = "Among all"
    among_all["type"] = "spline"
    among_all["data"] = list(ratio_all)
    among_all["color"] = "darkblue"
    among_all["yAxis"] = 1
    
    among_core = {}
    among_core["name"] = "Among core"
    among_core["type"] = "spline"
    among_core["data"] = list(ratio_core)
    among_core["color"] = "darkblue"
    among_core["yAxis"] = 1
    among_core["marker"] = { 
        "fillColor": '#FFFFFF',
        "radius": 5,
        "lineWidth": 2,
        "lineColor": 'darkblue'
    }    


    # Change window to date
    wins = dat["win"]
    x = []
    for win in wins:
        time = 3 * win
        year = 2008 + math.floor(time/12)
        month = time - math.floor(time/12)*12
        if not month:
            month = 12
        x.append("{}-{}".format(year,month))
    wins = x

    # Graph setup information
    lang_title = lang
    title = "Active Contributors in "  + lang_title + " Public Projects"
    label_x = 'Time (quarter)'
    label_y = 'Number of Contributors (thousand)'
    label_y_secondary = "Women Ratio = F/(F + M)"
    x_categories = wins
    height_ratio = (9 / 13 * 100) # 16:9 ratio
    data = [all_unknown, all_male, all_female, among_all, among_core]
   
    # write data to js file that creates variables referenced in script.js file
    out_dict = dict()
    out_dict['title'] = title
    out_dict['label_x'] = label_x 
    out_dict['label_y'] = label_y
    out_dict['label_y_secondary'] = label_y_secondary
    out_dict['x_categories'] = x_categories
    out_dict['height_ratio'] = height_ratio
    out_dict['data'] = data
    with open(store_path + '/' + lang + '.json', 'w') as out_file:
        json.dump(out_dict, out_file)

    

def load_commit(lang, dat_path, store_path):
    """
    Stores formatted JavaScript variables for graph from:
    Commit count by gender by window: './commit/graph'

    :string lang: programming language
    :string dat_path: CSV data path
    :string store_path: path to Contributor graph settings
    :return: None
    """ 
    dat = pd.read_csv(dat_path, error_bad_lines=False, warn_bad_lines=False, index_col=False)
    max_win = 45
    dat = dat[dat['win']<=max_win]
    
    # Format column data of contributors by gender
    all_female = {}
    all_female["name"] = "All Women"
    all_female["type"] = "column"
    all_female["data"] = list(dat["female_commit"] / 1000)
    all_female["color"] = "#de2d26"

    all_male = {}
    all_male["name"] = "All Men"
    all_male["type"] = "column"
    all_male["data"] = list((dat["female_commit"] + dat["male_commit"]) / 1000)
    all_male["color"] = "#f29d4b"

    all_unknown = {}
    all_unknown["name"] = "All Unknown"
    all_unknown["type"] = "column"
    all_unknown["data"] = list(dat["all_commit"] / 1000)
    all_unknown["color"] = "blanchedalmond"

    # Plot ratio line for female in all commits
    male = dat["male_commit"].replace(0, 1)
    ratio = dat["female_commit"] / (dat["female_commit"] + male)
    for win in dat["win"]:
        win = win - 1
        if dat["female_commit"][win] + male[win] <= 1000:
           ratio[win] = 0
           
    # Format line data of contributors
    ratio_female = {}
    ratio_female["name"] = "Among core"
    ratio_female["type"] = "spline"
    ratio_female["data"] = list(ratio)
    ratio_female["color"] = "darkblue"
    ratio_female["yAxis"] = 1
    ratio_female["marker"] = { 
        "fillColor": '#FFFFFF',
        "radius": 5,
        "lineWidth": 2,
        "lineColor": 'darkblue'
    }    

    # Change window to date
    wins = dat["win"]
    x = []
    for win in wins:
        time = 3 * win
        year = 2008 + math.floor(time/12)
        month = time - math.floor(time/12)*12
        if not month:
            month = 12
        x.append("{}-{}".format(year,month))
    wins = x

    # Graph setup information
    lang_title = lang

    title = "Commits in "+ lang_title +" Public Projects" 
    label_x = 'Time (quarter)'
    label_y = 'Commit Numbers (thousand)'
    label_y_secondary = "Women Commit Ratio = F/(F + M)"
    x_categories = wins
    height_ratio = (9 / 13 * 100) # 16:9 ratio
    data = [all_unknown, all_male, all_female, ratio_female]
    
    # write data to js file that creates variables referenced in script.js file
    out_dict = dict()
    out_dict['title'] = title
    out_dict['label_x'] = label_x 
    out_dict['label_y'] = label_y
    out_dict['label_y_secondary'] = label_y_secondary
    out_dict['x_categories'] = x_categories
    out_dict['height_ratio'] = height_ratio
    out_dict['data'] = data
    with open(store_path + '/' + lang + '.json', 'w') as out_file:
        json.dump(out_dict, out_file)



def load_project(lang, dat_path, store_path):
    """
    Stores formatted JavaScript variables for graph from:
    All active project count by window: './project/'

    :string lang: programming language
    :string dat_path: CSV data path
    :string store_path: path to Contributor graph settings
    :return: None
    """ 
    dat = pd.read_csv(dat_path, error_bad_lines=False, warn_bad_lines=False, index_col=False)
    max_win = 45
    dat = dat[dat['win']<=max_win]

    # Format column data of contributors by gender
    all = {}
    all["name"] = "All"
    all["type"] = "column"
    all["data"] = list(dat[lang+"_all"] / 1000)
    all["color"] = "#f29d4b"

    has_female = {}
    has_female["name"] = "Has Women"
    has_female["type"] = "column"
    has_female["data"] = list(dat[lang+"_fem"] / 1000)
    has_female["color"] = "#de2d26"

    
    # Plot ratio line for female in all commits
    ratio = dat[lang+"_fem"] / dat[lang+"_all"]
    for win in dat["win"]:
        win = win - 1
        if dat[lang+"_all"][win] <= 5:
            ratio[win] = 0

    # Format line data of contributors
    ratio_female = {}
    ratio_female["name"] = "Women Ratio"
    ratio_female["type"] = "spline"
    ratio_female["data"] = list(ratio)
    ratio_female["color"] = "darkblue"
    ratio_female["yAxis"] = 1
    ratio_female["marker"] = { 
        "fillColor": '#FFFFFF',
        "radius": 5,
        "lineWidth": 2,
        "lineColor": 'darkblue'
    } 


    # Change window to date
    wins = dat["win"]
    x = []
    for win in wins:
        x.append(_format_date(win))
    wins = x

    # Graph setup information
    lang_title = lang

    title = "Active Public Projects in "+ lang_title +" Ecosystem" 
    label_x = 'Time (quarter)'
    label_y = 'Active Public Project Numbers (thousand)'
    label_y_secondary = "Women Participated Project Ratio"
    x_categories = wins
    height_ratio = (9 / 13 * 100) # 16:9 ratio
    data = [all, has_female, ratio_female]
    
    # write data to js file that creates variables referenced in script.js file
    out_dict = dict()
    out_dict['title'] = title
    out_dict['label_x'] = label_x 
    out_dict['label_y'] = label_y
    out_dict['label_y_secondary'] = label_y_secondary
    out_dict['x_categories'] = x_categories
    out_dict['height_ratio'] = height_ratio
    out_dict['data'] = data
    with open(store_path + '/' + lang + '.json', 'w') as out_file:
        json.dump(out_dict, out_file)



## Single Graph functions ##

def load_contributor_bar(dat_path, store_path, compare_opt):
    """
    Stores formatted JavaScript variables for graph from:
    All active project count by window: './project/'

    :string lang: programming language
    :string dat_path: CSV data path
    :string store_path: path to Contributor graph settings
    :string compare_opt: "male" or "all" gender(s) that is compared against data for females
    :return: None
    """ 

    langs = ['Python', 'C#', 'JavaScript', 'Java', 'Go', 'Ruby', 'C++',
            'TypeScript', 'PHP', 'C', 'HTML', 'CSS', 'Jupyter', 'Shell', 'Objective-C', 'All']
    
 
    data = []
    colors = ["#f29d4b", "#de2d26"]
    for compare in ['female', compare_opt]:
        add_data = dict()
        # Change male or female to men or women
        if compare == 'male':
            add_data["name"] = 'Men'
        elif compare == 'female':
            add_data["name"] = 'Women'
        else:
            add_data["name"] = 'All'
        add_data["type"] = "column" 
        add_data["color"] = colors.pop()
        add_data["data"] = []

        # Combine all year data
        for lang in langs:
            dat = pd.read_csv(dat_path+lang+'.csv', error_bad_lines=False, 
                            warn_bad_lines=False, index_col=False)
            max_win = 45
            dat = dat[dat['win']<=max_win]
            total = sum(list(dat[compare+"_all"]))
            add_data["data"].append(total)

        data.append(add_data)
        
    # Retrieve time range
    start_date = _format_date(dat["win"].iloc[0])
    end_date = _format_date(dat["win"].iloc[-1])
    date_range = start_date + " to " + end_date

    # Graph setup information

    title = "Active Contributors All Languages "+date_range
    label_x = 'Languages'
    label_y = 'Total Number of Contributors'
    height_ratio = (7 / 13 * 100) # 16:9 ratio
    
    # write data to js file that creates variables referenced in script.js file
    out_dict = dict()
    out_dict['title'] = title
    out_dict['label_x'] = label_x 
    out_dict['label_y'] = label_y
    out_dict['x_categories'] = langs
    out_dict['height_ratio'] = height_ratio
    out_dict['data'] = data
    with open(store_path+'/'+'all_bar'+'.json', 'w') as out_file:
        json.dump(out_dict, out_file)



def load_contributor_pie(lang, dat_path, store_path, compare_opt, year_opt):
    """
    :string lang: programming language
    :string dat_path: CSV pandas data
    :string store_path: path to Contributor graph settings
    :string compare_opt: "male" or "all" gender(s) that is compared against data for females
    :string year_opt: "single" or "all" years considered. Taking in a value of single will
                         automatically select most recent year
    :return: None
    """ 
    lang = lang.lower()
    dat = pd.read_csv(dat_path, error_bad_lines=False, warn_bad_lines=False, index_col=False)
    max_win = 45
    dat = dat[dat['win']<=max_win]

    if year_opt == "single":
        # Single year
        female_total = list(dat["female_all"])[-1]
        male_total = list(dat["male_all"])[-1]
        all_total = list(dat["all_all"])[-1]
    else: 
        # Combine all year data
        female_total = sum(list(dat["female_all"]))
        male_total = sum(list(dat["male_all"]))
        all_total = sum(list(dat["all_all"]))

    # Set num_comparison to value of data for "all" if compared against female data
    if compare_opt == "all":
        num_comparison = all_total
    else:
        num_comparison = male_total
    num_contributors = female_total + num_comparison

    # Format column data of contributors by gender
    female_data = {}
    female_data["name"] = "Female"
    # Take most recent year of contributors at index -1
    female_data["y"] = 100 * (female_total / num_contributors)
    
    compare_data = {}
    compare_data["name"] = compare_opt.capitalize()
    # Take most recent year of contributors at index -1
    compare_data["y"] = 100 * (num_comparison / num_contributors)
    
    out_dict = {"data": [] }
    out_dict["data"].append(female_data)
    out_dict["data"].append(compare_data)
    

    # Set Title
    if compare_opt.lower() == "male":
        # Change male to men in title
        comparison_title = "Men"
    else:
        comparison_title = "All"
    out_dict["title"] = "Women vs. " + comparison_title + " for " + lang.capitalize()

    if year_opt == "single":
        # Select most recent year
        year = dat["win"].iloc[-1]
        out_dict["subtitle"] = _format_date(year)
    else:
        # Select All Years in range
        start_date = _format_date(dat["win"].iloc[0])
        end_date = _format_date(dat["win"].iloc[-1])
        out_dict["subtitle"] = start_date + " to " + end_date

    with open(store_path + '/' + lang + '.json', 'w') as out_file:
        json.dump(out_dict, out_file)


def _format_date(year):
    # Format year and month of dataframe value "{}-{}".format(year,month)

    time = 3 * year
    year = 2008 + math.floor(time/12)
    month = time - math.floor(time/12)*12
    if not month:
        month = 12

    return "{}-{}".format(year,month)