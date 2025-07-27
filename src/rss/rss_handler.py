"""
RSS feed parser and GitHub integration handler.
"""

import streamlit as st
import feedparser
import urllib.parse
from typing import Dict, List
from ..config import GITHUB_REPO


class RSSHandler:
    """Handle RSS feed parsing and GitHub integration"""
    
    @staticmethod
    def parse_rss_feed(rss_url: str) -> List[Dict]:
        """Parse RSS feed and extract workout information"""
        try:
            feed = feedparser.parse(rss_url)
            if feed.bozo:
                st.error(f"Error parsing RSS feed: {feed.bozo_exception}")
                return []
            
            rss_workouts = []
            for entry in feed.entries:
                workout_data = {
                    'title': entry.get('title', 'No Title'),
                    'description': entry.get('description', 'No description'),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'source': 'RSS',
                    'category': 'External'
                }
                rss_workouts.append(workout_data)
            
            return rss_workouts
            
        except Exception as e:
            st.error(f"Error fetching RSS feed: {str(e)}")
            return []
    
    @staticmethod
    def create_github_issue_url(workout_data: Dict) -> str:
        """Generate a GitHub issue URL for adding a new workout"""
        title = f"Add WOD: {workout_data.get('title', 'New Workout')}"
        body = f"""## New Workout from RSS Feed

**Title:** {workout_data.get('title', 'No Title')}

**Source:** {workout_data.get('link', 'No link')}

**Description:**
{workout_data.get('description', 'No description')}

**Published:** {workout_data.get('published', 'Unknown')}

---
Please review and add this workout to the appropriate category in the ideas/ directory.
"""
        
        # URL encode the title and body
        encoded_title = urllib.parse.quote(title)
        encoded_body = urllib.parse.quote(body)
        
        github_url = f"https://github.com/{GITHUB_REPO}/issues/new?title={encoded_title}&body={encoded_body}"
        return github_url
    
    @staticmethod
    def display_rss_workout(workout: Dict):
        """Display an RSS workout entry with GitHub integration"""
        with st.container():
            st.markdown(f"""
            <div style="
                border: 1px solid #2196F3;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
                background-color: #e3f2fd;
            ">
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"**{workout['title']}**")
                if workout.get('published'):
                    st.markdown(f"*Published: {workout['published']}*")
                
                # Show description (truncated)
                description = workout.get('description', '')
                if len(description) > 200:
                    description = description[:200] + "..."
                st.markdown(description)
                
                if workout.get('link'):
                    st.markdown(f"[Original Source]({workout['link']})")
            
            with col2:
                # GitHub issue creation button
                github_url = RSSHandler.create_github_issue_url(workout)
                st.markdown(f"""
                <a href="{github_url}" target="_blank">
                    <button style="
                        background-color: #4CAF50;
                        color: white;
                        padding: 10px 15px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 14px;
                    ">
                        📝 Create Issue
                    </button>
                </a>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)