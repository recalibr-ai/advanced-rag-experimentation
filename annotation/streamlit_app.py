#!/usr/bin/env python3
"""
Streamlit Restaurant Reviews Data Viewer & Annotator
Production-ready interface for reviewing restaurant data
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import logging
from typing import Optional, Dict, Any
import html

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
APP_TITLE = "Restaurant Reviews Viewer"
APP_ICON = "🍽️"
DATA_FILE = "reasoning_restaurant_reviews.csv"
POSSIBLE_DATA_PATHS = [
    Path("../data") / DATA_FILE,
    Path("data") / DATA_FILE,
    Path(".") / DATA_FILE
]

# Page config - should be first Streamlit command
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_custom_css() -> None:
    """Load custom CSS styles for the application."""
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
            word-wrap: break-word;
            overflow-wrap: break-word;
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
        /* Ensure proper text wrapping */
        .element-container {
            word-wrap: break-word;
        }
        </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_data() -> Optional[pd.DataFrame]:
    """
    Load restaurant reviews data from CSV file.
    
    Returns:
        DataFrame with restaurant reviews or None if file not found
    """
    for data_path in POSSIBLE_DATA_PATHS:
        if data_path.exists():
            try:
                df = pd.read_csv(data_path)
                logger.info(f"Successfully loaded data from {data_path}")
                
                # Validate required columns
                required_cols = ['id', 'restaurant', 'review', 'reviewer', 'rating']
                if not all(col in df.columns for col in required_cols):
                    st.error(f"Missing required columns. Expected: {required_cols}")
                    return None
                
                # Data validation and cleaning
                df['id'] = pd.to_numeric(df['id'], errors='coerce')
                df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
                df = df.dropna(subset=['id', 'restaurant', 'review', 'rating'])
                df['rating'] = df['rating'].clip(1, 5).astype(int)
                
                return df
            except Exception as e:
                logger.error(f"Error loading data: {e}")
                st.error(f"Error loading data: {e}")
                return None
    
    st.error(f"Could not find {DATA_FILE} in any expected location")
    st.info("Please ensure the CSV file is in the 'data' directory")
    return None


def escape_html(text: str) -> str:
    """Escape HTML characters in text to prevent XSS."""
    return html.escape(str(text))


def render_home_page(df: pd.DataFrame) -> None:
    """Render the home page with overview statistics."""
    st.markdown("""
        <div class="restaurant-header">
            <h1 style='text-align: center; color: white; font-size: 3em;'>🍽️ Restaurant Reviews Data Viewer</h1>
            <p style='text-align: center; color: white; font-size: 1.2em; margin-top: 20px;'>
                Explore authentic customer reviews for advanced RAG demo
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats overview with error handling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <h2>{len(df)}</h2>
                <p>Total Reviews</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_rating = df['rating'].mean()
        st.markdown(f"""
            <div class="stat-card">
                <h2>{avg_rating:.1f}</h2>
                <p>Average Rating</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        max_rating = df['rating'].max()
        st.markdown(f"""
            <div class="stat-card">
                <h2>{max_rating}</h2>
                <p>Max Rating</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        unique_restaurants = df['restaurant'].nunique()
        st.markdown(f"""
            <div class="stat-card">
                <h2>{unique_restaurants}</h2>
                <p>Restaurants</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Quick overview table
    st.markdown("### 📋 Quick Overview")
    overview_df = df[['id', 'restaurant', 'rating', 'reviewer']].copy()
    overview_df['rating'] = overview_df['rating'].apply(lambda x: '⭐' * int(x))
    st.dataframe(
        overview_df, 
        use_container_width=True, 
        height=400,
        hide_index=True
    )


def render_all_restaurants(df: pd.DataFrame) -> None:
    """Render the all restaurants view with filtering."""
    st.title("📊 All Restaurant Reviews")
    
    # Filter options
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        rating_filter = st.selectbox(
            "Filter by Rating",
            ["All"] + list(range(5, 0, -1))
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            ["ID", "Restaurant Name", "Rating", "Reviewer"]
        )
    
    # Apply filter
    filtered_df = df.copy()
    if rating_filter != "All":
        filtered_df = filtered_df[filtered_df['rating'] == rating_filter]
    
    # Apply sorting
    sort_mapping = {
        "ID": "id",
        "Restaurant Name": "restaurant",
        "Rating": "rating",
        "Reviewer": "reviewer"
    }
    filtered_df = filtered_df.sort_values(by=sort_mapping[sort_by])
    
    # Display count
    st.info(f"Showing {len(filtered_df)} of {len(df)} reviews")
    
    # Display cards for each restaurant
    for _, row in filtered_df.iterrows():
        rating_stars = '⭐' * int(row['rating'])
        with st.expander(
            f"**#{int(row['id'])} - {row['restaurant']}** | {rating_stars} | by {row['reviewer']}"
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**Review:**")
                # Escape HTML to prevent XSS
                review_text = escape_html(row['review'])
                st.markdown(
                    f"<div class='review-box'>{review_text}</div>", 
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown("**Details:**")
                st.metric("Rating", f"{int(row['rating'])}/5")
                st.info(f"**Reviewer:** {row['reviewer']}")
                st.caption(f"**ID:** #{int(row['id'])}")
                
                # Safe word/character counting
                review_str = str(row['review'])
                st.caption(f"**Words:** {len(review_str.split())}")
                st.caption(f"**Characters:** {len(review_str)}")


def render_individual_review(df: pd.DataFrame) -> None:
    """Render the individual review page with navigation."""
    st.title("🔍 Individual Restaurant Review")
    
    # Initialize session state
    if 'current_restaurant_idx' not in st.session_state:
        st.session_state.current_restaurant_idx = 0
    
    # Validate index bounds
    st.session_state.current_restaurant_idx = max(
        0, min(st.session_state.current_restaurant_idx, len(df) - 1)
    )
    
    # Restaurant selector
    restaurant_names = [
        f"#{int(row['id'])} - {row['restaurant']}" 
        for _, row in df.iterrows()
    ]
    
    # Update selectbox based on session state
    selected = st.selectbox(
        "Select Restaurant", 
        restaurant_names,
        index=st.session_state.current_restaurant_idx,
        key='restaurant_selector'
    )
    
    # Update session state when selectbox changes
    try:
        st.session_state.current_restaurant_idx = restaurant_names.index(selected)
    except ValueError:
        st.session_state.current_restaurant_idx = 0
    
    # Get current restaurant with bounds checking
    restaurant = df.iloc[st.session_state.current_restaurant_idx]
    
    # Display header
    restaurant_id = int(restaurant['id'])
    restaurant_name = escape_html(restaurant['restaurant'])
    rating_stars = '⭐' * int(restaurant['rating'])
    
    st.markdown(f"""
        <div class="restaurant-header">
            <h1 style='text-align: center; color: white;'>#{restaurant_id} - {restaurant_name}</h1>
            <p style='text-align: center; color: white; font-size: 2em; margin-top: 20px;'>
                {rating_stars}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Two column layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📝 Customer Review")
        review_text = escape_html(restaurant['review'])
        st.markdown(
            f"<div class='review-box'>{review_text}</div>", 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("### 📊 Details")
        
        # Rating
        rating_val = int(restaurant['rating'])
        st.markdown(f"""
            <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h4 style='color: #007bff; margin-bottom: 10px;'>⭐ Rating</h4>
                <h1 style='color: #ffc107; text-align: center;'>{rating_val}/5</h1>
                <p style='text-align: center; color: #ffc107; font-size: 1.5em;'>{'⭐' * rating_val}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Reviewer
        reviewer_name = escape_html(restaurant['reviewer'])
        st.markdown(f"""
            <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h4 style='color: #007bff; margin-bottom: 10px;'>👤 Reviewer</h4>
                <h3 style='color: #28a745; text-align: center;'>{reviewer_name}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Stats with safe string handling
        review_str = str(restaurant['review'])
        char_count = len(review_str)
        word_count = len(review_str.split())
        sentence_count = len([s for s in review_str.split('.') if s.strip()])
        
        st.markdown(f"""
            <div style='background: #f8f9fa; padding: 20px; border-radius: 10px;'>
                <h4 style='color: #007bff; margin-bottom: 15px;'>📈 Quick Stats</h4>
                <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; text-align: center;'>
                    <div>
                        <h3 style='color: #6c757d; margin: 0;'>{char_count:,}</h3>
                        <small>Characters</small>
                    </div>
                    <div>
                        <h3 style='color: #6c757d; margin: 0;'>{word_count:,}</h3>
                        <small>Words</small>
                    </div>
                    <div>
                        <h3 style='color: #6c757d; margin: 0;'>{sentence_count}</h3>
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
            if st.button("⬅️ Previous", use_container_width=True, key="prev_btn"):
                st.session_state.current_restaurant_idx -= 1
                st.rerun()
    
    with col2:
        current_pos = st.session_state.current_restaurant_idx + 1
        total = len(df)
        st.markdown(
            f"<p style='text-align: center; color: #6c757d;'>"
            f"Restaurant {current_pos} of {total}</p>", 
            unsafe_allow_html=True
        )
    
    with col3:
        if st.session_state.current_restaurant_idx < len(df) - 1:
            if st.button("Next ➡️", use_container_width=True, key="next_btn"):
                st.session_state.current_restaurant_idx += 1
                st.rerun()


def main():
    """Main application entry point."""
    # Load custom CSS
    load_custom_css()
    
    # Load data
    df = load_data()
    
    if df is None or df.empty:
        st.error("❌ No data available. Please check your data file.")
        st.stop()
    
    # Sidebar navigation
    st.sidebar.title(f"{APP_ICON} Navigation")
    st.sidebar.markdown("---")
    
    # Page selection
    page = st.sidebar.radio(
        "Select View",
        ["🏠 Home", "📊 All Restaurants", "🔍 Individual Review"]
    )
    
    # Route to appropriate page
    if page == "🏠 Home":
        render_home_page(df)
    elif page == "📊 All Restaurants":
        render_all_restaurants(df)
    else:  # Individual Review
        render_individual_review(df)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Tip:** Use keyboard shortcuts for navigation")
    st.sidebar.success(f"📊 Total Reviews: {len(df)}")
    
    # Add data quality indicator
    if df['review'].isna().any():
        st.sidebar.warning("⚠️ Some reviews have missing data")


if __name__ == "__main__":
    main()