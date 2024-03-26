import streamlit as st
import pandas as pd
import os 
import json 

with open("Auth.json","r") as f:
        auth=json.load(f)['auth']
if not auth:
    st.warning("Wrong username/password")
    quit()

def addData(df, column, value, addDF):
    value = value.strip().lower()
    col = df[column].astype(str).str.strip().str.lower()
    filtered_df1 = df[col.astype(str).str.contains(value)]
    filtered_df2 = addDF[col.astype(str).str.contains(value)]
    
    # Check for additional common columns
    common_columns = set(filtered_df1.columns).intersection(filtered_df2.columns)
    if column in common_columns:
        common_columns.remove(column)
    
    # Merge the common columns based on length comparison of unique values
    for common_col in common_columns:
        unique_values_df1 = len(filtered_df1[common_col].dropna().unique())
        unique_values_df2 = len(filtered_df2[common_col].dropna().unique())
        if unique_values_df1 < unique_values_df2:
            filtered_df1 = filtered_df1.drop(columns=[common_col])
        else:
            filtered_df2 = filtered_df2.drop(columns=[common_col])
    
    # Merge the dataframes
    merged_df = pd.merge(filtered_df1, filtered_df2, on=column, how='outer')
    
    return merged_df





folder_path = 'dataset'
folder_path = os.path.abspath(folder_path)
files = os.listdir(folder_path)

l = files
c1, c2 = st.columns(2)
with c1:
    f1 = st.selectbox("Select the first file:", l)
with c2:
    f2 = st.selectbox("Select the second file:", l)

common = []
df1 = pd.read_csv(folder_path+'/'+f1)
df2 = pd.read_csv(folder_path+'/'+f2)
h1 = df1.columns.tolist()
h2 = df2.columns.tolist()
for i in h2:
    vl1 = i.lower().strip()
    for j in h1:
        vl2 = j.lower().strip()
        if vl1 == vl2:
            if df1[i].astype(str).tolist().sort() == df2[j].astype(str).tolist().sort():
                common.append(i)

com = st.selectbox("Select the common column:", common)
if com:
    # Store the result of addData function call
    merged_df = addData(df1, com, '', df2)
    st.write(merged_df)
    fileName=st.text_input("Enter a File name to save:")
    if st.button("Save"):
        merged_df.to_csv(folder_path+"/"+fileName+".csv",index=False    )

else:
    st.write(df1)
