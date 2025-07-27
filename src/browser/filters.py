"""
Workout filtering functionality.
"""

import re
from typing import Dict, List


class WorkoutFilter:
    """Handle workout filtering and sorting operations"""
    
    @staticmethod
    def get_unique_values(workouts: List[Dict], field: str) -> List[str]:
        """Get unique values for a specific field across all workouts"""
        values = set()
        for workout in workouts:
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
    
    @staticmethod
    def sort_workouts(workouts: List[Dict], sort_by: str, reverse: bool = False) -> List[Dict]:
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
    
    @staticmethod
    def filter_workouts(workouts: List[Dict], selected_categories: List[str], 
                       selected_equipment: List[str], selected_tags: List[str], 
                       search_term: str) -> List[Dict]:
        """Filter workouts based on selected criteria"""
        filtered = []
        
        for workout in workouts:
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