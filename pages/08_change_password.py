import streamlit as st
import json  
import os 

with open("Auth.json","r") as f:
        auth=json.load(f)['auth']
if not auth:
    st.warning("Wrong username/password")
    quit()
authen=st.text_input("Enter the authen key")
new_user=st.text_input("Enter the new user name")
new_pass=st.text_input("Enter the new password")
if authen=="santhosh":
    if st.button("Change"):
        new={"user":new_user,"password":new_pass}
        with open("passuser.json","w") as f:
            json.dump(new,f,indent=4)
