import streamlit as st 
import gspread
from google.oauth2.service_account import Credentials
import json

with open("Auth.json","r") as f:
        auth=json.load(f)['auth']
if not auth:
    st.warning("Wrong username/password")
    quit()
crd=st.file_uploader("Enter  the api key file:",type="json")

url=st.text_input("Enter the url")
try:
    with open("api.json") as f: 
        mail=json.load(f)['client_email']
    st.write(mail)
    st.write("Share the sheet with this client id")
except:
    st.warning("No key file is been added") 
if st.button('Connect'):
    if crd:
        key=crd.read()
        key=key.decode("utf-8")
        json_data = json.loads(key)
        with open('api.json','w') as j:
            json.dump(json_data, j, indent=4)
    url_data={"url":url}
    with open('url.json','w') as j:
        json.dump(url_data, j, indent=4)

