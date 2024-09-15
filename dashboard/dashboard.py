import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import streamlit as st
import pandas as pd

# Load Dataset
@st.cache_data
def load_data():
    bike_data = pd.read_csv("day.csv")
    bike_data.loc[bike_data['holiday'] == 0, 'workingday'] = 1
    bike_data['dteday'] = pd.to_datetime(bike_data['dteday'])
    bike_data['season'] = bike_data['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    bike_data['weathersit'] = bike_data['weathersit'].map({1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain'})
    bike_data['yr'] = bike_data['yr'].map({0:"2011",1:"2012"})
    return bike_data

bike_data = load_data()



# sidebar
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime('2011-01-01').date())
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime('2012-12-31').date())
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# main content
st.title("Bike Sharing Datasets Analysis")
st.write("Tugas Submission Proyek Akhir Dicoding Belajar Analis Data Dengan Python")
col1,col2,col3 = st.columns(3)
with col1:
    st.write("Nama: Fardian Zahri Chaniago")
with col2:
    st.write("Email:fardianlubis@gmail.com")
with col3:
    st.write("ID Dicoding: fardianzahri")
    
st.header("Data Info")
filtered_data = bike_data[(bike_data['dteday'] >= start_date) & (bike_data['dteday'] <= end_date)]
st.write(f"Menampilkan data dari {start_date.date()} hingga {end_date.date()}")
st.write(filtered_data)

#data info
col1,col2 = st.columns(2)
with col1:
    total_registered = bike_data['registered'].sum()
    st.metric(label="Total Registered Users", value=total_registered)
with col2:
    total_casual = bike_data['casual'].sum()
    st.metric(label="Total Casual Users", value=total_casual)


## Peminjaman Sepeda Berdasarkan Waktu Hari
bike_data_by_days = filtered_data.groupby(by="weekday").agg({
    "cnt": "sum",
    "registered": "sum",
    "casual": "sum"
}).reset_index()
bike_data_by_days_melt = pd.melt(bike_data_by_days, id_vars="weekday", value_vars=["registered", "casual"], 
                           var_name="Tipe Pengguna", value_name="Count")

st.header("Peminjaman Sepeda Berdasarkan Hari")
plt.figure(figsize=(10,6))
sns.barplot(x="weekday", y="Count", hue="Tipe Pengguna", data=bike_data_by_days_melt, palette=['blue', 'orange'])
plt.title("Total Peminjaman Sepeda Berdasarkan Hari (Pengguna Terdaftar dan Kasual)")
plt.xlabel("Hari")
plt.ylabel("Jumlah Sepeda Terpinjam")
plt.xticks(ticks=range(7), labels=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], rotation=0)


st.pyplot(plt)



## Peminjaman Sepeda Berdasarkan Waktu Bulan
bike_data_by_month = filtered_data.groupby(by="mnth").agg({
    "registered": "sum",
    "casual": "sum"
}).reset_index()
plt.figure(figsize=(10,10))
MonthLinePlotRegistered = sns.lineplot(x="mnth",y="registered",data=bike_data_by_month)
MonthLinePlotCasual = sns.lineplot(x="mnth",y="casual",data=bike_data_by_month)
plt.title("Total Peminjaman Sepeda Berdasarkan Bulan")
plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'])
plt.xlabel("Bulan")
plt.ylabel("Jumlah Sepeda Terpinjam")
st.pyplot(plt)

## Peminjaman Sepeda Berdasarkan Workingday dan Holiday
st.header("Peminjaman Sepeda Berdasarkan Hari Kerja dan Hari Libur")
bike_data_by_workingdays = filtered_data.groupby(by="workingday").agg({
    "registered": "sum",
    "casual": "sum"
}).reset_index()
bike_data_by_workingdays_melt = pd.melt(bike_data_by_workingdays, id_vars="workingday", value_vars=["registered", "casual"], 
                           var_name="Tipe Pengguna", value_name="Count")
plt.figure(figsize=(8, 6))
bar_plot = sns.barplot(x="workingday", y="Count", data=bike_data_by_workingdays_melt,palette=['blue', 'orange'],hue="Tipe Pengguna")
plt.title('Perbandingan jumlah peminjaman sepeda antara hari kerja dan hari libur')
bar_plot.set_xticklabels(['Holyday', 'Working Day'])
st.pyplot(plt)




## Peminjaman Sepeda Berdasarkan Kondisi Cuaca
st.header("Peminjaman Sepeda Berdasarkan Kondisi Cuaca")
bike_data_by_weathersit = filtered_data.groupby(by="weathersit").agg({
    "registered": "sum",
    "casual": "sum",
    "cnt":"sum"
}).reset_index() 
bike_data_by_weathersit_melt = pd.melt(bike_data_by_weathersit, 
                                       id_vars="weathersit", 
                                       value_vars=["registered", "casual"], 
                                       var_name="Tipe Pengguna", 
                                       value_name="Count")

plt.figure(figsize=(10, 6))
sns.barplot(x="weathersit", y='Count', hue="Tipe Pengguna", data=bike_data_by_weathersit_melt, palette=['blue', 'orange'])
plt.title(f'Peminjaman Sepeda pada Kondisi Cuaca')
plt.xlabel('Cuaca')
plt.ylabel('Jumlah Peminjaman Sepeda')
st.pyplot(plt)





## Peminjaman Sepeda Berdasarkan Kondisi Suhu
st.header("Peminjaman Sepeda Berdasarkan Kondisi Suhu")
temp_bins = [0, 15/41, 25/41, 35/41, 38/41]
temp_labels = ['Cold', 'Mild', 'Warm', "Hot"]
filtered_data['temp_group'] = pd.cut(filtered_data['temp'], bins=temp_bins, labels=temp_labels, right=False)
bike_data_by_temp = filtered_data.groupby(by="temp_group").agg({
    "cnt": "sum",
    "registered": "sum",
    "casual": "sum",
}).reset_index()
bike_data_by_temp_melt = pd.melt(bike_data_by_temp, 
                                 id_vars="temp_group", 
                                 value_vars=["registered", "casual"], 
                                 var_name="Tipe Pengguna", 
                                 value_name="Count")
plt.figure(figsize=(10, 6))
sns.barplot(x="temp_group", y='Count', hue="Tipe Pengguna", data=bike_data_by_temp_melt, palette=['blue', 'orange'])
plt.title('Peminjaman Sepeda Berdasarkan Kondisi Suhu')
plt.xlabel('Suhu')
plt.ylabel('Jumlah Peminjaman Sepeda')
st.pyplot(plt)


# Scatter plot 
cold_data = filtered_data[filtered_data['temp_group'] == 'Cold']
mild_data = filtered_data[filtered_data['temp_group'] == 'Mild']
warm_data = filtered_data[filtered_data['temp_group'] == 'Warm']
hot_data = filtered_data[filtered_data['temp_group'] == 'Hot']

plt.figure(figsize=(12, 8))
plt.scatter(cold_data['temp'], cold_data['cnt'], color='blue', label='Cold', alpha=0.5)
plt.scatter(mild_data['temp'], mild_data['cnt'], color='lightblue', label='Mild', alpha=0.5)
plt.scatter(warm_data['temp'], warm_data['cnt'], color='yellow', label='Warm', alpha=0.5)
plt.scatter(hot_data['temp'], hot_data['cnt'], color='red', label='Hot', alpha=0.5)

plt.title('Peminjaman Sepeda Berdasarkan Suhu')
plt.xlabel('Suhu')
plt.ylabel('Jumlah Peminjaman Sepeda')
plt.legend()
st.pyplot(plt)


