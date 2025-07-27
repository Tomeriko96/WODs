"""
CSS styles and HTML formatting utilities.
"""


class UIStyles:
    """Collection of CSS styles and HTML formatting utilities"""
    
    @staticmethod
    def get_card_style():
        """Get CSS for workout card styling"""
        return """
        <div style="
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            background-color: #fafafa;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
        """
    
    @staticmethod
    def get_workout_section_style():
        """Get CSS for workout description section"""
        return """
        <div style="
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
            margin: 10px 0;
        ">
        """
    
    @staticmethod
    def get_notes_section_style():
        """Get CSS for notes section"""
        return """
        <div style="
            background-color: #fff3e0;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #FF9800;
            margin: 10px 0;
        ">
        """
    
    @staticmethod
    def get_rss_card_style():
        """Get CSS for RSS workout entry"""
        return """
        <div style="
            border: 1px solid #2196F3;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            background-color: #e3f2fd;
        ">
        """
    
    @staticmethod
    def get_github_button_style():
        """Get CSS for GitHub issue creation button"""
        return """
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
        """
    
    @staticmethod
    def format_tag_badges(tags):
        """Format tags as HTML badges"""
        return " ".join([
            f'<span style="background-color: #e1f5fe; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; margin: 2px;">{tag}</span>' 
            for tag in tags
        ])