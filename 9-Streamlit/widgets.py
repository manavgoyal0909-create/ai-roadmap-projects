import streamlit as st
import pandas as pd

st.title("Streamlit Text Input")

name = st.text_input("Enter your name:")
age = st.slider("Select your age:",0,100,18)
st.write(f"Your age is {age}.")

options= ["Python","Java","C++","Javascript"]
choice= st.selectbox("Choose your favoruite language:", options)
st.write(f"You selected {choice}.")
if name:
    st.write(f"Hello, {name}")
    
data = {
    "Name": ["John","Thomas","Ava","Christian"],
    "Age": [33,23,35,45],
    "City": ["Los Angelas","New York","Berlin","h\Houstan"]
}  

df=pd.DataFrame(data)
st.write(df)    