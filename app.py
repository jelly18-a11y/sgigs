import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="SGigs | Direct-to-Source Jobs",
    page_icon="🎯",
    layout="wide",
)

# Header Section
st.title("SGigs 🚀")
st.markdown(
    "**Zero-Noise, Privacy-First Job Board.** No profiles, no social feeds,"
    " no algorithms. Just direct links to official company career pages."
)
st.divider()


# Load Job Data Safely
@st.cache_data
def load_data():
  return pd.read_json("jobs.json")


try:
  df = load_data()
except Exception as e:
  st.error(f"Could not load job data: {e}")
  df = pd.DataFrame(columns=["title", "company", "category", "location", "url"])

# Sidebar Filters
st.sidebar.header("Filter Roles")
selected_category = st.sidebar.selectbox(
    "Select Domain",
    [
        "All",
        "Product Management",
        "Business Analytics",
        "Business Development",
        "Project Management",
    ],
)

# Apply Category Filter
if selected_category != "All":
  filtered_df = df[df["category"] == selected_category]
else:
  filtered_df = df

# Main Search Bar
search_query = st.text_input(
    "🔍 Search by keyword (e.g., Company name, role title):"
)
if search_query:
  filtered_df = filtered_df[
      filtered_df.apply(
          lambda row: row.astype(str)
          .str.contains(search_query, case=False)
          .any(),
          axis=1,
      )
  ]

# Display Results Count
st.subheader(f"Available Positions ({len(filtered_df)} listings found)")
st.write("")

# Render Job Cards
for index, row in filtered_df.iterrows():
  with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
      st.markdown(f"### {row['title']}")
      st.write(
          f"🏢 **{row['company']}** &nbsp;|&nbsp; 📍 `{row['location']}`"
          f" &nbsp;|&nbsp; 📂 `{row['category']}`"
      )
    with col2:
      st.markdown(f"[Apply Directly]({row['url']})")
    st.divider()
