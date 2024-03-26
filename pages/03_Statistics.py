import streamlit as st 
import os 
import pandas as pd 
import matplotlib.pyplot as plt
import json 

with open("Auth.json","r") as f:
        auth=json.load(f)['auth']
if not auth:
    st.warning("Wrong username/password")
    quit()


folder_path='dataset'
folder_path=os.path.abspath(folder_path)
files = os.listdir(folder_path)

def pie_chart(i):
    same=False
    names_column=st.selectbox("Select An label",columns,key=i+'names')
    values_column=st.selectbox("Select An value",columns,key=i+'values')
    if names_column == values_column:
        same=True  
    label_list=list(df[names_column])
    values_list=list(df[values_column])
    data={}
    for i in range(len(label_list)):
        if label_list[i] not in data:
            if same:
                data[label_list[i]]=1
            else:
                data[label_list[i]]=values_list[i]
        else:
            if same:
                data[label_list[i]]+=1
            else:
                data[label_list[i]]+=values_list[i]
    names=list(data.keys())
    values=list(data.values())
    fig, ax = plt.subplots()
    try:
        ax.pie(values, labels=names, autopct='%1.1f%%', startangle=90)
    except ValueError:
        st.warning('values column should contain only numbers')
    st.pyplot(fig)
def bar_chart(x,y):
    new_df=df[[x,y]]
    st.bar_chart(new_df.set_index(x))

files=st.multiselect("Select the table(s):",files)
chart=st.selectbox("Select a graph type:",["Pie chart","Bar chart"])

for i in files:
    df=pd.read_csv("dataset/"+i)
    columns = df.columns.tolist()
    st.subheader(i)
    st.write(df)
    if chart =='Pie chart':
        pie_chart(i)
    if chart=="Bar chart":
        x=st.selectbox("Select a x-axis: ",columns,key=i+'x')
        y=st.selectbox("Select a y-axis:",columns,key=i+'y')
        try:
            bar_chart(x,y)
        except ValueError:
            st.write("Give different axis values")
    st.write('---')
