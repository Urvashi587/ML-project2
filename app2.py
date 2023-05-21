import streamlit as st
import preprocess,mt
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
st.sidebar.title("Olympics Analysis")
choice=st.sidebar.radio('Choose the kind of analysis:',('Medal tally','Based on country','Based on athlete','General'))
ath=pd.read_csv('athlete_events.csv')
reg=pd.read_csv('noc_regions.csv')
ath=preprocess.preproc(ath,reg)
if choice=='Medal tally':
    st.sidebar.header("Medal Tally")
    yrs,country=mt.country_year(ath)
    yr=st.sidebar.selectbox("Select year",yrs)
    cntry=st.sidebar.selectbox("Select country",country)
    if yr=='Overall' and cntry=='Overall':
        st.title("Overall Medal Tally")
    if yr!='Overall' and cntry=='Overall':
        st.title(f"Medal Tally in year {yr}")
    if yr=='Overall' and cntry!='Overall':
        st.title(f"Medal Tally of {cntry} over all the years")
    if yr!='Overall' and cntry!='Overall':
        st.title(f"Medal Tally in year {yr} of {cntry}")
    medal_tally=mt.get_medal_tally(ath,yr,cntry)
    st.table(medal_tally)
if choice=='General':
    st.sidebar.header("General Analysis")
    st.title("Stats")
    nations=ath['region'].unique().shape[0]
    athletes = ath['Name'].unique().shape[0]
    events=ath['Event'].unique().shape[0]
    cities = ath['City'].unique().shape[0]
    held_till_now=ath['Year'].unique().shape[0]-1
    sports = ath['Sport'].unique().shape[0]
    col1,col2,col3=st.columns(3)
    with col1:
        st.subheader("Editions")
        st.header(held_till_now)
    with col2:
        st.subheader("Hosts")
        st.header(cities)
    with col3:
        st.subheader("Events")
        st.header(events)
    col1,col2,col3=st.columns(3)
    with col1:
        st.subheader("Sports")
        st.header(sports)
    with col2:
        st.subheader("Nations")
        st.header(nations)
    with col3:
        st.subheader("Athletes")
        st.header(athletes)
    participation_over_years = ath.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
    participation_over_years.rename(columns={"Year":"year","count":"No of participating countries"},inplace=True)
    fig = px.line(participation_over_years, x="year", y="No of participating countries")
    st.title("Participation over years")
    st.plotly_chart(fig)
    events_over_years = ath.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values(
        'Year')
    events_over_years.rename(columns={"Year": "year", "count": "No of events"}, inplace=True)
    fig = px.line(events_over_years, x="year", y="No of events")
    st.title("No of events over the years")
    st.plotly_chart(fig)
    athletes_over_years = ath.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values(
        'Year')
    athletes_over_years.rename(columns={"Year": "year", "count": "No of athletes"}, inplace=True)
    fig = px.line(athletes_over_years, x="year", y="No of athletes")
    st.title("No of athletes over the years")
    st.plotly_chart(fig)
    st.title("Events over time(sport-wise)")
    fig,ax = plt.subplots(figsize=(10, 10))
    x = ath.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)
    st.title("Top Athletes")
    sports=mt.sportlist(ath)
    selected_sport=st.sidebar.selectbox("Select sport",sports)
    x=mt.top_athletes(ath,selected_sport)
    st.table(x)
if choice=='Based on country':
    st.sidebar.header("Country Wise Analysis")
    country=mt.country(ath)
    selected_country=st.sidebar.selectbox("Select country",country)
    country_medal_tally=mt.country_wise_medals(ath,selected_country)
    fig = px.line(country_medal_tally, x="Year", y="Medals Won")
    st.title(f"Medal tally of {selected_country} over the years")
    st.plotly_chart(fig)
    x=mt.countrymap(ath,selected_country)
    st.title(f"{selected_country}'s data regarding different sports")
    fig, ax = plt.subplots(figsize=(10, 10))
    ax = sns.heatmap(x,annot=True)
    st.pyplot(fig)
    st.title(f"Top 10 athletes of {selected_country}")
    top_10=mt.top_athletes_countrywise(ath,selected_country)
    st.table(top_10)
if choice=='Based on athlete':
    new_df = ath.drop_duplicates(subset=['Name', 'region'])
    st.sidebar.header("Athlete Wise Analysis")
    st.title("Age distribution")
    x1 = new_df['Age'].dropna()
    x2 = new_df[new_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = new_df[new_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = new_df[new_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall age', 'Gold medalist', 'Silver medalist', 'Bronze medalist'],
                             show_hist=False, show_rug=False)
    st.plotly_chart(fig)
    sports = mt.sportlist(ath)
    selected_sport = st.sidebar.selectbox("Select sport", sports)
    temp_df=mt.weight_height(ath,selected_sport)
    st.title(f"Height vs Weight : {selected_sport}")
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=50)
    st.pyplot(fig)
    combined=mt.men_women(ath)
    st.title("Men vs Women Participation")
    fig = px.line(combined, x="Year", y=["Men", "Women"])
    st.plotly_chart(fig)

