import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
import plotly.graph_objects as go
import joblib


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
st.sidebar.title('Gender Inequality Index 2021')
st.sidebar.markdown('Explore dataset Gender Inequality Index')

# Table
st.sidebar.subheader('Data Descriptions')
st.sidebar.write("- **Gender Inequality Index:** Suatu ukuran komposit yang mencerminkan ketimpangan pencapaian antara perempuan dan laki-laki dalam tiga dimensi: kesehatan reproduksi, pemberdayaan, dan pasar kerja. Skala indeks ini berkisar antara 0, di mana perempuan dan laki-laki memiliki pencapaian yang sama, hingga 1, di mana satu gender memiliki pencapaian yang sangat buruk dalam semua dimensi yang diukur. Lihat Technical Note 4 di http://hdr.undp.org/sites/default/files/hdr2022_technical_notes.pdf untuk detail tentang bagaimana Indeks Ketimpangan Gender dihitung.")
st.sidebar.write("- **Maternal mortality ratio:** Jumlah kematian akibat penyebab terkait kehamilan per 100.000 kelahiran hidup.")
st.sidebar.write("- **Adolescent birth rate:** Jumlah kelahiran oleh perempuan usia 15–19 tahun per 1.000 perempuan usia 15–19 tahun.")
st.sidebar.write("- **Share of seats in parliament:** Proporsi kursi yang dipegang oleh perempuan di parlemen nasional, dinyatakan sebagai persentase dari total kursi. Untuk negara-negara dengan sistem legislatif bikameral, andil kursi dihitung berdasarkan kedua kamar.")
st.sidebar.write("- **Population with at least some secondary education:** Persentase penduduk usia 25 tahun ke atas yang telah mencapai (namun tidak selalu menyelesaikan) tingkat pendidikan menengah lanjutan.")
st.sidebar.write("- **Labour force participation rate:** Proporsi penduduk usia kerja (usia 15 tahun ke atas) yang terlibat dalam pasar kerja, baik dengan bekerja maupun mencari pekerjaan, dinyatakan sebagai persentase dari penduduk usia kerja.")

# Table
st.sidebar.subheader('Data Table')
st.sidebar.dataframe(df)

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
st.title('Gender Gap: Are We Stuck in the Past?')

'\n'
'\n'

st.subheader('Apa itu Gender Equality?')
st.write('Gender equality tercapai ketika semua individu, tanpa memandang jenis kelamin, memiliki hak yang sama, tanggung jawab yang sama, dan kesempatan yang sama. Hal ini melibatkan upaya untuk mengubah struktur sosial yang mempertahankan ketidaksetaraan kekuasaan antara perempuan dan laki-laki, dengan tujuan menciptakan distribusi yang lebih adil dari nilai dan prioritas antara kedua kelompok tersebut. Dengan demikian, diharapkan tercipta kehidupan yang lebih baik dan sejalan bagi semua individu.')

'\n'
st.subheader('About Gender Inequality Index (GII)')
st.write('GII (Indeks Ketimpangan Gender) adalah metrik gabungan yang mengukur ketimpangan gender menggunakan tiga dimensi: kesehatan reproduksi, pemberdayaan, dan pasar tenaga kerja. Rentang nilai GII adalah dari 0, di mana perempuan dan laki-laki memiliki kesetaraan, hingga 1, di mana salah satu gender mengalami kondisi yang paling buruk dalam semua dimensi yang diukur.')

'\n'
st.subheader('Apa itu Human Development?')
st.write('Human Development merujuk pada proses meningkatkan kesejahteraan dan kapabilitas individu, dengan fokus pada kesehatan, pendidikan, dan kualitas hidup secara keseluruhan.')

'\n'
'\n'

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
# Gender Inequality Index by Region
# Gender Inequality Index by Region
# Gender Inequality Index by Region
st.subheader('Gender Inequality Index by Region')
dv2 = df_clean.groupby(['region'])['gii value'].mean().to_frame().reset_index()
dv2['color'] = ['blue' if r == 'Sub-Saharan Africa' else 'gray' for r in dv2['region']]
fig = px.pie(dv2, values='gii value', names='region', hole=0.4,
             color='color', color_discrete_map={'blue': 'blue', 'gray': 'lightgray'},
             labels={'region': 'Region', 'gii value': 'GII Value'})
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)





st.set_option('deprecation.showPyplotGlobalUse', False)

# Melihat Korelasi
st.subheader('Melihat Korelasi')
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


'\n'
'\n'


# Visualisasi Gender Inequality Index by Country
st.subheader('Gender Inequality Index by Country')
fig = px.choropleth(df_clean, locations='country', locationmode='country names', color='gii value',
                    hover_data=['gii value', 'region'], 
                    color_continuous_scale='Viridis')

fig.update_layout(
    
    geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular')
)

st.plotly_chart(fig)

st.write('Wilayah Amerika Utara dan Eropa, serta Asia Tengah, didominasi oleh negara-negara dengan tingkat pembangunan manusia yang sangat tinggi. Hal ini disebabkan oleh rendahnya nilai GII, yang menunjukkan kesenjangan gender yang lebih kecil. Di sisi lain, Afrika Sub-Sahara memiliki tingkat human development yang rendah karena nilai GII yang tinggi.')

