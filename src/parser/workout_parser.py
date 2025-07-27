"""
Workout file parser for .md and .txt files.
"""

import re
import streamlit as st
from pathlib import Path
from typing import Dict


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