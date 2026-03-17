import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Load Test Dashboard", layout="wide")
plt.style.use("seaborn-v0_8-whitegrid")

# lets user upload multiple CSVs to compare different test runs
uploaded_files= st.file_uploader("Upload your CSV file", type="csv", accept_multiple_files=True)

if len(uploaded_files) > 0:
    st.title("Locust Load Test Dashboard")
    st.caption("Compare performance metrics across load test runs. Powered by Locust and Streamlit")

    # reads the first file to get endpoint names for the dropdown
    df = pd.read_csv(uploaded_files[0])
    endpoint = st.selectbox("Select endpoint", options=df["Name"].unique(), key="selected_endpoint")
    df = df[df["Name"] == endpoint]

    # summary metrics across the top - uses first file only
    Avg_Resp, Total_Request, Failure_Rate = st.columns(3)
    Avg_Resp.metric(label="Total Average Response Time", value=f"{df['Total Average Response Time'].mean():.2f} ms")
    Total_Request.metric(label="Total Request Count", value=f"{df['Total Request Count'].sum()}")
    Failure_Rate.metric(label="Failure Rate", value=f"{df['Total Failure Count'].sum() / df['Total Request Count'].sum() * 100:.2f}%")

    # charts side by side - each loop reads all files and overlays them
    left, right = st.columns(2)
    with left:
        fig1, ax1 = plt.subplots()
        for file in uploaded_files:
            file.seek(0)  # rewinds so we can read the file again
            df = pd.read_csv(file)
            df = df[df["Name"] == endpoint]
            # converts unix timestamp to elapsed seconds so different runs line up
            df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")
            df["Elapsed"] = (df["Timestamp"] - df["Timestamp"].iloc[0]).dt.total_seconds()
            
            ax1.plot(df["Elapsed"], df["Requests/s"], label=file.name)
        ax1.set_title("Requests per Second")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Requests/s")
        ax1.legend()
        st.pyplot(fig1)

    with right:
        fig2, ax2 = plt.subplots()
        for file in uploaded_files:
            file.seek(0)
            df = pd.read_csv(file)
            df = df[df["Name"] == endpoint]
            df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")
            df["Elapsed"] = (df["Timestamp"] - df["Timestamp"].iloc[0]).dt.total_seconds()
            ax2.plot(df["Elapsed"], df["Total Average Response Time"], label=file.name)
        ax2.set_title("Average Response Time")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Response Time (ms)")
        ax2.legend()
        st.pyplot(fig2)

else:
    st.warning("Please upload a CSV file to see the dashboard.")