import streamlit as st
import os
import re
import random
import feedparser
import requests
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="WOD Browser",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class WorkoutParser:
    """Parser for workout .md and .txt files"""
    
    @staticmethod
    def parse_workout_file(file_path: str, category: str) -> Dict:
        """Parse a single workout file and extract structured data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.md':
                return WorkoutParser._parse_md_file(content, file_path, category)
            elif file_extension == '.txt':
                return WorkoutParser._parse_txt_file(content, file_path, category)
            else:
                # Fallback to .md parsing for unknown extensions
                return WorkoutParser._parse_md_file(content, file_path, category)
            
        except Exception as e:
            st.error(f"Error parsing file {file_path}: {str(e)}")
            return None
    
    @staticmethod
    def _parse_md_file(content: str, file_path: str, category: str) -> Dict:
        """Parse a markdown (.md) workout file"""
        # Extract title (first line with #)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else Path(file_path).stem
        
        # Extract fields using regex for markdown format
        equipment_match = re.search(r'\*\*Equipment:\*\*\s*(.+?)(?:\n|$)', content)
        equipment = equipment_match.group(1).strip() if equipment_match else "Unknown"
        
        time_cap_match = re.search(r'\*\*Time Cap:\*\*\s*(.+?)(?:\n|$)', content)
        time_cap = time_cap_match.group(1).strip() if time_cap_match else "Unknown"
        
        scaling_match = re.search(r'\*\*Scaling:\*\*\s*(.+?)(?:\n|$)', content)
        scaling = scaling_match.group(1).strip() if scaling_match else "Unknown"
        
        # Extract workout section
        workout_match = re.search(r'\*\*Workout:\*\*\s*\n(.*?)(?:\n\*\*|\n$)', content, re.DOTALL)
        workout = workout_match.group(1).strip() if workout_match else "No workout description"
        
        # Extract notes section
        notes_match = re.search(r'\*\*Notes:\*\*\s*\n(.*?)$', content, re.DOTALL)
        notes = notes_match.group(1).strip() if notes_match else "No notes"
        
        # Extract tags (optional, may not exist)
        tags_match = re.search(r'\*\*Tags:\*\*\s*(.+?)(?:\n|$)', content)
        tags = [tag.strip() for tag in tags_match.group(1).split(',')] if tags_match else []
        
        return {
            'title': title,
            'category': category,
            'equipment': equipment,
            'time_cap': time_cap,
            'scaling': scaling,
            'workout': workout,
            'notes': notes,
            'tags': tags,
            'file_path': file_path,
            'raw_content': content
        }
    
    @staticmethod
    def _parse_txt_file(content: str, file_path: str, category: str) -> Dict:
        """Parse a plain text (.txt) workout file as specified in the issue"""
        lines = content.strip().split('\n')
        
        # Title is the first line
        title = lines[0].strip() if lines else Path(file_path).stem
        
        # Initialize default values
        equipment = "Unknown"
        time_cap = "Unknown"
        scaling = "Unknown"
        workout = "No workout description"
        notes = "No notes"
        tags = []
        
        # Parse the rest of the content
        workout_started = False
        notes_started = False
        workout_lines = []
        notes_lines = []
        
        for i, line in enumerate(lines[1:], 1):
            line_stripped = line.strip()
            
            # Check for field patterns (case-insensitive)
            if line_stripped.lower().startswith('equipment:'):
                equipment = line_stripped[10:].strip()  # Remove "Equipment:" prefix
                workout_started = False
                notes_started = False
            elif line_stripped.lower().startswith('time cap:'):
                time_cap = line_stripped[9:].strip()  # Remove "Time Cap:" prefix
                workout_started = False
                notes_started = False
            elif line_stripped.lower().startswith('scaling:'):
                scaling = line_stripped[8:].strip()  # Remove "Scaling:" prefix
                workout_started = False
                notes_started = False
            elif line_stripped.lower().startswith('tags:'):
                tags_str = line_stripped[5:].strip()  # Remove "Tags:" prefix
                tags = [tag.strip() for tag in tags_str.split(',')] if tags_str else []
                workout_started = False
                notes_started = False
            elif line_stripped.lower().startswith('workout:'):
                workout_started = True
                notes_started = False
                workout_lines = []
                # If there's content after "Workout:" on the same line, include it
                after_colon = line_stripped[8:].strip()
                if after_colon:
                    workout_lines.append(after_colon)
            elif line_stripped.lower().startswith('notes:'):
                notes_started = True
                workout_started = False
                notes_lines = []
                # If there's content after "Notes:" on the same line, include it
                after_colon = line_stripped[6:].strip()
                if after_colon:
                    notes_lines.append(after_colon)
            elif workout_started:
                # Add all lines to workout section, including empty ones for formatting
                workout_lines.append(line)
            elif notes_started:
                # Add all lines to notes section, including empty ones for formatting
                notes_lines.append(line)
        
        # Join workout and notes content
        if workout_lines:
            workout = '\n'.join(workout_lines).strip()
        if notes_lines:
            notes = '\n'.join(notes_lines).strip()
        
        return {
            'title': title,
            'category': category,
            'equipment': equipment,
            'time_cap': time_cap,
            'scaling': scaling,
            'workout': workout,
            'notes': notes,
            'tags': tags,
            'file_path': file_path,
            'raw_content': content
        }

class WODBrowser:
    """Main WOD Browser application"""
    
    def __init__(self):
        # Use relative path to ideas directory for better portability
        self.ideas_path = Path(__file__).parent / "ideas"
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
            if category_dir.is_dir() and category_dir.name != "resources":
                category = category_dir.name
                
                # Process all .md and .txt files in the category
                for pattern in ["*.md", "*.txt"]:
                    for workout_file in category_dir.glob(pattern):
                        parsed_workout = WorkoutParser.parse_workout_file(str(workout_file), category)
                        if parsed_workout:
                            self.workouts.append(parsed_workout)
        
        st.session_state.total_workouts = len(self.workouts)
    
    def get_unique_values(self, field: str) -> List[str]:
        """Get unique values for a specific field across all workouts"""
        values = set()
        for workout in self.workouts:
            if field == 'equipment':
                # Handle equipment field specially to split multiple items
                equipment = workout.get(field, "")
                if equipment and equipment != "Unknown":
                    # Split by common separators and clean up
                    items = re.split(r'[,/&+]|(?:\s+or\s+)|(?:\s+and\s+)', equipment.lower())
                    for item in items:
                        clean_item = item.strip()
                        if clean_item:
                            values.add(clean_item.title())
            elif field == 'tags':
                values.update(workout.get(field, []))
            else:
                value = workout.get(field, "")
                if value and value != "Unknown":
                    values.add(value)
        
        return sorted(list(values))
    
    def sort_workouts(self, workouts: List[Dict], sort_by: str, reverse: bool = False) -> List[Dict]:
        """Sort workouts by the specified field"""
        if sort_by == "title":
            return sorted(workouts, key=lambda x: x.get('title', '').lower(), reverse=reverse)
        elif sort_by == "category":
            return sorted(workouts, key=lambda x: x.get('category', '').lower(), reverse=reverse)
        elif sort_by == "time_cap":
            # Custom sorting for time caps to handle different formats
            def time_cap_sort_key(workout):
                time_cap = workout.get('time_cap', 'Unknown')
                if time_cap == 'Unknown':
                    return float('inf')
                # Extract numbers from time cap for sorting
                numbers = re.findall(r'\d+', time_cap)
                return int(numbers[0]) if numbers else float('inf')
            return sorted(workouts, key=time_cap_sort_key, reverse=reverse)
        else:
            return workouts
    
    def parse_rss_feed(self, rss_url: str) -> List[Dict]:
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
    
    def create_github_issue_url(self, workout_data: Dict) -> str:
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
        import urllib.parse
        encoded_title = urllib.parse.quote(title)
        encoded_body = urllib.parse.quote(body)
        
        github_url = f"https://github.com/Tomeriko96/WODs/issues/new?title={encoded_title}&body={encoded_body}"
        return github_url
    
    def display_rss_workout(self, workout: Dict):
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
                github_url = self.create_github_issue_url(workout)
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
    
    def display_rss_browser(self):
        """Display RSS feed browser interface"""
        st.header("📡 RSS Feed Browser")
        st.markdown("Parse RSS feeds from external WOD sources and create GitHub issues to add them to the repository.")
        
        # Popular WOD RSS feeds (you can add more)
        default_feeds = [
            "https://www.crossfit.com/rss/workouts",
            "https://wodwell.com/feed/",
            # Add more RSS feeds here
        ]
        
        # RSS URL input
        rss_url = st.selectbox(
            "Select a WOD RSS feed or enter custom URL:",
            [""] + default_feeds + ["Custom URL"],
            index=0
        )
        
        if rss_url == "Custom URL":
            rss_url = st.text_input("Enter RSS URL:", placeholder="https://example.com/rss")
        
        if rss_url and rss_url != "Custom URL":
            if st.button("📡 Parse RSS Feed", type="primary"):
                with st.spinner("Parsing RSS feed..."):
                    rss_workouts = self.parse_rss_feed(rss_url)
                    
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
                self.display_rss_workout(workout)
    def get_workout_statistics(self) -> Dict:
        """Generate comprehensive workout statistics"""
        if not self.workouts:
            return {}
        
        stats = {}
        
        # Category distribution
        category_counts = {}
        equipment_counts = {}
        tag_counts = {}
        time_cap_distribution = {}
        
        for workout in self.workouts:
            # Category stats
            category = workout.get('category', 'Unknown')
            category_counts[category] = category_counts.get(category, 0) + 1
            
            # Equipment stats
            equipment = workout.get('equipment', 'Unknown')
            if equipment and equipment != 'Unknown':
                # Split equipment by common separators
                items = re.split(r'[,/&+]|(?:\s+or\s+)|(?:\s+and\s+)', equipment.lower())
                for item in items:
                    clean_item = item.strip().title()
                    if clean_item:
                        equipment_counts[clean_item] = equipment_counts.get(clean_item, 0) + 1
            
            # Tag stats
            tags = workout.get('tags', [])
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            # Time cap stats
            time_cap = workout.get('time_cap', 'Unknown')
            if time_cap and time_cap != 'Unknown':
                time_cap_distribution[time_cap] = time_cap_distribution.get(time_cap, 0) + 1
        
        stats['total_workouts'] = len(self.workouts)
        stats['categories'] = dict(sorted(category_counts.items(), key=lambda x: x[1], reverse=True))
        stats['equipment'] = dict(sorted(equipment_counts.items(), key=lambda x: x[1], reverse=True)[:10])  # Top 10
        stats['tags'] = dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10])  # Top 10
        stats['time_caps'] = dict(sorted(time_cap_distribution.items(), key=lambda x: x[1], reverse=True)[:10])  # Top 10
        
        return stats
    
    def display_statistics(self):
        """Display workout statistics with visualizations"""
        st.header("📊 Workout Statistics")
        
        stats = self.get_workout_statistics()
        if not stats:
            st.warning("No statistics available")
            return
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Workouts", stats['total_workouts'])
        
        with col2:
            st.metric("Categories", len(stats['categories']))
        
        with col3:
            st.metric("Unique Equipment", len(stats['equipment']))
        
        with col4:
            st.metric("Unique Tags", len(stats['tags']))
        
        # Charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Category distribution pie chart
            if stats['categories']:
                st.subheader("Workouts by Category")
                fig_categories = px.pie(
                    values=list(stats['categories'].values()),
                    names=list(stats['categories'].keys()),
                    title="Distribution by Category"
                )
                fig_categories.update_layout(showlegend=True, height=400)
                st.plotly_chart(fig_categories, use_container_width=True)
        
        with chart_col2:
            # Equipment distribution bar chart
            if stats['equipment']:
                st.subheader("Top Equipment Usage")
                fig_equipment = px.bar(
                    x=list(stats['equipment'].values()),
                    y=list(stats['equipment'].keys()),
                    orientation='h',
                    title="Most Common Equipment",
                    labels={'x': 'Number of Workouts', 'y': 'Equipment'}
                )
                fig_equipment.update_layout(height=400)
                st.plotly_chart(fig_equipment, use_container_width=True)
        
        # Tags and Time Caps
        if stats['tags'] or stats['time_caps']:
            tag_col, time_col = st.columns(2)
            
            with tag_col:
                if stats['tags']:
                    st.subheader("Popular Tags")
                    tags_df = pd.DataFrame(list(stats['tags'].items()), columns=['Tag', 'Count'])
                    st.dataframe(tags_df, hide_index=True, use_container_width=True)
            
            with time_col:
                if stats['time_caps']:
                    st.subheader("Common Time Caps")
                    time_caps_df = pd.DataFrame(list(stats['time_caps'].items()), columns=['Time Cap', 'Count'])
                    st.dataframe(time_caps_df, hide_index=True, use_container_width=True)
    
    def filter_workouts(self, selected_categories: List[str], selected_equipment: List[str], 
                       selected_tags: List[str], search_term: str) -> List[Dict]:
        """Filter workouts based on selected criteria"""
        filtered = []
        
        for workout in self.workouts:
            # Category filter
            if selected_categories and workout['category'] not in selected_categories:
                continue
            
            # Equipment filter
            if selected_equipment:
                workout_equipment = workout.get('equipment', '').lower()
                equipment_match = any(
                    equipment.lower() in workout_equipment 
                    for equipment in selected_equipment
                )
                if not equipment_match:
                    continue
            
            # Tags filter
            if selected_tags:
                workout_tags = [tag.lower() for tag in workout.get('tags', [])]
                tags_match = any(
                    tag.lower() in workout_tags 
                    for tag in selected_tags
                )
                if not tags_match:
                    continue
            
            # Search filter
            if search_term:
                search_fields = [
                    workout.get('title', ''),
                    workout.get('workout', ''),
                    workout.get('notes', ''),
                    workout.get('equipment', '')
                ]
                search_text = ' '.join(search_fields).lower()
                if search_term.lower() not in search_text:
                    continue
            
            filtered.append(workout)
        
        return filtered
    
    def display_workout(self, workout: Dict, use_card_layout: bool = True):
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
    
    def run(self):
        """Run the main Streamlit app"""
        st.title("🏋️ WOD Browser")
        st.markdown("Browse, search, filter, and discover workout ideas from the WODs repository")
        
        if not self.workouts:
            st.error("No workout files found. Please check the ideas directory structure.")
            return
        
        # Create tabs for different features
        tab1, tab2, tab3 = st.tabs(["🔍 Browse Workouts", "📊 Statistics", "📡 RSS Feed Browser"])
        
        with tab1:
            self._display_workout_browser()
        
        with tab2:
            self.display_statistics()
        
        with tab3:
            self.display_rss_browser()
    
    def _display_workout_browser(self):
        """Display the main workout browsing interface"""
        # Sidebar filters
        st.sidebar.header("🔍 Filters")
        
        # Category filter - dynamically discover categories
        categories = self.get_unique_values('category')
        selected_categories = st.sidebar.multiselect(
            "Categories",
            categories,
            help="Filter by workout category"
        )
        
        # Equipment filter
        all_equipment = self.get_unique_values('equipment')
        selected_equipment = st.sidebar.multiselect(
            "Equipment",
            all_equipment,
            help="Filter by required equipment"
        )
        
        # Tags filter (if any tags exist)
        all_tags = self.get_unique_values('tags')
        selected_tags = []
        if all_tags:
            selected_tags = st.sidebar.multiselect(
                "Tags",
                all_tags,
                help="Filter by workout tags"
            )
        
        # Search box
        search_term = st.sidebar.text_input(
            "🔍 Search",
            placeholder="Search in title, workout, notes...",
            help="Case-insensitive keyword search"
        )
        
        # UI Options
        st.sidebar.header("🎨 Display Options")
        use_card_layout = st.sidebar.checkbox("Enhanced Card Layout", value=True)
        
        # Sorting options
        sort_options = ["None", "Title (A-Z)", "Title (Z-A)", "Category (A-Z)", "Category (Z-A)", "Time Cap (Low-High)", "Time Cap (High-Low)"]
        sort_selection = st.sidebar.selectbox("Sort by:", sort_options)
        
        # Clear filters button
        if st.sidebar.button("Clear All Filters"):
            st.rerun()
        
        # Filter workouts
        filtered_workouts = self.filter_workouts(
            selected_categories, selected_equipment, selected_tags, search_term
        )
        
        # Apply sorting
        if sort_selection != "None":
            if "Title" in sort_selection:
                filtered_workouts = self.sort_workouts(filtered_workouts, "title", "Z-A" in sort_selection)
            elif "Category" in sort_selection:
                filtered_workouts = self.sort_workouts(filtered_workouts, "category", "Z-A" in sort_selection)
            elif "Time Cap" in sort_selection:
                filtered_workouts = self.sort_workouts(filtered_workouts, "time_cap", "High-Low" in sort_selection)
        
        # Main content area header
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{len(filtered_workouts)} workouts found** (out of {len(self.workouts)} total)")
        
        with col2:
            # Random workout button
            if filtered_workouts:
                if st.button("🎲 Random Workout", type="primary"):
                    random_workout = random.choice(filtered_workouts)
                    st.session_state.show_random = random_workout
            else:
                st.warning("No workouts to choose from.")
        
        with col3:
            # Export button (placeholder for future feature)
            if filtered_workouts:
                st.button("📤 Export Results", disabled=True, help="Coming soon!")
        
        # Show random workout if selected
        if hasattr(st.session_state, 'show_random'):
            st.markdown("## 🎲 Random Workout Selection")
            self.display_workout(st.session_state.show_random, use_card_layout)
            if st.button("Clear Random Selection"):
                del st.session_state.show_random
                st.rerun()
            st.markdown("---")
        
        # Display filtered workouts
        if filtered_workouts:
            st.markdown("## 📋 All Matching Workouts")
            
            # Add pagination for large results
            items_per_page = 10
            total_pages = (len(filtered_workouts) - 1) // items_per_page + 1
            
            if total_pages > 1:
                page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
                start_idx = (page - 1) * items_per_page
                end_idx = start_idx + items_per_page
                page_workouts = filtered_workouts[start_idx:end_idx]
                st.markdown(f"*Showing {start_idx + 1}-{min(end_idx, len(filtered_workouts))} of {len(filtered_workouts)} workouts*")
            else:
                page_workouts = filtered_workouts
            
            for workout in page_workouts:
                self.display_workout(workout, use_card_layout)
        else:
            st.info("No workouts match your current filters. Try adjusting your selection.")

# Main app
if __name__ == "__main__":
    app = WODBrowser()
    app.run()