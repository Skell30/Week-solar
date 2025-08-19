import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Solar Data Dashboard", layout="wide")

# Sidebar
st.sidebar.title("🌍 Solar Data Dashboard")
st.sidebar.write("Compare solar potential across countries")

# Country selection
countries = ["Benin", "Sierra Leone", "Togo"]
selected_country = st.sidebar.selectbox("Select a country", countries)

# Load cleaned data
@st.cache_data
def load_data(country):
    path_map = {
        "Benin": r"C:\Users\pc\Week-solar\data\benin_clean.csv",
        "Sierra Leone": r"C:\Users\pc\Week-solar\data\sierra_leone.csv",
        "Togo": r"C:\Users\pc\Week-solar\data\togo_clean.csv"
    }
    return pd.read_csv(path_map[country], parse_dates=["Timestamp"])

df = load_data(selected_country)

# Show summary
st.subheader(f"📊 Summary Statistics - {selected_country}")
st.write(df[["GHI","DNI","DHI","Tamb","RH"]].describe())

# Plot distribution
st.subheader("☀️ Solar Radiation Distribution")
fig, ax = plt.subplots()
sns.histplot(df["GHI"], bins=50, kde=True, ax=ax)
ax.set_title(f"GHI Distribution - {selected_country}")
st.pyplot(fig)

# Time series
st.subheader("📈 Time Series of GHI")
fig, ax = plt.subplots(figsize=(12,4))
ax.plot(df["Timestamp"], df["GHI"], label="GHI", color="orange")
ax.set_xlabel("Time")
ax.set_ylabel("GHI (W/m²)")
ax.legend()
st.pyplot(fig)

# Cross-country comparison (optional)
if st.sidebar.checkbox("Compare Countries"):
    benin = pd.read_csv(r"C:\Users\pc\Week-solar\data\benin_clean.csv")
    sierra = pd.read_csv(r"C:\Users\pc\Week-solar\data\sierra_leone.csv")
    togo = pd.read_csv(r"C:\Users\pc\Week-solar\data\togo_clean.csv")

    benin["Country"] = "Benin"
    sierra["Country"] = "Sierra Leone"
    togo["Country"] = "Togo"

    df_all = pd.concat([benin, sierra, togo])

    st.subheader("🌍 Cross-Country Comparison")
    fig, ax = plt.subplots()
    sns.boxplot(x="Country", y="GHI", data=df_all, ax=ax)
    st.pyplot(fig)
