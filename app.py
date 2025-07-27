import streamlit as st
import os
import re
import random
from pathlib import Path
from typing import Dict, List, Optional

# Set page config
st.set_page_config(
    page_title="WOD Browser",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class WorkoutParser:
    """Parser for workout .md files"""
    
    @staticmethod
    def parse_workout_file(file_path: str, category: str) -> Dict:
        """Parse a single workout file and extract structured data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title (first line with #)
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else Path(file_path).stem
            
            # Extract fields using regex
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
            
        except Exception as e:
            st.error(f"Error parsing file {file_path}: {str(e)}")
            return None

class WODBrowser:
    """Main WOD Browser application"""
    
    def __init__(self):
        self.ideas_path = Path("/home/runner/work/WODs/WODs/ideas")
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
                
                # Process all .md files in the category
                for workout_file in category_dir.glob("*.md"):
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
    
    def display_workout(self, workout: Dict):
        """Display a single workout in a formatted way"""
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
        st.markdown("Browse, search, and filter workout ideas from the WODs repository")
        
        if not self.workouts:
            st.error("No workout files found. Please check the ideas directory structure.")
            return
        
        # Sidebar filters
        st.sidebar.header("🔍 Filters")
        
        # Category filter
        categories = ["bodyweight", "endurance", "mixed-modal", "strength"]
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
        
        # Clear filters button
        if st.sidebar.button("Clear All Filters"):
            st.rerun()
        
        # Filter workouts
        filtered_workouts = self.filter_workouts(
            selected_categories, selected_equipment, selected_tags, search_term
        )
        
        # Main content area
        col1, col2 = st.columns([3, 1])
        
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
        
        # Show random workout if selected
        if hasattr(st.session_state, 'show_random'):
            st.markdown("## 🎲 Random Workout Selection")
            self.display_workout(st.session_state.show_random)
            if st.button("Clear Random Selection"):
                del st.session_state.show_random
                st.rerun()
            st.markdown("---")
        
        # Display filtered workouts
        if filtered_workouts:
            st.markdown("## 📋 All Matching Workouts")
            for workout in filtered_workouts:
                self.display_workout(workout)
        else:
            st.info("No workouts match your current filters. Try adjusting your selection.")

# Main app
if __name__ == "__main__":
    app = WODBrowser()
    app.run()