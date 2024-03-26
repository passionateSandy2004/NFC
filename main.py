import streamlit as st 
import os 
import pandas as pd 


current_directory = os.path.dirname(os.path.realpath(__file__))

# Path to the CSV file in the same directory as the script
csv_file_path = os.path.join(current_directory, 'check_in_data.csv')
table=pd.read_csv(csv_file_path)
for i in table["UID"]:
    st.success(i) 