import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def formatter(s, dict):
    i, j = 0, 0
    n = len(s)
    res = []
    while i < n and j < n:
        if s[j] != ';' and s[j] != '|':
            j = j+1
        else:
            substr = s[i:j]
            if s[j] == '|':
                j = j+2
                i = j
            else:
                j = j+1
                i = j
            res.append(substr.strip())
    res.append(s[i:j].strip())
    frmt_string = res
    not_spec = ['Not specified', 'Not Specified',
                'not Specified', 'not specified']
    count = 0
    for val in frmt_string:
        if ',' in val:
            temp = val.split(',')
            if len(temp) > 1 and temp[1].strip() in not_spec:
                if dict.get(temp[0].strip()) is None:
                    dict[temp[0].strip()] = 1
                    count = count+1

                else:
                    dict[temp[0].strip()] = dict.get(temp[0].strip()) + 1
            else:
                if dict.get(val.strip()) is None:
                    dict[val.strip()] = 1
                    count = count+1
                else:
                    dict[val.strip()] = dict.get(val.strip()) + 1
        else:
            if dict.get(val.strip()) is None:
                dict[val.strip()] = 1
                count = count+1
            else:
                dict[val.strip()] = dict.get(val.strip()) + 1
    return dict,frmt_string


# a list of unique flavors based on your analysis. What is the total number
# of unique flavors in your list?
def tot_no_of_uniq_flav(df):
    df = df['flavor'].to_list()
    dict = {}
    for i in range(0, len(df)):
        s = str(df[i])
        dict, _ = formatter(s, dict)
    print(len(dict))


# histogram of market subcategory against eventdate (years). Do any
# categories show negative trend over years?
def histogram(df):
    df['eventdate'] = pd.to_datetime(df['eventdate'], format='%m-%d-%Y')
    df['eventdate'] = pd. DatetimeIndex(df['eventdate']). year
    df = df.groupby([
        'market_subcategory', 'eventdate'])['id'].count().reset_index()
    df.rename(columns={'id': 'count'}, inplace=True)
    mar_sub = list(set(df['market_subcategory']))
    print(mar_sub)
    print(df)
    dict = {}
    for val in mar_sub:
        df_sub = df[df['market_subcategory'] == val].reset_index()
        index = list(df_sub['eventdate'])
        values = list(df_sub['count'])
        result = np.polyfit(index, list(values), deg=1)
        slope = result[-2]
        dict[val] = slope
    print(dict)
    marsub_neg_tend = []
    for key, val in dict.items():
        if val < 0:
            marsub_neg_tend.append(key)
            print(key+" ,market sub cat has negative trend with  years")
    for val in marsub_neg_tend:
        ax = plt.gca()
        x = df[df['market_subcategory'] == val].reset_index()  
        x.plot(kind='bar',
               x='eventdate',
               y='count',
               color='blue', ax=ax)
        plt.title("market sub category "+val)
        plt.show()


# market subcategory has highest unique flavors
def subcat_high_uniq_flav(df):
    df = df.groupby('market_subcategory')['flavor'].apply(list).reset_index()
    maxi = 0
    sub_cat = ""
    print(df)
    for i in range(0, len(df)):
        flavor_list = df['flavor'].loc[i]
        dict = {}
        count = 0
        for s in flavor_list:
            if type(s) == float:
                continue
            dict, _ = formatter(s, dict)
        count = len(dict)
        if count > maxi:
            maxi = count
            sub_cat = df['market_subcategory'].loc[i]
        print(count, df['market_subcategory'].loc[i])
    print(sub_cat, maxi)
    return


# on the number of product launches over different quarters for “fruit” flavor
# no of fruit flav launches
def no_of_prod_launch(df):
    df['eventdate'] = pd.to_datetime(df['eventdate'], format='%m-%d-%Y')
    df['fruit flavor'] = "No"
    fc = pd.read_csv('Flavor Classification Dataset.csv', encoding='latin-1')
    fc = fc[fc['Flavor_Group'] == 'Fruit'].reset_index()
    fruit_flav = []
    for i in range(0, len(fc)):
        fruit_flav.append(fc['flavor'].loc[i].strip())
    for i in range(0, len(df)):
        flav_list = df['flavor'].loc[i]
        flag = 0
        if type(flav_list) == float:
            continue
        _, frmt_flav_list = formatter(flav_list)
        for val in frmt_flav_list:
            for j in range(0, len(fruit_flav)):
                if val.strip().lower() == fruit_flav[j].strip().lower():
                    df['fruit flavor'].loc[i] = "Yes"
                    flag = 1
                    break
            if flag == 1:
                break
    df = df[df['fruit flavor'] == "Yes"].reset_index()
    df = df.groupby(df['eventdate'].dt.to_period('Q'))['id'].count().reset_index()
    print(df)


def data_for_client(df):
    # filtering country
    df = df[df['country'] == 'Canada']
    # filtering date
    regex = '2013.*'
    df = df[df.eventdate.str.contains(regex, na=False)]
    # filtering positioning
    regex = 'Ethical - Packaging.*'
    df = df[df.positioning.str.contains(regex, na=False)]
    # filering market subcategory
    regex = 'Energy Drinks.*'
    df = df[df.market_subcategory.str.contains(regex, na=False)]
    print(df)


# TOP 5 unique flavors across countries in 2013
def top_uniq_flav(df, year='2013'):
    regex = '2013.*'
    df = df[df.eventdate.str.contains(regex, na=False)].reset_index()
    df = df.groupby('country')['flavor'].apply(list).reset_index()
    df["Top 5 unique flavor"] = ""
    for i in range(0, len(df)):
        flavor_list = df['flavor'].loc[i]
        dict = {}
        for s in flavor_list:
            if type(s) == float:
                continue
            dict, _ = formatter(s, dict)
            flavors = []
            for val, key in dict.items():
                flavors.append([val, key])
            flavors = sorted(flavors, key=lambda x: x[1], reverse=True)
            df["Top 5 unique flavor"].loc[i] = flavors[0:5]
    print(df['Top 5 unique flavor'].head(5).loc[0])


def MapPositioningCategory(df):
    df_pos_map = pd.read_csv('Positioning Category Mapping Dataset.csv',
                             encoding='latin-1')
    df['Positioning Group'] = ""
    map = {}
    for i in range(0, len(df_pos_map)):
        pos_subgrp = df_pos_map['Positioning Subcategory'].loc[i]
        pos_grp = df_pos_map['Positioning Group'].loc[i]
        map[str(pos_subgrp)] = str(pos_grp)
    for i in range(0, len(df)):
        pos_sub_grp = df['positioning'].loc[i]
        regex = str(pos_sub_grp).split(',')
        for j in range(0, len(regex)):
            if map.get(regex[j].strip()) is not None:
                df['Positioning Group'].loc[i] = map.get(regex[j].strip())
                break
    return df


def Hypothesis_Testing(df):
    regex = '2013.*'
    df = df[df.eventdate.str.contains(regex, na=False)].reset_index()
    df = MapPositioningCategory(df)
    df = df.groupby('Positioning Group')['country'].count().reset_index()
    print(df)
    return


# read the product lauch dataset
df = pd.read_csv('Product Launch Dataset.csv', encoding='latin-1')
# sub_cat=subcat_high_uniq_flav(df)
# tot_no_of_uniq_flav(df)
# data_for_client(df)
#top_uniq_flav(df,"")
# no_of_prod_launch(df)
# ans = formatter("Lemon; Honey; Ginger, Mango|| Passion Fruit,k")
# print(ans)
# MapPositioningCategory(df)
# histogram(df)
Hypothesis_Testing(df)
