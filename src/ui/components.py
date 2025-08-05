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
                st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">', unsafe_allow_html=True)
                st.markdown(f'<div class="wod-title"><i class="fa-solid fa-dumbbell" style="margin-right:8px;"></i>{workout["title"]}</div>', unsafe_allow_html=True)
                # Meta info row with FontAwesome icons
                meta_cols = st.columns([1.2,1,1])
                with meta_cols[0]:
                    st.markdown(f'<span class="wod-meta-label"><i class="fa-solid fa-layer-group"></i> Category</span><br><span class="wod-meta-value">{workout["category"].title()}</span>', unsafe_allow_html=True)
                    st.markdown(f'<span class="wod-meta-label"><i class="fa-solid fa-toolbox"></i> Equipment</span><br><span class="wod-meta-value">{workout["equipment"]}</span>', unsafe_allow_html=True)
                with meta_cols[1]:
                    st.markdown(f'<span class="wod-meta-label"><i class="fa-solid fa-stopwatch"></i> Time Cap</span><br><span class="wod-meta-value">{workout["time_cap"]}</span>', unsafe_allow_html=True)
                    if workout['tags']:
                        st.markdown(f'<span class="wod-meta-label"><i class="fa-solid fa-tags"></i> Tags</span>', unsafe_allow_html=True)
                        tags_html = " ".join([f'<span class="wod-tag">{tag}</span>' for tag in workout['tags']])
                        st.markdown(tags_html, unsafe_allow_html=True)
                with meta_cols[2]:
                    st.markdown(f'<span class="wod-meta-label"><i class="fa-solid fa-person-running"></i> Scaling</span>', unsafe_allow_html=True)
                    st.markdown(f'<div class="wod-scaling">{workout["scaling"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                # Workout steps as Markdown list with bolder border/background
                st.markdown('<div class="wod-section">💪 Workout:</div>', unsafe_allow_html=True)
                workout_lines = [line.strip('- ').strip() for line in workout['workout'].split('\n') if line.strip()]
                if len(workout_lines) > 1:
                    st.markdown('<div style="background:#f0f6ff;border-left:6px solid #4361ee;padding:1em 1.2em 1em 1.5em;border-radius:10px;margin-bottom:1em;">' +
                        '<ul class="wod-workout-list" style="margin-bottom:0;">' + ''.join(f'<li>{step}</li>' for step in workout_lines) + '</ul></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="wod-workout-list" style="background:#f0f6ff;border-left:6px solid #4361ee;padding:1em 1.2em 1em 1.5em;border-radius:10px;margin-bottom:1em;">{workout["workout"]}</div>', unsafe_allow_html=True)
                # Notes
                if workout['notes'] and workout['notes'] != "No notes":
                    st.markdown('<div class="wod-section">📝 Notes:</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="wod-notes">{workout["notes"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
        else:
            # Original simple layout, now with FontAwesome icons for metadata
            with st.container():
                st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">', unsafe_allow_html=True)
                st.markdown(f"<div class='wod-title'><i class='fa-solid fa-dumbbell' style='margin-right:8px;'></i>{workout['title']}</div>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"<span class='wod-meta-label'><i class='fa-solid fa-layer-group'></i> Category</span><br><span class='wod-meta-value'>{workout['category'].title()}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span class='wod-meta-label'><i class='fa-solid fa-toolbox'></i> Equipment</span><br><span class='wod-meta-value'>{workout['equipment']}</span>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<span class='wod-meta-label'><i class='fa-solid fa-stopwatch'></i> Time Cap</span><br><span class='wod-meta-value'>{workout['time_cap']}</span>", unsafe_allow_html=True)
                    if workout['tags']:
                        st.markdown(f"<span class='wod-meta-label'><i class='fa-solid fa-tags'></i> Tags</span>", unsafe_allow_html=True)
                        tags_html = " ".join([f"<span class='wod-tag'>{tag}</span>" for tag in workout['tags']])
                        st.markdown(tags_html, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<span class='wod-meta-label'><i class='fa-solid fa-person-running'></i> Scaling</span>", unsafe_allow_html=True)
                    st.markdown(f"<div class='wod-scaling'>{workout['scaling'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
                st.markdown('<div class="wod-section">💪 Workout:</div>', unsafe_allow_html=True)
                workout_lines = [line.strip('- ').strip() for line in workout['workout'].split('\n') if line.strip()]
                if len(workout_lines) > 1:
                    st.markdown('<div style="background:#f0f6ff;border-left:6px solid #4361ee;padding:1em 1.2em 1em 1.5em;border-radius:10px;margin-bottom:1em;">' +
                        '<ul class="wod-workout-list" style="margin-bottom:0;">' + ''.join(f'<li>{step}</li>' for step in workout_lines) + '</ul></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="wod-workout-list" style="background:#f0f6ff;border-left:6px solid #4361ee;padding:1em 1.2em 1em 1.5em;border-radius:10px;margin-bottom:1em;">{workout["workout"]}</div>', unsafe_allow_html=True)
                if workout['notes'] and workout['notes'] != "No notes":
                    st.markdown('<div class="wod-section">📝 Notes:</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="wod-notes">{workout["notes"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
    @staticmethod
    def display_filters_sidebar(categories, equipment, tags):
        """Display the filters sidebar with collapsible filter panels and a clear all button"""
        st.sidebar.markdown('<style>.sidebar-section-header{margin-bottom:0.5em;}.sidebar-scroll{max-height:80vh;overflow-y:auto;padding-right:8px;}</style>', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-section-header">🔍 FILTER BY</div>', unsafe_allow_html=True)
        with st.sidebar.container():
            st.markdown('<div class="sidebar-scroll">', unsafe_allow_html=True)
            # Category filter in expander (expanded by default)
            with st.expander("Categories", expanded=True):
                selected_categories = st.multiselect(
                    "Select categories",
                    categories,
                    help="Choose one or more workout categories to filter results."
                )
            with st.expander("Equipment", expanded=False):
                selected_equipment = st.multiselect(
                    "Select equipment",
                    equipment,
                    help="Choose equipment required for workouts. You can select multiple."
                )
            selected_tags = []
            if tags:
                with st.expander("Tags", expanded=False):
                    selected_tags = st.multiselect(
                        "Select tags",
                        tags,
                        help="Filter workouts by tags (e.g., cardio, strength, HIIT)."
                    )
            search_term = st.text_input(
                "🔍 Search",
                placeholder="Search in title, workout, notes...",
                help="Type keywords to search workouts. Case-insensitive."
            )
            if selected_categories or selected_equipment or selected_tags or search_term:
                st.markdown('<div class="sidebar-clear-btn" style="margin-top:0.5em;">', unsafe_allow_html=True)
                if st.button("🧹 Clear All Filters", help="Reset all filters and show all workouts."):
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        return selected_categories, selected_equipment, selected_tags, search_term
    
    @staticmethod
    def display_sorting_options():
        """Display sorting options in the sidebar, grouped in a collapsible panel"""
        with st.sidebar.expander("Display & Sorting Options", expanded=False):
            use_card_layout = st.checkbox("Enhanced Card Layout", value=True)
            sort_options = ["None", "Title (A-Z)", "Title (Z-A)", "Category (A-Z)", "Category (Z-A)", "Time Cap (Low-High)", "Time Cap (High-Low)"]
            sort_selection = st.selectbox("Sort by:", sort_options)
        return use_card_layout, sort_selection
    
    @staticmethod
    def display_pagination(total_items, items_per_page):
        """Display pagination controls in a collapsible panel"""
        total_pages = (total_items - 1) // items_per_page + 1
        start_idx, end_idx = 0, total_items
        if total_pages > 1:
            with st.sidebar.expander("Pagination", expanded=False):
                page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
                start_idx = (page - 1) * items_per_page
                end_idx = start_idx + items_per_page
                st.markdown(f"*Showing {start_idx + 1}-{min(end_idx, total_items)} of {total_items} workouts*")
        return start_idx, min(end_idx, total_items)