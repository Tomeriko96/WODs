# WOD Browser - Modular Architecture

This document describes the modular architecture of the WOD Browser application, which has been refactored from a single monolithic file into a maintainable, organized structure.

## 📁 Project Structure

```
/
├── app.py                    # Main entry point (minimal)
├── requirements.txt          # Python dependencies
├── ideas/                    # Workout files directory
└── src/                      # Source code modules
    ├── __init__.py          # Package initialization
    ├── config.py            # Application configuration
    ├── parser/              # Workout file parsing
    │   ├── __init__.py
    │   └── workout_parser.py
    ├── browser/             # Main browsing functionality
    │   ├── __init__.py
    │   ├── wod_browser.py   # Main browser class
    │   └── filters.py       # Filtering and sorting logic
    ├── rss/                 # RSS feed handling
    │   ├── __init__.py
    │   └── rss_handler.py   # RSS parsing and GitHub integration
    ├── stats/               # Statistics and visualizations
    │   ├── __init__.py
    │   └── statistics.py    # Statistics generation
    └── ui/                  # User interface components
        ├── __init__.py
        ├── components.py    # Reusable UI components
        └── styling.py       # CSS styles and formatting
```

## 🏗️ Architecture Benefits

### Separation of Concerns
- **Parser**: Handles workout file parsing (.md and .txt formats)
- **Browser**: Core browsing functionality and coordination
- **RSS**: RSS feed integration and GitHub issue creation
- **Stats**: Statistics generation and visualization
- **UI**: Reusable user interface components

### Maintainability
- Each module has a single responsibility
- Easy to locate and modify specific functionality
- Reduced code duplication
- Clear interfaces between modules

### Testability
- Individual modules can be tested in isolation
- Mock dependencies easily for unit testing
- Clear separation makes debugging easier

### Scalability
- New features can be added as separate modules
- Existing modules can be extended without affecting others
- Easy to add new file formats, data sources, or UI components

## 📚 Module Details

### `src/config.py`
Central configuration management including:
- Streamlit page configuration
- Application constants and settings
- File handling settings
- GitHub repository information

### `src/parser/workout_parser.py`
Workout file parsing functionality:
- `WorkoutParser.parse_workout_file()` - Main parsing entry point
- Support for both .md and .txt formats
- Structured data extraction (title, equipment, time cap, etc.)

### `src/browser/wod_browser.py`
Main application class:
- `WODBrowser` - Central coordinator class
- File system scanning and workout loading
- Tab-based UI organization
- Integration with other modules

### `src/browser/filters.py`
Filtering and sorting functionality:
- `WorkoutFilter.filter_workouts()` - Multi-criteria filtering
- `WorkoutFilter.sort_workouts()` - Various sorting options
- `WorkoutFilter.get_unique_values()` - Extract filter options

### `src/rss/rss_handler.py`
RSS feed integration:
- `RSSHandler.parse_rss_feed()` - RSS feed parsing
- `RSSHandler.create_github_issue_url()` - GitHub integration
- `RSSHandler.display_rss_workout()` - RSS workout display

### `src/stats/statistics.py`
Statistics and visualizations:
- `StatisticsGenerator.get_workout_statistics()` - Data analysis
- `StatisticsGenerator.display_statistics()` - Chart generation
- Category, equipment, and tag distributions

### `src/ui/components.py`
Reusable UI components:
- `UIComponents.display_workout()` - Workout card display
- `UIComponents.display_filters_sidebar()` - Filter interface
- `UIComponents.display_pagination()` - Pagination controls

### `src/ui/styling.py`
CSS and styling utilities:
- Card styling functions
- HTML formatting helpers
- Consistent visual theme

## 🚀 Usage

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Extending the Application

#### Adding a New File Format
1. Extend `WorkoutParser` in `src/parser/workout_parser.py`
2. Add parsing logic for the new format
3. Update `SUPPORTED_EXTENSIONS` in `src/config.py`

#### Adding New Statistics
1. Extend `StatisticsGenerator` in `src/stats/statistics.py`
2. Add new statistical calculations
3. Create visualization components

#### Adding New UI Components
1. Add components to `src/ui/components.py`
2. Add styling helpers to `src/ui/styling.py`
3. Import and use in browser modules

#### Adding New Data Sources
1. Create a new module in `src/` (e.g., `src/api/`)
2. Implement data fetching and parsing
3. Integrate with the main browser class

## 🔧 Development Guidelines

### Code Organization
- Keep modules focused on single responsibilities
- Use clear, descriptive function and class names
- Include docstrings for all public methods
- Follow PEP 8 style guidelines

### Adding Dependencies
- Add new dependencies to `requirements.txt`
- Import dependencies within functions when possible
- Consider the impact on application startup time

### Error Handling
- Use try-catch blocks for file operations
- Display user-friendly error messages via Streamlit
- Log errors for debugging purposes

### Testing
- Test each module independently
- Mock external dependencies (file system, network)
- Test edge cases and error conditions

## 📈 Performance Considerations

### File Loading
- Workout files are loaded once at startup
- Results are cached in memory for fast filtering
- Consider implementing lazy loading for very large datasets

### UI Rendering
- Pagination limits the number of workouts displayed
- Card layout can be toggled for performance
- Statistics are calculated on-demand

### Memory Usage
- Raw file content is stored for each workout
- Consider removing raw content if memory is constrained
- Use generators for large datasets when possible

## 🎯 Future Enhancements

The modular architecture supports easy addition of:
- Database integration
- User authentication and personalization
- Workout rating and favorites
- Export functionality
- Mobile-responsive design
- API endpoints for external access
- Advanced search with Elasticsearch
- Workout recommendations based on user preferences