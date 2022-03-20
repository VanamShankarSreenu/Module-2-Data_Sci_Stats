import pandas as pd
import matplotlib.pyplot as plt


def formatter(s,dict):
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
    return res

# a list of unique flavors based on your analysis. What is the total number 
# of unique flavors in your list?
def tot_no_of_uniq_flav(df):
    df = df['flavor'].to_list()
    count = 0
    dict = {}
    not_spec = ['Not specified', 'Not Specified', 'not Specified', 'not specified']
    for i in range(0, len(df)):
        s = str(df[i])
        frmt_string = formatter(s)
        for val in frmt_string:
            val = val.strip()
            if ',' in val:
                temp = val.split(',')
                if len(temp) > 1 and temp[1].strip() in not_spec:
                    if dict.get(temp[0].strip()) is None:
                        count = count+1
                        dict[temp[0].strip()] = True
                else:
                    if dict.get(val) is None:
                        count = count+1
                        dict[val] = True
            else:
                if dict.get(val) is None:
                    count = count+1
                    dict[val] = True
    print(len(dict))


# histogram of market subcategory against eventdate (years). Do any 
# categories show negative trend over years?
def histogram(df):
    pass


# market subcategory has highest unique flavors
def subcat_high_uniq_flav(df):
    df = df.groupby('market_subcategory')['flavor'].apply(list).reset_index()
    not_spec = ['Not specified', 'Not Specified', 'not Specified', 'not specified']
    maxi = 0
    sub_cat = ""
    print(df)
    for i in range(0,len(df)):
        flavor_list = df['flavor'].loc[i]
        dict = {}
        count = 0
        for s in flavor_list:
            if type(s) == float:
                continue
            frmt_string = formatter(s)
            for val in frmt_string:
                if ',' in val:
                    temp = val.split(',')
                    if len(temp)>1 and temp[1].strip() in not_spec:
                        if dict.get(temp[0].strip())==None:
                            count = count+1
                            dict[temp[0]] = True
                    else:
                        if dict.get(val.strip())==None:
                            count=count+1
                            dict[val.strip()] = True
                else:
                    if dict.get(val.strip())==None:
                        count = count+1
                        dict[val.strip()] = True
        if count>maxi:
            maxi = count
            sub_cat = df['market_subcategory'].loc[i]
        print(count,df['market_subcategory'].loc[i])
    print(sub_cat,maxi)
    return 


#  on the number of product launches over different quarters for “fruit” flavor
def no_of_prod_launch(df):
    df['eventdate'] = pd.to_datetime(df['eventdate'], format='%m-%d-%Y')
    df = df.groupby('eventdate')['flavor'].apply(list).reset_index()
    df = df.sort_values(by='eventdate')
    df['count of fruit flavor'] = ""
    fc = pd.read_csv('Flavor Classification Dataset.csv', encoding='latin-1')
    fc = fc[ fc['Flavor_Group'] == 'Fruit'].reset_index()
    fruit_flav = []
    for i in range(0,len(fc)):
        fruit_flav.append(fc['flavor'].loc[i].strip())
    for i in range(0,len(df)):
        flav_list = df['flavor'].loc[i]
        count = 0
        for s in flav_list:
            if type(s) == float:
                s = str(s)
            frmt_flav_list = formatter(s)
            # print(frmt_flav_list)
            for val in frmt_flav_list:
                for j in range(0,len(fruit_flav)):
                    if val.strip().lower() == fruit_flav[j].strip().lower():
                        count = count+1
                        break
        df['count of fruit flavor'].loc[i] = count
    print(df)
    ax = plt.gca()
    # line plot for math marks
    df.plot(kind = 'line',
            x = 'eventdate',
            y = 'count of fruit flavor',
            color = 'blue',ax = ax)
    
    plt.show()


def data_for_client(df, country = "", positioning = "", year = ""):
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
    df =  df[df.eventdate.str.contains(regex,na=False)].reset_index()
    dict = {}
    not_spec = ['Not specified', 'Not Specified', 'not Specified', 'not specified']
    for i in range(0, len(df)):
        s = df['flavor'].loc[i]
        if type(s) == float:
            continue
        frmt_string = formatter(s)
        for val in frmt_string:
            if ',' in val:
                temp = val.split(',')
                if len(temp)>1 and temp[1].strip() in not_spec:
                    if dict.get(temp[0].strip())==None:
                        dict[temp[0].strip()] = 1
                    else:
                        dict[temp[0].strip()] = dict.get(temp[0].strip()) + 1
                else:
                    if dict.get(val.strip())==None:
                        dict[val.strip()]=1
                    else:
                        dict[val.strip()] = dict.get(val.strip()) + 1
            else:
                if dict.get(val.strip())==None:
                    dict[val.strip()] = 1
                else:
                    dict[val.strip()] = dict.get(val.strip()) + 1
    flavors  =  []
    for val,key in dict.items():
        flavors.append([val,key])
    flavors = sorted(flavors,key=lambda x:x[1],reverse = True)
    print(flavors[0:5])


def MapPositioningCategory(df):
    df_pos_map = pd.read_csv('Positioning Category Mapping Dataset.csv', encoding = 'latin-1')
    df['Positioning Group'] = ""
    map = {}
    for i in range(0, len(df_pos_map)):
        pos_subgrp, pos_grp = df_pos_map['Positioning Subcategory'].loc[i],df_pos_map['Positioning Group'].loc[i]
        map[str(pos_subgrp)] = str(pos_grp)
    print(map)
    for i in range(0, len(df)):
        pos_sub_grp = df['positioning'].loc[i]
        regex = str(pos_sub_grp).split(',')
        for j in range(0, len(regex)):
            if map.get(regex[j].strip()) is not None:
                df['Positioning Group'].loc[i] = map.get(regex[j].strip())
                break
    conv_posi = df[df['Positioning Group'] == 'Convenience'].reset_index()
    eth_posi = df[df['Positioning Group'] == 'Ethical'].reset_index()

    





# read the product lauch dataset


df = pd.read_csv('Product Launch Dataset.csv',encoding='latin-1')
fun(df)
#sub_cat=subcat_high_uniq_flav(df)
#tot_no_of_uniq_flav(df)
#data_for_client(df,"","","")
#top_uniq_flav(df,"")
#no_of_prod_launch(df)
#ans = formatter("Lemon; Honey; Ginger, Mango|| Passion Fruit,k")
#print(ans)