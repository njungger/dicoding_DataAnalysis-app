import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# '''
# === ekspor data ===
# '''
hour_df = pd.read_csv('hour_data.csv')
day_df = pd.read_csv('day_data.csv')
# merubah tipedata dari kolom dteday, season, weathersit, dan weekday
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# ''' 
# === reset index ===
# '''
hour_df.reset_index(inplace=True)
day_df.reset_index(inplace=True)

# '''
# === function ===
# '''
# function total harian
# def create_daily_sharing_df(df):
#     daily_sharing_df = df.resample(rule='D', on='dteday').agg({
#         "instant": "nunique",
#         "cnt": "sum"
#     })
#     daily_sharing_df = daily_sharing_df.reset_index()
#     daily_sharing_df.rename(columns={
#         "instant": "day_count",
#         "cnt": "sharing_sum"
#     }, inplace=True)

#     return daily_sharing_df

# function untuk filter by (day_df)
def create_byseason_df(df):
    byseason_df = df.groupby(by="season").agg({
        "cnt": "mean"
    })
    byseason_df = byseason_df.reset_index()
    byseason_df.rename(columns={
        "cnt": "sharing_sum"
    }, inplace=True)

    return byseason_df

def create_byholiday_df(df):
    byholiday_df = df.groupby(by="holiday").agg({
        "cnt": "mean"
    })
    byholiday_df = byholiday_df.reset_index()
    byholiday_df.rename(columns={
        "cnt": "sharing_sum"
    }, inplace=True)

    return byholiday_df

def create_byweathersit_df(df):
    byweathersit_df = df.groupby(by="weathersit").agg({
        "cnt": "mean"
    })
    byweathersit_df = byweathersit_df.reset_index()
    byweathersit_df.rename(columns={
        "cnt": "sharing_sum"
    }, inplace=True)

    return byweathersit_df

def create_byworkingday_df(df):
    byworkingday_df = df.groupby(by="workingday").agg({
        "cnt": "mean"
    })
    byworkingday_df = byworkingday_df.reset_index()
    byworkingday_df.rename(columns={
        "cnt": "sharing_sum"
    }, inplace=True)

    return byworkingday_df

def create_byweekday_df(df):
    byweekday_df = df.groupby(by="weekday").agg({
        "cnt": "mean"
    })
    byweekday_df = byweekday_df.reset_index()
    byweekday_df.rename(columns={
        "cnt": "sharing_sum"
    }, inplace=True)

    return byweekday_df

# function filter untuk by (hour_df)
def create_byhr_df(df):
    byhr_df = df.groupby(by="hr").agg({
        "cnt": "mean"
    })
    byhr_df = byhr_df.reset_index()
    byhr_df.rename(columns={
        "cnt": "sharing_sum"
    }, inplace=True)

    return byhr_df

# '''
# === filter data dan membuat main data
# '''
# filter tanggal
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# main dataframe
daymain_df = day_df[(day_df["dteday"] >= str(start_date)) &
                (day_df["dteday"] <= str(end_date))]
hourmain_df = hour_df[(hour_df["dteday"] >= str(start_date)) &
                (hour_df["dteday"] <= str(end_date))]

# menggunakan semua function
# daily_sharing_df = create_daily_sharing_df(daymain_df)
byseason_df = create_byseason_df(daymain_df)
byholiday_df = create_byholiday_df(daymain_df)
byweathersit_df = create_byweathersit_df(daymain_df)
byworkingday_df = create_byworkingday_df(daymain_df)
byweekday_df = create_byweekday_df(daymain_df)
byhr_df = create_byhr_df(hour_df)

# '''
# === elemen streamlit ===
# '''
st.header('zuhair_abid :sparkles:')

# visualisasi daily sharing
st.subheader("Bike Sharing Harian")
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daymain_df["dteday"],
    daymain_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_title("Number of Customer by date", loc="center", fontsize=30)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# fig, ax = plt.subplots(figsize=(20, 10))
# colors = ["#90CAF9"]
# sns.barplot(
#     x="dteday", 
#     y="cnt",
#     data=daymain_df[['dteday','cnt']],
#     palette=colors,
#     ax=ax
# )
# ax.set_title("Number of Customer by date", loc="center", fontsize=30)
# ax.set_ylabel(None)
# ax.set_xlabel(None)
# ax.tick_params(axis='y', labelsize=20)
# ax.tick_params(axis='x', labelsize=20)
# st.pyplot(fig)

# visualisasi byseason
st.subheader("Bike Sharing Berdasarkan Season")
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
byseason_df['season'] = byseason_df['season'].astype(str)
sns.barplot(
    x="season", 
    y="sharing_sum",
    data=byseason_df.sort_values(by="sharing_sum", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Mean Bike Sharing by Season", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

# visualisasi byholiday
st.subheader("Bike Sharing Holiday")
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3"]
byholiday_df['holiday'] = byholiday_df['holiday'].astype(str)
sns.barplot(
    x="holiday", 
    y="sharing_sum",
    data=byholiday_df.sort_values(by="sharing_sum", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Mean Bike Sharing by holiday", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

# visualisasi byworkingday
st.subheader("Bike Sharing Berdasarkan Workingday")
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3"]
byworkingday_df['workingday'] = byworkingday_df['workingday'].astype(str)
sns.barplot(
    x="workingday", 
    y="sharing_sum",
    data=byworkingday_df.sort_values(by="sharing_sum", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Mean Bike Sharing by workingday", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

# visualisasi byweathersit
st.subheader("Bike Sharing Berdasarkan Weathersit")
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3"]
byweathersit_df['weathersit'] = byweathersit_df['weathersit'].astype(str)
sns.barplot(
    x="weathersit", 
    y="sharing_sum",
    data=byweathersit_df.sort_values(by="sharing_sum", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Mean Bike Sharing by weathersit", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

# visuallisai byweekday
st.subheader("Bike Sharing Berdasarkan Hari")
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="weekday", 
    y="sharing_sum",
    data=byweekday_df.sort_values(by="sharing_sum", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by weekday", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

# visualisasi byhr
st.subheader("Bike Sharing Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(20, 10))
byhr_df['hr'] = byhr_df['hr'].astype(str)
colors = ["#90CAF9"]
sns.barplot(
    x="hr", 
    y="sharing_sum",
    data=byhr_df.sort_values(by="sharing_sum", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Mean Bike Sharing by Hour", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)