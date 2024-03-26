import streamlit as st 
import pandas as pd 
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
def clear_folder():
    # Iterate over each file and delete it
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)

upload=st.file_uploader("Uplaod your csv file",accept_multiple_files=True)
dataframes=[]
if files:
    st.write('**You Have already uploaded files**')
   
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        st.write(file_name)
        st.write(pd.read_csv(file_path))
        dataframes.append(pd.read_csv(file_path))
        remove=st.button('Remove',key=file_name+'remove')
        if remove:
            os.remove(file_path)
        st.write("---")



names=[]
merge=st.checkbox("Merge them")
for i in upload:
    file_extension = i.name.split('.')
    if file_extension[-1].lower() == 'xlsx':
        df=pd.read_excel(i)
    elif file_extension[-1].lower() == 'csv':
        df=pd.read_csv(i)
    dataframes.append(df)
    names.append(file_extension[0])
    st.write(file_extension[0])
    st.write(df)
if merge:
    merged_df = pd.concat(dataframes, ignore_index=True)
    st.write(merged_df)
sett=st.button("Set")
if sett:
    
    if merge:
        merged_df.to_csv(f'{folder_path}/merged.csv',index=False)
    else:
        n=0
        for i in dataframes:
            i.to_csv(f'{folder_path}/{names[n]}.csv',index=False)
            n+=1