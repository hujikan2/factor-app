import tensorflow as tf
import streamlit as st
import numpy as np
import requests
import string 
import json
from streamlit_lottie import st_lottie
import re
import string
import nltk
from nltk.corpus import stopwords

    
# Load model from directory
model_loaded = tf.keras.models.load_model('my_model')

# stopwords
try:
  stop_words = set(stopwords.words("english"))
except:
  nltk.download('stopwords')
  stop_words = set(stopwords.words("english"))

# remove the stopwords and single-character words
def remove_sw_and_sc(text):
    final_text = []
    for i in text.split():
        if i.strip() not in stop_words and len(i) > 1:
            final_text.append(i.strip())
    return " ".join(final_text)

# Create function for preprocessing text
def clean_text(text):
    text = text.lower() # Convert to lower case
    text = re.sub('\[.*\]', '', text) # Remove text in square brackets
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text) # remove punctuation
    text = re.sub('\w*\d\w*', '', text) # remove words containing numbers
    text = re.sub('https\S+|\S+\.com\S+|bit.ly\S+', '', text) # remove url characters
    text = re.sub(r'\@\S+', '', text) # remove mention
    text = re.sub('[‘’“”…]', '', text) # remove other punctuation
    text = remove_sw_and_sc(text)
    return text

# Set pages title
st.set_page_config(page_title="FACTOR APP", page_icon=":bookmark_tabs:", layout="wide", initial_sidebar_state='auto')

# function for load lottie
def load_lottie(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Side Bar 
st.sidebar.header("Navigation Menu")
menu = st.sidebar.radio("Select Navigation", ['Home', "Detector News"])

if menu == "Home":
    left_column, right_column = st.columns(2)
    lottie_left = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_dyimsq5i.json")
    with left_column:
        st_lottie(lottie_left, speed=1, reverse=False, loop=True, quality="low", height=450, width=400, key=None)
    with right_column:
        st.title("Welcome to FACTOR APP")
        st.write("Fake News Detector Aplication")
        st.write("Berita palsu, salah satu masalah saat ini karena memiliki potensi untuk membentuk opini dan memengaruhi keputusan.")
        st.write("FACTOR APP memiliki kemampuan untuk mendeteksi berita palsu hanya dengan sekali klik dengan akurasi lebih dari 98%. Jika ingin menggunakan aplikasi kami, silakan pilih Detector News pada navigation bar di sebelah kanan.") 
        
    st.subheader("Beberapa hal yang dapat dilakukan untuk mengenali berita hoaks.")

    col1, col2, col3 = st.columns(3)
    lottie_col1 = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_4lnybhkt.json")
    with col1:
        st_lottie(lottie_col1, speed=1, reverse=False, loop=True, quality="low", height=350, width=320)
        st.subheader("Kredibilitas Narasumber dalam Berita")
        st.write("* Dapat melakukan pencarian nama narasumber atau reporter pada berita dan melihat apakah nama-nama tersebut memiliki rekam jejak yang baik dalam pemberitaan.")
    lottie_col2 = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_cn2e3rvz.json")
    with col2:
        st_lottie(lottie_col2, speed=1, reverse=False, loop=True, quality="low", height=350, width=320) 
        st.subheader("Gambar Berita")
        st.write("Cara efektif untuk mengidentifikasi berita hoaks dengan mengecek gambar/foto yang digunakan pada berita. Lakukan pencarian gambar/foto yang dicantumkan pada berita dengan google images. Apakah gambar/foto merupakan foto lama dan berasal dari kejadian di tempat lain, tetapi digunakan kembali oleh berita hoaks dengan memanipulasi keterangan gambar/foto. Hal yang bisa dilakukan juga ialah mencari gambar/foto yang terkait dengan topik berita.")
    lottie_col3 = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_tnrzlN.json")
    with col3:
        st_lottie(lottie_col3, speed=1, reverse=False, loop=True, quality="low", height=350, width=320 )   
        st.subheader("Mengenali ciri-ciri berita hoaks.")
        st.write("* Judul dan pengantar berita terkesan provokatif dan tidak sesuai dengan isi berita.")
        st.write("* Argumen dan data yang disampaikan sangat teknis agar terlihat ilmiah dan dipercaya.")
        st.write("* Berita ditulis dengan menyembunyikan fakta dan data serta memelintir pernyataan narasumbernya.")
        st.write("* Sebagian besar berita ditulis oleh media abal-abal, di mana alamat media dan penanggung jawab tidak jelas.")

if menu == 'Detector News':
    st.title("Fake News Detector :newspaper:")
    st.write("Aplikasi ini mampu mendeteksi berita palsu dengan tingkat akurasi ketepatan sekitar 98%.")
    st.markdown("--------------------------------")
    st.write("")
    judul = st.text_input("Masukkan judul berita disini 👇")
    isi_berita = st.text_area("Masukkan isi berita di sini 👇 (min 50 kata)")

    # Predict news
    sample_news = [judul + " " + isi_berita]

    import time
    if st.button("Detection"):
        time.sleep(2)
        for ind, sample in enumerate(sample_news):
            sample = clean_text(sample)

            hasil = model_loaded.predict([sample])
            if np.round(hasil) == 1:
                st.warning(f"Hati-hati, berita dideteksi sebagai berita palsu.")
                st.write("")
                st.subheader("Berikut Rekomendasi Portal Berita")
                st.write("10 Portal berita yang dapat dipercaya berdasarkan jumlah pelanggan berbayar terbanyak.")
                st.write("Sumber: databooks 2020")
                st.image('images/portal-berita.png')
            else:
                st.success(f"Berita di deteksi sebagai berita terpercaya")


