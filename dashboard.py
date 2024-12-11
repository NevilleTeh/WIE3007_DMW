import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Dashboard",
    page_icon="📈",
    layout="wide")

#load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('Data Science Salary 2021 to 2023.csv')
    return df

df_salary = load_data()

st.title(':blue[Dashboard]')

r1c1, r1c2 = st.columns((4, 5), gap='small')
with r1c1:
    st.subheader('Salary Trend over Time')
    plt.figure(figsize = (10,6))
    salary_trend = df_salary[['salary_in_usd', 'work_year']].sort_values(by = 'work_year')
    chart_salary_trend = sns.lineplot(data =salary_trend ,x = 'work_year', y = 'salary_in_usd', marker = 'o',linestyle='--', color='Blue', markersize=8 )
    plt.title('Salary Trend Over The Time', fontsize=12, fontweight='bold')

    # Customize the background color
    chart_salary_trend.set_facecolor("#f4f4f4")
    plt.legend(['Salary'], loc='best', fontsize=12)

    # Remove the grid lines
    chart_salary_trend.grid(False)

    st.pyplot(plt)

with r1c2:
    st.subheader('Top 10 High-Paying Job Designations')
    xdf=df_salary.groupby(['job_title'])['salary_in_usd'].median().sort_values(ascending=False).head(10)
    # Create the bar chart
    chart_job_title = px.bar(
        x=xdf.index,
        y=xdf,
        # title='Top 10 High-Paying Job Designations',
        labels={'y': 'Median Salary (USD)', 'x': 'Job Designations'},
        text=xdf,  # Add values on top of each bar
        color=xdf,  # Color based on salary values
        color_continuous_scale='Blues'  # Color scheme for a more dynamic look
    )

    # Customize the text on bars
    chart_job_title.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    # Remove grid lines for a cleaner look
    chart_job_title.update_xaxes(showgrid=False)
    chart_job_title.update_yaxes(showgrid=False)

    # Show the figure
    st.plotly_chart(chart_job_title)

r2c1, r2c2 = st.columns((6, 4), gap='small')

with r2c1:
    st.subheader('Top 10 Most Popular Job Desginations')
    # Create the bar chart with enhancements
    chart_popular_job = px.bar(
        x=df_salary['job_title'].value_counts().head(10).index,
        y=df_salary['job_title'].value_counts().head(10),
        # title='Top 10 Most Popular Job Designations',
        labels={'y': 'No. of Posts', 'x': 'Job Designations'},
        color=df_salary['job_title'].value_counts().head(10),  # Adds color to each bar
        color_continuous_scale='Reds'  # Choose a color scale
    )

    # Display count values on top of bars
    chart_popular_job.update_traces(texttemplate='%{y}', textposition='outside')

    st.plotly_chart(chart_popular_job)

with r2c2:
    st.subheader('Job Title Distribution')
    # Calculate frequency of each job title
    job_title_counts = df_salary['job_title'].value_counts()

    # Determine titles below the threshold, e.g., less than N occurrences
    N=50
    low_frequency_titles = job_title_counts[job_title_counts < N].index

    # Replace these titles in the dataframe with "Others"
    df_salary['adjusted_job_title'] = df_salary['job_title'].apply(lambda x: "Others" if x in low_frequency_titles else x)

    # Recalculate the frequency
    adjusted_counts = df_salary['adjusted_job_title'].value_counts()

    #Plot
    df_salary1 = df_salary.groupby('adjusted_job_title').size().reset_index(name='Total')
    chart_job_title = px.pie(df_salary1, values='Total', names='adjusted_job_title', color='adjusted_job_title', hole=0.5)
    st.plotly_chart(chart_job_title)