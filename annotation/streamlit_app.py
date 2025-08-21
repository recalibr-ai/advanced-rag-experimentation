#!/usr/bin/env python3
"""
Streamlit Restaurant Reviews Data Viewer & Annotator
Beautiful, clean interface for reviewing restaurant data
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Restaurant Reviews Viewer",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .review-box {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        font-size: 1.1em;
        line-height: 1.8;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .stat-card h2 {
        margin: 0;
        font-size: 2.5em;
    }
    .stat-card p {
        margin: 5px 0 0 0;
        opacity: 0.9;
    }
    .restaurant-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    data_path = Path("../data/restaurant_reviews.csv")
    if not data_path.exists():
        data_path = Path("data/restaurant_reviews.csv")
    return pd.read_csv(data_path)

df = load_data()

# Sidebar for navigation
st.sidebar.title("🍽️ Navigation")
st.sidebar.markdown("---")

# Page selection
page = st.sidebar.radio(
    "Select View",
    ["🏠 Home", "📊 All Restaurants", "🔍 Individual Review"]
)

if page == "🏠 Home":
    # Home page
    st.markdown("""
        <div class="restaurant-header">
            <h1 style='text-align: center; color: white; font-size: 3em;'>🍽️ Restaurant Reviews Data Viewer</h1>
            <p style='text-align: center; color: white; font-size: 1.2em; margin-top: 20px;'>
                Explore 12 authentic customer reviews for advanced RAG demo
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <h2>{len(df)}</h2>
                <p>Total Reviews</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <h2>{df['rating'].mean():.1f}</h2>
                <p>Average Rating</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-card">
                <h2>{df['rating'].max()}</h2>
                <p>Max Rating</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stat-card">
                <h2>{len(df['restaurant'].unique())}</h2>
                <p>Restaurants</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Quick overview table
    st.markdown("### 📋 Quick Overview")
    overview_df = df[['id', 'restaurant', 'rating', 'reviewer']].copy()
    overview_df['rating'] = overview_df['rating'].apply(lambda x: '⭐' * x)
    st.dataframe(overview_df, use_container_width=True, height=400)

elif page == "📊 All Restaurants":
    st.title("📊 All Restaurant Reviews")
    
    # Filter options
    col1, col2 = st.columns([1, 3])
    with col1:
        rating_filter = st.selectbox(
            "Filter by Rating",
            ["All"] + list(range(5, 0, -1))
        )
    
    # Apply filter
    filtered_df = df if rating_filter == "All" else df[df['rating'] == rating_filter]
    
    # Display cards for each restaurant
    for _, row in filtered_df.iterrows():
        with st.expander(f"**#{row['id']} - {row['restaurant']}** | {'⭐' * row['rating']} | by {row['reviewer']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**Review:**")
                st.markdown(f"<div class='review-box'>{row['review']}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("**Details:**")
                st.metric("Rating", f"{row['rating']}/5")
                st.info(f"**Reviewer:** {row['reviewer']}")
                st.caption(f"**ID:** #{row['id']}")
                st.caption(f"**Words:** {len(row['review'].split())}")
                st.caption(f"**Characters:** {len(row['review'])}")

else:  # Individual Review page
    st.title("🔍 Individual Restaurant Review")
    
    # Initialize session state for current restaurant
    if 'current_restaurant_idx' not in st.session_state:
        st.session_state.current_restaurant_idx = 0
    
    # Restaurant selector
    restaurant_names = [f"#{row['id']} - {row['restaurant']}" for _, row in df.iterrows()]
    
    # Update selectbox based on session state
    selected = st.selectbox(
        "Select Restaurant", 
        restaurant_names,
        index=st.session_state.current_restaurant_idx,
        key='restaurant_selector'
    )
    
    # Update session state when selectbox changes
    st.session_state.current_restaurant_idx = restaurant_names.index(selected)
    
    # Get current restaurant
    restaurant = df.iloc[st.session_state.current_restaurant_idx]
    restaurant_id = restaurant['id']
    
    # Display header
    st.markdown(f"""
        <div class="restaurant-header">
            <h1 style='text-align: center; color: white;'>#{restaurant['id']} - {restaurant['restaurant']}</h1>
            <p style='text-align: center; color: white; font-size: 2em; margin-top: 20px;'>
                {'⭐' * restaurant['rating']}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Two column layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📝 Customer Review")
        st.markdown(f"<div class='review-box'>{restaurant['review']}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Details")
        
        # Rating
        st.markdown(f"""
            <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h4 style='color: #007bff; margin-bottom: 10px;'>⭐ Rating</h4>
                <h1 style='color: #ffc107; text-align: center;'>{restaurant['rating']}/5</h1>
                <p style='text-align: center; color: #ffc107; font-size: 1.5em;'>{'⭐' * restaurant['rating']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Reviewer
        st.markdown(f"""
            <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h4 style='color: #007bff; margin-bottom: 10px;'>👤 Reviewer</h4>
                <h3 style='color: #28a745; text-align: center;'>{restaurant['reviewer']}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Stats
        st.markdown(f"""
            <div style='background: #f8f9fa; padding: 20px; border-radius: 10px;'>
                <h4 style='color: #007bff; margin-bottom: 15px;'>📈 Quick Stats</h4>
                <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; text-align: center;'>
                    <div>
                        <h3 style='color: #6c757d; margin: 0;'>{len(restaurant['review'])}</h3>
                        <small>Characters</small>
                    </div>
                    <div>
                        <h3 style='color: #6c757d; margin: 0;'>{len(restaurant['review'].split())}</h3>
                        <small>Words</small>
                    </div>
                    <div>
                        <h3 style='color: #6c757d; margin: 0;'>{len([s for s in restaurant['review'].split('.') if s.strip()])}</h3>
                        <small>Sentences</small>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_restaurant_idx > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_restaurant_idx -= 1
                st.rerun()
    
    with col2:
        st.markdown(f"<p style='text-align: center; color: #6c757d;'>Restaurant {st.session_state.current_restaurant_idx + 1} of {len(df)}</p>", unsafe_allow_html=True)
    
    with col3:
        if st.session_state.current_restaurant_idx < len(df) - 1:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.current_restaurant_idx += 1
                st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Use the Individual Review page for detailed analysis")
st.sidebar.success(f"📊 Total Reviews: {len(df)}")