from turtle import position
import pandas as pd
#a list of unique flavors based on your analysis. What is the total number 
# of unique flavors in your list?
def tot_no_of_uniq_flav(df):
    df = df['flavor'].to_list()
    count = 0
    dict = {}
    not_spec = ['Not specified','Not Specified','not Specified','not specified']
    for i in range(0,len(df)):
        s =str(df[i])
        l,r=0,0
        n=len(s)
        while l<n and r<n:
            if s[r] !=';' and s[r] !='|':
                r=r+1
            else:
                sub = s[l:r]
                if s[r]==';':
                    l=r+1
                    r=r+1
                else:
                    l=r+2
                    r=r+2
                if ',' in sub:
                    temp = sub.split(',')
                    if len(temp)>1 and temp[1].strip() in not_spec:
                        if dict.get(temp[0].strip()) == None:
                            count = count+1
                            dict[temp[0].strip()] = True
                    else:
                        if dict.get(sub.strip()) == None:
                            count = count+1
                            dict[sub.strip()] = True
                else:
                    if dict.get(sub.strip()) == None:
                        count = count+1
                        dict[sub.strip()] = True
        sub = s[l:r].strip()
        temp = sub.split(',')
        if len(temp)>1 and temp[1].strip() in not_spec:
            if dict.get(temp[0].strip())==None:
                count = count+1
                dict[temp[0].strip()] = True
        else:
            if dict.get(sub.strip())==None:
                count = count+1
                dict[sub.strip()] = True
    #print(dict)
    print(len(dict))



# histogram of market subcategory against eventdate (years). Do any 
# categories show negative trend over years?
def histogram():
    pass

#market subcategory has highest unique flavors
def subcat_high_uniq_flav(df):
    df = df.groupby('market_subcategory')['flavor'].apply(list).reset_index()
    not_spec = ['Not specified','Not Specified','not Specified','not specified']
    maxi=0
    sub_cat = ""
    print(df)
    for i in range(0,len(df)):
        flavor_list = df['flavor'].loc[i]
        dict={}
        count = 0
        for s in flavor_list:
            if type(s)==float:
                s=str(s)
            n=len(s)
            l,r=0,0
            sub = ""
            while l<n and r<n:
                if s[r]!=';' and s[r]!='|':
                    r=r+1
                else:
                    sub = s[l:r+1]
                    if s[r]==';':
                        l=r+1
                        r=r+1
                    else:
                        l=r+2
                        r=r+2
                    if ',' in sub:
                        temp = sub.split(',')
                        if len(temp)>1 and temp[1].strip() in not_spec:
                            if dict.get(temp[0].strip())==None:
                                count = count+1
                                dict[temp[0]] = True
                        else:
                            if dict.get(sub.strip())==None:
                                count=count+1
                                dict[sub.strip()]=1
                    else:
                        if dict.get(sub.strip())==None:
                            count = count+1
                            dict[sub.strip()] = True
        sub = s[l:r].strip()
        temp = sub.split(',')
        if len(temp)>1 and temp[1].strip() in not_spec:
            if dict.get(temp[0].strip())==None:
                count = count+1
                dict[temp[0].strip()] = True
        else:
            if dict.get(sub.strip())==None:
                count = count+1
                dict[sub.strip()] = True
        
        if count>maxi:
            maxi = count
            sub_cat = df['market_subcategory'].loc[i]
        print(count,df['market_subcategory'].loc[i])
    return sub_cat


def data_for_client(df,country,positioning,year):
    #filtering country
    df = df[df['country'] == 'Canada']
    #filtering date
    regex = '2013.*'
    df =  df[df.eventdate.str.contains(regex,na=False)]
    # filtering positioning
    regex = 'Ethical - Packaging.*'
    df = df[df.positioning.str.contains(regex,na=False)]
    #filering market subcategory
    regex = 'Energy Drinks.*'
    df = df[df.market_subcategory.str.contains(regex,na=False)]
    print(df)


#TOP 5 unique flavors across countries in 2013
def top_uniq_flav(df,year='2013'):
    regex = '2013.*'
    df =  df[df.eventdate.str.contains(regex,na=False)].reset_index()
    dict = {}
    not_spec = ['Not specified','Not Specified','not Specified','not specified']
    for i in range(0,len(df)):
        s = df['flavor'].loc[i]
        l,r = 0,0
        s = str(s)
        n = len(s)
        while l<n and r<n:
            if s[r]!=';' and s[r]!='|':
                r=r+1
            else:
                sub = s[l:r]
                if s[r]==';':
                    l=r+1
                    r=r+1
                else:
                    l=r+2
                    r=r+2
                if ',' in sub:
                    temp = sub.split(',')
                    if len(temp)>1 and temp[1].strip() in not_spec:
                        if dict.get(temp[0].strip())==None:
                            dict[temp[0].strip()] = 1
                        else:
                            dict[temp[0].strip()] = dict.get(temp[0].strip()) + 1
                    else:
                        if dict.get(sub.strip())==None:
                            dict[sub.strip()]=1
                        else:
                            dict[sub.strip()] = dict.get(sub.strip()) + 1
                else:
                    if dict.get(sub.strip())==None:
                        dict[sub.strip()] = 1
                    else:
                        dict[sub.strip()] = dict.get(sub.strip()) + 1
        sub = s[l:r].strip()
        temp = sub.split(',')
        if len(temp)>1 and temp[1].strip() in not_spec:
            if dict.get(temp[0].strip())==None:
                dict[temp[0].strip()] = 1
            else:
                dict[temp[0].strip()] = dict.get(temp[0].strip()) + 1
        else:
            if dict.get(sub.strip())==None:
                dict[sub.strip()] = 1
            else:
                dict[sub.strip()] = dict.get(sub.strip()) + 1
    flavors  =  []
    for val,key in dict.items():
        flavors.append([val,key])
    flavors = sorted(flavors,key=lambda x:x[1],reverse = True)
    print(flavors[0:5])

# read the product lauch dataset
df = pd.read_csv('Product Launch Dataset.csv',encoding='latin-1')
#sub_cat,maxi=subcat_high_uniq_flav(df)
#tot_no_of_uniq_flav(df)
#data_for_client(df,"","","")
#top_uniq_flav(df,"")