'\n'

# Visualisasi Trend of Female and Male Labor Force Participation
st.subheader('Trend of Female and Male Labor Force Participation')
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_clean['country'], y=df_clean['f_labour_force'], mode='lines', name='Female Labor Force'))
fig.add_trace(go.Scatter(x=df_clean['country'], y=df_clean['m_labour_force'], mode='lines', name='Male Labor Force'))
fig.update_layout(
                  xaxis_title='Country', yaxis_title='Labor Force Participation')
st.plotly_chart(fig)

# Keterangan Visualisasi Trend of Female and Male Labor Force Participation
st.write("Berdasarkan grafik di atas, dapat dilihat bahwa proporsi penduduk usia kerja (usia 15 tahun ke atas) yang terlibat dalam pasar tenaga kerja, baik dengan bekerja atau mencari pekerjaan pada tahun 2021 di dominasi jumlahnya oleh laki-laki. Secara garis besar, dapat dilihat bahwa ada ketimpangan dalam jumlah persentase partisipasi angkatan kerja. Nilai persentase paling rendah dimiliki oleh female labour negara Yemen sebesar 5.9. Sedangkan persentase tertinggi dimiliki oleh male labour negara Qatar sebesar 95.4.")

'\n'
'\n'

# Visualisasi Trend of Female and Male Secondary Education Participation
st.subheader('Trend of Female and Male Secondary Education Participation')
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_clean['country'], y=df_clean['f_secondary_edu'], mode='lines', name='Female Secondary Education'))
fig.add_trace(go.Scatter(x=df_clean['country'], y=df_clean['m_secondary_edu'], mode='lines', name='Male Secondary Education'))
fig.update_layout(title='Trend of Female and Male Secondary Education Participation',
                  xaxis_title='Country', yaxis_title='Secondary Education Participation')
st.plotly_chart(fig)

# Keterangan Visualisasi Trend of Female and Male Secondary Education Participation
st.write("Berdasarkan grafik di atas, dapat dilihat bahwa secara garis besar di semua negara, perempuan yang memiliki pendidikan menengah (secondary education) jumlahnya lebih sedikit hingga menyamai jumlah laki-laki yang memiliki pendidikan tersebut. Secondary education disini merujuk pada tingkat pendidikan yang berada di antara pendidikan dasar (misalnya, SD atau MI) dan pendidikan tinggi (seperti perguruan tinggi atau universitas). Biasanya, pendidikan menengah mencakup jenjang pendidikan seperti SMP atau MTs, SMA atau MA, dan sejenisnya")

'\n'
'\n'

# Correlation Heatmap
st.subheader('Correlation Heatmap')
# Human development
mapping_hd = {
    'Low': 0,
    'Medium': 1,
    'High': 2,
    'Very High': 3
}
df_clean['human development'] = df_clean['human development'].map(mapping_hd)

columns_to_exclude = ['hdi rank', 'country', 'gii rank', 'region']  # Kolom yang ingin dikecualikan


# Menghapus kolom yang tidak diinginkan dari DataFrame
corr_matrix = df_clean.drop(columns=columns_to_exclude).corr()

fig = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=list(corr_matrix.columns),
    y=list(corr_matrix.index),
    text=corr_matrix.round(2).values,  # Menambahkan nilai angka ke dalam kotak
    colorscale='RdBu',
    zmin=-1,
    zmax=1,
    colorbar=dict(title='Correlation')
))

fig.update_layout(
    xaxis_tickangle=-55,
    yaxis_tickangle=0,
    width=700,
    height=700,
    title='Correlation Heatmap'
)

fig.update_traces(hovertemplate='Correlation: %{text}')  # Menampilkan angka saat dihover
st.plotly_chart(fig)

# Penjelasan umum
st.write("Berdasarkan heatmap diatas, ada beberapa fitur target yang memiliki korelasi yang tinggi (>0.7) dengan fitur target human development, diantaranya:")

# Poin 1
st.write("1. Fitur-fitur yang memiliki hubungan negatif dengan fitur target yang menunjukkan bahwa apabila fitur target nilainya meningkat maka fitur ini nilainya akan menurun:")
st.write("   - human development dan gii value: -0.86")
st.write("   - human development dan maternal mortality ratio: -0.88")
st.write("   - human development dan adolescent birth rate: -0.79")
st.write("   ***Semakin rendah nilai 3 fitur tersebut (gii value, maternal mortality ratio, adolescent birth rate) maka human development pun akan semakin bagus***")

# Poin 2
st.write("2. Fitur-fitur yang memiliki hubungan positif dengan fitur target, yang mana sifatnya berbanding lurus. Jika nilai fitur target meningkat, maka nilai fitur tersebut juga akan meningkat:")
st.write("   - human development dan f_secondary_edu: 0.84")
st.write("   - human development dan m_secondary_edu: 0.8")



# Data Modeling
# Load the saved model
model = joblib.load('/Users/keiziapurba/xgb_model.pkl')

