"""
Main WOD Browser application class.
"""

import random
import streamlit as st
from pathlib import Path
from typing import List, Dict

from ..config import EXCLUDED_DIRECTORIES, DEFAULT_RSS_FEEDS, ITEMS_PER_PAGE
from ..parser import WorkoutParser
from ..rss import RSSHandler
from ..stats import StatisticsGenerator
from ..ui import UIComponents
from .filters import WorkoutFilter


class WODBrowser:
    """Main WOD Browser application"""
    
    def __init__(self):
        # Use relative path to ideas directory for better portability
        self.ideas_path = Path(__file__).parent.parent.parent / "ideas"
        self.workouts = []
        self.load_workouts()
    
    def load_workouts(self):
        """Load all workout files from the ideas directory"""
        if not self.ideas_path.exists():
            st.error(f"Ideas directory not found: {self.ideas_path}")
            return
        
        self.workouts = []
        
        # Scan each category directory
        for category_dir in self.ideas_path.iterdir():
            if category_dir.is_dir() and category_dir.name not in EXCLUDED_DIRECTORIES:
                category = category_dir.name
                
                # Process all .md and .txt files in the category
                for pattern in ["*.md", "*.txt"]:
                    for workout_file in category_dir.glob(pattern):
                        parsed_workout = WorkoutParser.parse_workout_file(str(workout_file), category)
                        if parsed_workout:
                            self.workouts.append(parsed_workout)
        
        st.session_state.total_workouts = len(self.workouts)
    
    def display_rss_browser(self):
        """Display RSS feed browser interface"""
        st.header("📡 RSS Feed Browser")
        st.markdown("Parse RSS feeds from external WOD sources and create GitHub issues to add them to the repository.")
        
        # RSS URL input
        rss_url = st.selectbox(
            "Select a WOD RSS feed or enter custom URL:",
            [""] + DEFAULT_RSS_FEEDS + ["Custom URL"],
            index=0
        )
        
        if rss_url == "Custom URL":
            rss_url = st.text_input("Enter RSS URL:", placeholder="https://example.com/rss")
        
        if rss_url and rss_url != "Custom URL":
            if st.button("📡 Parse RSS Feed", type="primary"):
                with st.spinner("Parsing RSS feed..."):
                    rss_workouts = RSSHandler.parse_rss_feed(rss_url)
                    
                    if rss_workouts:
                        st.success(f"Found {len(rss_workouts)} entries in the RSS feed")
                        st.session_state.rss_workouts = rss_workouts
                    else:
                        st.warning("No entries found or failed to parse RSS feed")
        
        # Display RSS workouts if available
        if hasattr(st.session_state, 'rss_workouts') and st.session_state.rss_workouts:
            st.markdown(f"### Found {len(st.session_state.rss_workouts)} RSS Entries")
            st.markdown("Click the 'Create Issue' button next to any workout to add it to the GitHub repository.")
            
            for workout in st.session_state.rss_workouts:
                RSSHandler.display_rss_workout(workout)
    
    def run(self):
        """Run the main Streamlit app"""
        from ..config import APP_TITLE, APP_DESCRIPTION
        
        st.title(APP_TITLE)
        st.markdown(APP_DESCRIPTION)
        
        if not self.workouts:
            st.error("No workout files found. Please check the ideas directory structure.")
            return
        
        # Create tabs for different features
        tab1, tab2, tab3 = st.tabs(["🔍 Browse Workouts", "📊 Statistics", "📡 RSS Feed Browser"])
        
        with tab1:
            self._display_workout_browser()
        
        with tab2:
            StatisticsGenerator.display_statistics(self.workouts)
        
        with tab3:
            self.display_rss_browser()
    
    def _display_workout_browser(self):
        """Display the main workout browsing interface"""
        # Get filter options
        categories = WorkoutFilter.get_unique_values(self.workouts, 'category')
        all_equipment = WorkoutFilter.get_unique_values(self.workouts, 'equipment')
        all_tags = WorkoutFilter.get_unique_values(self.workouts, 'tags')
        
        # Display filters sidebar
        selected_categories, selected_equipment, selected_tags, search_term = \
            UIComponents.display_filters_sidebar(categories, all_equipment, all_tags)
        
        # Display UI options
        use_card_layout, sort_selection = UIComponents.display_sorting_options()
        
        # Clear filters button
        if st.sidebar.button("Clear All Filters"):
            st.rerun()
        
        # Filter workouts
        filtered_workouts = WorkoutFilter.filter_workouts(
            self.workouts, selected_categories, selected_equipment, selected_tags, search_term
        )
        
        # Apply sorting
        if sort_selection != "None":
            if "Title" in sort_selection:
                filtered_workouts = WorkoutFilter.sort_workouts(filtered_workouts, "title", "Z-A" in sort_selection)
            elif "Category" in sort_selection:
                filtered_workouts = WorkoutFilter.sort_workouts(filtered_workouts, "category", "Z-A" in sort_selection)
            elif "Time Cap" in sort_selection:
                filtered_workouts = WorkoutFilter.sort_workouts(filtered_workouts, "time_cap", "High-Low" in sort_selection)
        
        # Main content area header
        st.markdown(f"**{len(filtered_workouts)} workouts found** (out of {len(self.workouts)} total)")
        st.markdown('<div style="display:flex;justify-content:center;margin:2em 0 2em 0;">', unsafe_allow_html=True)
        if filtered_workouts:
            if st.button("🎲 Random Workout", type="primary", key="central_random", help="Show a random workout", args=None):
                random_workout = random.choice(filtered_workouts)
                st.session_state.show_random = random_workout
        else:
            st.warning("No workouts to choose from.")
        st.markdown('</div>', unsafe_allow_html=True)
        # Export button (placeholder for future feature)
        if filtered_workouts:
            st.button("📤 Export Results", disabled=True, help="Coming soon!", key="export_results")
        
        # Show random workout if selected
        if hasattr(st.session_state, 'show_random'):
            st.markdown("## 🎲 Random Workout Selection")
            UIComponents.display_workout(st.session_state.show_random, use_card_layout)
            if st.button("Clear Random Selection"):
                del st.session_state.show_random
                st.rerun()
            st.markdown("---")
        
        # Display filtered workouts
        if filtered_workouts:
            st.markdown("## 📋 All Matching Workouts")
            
            # Add pagination for large results
            start_idx, end_idx = UIComponents.display_pagination(len(filtered_workouts), ITEMS_PER_PAGE)
            page_workouts = filtered_workouts[start_idx:end_idx]
            
            for workout in page_workouts:
                UIComponents.display_workout(workout, use_card_layout)
        else:
            st.info("No workouts match your current filters. Try adjusting your selection.")