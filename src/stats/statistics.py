"""
Statistics generation and visualization for workout data.
"""

import re
import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, List


class StatisticsGenerator:
    """Generate and display workout statistics"""
    
    @staticmethod
    def get_workout_statistics(workouts: List[Dict]) -> Dict:
        """Generate comprehensive workout statistics"""
        if not workouts:
            return {}
        
        stats = {}
        
        # Category distribution
        category_counts = {}
        equipment_counts = {}
        tag_counts = {}
        time_cap_distribution = {}
        
        for workout in workouts:
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
        
        stats['total_workouts'] = len(workouts)
        stats['categories'] = dict(sorted(category_counts.items(), key=lambda x: x[1], reverse=True))
        stats['equipment'] = dict(sorted(equipment_counts.items(), key=lambda x: x[1], reverse=True)[:10])  # Top 10
        stats['tags'] = dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10])  # Top 10
        stats['time_caps'] = dict(sorted(time_cap_distribution.items(), key=lambda x: x[1], reverse=True)[:10])  # Top 10
        
        return stats
    
    @staticmethod
    def display_statistics(workouts: List[Dict]):
        """Display workout statistics with visualizations"""
        st.header("📊 Workout Statistics")
        
        stats = StatisticsGenerator.get_workout_statistics(workouts)
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