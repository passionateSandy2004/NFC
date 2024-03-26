import gspread
from google.oauth2.service_account import Credentials
import streamlit as st 
import pandas as pd 
import json  
import os 

with open("Auth.json","r") as f:
        auth=json.load(f)['auth']
if not auth:
    st.warning("Wrong username/password")
    quit()

folder_path='dataset'
folder_path=os.path.abspath(folder_path)
files = os.listdir(folder_path)


scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("api.json", scopes=scopes)
client = gspread.authorize(creds)


with open("url.json") as f:
    url=json.load(f)['url']
if url:
    h=url
    code=h[h.index("/d/")+3:]
    code=code[:code.index("/")]
    sheet_id = code
    try:
        workbook = client.open_by_key(sheet_id)
    except: 
        st.info("No internet connection")
        quit()
    cretORedit=st.selectbox("Select type of sheet",["Existing","New"])
    if cretORedit=="Existing":
        worksheet_list = map(lambda x: x.title, workbook.worksheets())
        sheets=list(worksheet_list)
        sheet=st.selectbox("Enter the sheet:",sheets)

        worksheet = workbook.worksheet(sheet)
        def getData():
            global worksheet_data,df
            worksheet_data = worksheet.get_all_values()
            df = pd.DataFrame(worksheet_data[1:], columns=worksheet_data[0])
            st.write(df)
        getData()
        check=False
        with open("names.json") as f:
            try:
                checkdf=json.load(f)[sheet]
                checkdf=pd.read_csv(checkdf)
                checkdf = checkdf.astype(str)
                check=True
            except:
                st.info("The table is not already saved")
            

        issame=True
        if check:
            issame=df.equals(checkdf)
            
        
        name=st.text_input("Save the file with name:")
        if st.button("Save"):
            df.to_csv("dataset/"+name+".csv", index=False)
            with open("names.json","w") as f: 
                names={sheet:"dataset/"+name+".csv"}
                json.dump(names,f)

        if not issame:
            if st.button("Update the sheet"):
                data = [checkdf.columns.tolist()] + checkdf.values.tolist()
                worksheet.update('A1', data)
                getData()
                st.write("Sheet is updated")

    elif cretORedit=="New":
        file=st.selectbox("Select a file:",files,key='choice')
        sheetdf=pd.read_csv(folder_path+'/'+file)
        sheet_name=st.text_input("Enter the name of the sheet")
        num_rows, num_cols = sheetdf.shape
        new_data = [sheetdf.columns.tolist()] + sheetdf.values.tolist()

        # Update the range of cells with the data
        if st.button("Add sheet"):
            worksheet = workbook.add_worksheet(sheet_name,rows=100,cols=100)
            worksheet.update('A1', new_data)
            st.success("Written!")
        
        

else:
    st.warning('No url information')