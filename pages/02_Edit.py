import streamlit as st
import pandas as pd
import os 
import json 

with open("Auth.json","r") as f:
        auth=json.load(f)['auth']
if not auth:
    st.warning("Wrong username/password")
    quit()
    
# File uploader
folder_path='dataset'
folder_path=os.path.abspath(folder_path)
files = os.listdir(folder_path)
file=st.selectbox("Select a file:",files,key='choice')


# Function to display DataFrame
def display_dataframe(df):
    st.write(df)
    st.write(f"{len(df)} rows")

# Function to filter DataFrame
def filter_dataframe(df, column, value):
    value = value.strip().lower()
    col = df[column].astype(str).str.strip().str.lower()
    filtered_df = df[col.astype(str).str.contains(value)]
    return filtered_df

# Function to sort DataFrame
def sort_dataframe(df, column, ascending=True):
    sorted_df = df.sort_values(by=column, ascending=ascending)
    return sorted_df

# Function to add column to DataFrame based on conditions
def add_column_with_conditions(df, column_name, value, conditions,similar):
    if conditions:
        for index, row in df.iterrows():
            add_value = False
            for col, cond in conditions.items():
                if similar and  str(cond.strip().lower()) in str(row[col]).strip().lower():
                    add_value = True
                    break
                elif str(row[col]).strip().lower() == cond.strip().lower():  # Convert column value to string for comparison
                    add_value = True
                    break
            if add_value:
                df.at[index, column_name] = value
    else:
        df[column_name] = value
    return df

# Function to remove row from DataFrame
def remove_row(df, index):
    df = df.drop(index=index, axis=0)
    return df

# Function to remove column from DataFrame
def remove_column(df, column_name):
    df = df.drop(column_name, axis=1)
    return df

def main():
    if file is not None:
        df=pd.read_csv(folder_path+'/'+file)

        # Display DataFrame
        st.subheader("Original Data")
        display_dataframe(df)

        # Operations
        operation = st.sidebar.selectbox("Select Operation", ["Filter", "Sort", "Operation on Column","Add Record", "Remove Row", "Remove Column"])

        if operation == "Filter":
            column = st.sidebar.selectbox("Select Column to Filter", df.columns)
            value = st.sidebar.text_input(f"Enter Value to Filter in {column}")
            if st.sidebar.button("Filter"):
                filtered_df = filter_dataframe(df, column, value)
                st.subheader("Filtered Data")
                filtered_df.to_csv('update.csv', index=False)
                display_dataframe(filtered_df)
                

        elif operation == "Sort":
            column = st.sidebar.selectbox("Select Column to Sort", df.columns)
            ascending = st.sidebar.checkbox("Ascending", True)
            if st.sidebar.button("Sort"):
                sorted_df = sort_dataframe(df, column, ascending)
                st.subheader("Sorted Data")
                sorted_df.to_csv('update.csv', index=False)
                display_dataframe(sorted_df)
            

        elif operation == "Operation on Column":
            st.sidebar.subheader("Edit the existing or add new column name:")
            column_name = st.sidebar.text_input("Enter Column Name")
            value = st.sidebar.text_input("Enter Value for the New Column")
            conditions = {}
            
            st.subheader("Specify Conditions (optional)")
            similar=st.checkbox('Edit on similar datas',key='similar')
            for col in df.columns:
                condition_value = st.text_input(f"Enter condition for column '{col}'", key=f"condition_{col}")
                
                if condition_value:
                    conditions[col] = condition_value
            if st.sidebar.button("Add Column"):
                df = add_column_with_conditions(df, column_name, value, conditions,similar)
                st.subheader("Updated Data")
                display_dataframe(df)
                df.to_csv('update.csv', index=False)
                

        elif operation == "Remove Row":
            index = st.sidebar.number_input("Enter Row Index to Remove", min_value=0, max_value=len(df)-1)
            if st.sidebar.button("Remove Row"):
                df = remove_row(df, index)
                st.subheader("Updated Data")
                display_dataframe(df)
                df.to_csv('update.csv', index=False)

        elif operation == "Remove Column":
            column_name = st.sidebar.selectbox("Select Column to Remove", df.columns)
            if st.sidebar.button("Remove Column"):
                df = remove_column(df, column_name)
                st.subheader("Updated Data")
                display_dataframe(df)
                df.to_csv('update.csv', index=False)

        elif operation == "Add Record":
            st.subheader("Add New Record")
            new_record = {}
            for col in df.columns:
                new_value = st.text_input(f"Enter value for '{col}'", key=f"new_record_{col}")
                new_record[col] = new_value
            if st.button("Add Record"):
                df = df.append(new_record, ignore_index=True)
                st.subheader("Updated Data")
                display_dataframe(df)
                df.to_csv('update.csv', index=False)
        st.write("---")
        if st.button('Save changes'):
            r=pd.read_csv('update.csv')
            st.write(r)
            r.to_csv(folder_path+'/'+file,index=False)
        st.write("---")
        path=st.text_input("Enter the name of the new file")
        if st.button("Save as new table"):
            r=pd.read_csv('update.csv')
            st.write(r)
            r.to_csv(folder_path+'/'+path+".csv",index=False)



if __name__ == "__main__":
    main()
