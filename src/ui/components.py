"""
Reusable UI components for the WOD Browser application.
"""

import streamlit as st
from typing import Dict


class UIComponents:
    """Collection of reusable UI components"""
    
    @staticmethod
    def display_workout(workout: Dict, use_card_layout: bool = True):
        """Display a single workout in a formatted way"""
        if use_card_layout:
            # Enhanced card-style layout
            with st.container():
                # Create a styled card with border
                st.markdown("""
                <div style="
                    border: 1px solid #e0e0e0;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px 0;
                    background-color: #fafafa;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                """, unsafe_allow_html=True)
                
                # Title with icon
                st.markdown(f"### 🏋️ {workout['title']}")
                
                # Create columns for key info in a more structured way
                info_col1, info_col2, info_col3 = st.columns(3)
                
                with info_col1:
                    st.markdown(f"**📂 Category**")
                    st.markdown(f"`{workout['category'].title()}`")
                    st.markdown(f"**⚡ Equipment**")
                    st.markdown(f"`{workout['equipment']}`")
                
                with info_col2:
                    st.markdown(f"**⏱️ Time Cap**")
                    st.markdown(f"`{workout['time_cap']}`")
                    if workout['tags']:
                        st.markdown(f"**🏷️ Tags**")
                        # Display tags as badges
                        tags_html = " ".join([f'<span style="background-color: #e1f5fe; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; margin: 2px;">{tag}</span>' for tag in workout['tags']])
                        st.markdown(tags_html, unsafe_allow_html=True)
                
                with info_col3:
                    st.markdown(f"**📊 Scaling**")
                    st.markdown(f"`{workout['scaling']}`")
                
                # Workout description with better formatting
                st.markdown("**💪 Workout:**")
                with st.container():
                    st.markdown(f"""
                    <div style="
                        background-color: #f0f2f6;
                        padding: 15px;
                        border-radius: 5px;
                        border-left: 4px solid #4CAF50;
                        margin: 10px 0;
                    ">
                    {workout['workout'].replace('\n', '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Notes with conditional display
                if workout['notes'] and workout['notes'] != "No notes":
                    st.markdown("**📝 Notes:**")
                    with st.container():
                        st.markdown(f"""
                        <div style="
                            background-color: #fff3e0;
                            padding: 15px;
                            border-radius: 5px;
                            border-left: 4px solid #FF9800;
                            margin: 10px 0;
                        ">
                        {workout['notes'].replace('\n', '<br>')}
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("---")
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
        """Display the filters sidebar"""
        st.sidebar.header("🔍 Filters")
        
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