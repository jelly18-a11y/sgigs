import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="SGigs | Direct-to-Source Jobs",
    page_icon="🎯",
    layout="centered",
)

# Custom Styling & Header
st.markdown(
    """
    <style>
    .main-title { font-size: 2.5rem; font-weight: 800; margin-bottom: 0px; }
    .subtitle { color: #666; font-size: 1.1rem; margin-bottom: 20px; }
    .job-card { padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 15px; background-color: #ffffff; }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown('<p class="main-title">SGigs 🚀</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Zero-Noise, Privacy-First Job Board. No profiles,'
    " social feeds, or algorithms. Just direct links to official company"
    " career pages.</p>",
    unsafe_allow_html=True,
)
st.divider()


# Load Data Safely
@st.cache_data
def load_data():
  return pd.read_json("jobs.json")


try:
  df = load_data()
except Exception as e:
  st.error(f"Could not load job data: {e}")
  df = pd.DataFrame(columns=["title", "company", "category", "location", "url"])

# Sidebar Filters
st.sidebar.header("Filters")
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

# Filter by Category
if selected_category != "All":
  filtered_df = df[df["category"] == selected_category]
else:
  filtered_df = df

# Search Bar
search_query = st.text_input(
    "🔍 Search roles or companies:",
    placeholder="e.g., Razorpay, Analyst, Remote",
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

# Results Header
st.subheader(f"Open Positions ({len(filtered_df)})")
st.write("")

# Render Smooth Job Cards & Real Links
if filtered_df.empty:
  st.info("No matching roles found right now. Try a different search filter!")
else:
  for index, row in filtered_df.iterrows():
    st.markdown(
        f"""
        <div class="job-card">
            <h3>{row['title']}</h3>
            <p>🏢 <b>{row['company']}</b> &nbsp;|&nbsp; 📍 <code>{row['location']}</code> &nbsp;|&nbsp; 📂 <code>{row['category']}</code></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Direct Official Link Button
    st.link_button("Apply Directly on Career Page ➔", row["url"])
    st.write("")
