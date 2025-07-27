"""
Reusable UI components for the WOD Browser application.
"""

import streamlit as st
from typing import Dict


class UIComponents:
    """Collection of reusable UI components"""
    
    @staticmethod
    def display_workout(workout: Dict, use_card_layout: bool = True):
        """Display a single workout in a formatted, visually enhanced way"""
        if use_card_layout:
            with st.container():
                st.markdown('<div class="wod-card">', unsafe_allow_html=True)
                # Title
                st.markdown(f'<div class="wod-title">🏋️ {workout["title"]}</div>', unsafe_allow_html=True)
                # Meta info row
                meta_cols = st.columns([1.2,1,1])
                with meta_cols[0]:
                    st.markdown(f'<span class="wod-meta-label">📂 Category</span><br><span class="wod-meta-value">{workout["category"].title()}</span>', unsafe_allow_html=True)
                    st.markdown(f'<span class="wod-meta-label">⚡ Equipment</span><br><span class="wod-meta-value">{workout["equipment"]}</span>', unsafe_allow_html=True)
                with meta_cols[1]:
                    st.markdown(f'<span class="wod-meta-label">⏱️ Time Cap</span><br><span class="wod-meta-value">{workout["time_cap"]}</span>', unsafe_allow_html=True)
                    if workout['tags']:
                        st.markdown(f'<span class="wod-meta-label">🏷️ Tags</span>', unsafe_allow_html=True)
                        tags_html = " ".join([f'<span class="wod-tag">{tag}</span>' for tag in workout['tags']])
                        st.markdown(tags_html, unsafe_allow_html=True)
                with meta_cols[2]:
                    st.markdown(f'<span class="wod-meta-label">⚡ Scaling</span>', unsafe_allow_html=True)
                    st.markdown(f'<div class="wod-scaling">{workout["scaling"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                # Workout steps as Markdown list
                st.markdown('<div class="wod-section">💪 Workout:</div>', unsafe_allow_html=True)
                workout_lines = [line.strip('- ').strip() for line in workout['workout'].split('\n') if line.strip()]
                if len(workout_lines) > 1:
                    st.markdown('<ul class="wod-workout-list">' + ''.join(f'<li>{step}</li>' for step in workout_lines) + '</ul>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="wod-workout-list">{workout["workout"]}</div>', unsafe_allow_html=True)
                # Notes
                if workout['notes'] and workout['notes'] != "No notes":
                    st.markdown('<div class="wod-section">📝 Notes:</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="wod-notes">{workout["notes"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
        else:
            # Original simple layout
            with st.container():
                st.markdown(f"### 🏋️ {workout['title']}")
                
                # Create columns for key info
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Category:** {workout['category'].title()}")
                    st.markdown(f"**Equipment:** {workout['equipment']}")
                
                with col2:
                    st.markdown(f"**Time Cap:** {workout['time_cap']}")
                    if workout['tags']:
                        st.markdown(f"**Tags:** {', '.join(workout['tags'])}")
                
                with col3:
                    st.markdown(f"**Scaling:** {workout['scaling']}")
                
                # Workout description
                st.markdown("**Workout:**")
                st.markdown(workout['workout'])
                
                # Notes
                if workout['notes'] and workout['notes'] != "No notes":
                    st.markdown("**Notes:**")
                    st.markdown(workout['notes'])
                
                st.markdown("---")
    
    @staticmethod
    def display_filters_sidebar(categories, equipment, tags):
        """Display the filters sidebar with grouped sections and a clear all button"""
        st.sidebar.markdown('<div class="sidebar-section-header">🔍 FILTER BY</div>', unsafe_allow_html=True)
        # Category filter
        selected_categories = st.sidebar.multiselect(
            "Categories",
            categories,
            help="Filter by workout category"
        )
        # Equipment filter
        selected_equipment = st.sidebar.multiselect(
            "Equipment",
            equipment,
            help="Filter by required equipment"
        )
        # Tags filter (if any tags exist)
        selected_tags = []
        if tags:
            selected_tags = st.sidebar.multiselect(
                "Tags",
                tags,
                help="Filter by workout tags"
            )
        # Search box
        search_term = st.sidebar.text_input(
            "🔍 Search",
            placeholder="Search in title, workout, notes...",
            help="Case-insensitive keyword search"
        )
        # Clear all filters button
        if selected_categories or selected_equipment or selected_tags or search_term:
            with st.sidebar.container():
                st.markdown('<div class="sidebar-clear-btn">', unsafe_allow_html=True)
                if st.button("🧹 Clear All Filters"):
                    st.experimental_rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        return selected_categories, selected_equipment, selected_tags, search_term
    
    @staticmethod
    def display_sorting_options():
        """Display sorting options in the sidebar"""
        st.sidebar.header("🎨 Display Options")
        use_card_layout = st.sidebar.checkbox("Enhanced Card Layout", value=True)
        
        # Sorting options
        sort_options = ["None", "Title (A-Z)", "Title (Z-A)", "Category (A-Z)", "Category (Z-A)", "Time Cap (Low-High)", "Time Cap (High-Low)"]
        sort_selection = st.sidebar.selectbox("Sort by:", sort_options)
        
        return use_card_layout, sort_selection
    
    @staticmethod
    def display_pagination(total_items, items_per_page):
        """Display pagination controls"""
        total_pages = (total_items - 1) // items_per_page + 1
        
        if total_pages > 1:
            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
            start_idx = (page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            st.markdown(f"*Showing {start_idx + 1}-{min(end_idx, total_items)} of {total_items} workouts*")
            return start_idx, end_idx
        else:
            return 0, total_items