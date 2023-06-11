import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.impute import KNNImputer
import warnings


# Set page config
st.set_page_config(
    page_title='Gender Inequality Index',
    layout='wide',
    initial_sidebar_state='collapsed'
)


# Set color palette
color_palette = ['#005A8D', '#FF6363', '#FFBD69', '#7BC950', '#843FA1']

# Initialize Streamlit
warnings.filterwarnings('ignore')

# Custom CSS styles
st.markdown(
    """
    <style>
    .stApp {
        max-width: 1200px;
        padding-top: 3rem;
    }
    .st-bqplot {
        max-width: 100%;
    }
    .st-bqplot.-full-width {
        max-width: 100%;
        margin: 0;
    }
    .st-bqplot figure {
        max-width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the dataset
file_path = '/Users/keiziapurba/gender_inequality_index.xlsx'


@st.cache_data
def load_data():
    df = pd.read_excel(file_path)
    return df

df = load_data()


# Set sidebar
st.sidebar.title('Gender Inequality Index')
st.sidebar.markdown('Explore the Gender Inequality Index dataset')

# Data Understanding
st.sidebar.subheader('Data Understanding')
st.sidebar.write("Jumlah baris dan kolom dalam dataset:", df.shape[0], 'baris', df.shape[1], 'kolom')
st.sidebar.write("Info dataset:")
st.sidebar.code(df.info())

# Data Cleaning
st.sidebar.subheader('Data Cleaning')
# Ubah kolom menjadi huruf kecil
df = df.rename(columns=str.lower)
# Check apakah ada data duplikat
duplicated = df.duplicated().any()
st.sidebar.write("Apakah ada data duplikat?:", duplicated)
# Identifikasi kolom dengan nilai NaN
kolom_nan = df.columns[df.isnull().any()]
st.sidebar.write("Kolom dengan nilai NaN:", kolom_nan)
# Evaluasi tingkat missing values dalam setiap kolom
missing_values = df.isnull().sum()
st.sidebar.write("Jumlah missing values dalam setiap kolom:")
st.sidebar.code(missing_values)

# Data Cleaning - Remove NaN values
df_clean = df.dropna()

# Data Cleaning - Data Types
df_clean[['gii rank', 'maternal mortality ratio']] = df_clean[['gii rank', 'maternal mortality ratio']].astype(int)

# Main content
st.title('Gender Inequality Index')
st.subheader('Exploratory Data Analysis')

# Human Development
st.subheader('Human Development')
dv1 = df_clean.groupby(['human development'])['hdi rank'].count().to_frame().rename(columns={'hdi rank': 'count'}).reset_index()
fig = px.bar(dv1, x='human development', y='count', color='human development',
             color_discrete_sequence=color_palette)
fig.update_layout(
    xaxis=dict(title='Human Development'),
    yaxis=dict(title='Count'),
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

country_to_region = {
    'Switzerland': 'Europe and Central Asia',
    'Norway': 'Europe and Central Asia',
    'Iceland': 'Europe and Central Asia',
    'Hong Kong, China (SAR)': 'East Asia and the Pacific',
    'Australia': 'East Asia and the Pacific',
    'Denmark': 'Europe and Central Asia',
    'Sweden': 'Europe and Central Asia',
    'Ireland': 'Europe and Central Asia',
    'Germany': 'Europe and Central Asia',
    'Netherlands': 'Europe and Central Asia',
    'Finland': 'Europe and Central Asia',
    'Singapore': 'East Asia and the Pacific',
    'Belgium': 'Europe and Central Asia',
    'New Zealand': 'East Asia and the Pacific',
    'Canada': 'North America',
    'Liechtenstein': 'Europe and Central Asia',
    'Luxembourg': 'Europe and Central Asia',
    'United Kingdom': 'Europe and Central Asia',
    'Japan': 'East Asia and the Pacific',
    'Korea (Republic of)': 'East Asia and the Pacific',
    'United States': 'North America',
    'Israel': 'Middle East and North Africa',
    'Malta': 'Europe and Central Asia',
    'Slovenia': 'Europe and Central Asia',
    'Austria': 'Europe and Central Asia',
    'United Arab Emirates': 'Middle East and North Africa',
    'Spain': 'Europe and Central Asia',
    'France': 'Europe and Central Asia',
    'Cyprus': 'Europe and Central Asia',
    'Italy': 'Europe and Central Asia',
    'Estonia': 'Europe and Central Asia',
    'Czechia': 'Europe and Central Asia',
    'Greece': 'Europe and Central Asia',
    'Poland': 'Europe and Central Asia',
    'Bahrain': 'Middle East and North Africa',
    'Lithuania': 'Europe and Central Asia',
    'Saudi Arabia': 'Middle East and North Africa',
    'Portugal': 'Europe and Central Asia',
    'Latvia': 'Europe and Central Asia',
    'Andorra': 'Europe and Central Asia',
    'Croatia': 'Europe and Central Asia',
    'Chile': 'Latin America and the Caribbean',
    'Qatar': 'Middle East and North Africa',
    'San Marino': 'Europe and Central Asia',
    'Slovakia': 'Europe and Central Asia',
    'Hungary': 'Europe and Central Asia',
    'Argentina': 'Latin America and the Caribbean',
    'Türkiye': 'Europe and Central Asia',
    'Montenegro': 'Europe and Central Asia',
    'Kuwait': 'Middle East and North Africa',
    'Brunei Darussalam': 'East Asia and the Pacific',
    'Russian Federation': 'Europe and Central Asia',
    'Romania': 'Europe and Central Asia',
    'Oman': 'Middle East and North Africa',
    'Bahamas': 'Latin America and the Caribbean',
    'Kazakhstan': 'Europe and Central Asia',
    'Trinidad and Tobago': 'Latin America and the Caribbean',
    'Costa Rica': 'Latin America and the Caribbean',
    'Uruguay': 'Latin America and the Caribbean',
    'Belarus': 'Europe and Central Asia',
    'Panama': 'Latin America and the Caribbean',
    'Malaysia': 'East Asia and the Pacific',
    'Georgia': 'Europe and Central Asia',
    'Mauritius': 'Sub-Saharan Africa',
    'Serbia': 'Europe and Central Asia',
    'Thailand': 'East Asia and the Pacific',
    'Albania': 'Europe and Central Asia',
    'Bulgaria': 'Europe and Central Asia',
    'Grenada': 'Latin America and the Caribbean',
    'Barbados': 'Latin America and the Caribbean',
    'Antigua and Barbuda': 'Latin America and the Caribbean',
    'Seychelles': 'Sub-Saharan Africa',
    'Sri Lanka': 'South Asia',
    'Bosnia and Herzegovina': 'Europe and Central Asia',
    'Saint Kitts and Nevis': 'Latin America and the Caribbean',
    'Iran (Islamic Republic of)': 'Middle East and North Africa',
    'Ukraine': 'Europe and Central Asia',
    'North Macedonia': 'Europe and Central Asia',
    'China': 'East Asia and the Pacific',
    'Dominican Republic': 'Latin America and the Caribbean',
    'Moldova (Republic of)': 'Europe and Central Asia',
    'Palau': 'East Asia and the Pacific',
    'Cuba': 'Latin America and the Caribbean',
    'Peru': 'Latin America and the Caribbean',
    'Armenia': 'Europe and Central Asia',
    'Mexico': 'Latin America and the Caribbean',
    'Brazil': 'Latin America and the Caribbean',
    'Colombia': 'Latin America and the Caribbean',
    'Saint Vincent and the Grenadines': 'Latin America and the Caribbean',
    'Maldives': 'South Asia',
    'Algeria': 'Middle East and North Africa',
    'Azerbaijan': 'Europe and Central Asia',
    'Tonga': 'East Asia and the Pacific',
    'Turkmenistan': 'Europe and Central Asia',
    'Ecuador': 'Latin America and the Caribbean',
    'Mongolia': 'East Asia and the Pacific',
    'Egypt': 'Middle East and North Africa',
    'Tunisia': 'Middle East and North Africa',
    'Fiji': 'East Asia and the Pacific',
    'Suriname': 'Latin America and the Caribbean',
    'Uzbekistan': 'Europe and Central Asia',
    'Dominica': 'Latin America and the Caribbean',
    'Jordan': 'Middle East and North Africa',
    'Libya': 'Middle East and North Africa',
    'Paraguay': 'Latin America and the Caribbean',
    'Palestine, State of': 'Middle East and North Africa',
    'Saint Lucia': 'Latin America and the Caribbean',
    'Guyana': 'Latin America and the Caribbean',
    'South Africa': 'Sub-Saharan Africa',
    'Jamaica': 'Latin America and the Caribbean',
    'Samoa': 'East Asia and the Pacific',
    'Gabon': 'Sub-Saharan Africa',
    'Lebanon': 'Middle East and North Africa',
    'Indonesia': 'East Asia and the Pacific',
    'Viet Nam': 'East Asia and the Pacific',
    'Philippines': 'East Asia and the Pacific',
    'Botswana': 'Sub-Saharan Africa',
    'Bolivia (Plurinational State of)': 'Latin America and the Caribbean',
    'Kyrgyzstan': 'Europe and Central Asia',
    'Venezuela (Bolivarian Republic of)': 'Latin America and the Caribbean',
    'Iraq': 'Middle East and North Africa',
    'Tajikistan': 'Europe and Central Asia',
    'Belize': 'Latin America and the Caribbean',
    'Morocco': 'Middle East and North Africa',
    'El Salvador': 'Latin America and the Caribbean',
    'Nicaragua': 'Latin America and the Caribbean',
    'Bhutan': 'South Asia',
    'Cabo Verde': 'Sub-Saharan Africa',
    'Bangladesh': 'South Asia',
    'Tuvalu': 'East Asia and the Pacific',
    'Marshall Islands': 'East Asia and the Pacific',
    'India': 'South Asia',
    'Ghana': 'Sub-Saharan Africa',
    'Micronesia (Federated States of)': 'East Asia and the Pacific',
    'Guatemala': 'Latin America and the Caribbean',
    'Kiribati': 'East Asia and the Pacific',
    'Honduras': 'Latin America and the Caribbean',
    'Sao Tome and Principe': 'Sub-Saharan Africa',
    'Namibia': 'Sub-Saharan Africa',
    "Lao People's Democratic Republic": 'East Asia and the Pacific',
    'Timor-Leste': 'East Asia and the Pacific',
    'Vanuatu': 'East Asia and the Pacific',
    'Nepal': 'South Asia',
    'Eswatini (Kingdom of)': 'Sub-Saharan Africa',
    'Equatorial Guinea': 'Sub-Saharan Africa',
    'Cambodia': 'East Asia and the Pacific',
    'Zimbabwe': 'Sub-Saharan Africa',
    'Angola': 'Sub-Saharan Africa',
    'Myanmar': 'East Asia and the Pacific',
    'Syrian Arab Republic': 'Middle East and North Africa',
    'Cameroon': 'Sub-Saharan Africa',
    'Kenya': 'Sub-Saharan Africa',
    'Congo': 'Sub-Saharan Africa',
    'Zambia': 'Sub-Saharan Africa',
    'Solomon Islands': 'East Asia and the Pacific',
    'Comoros': 'Sub-Saharan Africa',
    'Papua New Guinea': 'East Asia and the Pacific',
    'Mauritania': 'Sub-Saharan Africa',
    "Côte d'Ivoire": 'Sub-Saharan Africa',
    'Tanzania (United Republic of)': 'Sub-Saharan Africa',
    'Pakistan': 'South Asia',
    'Togo': 'Sub-Saharan Africa',
    'Haiti': 'Latin America and the Caribbean',
    'Nigeria': 'Sub-Saharan Africa',
    'Rwanda': 'Sub-Saharan Africa',
    'Benin': 'Sub-Saharan Africa',
    'Uganda': 'Sub-Saharan Africa',
    'Lesotho': 'Sub-Saharan Africa',
    'Malawi': 'Sub-Saharan Africa',
    'Senegal': 'Sub-Saharan Africa',
    'Djibouti': 'Middle East and North Africa',
    'Sudan': 'Sub-Saharan Africa',
    'Madagascar': 'Sub-Saharan Africa',
    'Gambia': 'Sub-Saharan Africa',
    'Ethiopia': 'Sub-Saharan Africa',
    'Eritrea': 'Sub-Saharan Africa',
    'Guinea-Bissau': 'Sub-Saharan Africa',
    'Liberia': 'Sub-Saharan Africa',
    'Congo (Democratic Republic of the)': 'Sub-Saharan Africa',
    'Afghanistan': 'South Asia',
    'Sierra Leone': 'Sub-Saharan Africa',
    'Guinea': 'Sub-Saharan Africa',
    'Yemen': 'Middle East and North Africa',
    'Burkina Faso': 'Sub-Saharan Africa',
    'Mozambique': 'Sub-Saharan Africa',
    'Mali': 'Sub-Saharan Africa',
    'Burundi': 'Sub-Saharan Africa',
    'Central African Republic': 'Sub-Saharan Africa',
    'Niger': 'Sub-Saharan Africa',
    'Chad': 'Sub-Saharan Africa',
    'South Sudan': 'Sub-Saharan Africa',
    'Somalia': 'Sub-Saharan Africa',
    'Timor-Leste': 'East Asia and the Pacific',
    'Unknown': 'Unknown'
}

df_clean['region'] = df_clean['country'].map(country_to_region)


# Gender Inequality Index by Region
st.subheader('Gender Inequality Index by Region')
dv2 = df_clean.groupby(['region'])['gii value'].mean().to_frame().reset_index()
fig = px.pie(dv2, values='gii value', names='region', hole=0.4, color='region',
             color_discrete_sequence=color_palette)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)


st.set_option('deprecation.showPyplotGlobalUse', False)

# Scatter plot
st.subheader('Scatter plot')
x_label = st.selectbox('Select x-axis:', df_clean.columns[2:])
y_label = st.selectbox('Select y-axis:', df_clean.columns[2:])
scatter_plot = px.scatter(df_clean, x=x_label, y=y_label, color='region',
                          color_discrete_sequence=px.colors.qualitative.Pastel1)
scatter_plot.update_layout(
    xaxis=dict(title=x_label),
    yaxis=dict(title=y_label),
    showlegend=True
)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.plotly_chart(scatter_plot, use_container_width=True)

# Box plot
st.subheader('Box plot')
boxplot_column = st.selectbox('Select column:', df_clean.columns[2:])
box_plot = px.box(df_clean, x='region', y=boxplot_column, color='region',
                  color_discrete_sequence=px.colors.qualitative.Pastel1)
box_plot.update_layout(
    xaxis=dict(title='Region'),
    yaxis=dict(title=boxplot_column),
    showlegend=False
)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.plotly_chart(box_plot, use_container_width=True)


# Correlation Heatmap
st.subheader('Correlation Heatmap')
plt.figure(figsize=(12, 8))
numeric_columns = df_clean.select_dtypes(include=np.number)
sns.heatmap(numeric_columns.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
st.pyplot()

# Table
st.subheader('Data Table')
st.dataframe(df_clean)

# Data Modeling
st.subheader('Data Modeling')
st.write("Coming soon...")

# About
st.sidebar.subheader('About')
st.sidebar.write('This app is an interactive exploration of the Gender Inequality Index dataset. '
                 'It provides visualizations and insights into various aspects of gender inequality. '
                 'The dataset contains information about different countries and their gender inequality index. '
                 'For more information, please refer to the [Gender Inequality Index](https://example.com) website.')

# Footer
st.sidebar.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f8f9fa;
        color: #868e96;
        text-align: center;
        padding: 0.5rem;
        font-size: 0.85rem;
        border-top: 1px solid #dee2e6;
    }
    </style>
    """
    "<div class='footer'>"
    "Made with ❤️ by Your Name"
    "</div>",
    unsafe_allow_html=True
)


import os

main_file_path = os.path.abspath(__file__)
print("Main file path:", main_file_path)
