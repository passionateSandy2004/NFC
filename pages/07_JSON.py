import pandas as pd 
import streamlit as st 
import os 
import json 

with open("Auth.json","r") as f:
        auth=json.load(f)['auth']
if not auth:
    st.warning("Wrong username/password")
    quit()

folder_path='dataset'
folder_path=os.path.abspath(folder_path)
files = os.listdir(folder_path)

table=st.selectbox("Select a file:",files)
df=pd.read_csv(folder_path+'/'+table)
records=st.checkbox('Make records into objects')
if records:
    json=df.to_json(orient='records')
else:
    json=df.to_json()

st.write(json)

st.download_button('Download',json,file_name=table+'_.json')