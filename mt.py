import numpy as np

def country_year(ath):
    yrs = ath['Year'].unique().tolist()
    yrs.sort()
    yrs.insert(0, 'Overall')
    country = np.unique(ath['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return yrs,country
def country(ath):
    country = np.unique(ath['region'].dropna().values).tolist()
    country.sort()
    return country
def sportlist(ath):
    sports=ath['Sport'].unique().tolist()
    sports.sort()
    sports.insert(0,'Overall')
    return sports
def get_medal_tally(df,yr,cntry):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if yr=='Overall' and cntry=='Overall':
        temp_df=medal_df
    if yr!='Overall' and cntry=='Overall':
        temp_df=medal_df[medal_df['Year']==int(yr)]
    if yr=='Overall' and cntry!='Overall':
        temp_df=medal_df[medal_df['region']==cntry]
        flag=1
    if yr!='Overall' and cntry!='Overall':
        temp_df=medal_df[(medal_df['region']==cntry) & (medal_df['Year']==int(yr))]
    if flag==1:
        temp_df=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        temp_df=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    temp_df['Total']=temp_df['Gold']+temp_df['Silver']+temp_df['Bronze']
    return temp_df
def top_athletes(df,sport):
    temp_df=df.dropna(subset=['Medal'])
    if sport!='Overall':
        temp_df=temp_df[temp_df['Sport']==sport]
    x=temp_df['Name'].value_counts().reset_index().head(10).merge(df,on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={"Name":"Name","count":"Medals Won","Sport":"Sport","region":"Country"},inplace=True)
    return x
def country_wise_medals(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df=temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    temp_df=temp_df[temp_df['region']==country]
    x=temp_df.groupby('Year').count()['Medal'].reset_index()
    x.rename(columns={"Year":"Year","Medal":"Medals Won"},inplace=True)
    return x
def countrymap(ath,country):
    temp_df=ath.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    x=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return x
def top_athletes_countrywise(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df=temp_df[temp_df['region']==country]
    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,on='Name',how='left')[['Name','count','Sport']].drop_duplicates('Name')
    x.rename(columns={"Name":"Name","count":"Medals Won","Sport":"Sport"},inplace=True)
    return x
def weight_height(df,sport):
    new_df=df.drop_duplicates(subset=['Name','region'])
    new_df['Medal'].fillna('No Medal',inplace=True)
    if sport!='Overall':
        temp_df = new_df[new_df['Sport'] == sport]
        return temp_df
    else:
        return new_df
def men_women(df):
    new_df = df.drop_duplicates(subset=['Name', 'region'])
    m = new_df[new_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    f = new_df[new_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    combined = m.merge(f, on='Year', how='left')
    combined.rename(columns={"Name_x": "Men", "Name_y": "Women"}, inplace=True)
    combined.fillna(0,inplace=True)
    return combined