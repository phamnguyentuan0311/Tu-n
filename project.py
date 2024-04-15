import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.express as px
import base64

# xử lý dữ liệu
movies_data=pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/movies.csv")
movies_data.info()
movies_data.dropna()

# lọc dữ liệu
years=movies_data['year'].unique().tolist()
genres=movies_data['genre'].unique().tolist()
scores = movies_data['score'].unique().tolist()

# tạo sidebar
st.sidebar.markdown("Select a range on the slider (it represents movie score) to view the total number of movies in a genre that falls within that range")
min_value = 1.00
max_value = 10.00
filter_score = st.sidebar.slider('Choose a value::', min_value, max_value,value=(3.00, 4.00))
st.sidebar.markdown('Choose a value:')

# sidebar genre
st.sidebar.markdown("Select your preferred genre(s) and year to view the movies released that year and on that genre")
filter_genres = st.sidebar.multiselect('Choose Genre:', genres,default = ['Animation','Horror','Fantasy','Romance'])

# sidebar year
filter_year = st.sidebar.selectbox('Choose a year:',years,0)

# Loc theo so diem cua film
score_info = (movies_data['score'].between(*filter_score))
# Loc theo the loai va nam phat hanh
year_info = (movies_data['genre'].isin(filter_genres))&(movies_data['year'] == filter_year)

#st.markdown("<p style='text-align: right;'>Interactive Dashboard</p>", unsafe_allow_html=True)
st.header("Interactive Dashboard")
st.subheader(" Interact  with  this  dashboard  using  the  widgets  on  the  sidebar ")

## bieu do linechart

table1, linechart2 = st.columns([6,8])
with table1:
    st.subheader(" Lists of movies filtered by year and Genre ")
    dataframe_genre_year = movies_data[year_info].groupby(['name', 'genre'])['year'].sum()
    dataframe_genre_year = dataframe_genre_year.reset_index()
    st.dataframe(dataframe_genre_year, width = 600)
with linechart2:
    st.subheader(" User score of movies and their genre ")
    dataframe_count_year = movies_data[score_info].groupby('genre')['score'].count()
    dataframe_count_year = dataframe_count_year.reset_index()

    figpx = px.line(dataframe_count_year, x = 'genre', y = 'score')

    figpx.update_xaxes(showgrid=True)
    figpx.update_yaxes(showgrid=True)
with linechart2:
    st.plotly_chart(figpx)


### ve bieu do barchart
st.markdown("""Average Movie Budget, Grouped by Genre""")
avg_budget = movies_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()
genre = avg_budget['genre']
avg_bud = avg_budget['budget']
fig = plt.figure(figsize = (20,10))
plt.bar(genre, avg_bud, color = 'maroon')
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Matplotlib Bar Chart Showing The Average Budget of Movies in Each Genre')
st.pyplot(fig)
