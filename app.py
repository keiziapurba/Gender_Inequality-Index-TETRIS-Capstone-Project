import streamlit as st
import datetime
#from lorem_text import lorem

st.set_page_config(
    page_title = 'Mari Belajar Streamlit',
    layout = 'wide'
)

st.write("Hello World!")


"Welcome babes"

"_Ini hw2_"

"**hw3**"

st.title("Ini judul")

st.header("Ini header")

st.caption("ini caption")

st.code("import gradio as gr")

st.code('''
import pandas as pd
import streamlit as st #ini untuk memanggil package streamlit
''')
        
#latex
st.latex("ax^2 + bx + c = 0")

#WIDGET > input elements

# 1. tombol
tombol = st.button("click this!")
tombol

cb = st.checkbox("tick if agree")
if cb:
    st.write("you agree")
else:
    st.write("Let's learn!")


# memilih salah satu opsi dari sekian opsi
 #radio button
fav = st.radio(
    "Your fav, chose",
    ['aple', 'avo', 'Mango']
)

fav

food = st.selectbox(
    "Choose your food",
    ['Tacos with guac', 'honey chicken breast', 'spinach']
)

food


bag = st.multiselect(
    "Choose your item",
    ['sweatpants', 'hoodie', 'cargo pants', 'blade']
)

bag

st.write(type(bag))


parameter_alpha = st.slider(
    "Insert alpha value",
    min_value = 0.0,
    max_value = 1.0,
    step = 0.1
)
parameter_alpha

size = st.select_slider(
    "Ukuran baju",
    ['XS', 'S', 'M', 'L', 'XL', 'XXL']
)

size

kode_pos = st.number_input(
    "Input your number",
    min_value = 0,
    max_value = 9999999999,
    step = 1
)

kode_pos

nama = st.text_input("Write your name")
nama

komen = st.text_area("Comment here")

komen

date = st.date_input(
    "Birth of Date",
    min_value = datetime.date(1999,1,1)
)
date

time = st.time_input('Enter time')

color = st.color_picker("Choose color")
color


#Masukkan image, video, dan suara


#container and layouting

#kolom
col1, col2, col3 = st.columns(3)

with col1:
    bod = st.date_input("Your Birth of Date")

with col2:
    so = st.date_input("Your S/O Birth of Date") 

with col3:
    anv = st.date_input("Y'all Anniversary")

st.button("Hitung") 


# with st.sidebar:
 #   st.title("Titanic model explorer")
  #  name = st.text_input("Enter your name luv")

   # with st.expander("Lorem ipsum"):
  #      st.write(lorem.paragraphs(1))


tab1, tab2, tab3 = st.tabs(['Tab1', 'Tab2', 'Tab3'])

#with tab1:
 #   st.write(lorem.paragraphs(1))

#with tab2:
 #   st.write(lorem.paragraphs(1))

#with tab3:
 #   st.write(lorem.paragraphs(1))

#with st.container():
 #   st.write("inni teks di dalam kontainer")

