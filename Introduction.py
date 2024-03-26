import pages

import streamlit as st
import json  
import os 
import pandas as pd 

st.set_page_config(page_title='NFC Attendence system')
authdata = {"auth": False}
username = st.text_input("Enter the username:")
pw = st.text_input("Enter the password:")
with open("passuser.json") as file1:
    data=json.load(file1)

if username == data['user'] and pw == data['password']:
    authdata = {"auth": True}

if st.button("Login"):
    with open("Auth.json", "w") as f:
        json.dump(authdata, f, indent=4)

if st.button("Log out"):
    authdata = {"auth": False}
    with open("Auth.json", "w") as f:
        json.dump(authdata, f, indent=4)
st.write('---')

def main():
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Path to the CSV file in the same directory as the script
    csv_file_path = os.path.join(current_directory, 'dataset/check_in_data.csv')
    table=pd.read_csv(csv_file_path)
    for i in table["UID"]:
        st.success(i) 

if __name__ == "__main__":
    main()