# Streamlit App
'\n'
'\n'
# Title
st.title('Human Development Category Prediction')

'\n'

# Input form
st.subheader('Input Features')
gii_value = st.number_input('GII Value')
maternal_mortality_ratio = st.number_input('Maternal Mortality Ratio')
adolescent_birth_rate = st.number_input('Adolescent Birth Rate')
share_of_seats_in_parliament = st.number_input('Share of Seats in Parliament')
f_secondary_edu = st.number_input('Female Secondary Education')
m_secondary_edu = st.number_input('Male Secondary Education')
f_labour_force = st.number_input('Female Labour Force')
m_labour_force = st.number_input('Male Labour Force')
region_east_asia_pacific = st.checkbox('Region: East Asia and the Pacific')
region_europe_central_asia = st.checkbox('Region: Europe and Central Asia')
region_latin_america_caribbean = st.checkbox('Region: Latin America and the Caribbean')
region_middle_east_north_africa = st.checkbox('Region: Middle East and North Africa')
region_north_america = st.checkbox('Region: North America')
region_south_asia = st.checkbox('Region: South Asia')
region_sub_saharan_africa = st.checkbox('Region: Sub-Saharan Africa')

# Prepare input data
input_data = {
    'gii value': gii_value,
    'maternal mortality ratio': maternal_mortality_ratio,
    'adolescent birth rate': adolescent_birth_rate,
    'share of seats in parliament': share_of_seats_in_parliament,
    'f_secondary_edu': f_secondary_edu,
    'm_secondary_edu': m_secondary_edu,
    'f_labour_force': f_labour_force,
    'm_labour_force': m_labour_force,
    'region_East Asia and the Pacific': region_east_asia_pacific,
    'region_Europe and Central Asia': region_europe_central_asia,
    'region_Latin America and the Caribbean': region_latin_america_caribbean,
    'region_Middle East and North Africa': region_middle_east_north_africa,
    'region_North America': region_north_america,
    'region_South Asia': region_south_asia,
    'region_Sub-Saharan Africa': region_sub_saharan_africa
}

# Create DataFrame from input data
input_df = pd.DataFrame(input_data, index=[0])

# Make prediction
prediction = model.predict(input_df)

# Get prediction label
prediction_labels = ['Low', 'Medium', 'High', 'Very High']
prediction_label = prediction_labels[prediction[0]]

'\n'

# Display the prediction
st.subheader('Prediction')
st.write('Human Development category:', prediction_label)

'\n'

# About
st.sidebar.subheader('About')
st.sidebar.write('This app is an interactive exploration of the Gender Inequality Index dataset. '
                 'It provides visualizations and insights into various aspects of gender inequality. '
                 'The dataset contains information about different countries and their gender inequality index. '
                 'For more information, please refer to the [Gender Inequality Index](https://hdr.undp.org/data-center/thematic-composite-indices/gender-inequality-index#/indicies/GII) website.')

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
    "Made with ❤️ by Keizia Purba"
    "</div>",
    unsafe_allow_html=True
)

'\n'
'\n'


# Findings
st.subheader('What Can We Do?')
st.write("- Stop stereotipe peran laki-laki dan perempuan")
st.write("- Stop pernikahan anak dan pelecehan seksual")
st.write("- Talk to women and girls")
st.write("- Give proper value to ‘women’s work’")
st.write("- Menghentikan penggunaan bahasa seksis dan diskriminatif")

'\n'
'\n'
'\n'
'\n'
'\n'
'\n'


# Daftar sumber
sources = [
    {
        "name": "Victoria State Government",
        "link": "https://www.vic.gov.au/gender-equality-what-it-and-why-do-we-need-it#"
    },
    {
        "name": "Council of Europe",
        "link": "https://www.coe.int/en/web/gender-matters/gender-equality-and-gender-mainstreaming"
    },
    {
        "name": "United Nations Development Programme (UNDP)",
        "link": "https://hdr.undp.org/data-center/thematic-composite-indices/gender-inequality-index#/indicies/GII"
    },
    {
        "name": "World Health Organization (WHO)",
        "link": "https://www.who.int/data/nutrition/nlis/info/gender-inequality-index-(gii)"
    },
    {
        "name": "The Guardian",
        "link": "https://www.theguardian.com/global-development-professionals-network/2016/mar/14/gender-equality-women-girls-rights-education-empowerment-politics"
    },
    {
        "name": "Government of Newfoundland and Labrador",
        "link": "https://www.gov.nl.ca/vpi/tips-and-tools/tips-for-youth-to-prevent-gender-based-violence-and-inequality/"
    },
    {
        "name": "United Nations Development Programme (UNDP)",
        "link": "https://hdr.undp.org/data-center/documentation-and-downloads"
    }
]


# Menampilkan daftar sumber dengan tulisan kecil
st.markdown("<h3>Sources:</h3>", unsafe_allow_html=True)
for i, source in enumerate(sources):
    st.markdown(
        f"{i+1}. [<span style='font-size:small'>{source['name']}</span>]({source['link']})",
        unsafe_allow_html=True
    )
