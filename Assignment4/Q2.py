
# 2. For unauthenticated users, show menu (in sidebar) as Home, Login,
# Register. Keep login details in users.csv. For authenticated users, show
# menu explore CSV, See history, Logout. Maintain CSV upload history
# (userid, csv file name, date-time of upload) into userfiles.csv. Use pandas
# for reading/writing data CSVs.

import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="CSV App")


USERS_FILE = "users.csv"
HISTORY_FILE = "userfiles.csv"

if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["userid", "password"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=["userid", "filename", "datetime"]).to_csv(HISTORY_FILE, index=False)


if "user" not in st.session_state:
    st.session_state.user = None


def register_user(userid, password):
    df = pd.read_csv(USERS_FILE)
    if userid in df["userid"].values:
        return False
    df.loc[len(df)] = [userid, password]
    df.to_csv(USERS_FILE, index=False)
    return True

def authenticate(userid, password):
    df = pd.read_csv(USERS_FILE)
    return not df[(df.userid == userid) & (df.password == password)].empty

def save_upload_history(userid, filename):
    df = pd.read_csv(HISTORY_FILE)
    df.loc[len(df)] = [userid, filename, datetime.now()]
    df.to_csv(HISTORY_FILE, index=False)


st.sidebar.title("Menu")

if st.session_state.user is None:
    menu = st.sidebar.radio("Select", ["Home", "Login", "Register"])
else:
    menu = st.sidebar.radio("Select", ["Explore CSV", "See History", "Logout"])


if menu == "Home":
    st.title("Home")
    st.write("Welcome  ! Please login or register.")

elif menu == "Register":
    st.title(" Register")
    userid = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if register_user(userid, password):
            st.success("Registration successful!")
        else:
            st.error("User already exists")

elif menu == "Login":
    st.title("  Login")
    userid = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(userid, password):
            st.session_state.user = userid
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

elif menu == "Explore CSV":
    st.title(" Upload & Explore CSV")

    file = st.file_uploader("Upload CSV file", type="csv")

    if file:
        df = pd.read_csv(file)
        st.dataframe(df)

        save_upload_history(st.session_state.user,file.name)
        st.success("File uploaded and history saved")

elif menu == "See History":
    st.title(" Upload History")

    df = pd.read_csv(HISTORY_FILE)
    user_history = df[df.userid == st.session_state.user]

    if user_history.empty:
        st.info("No uploads by user")
    else:
        st.dataframe(user_history)

elif menu == "Logout":
    st.session_state.user = None
    st.success("Logged out successfully")
    st.rerun()
