
# WOD Ideas Repository & 🏋️ WOD Browser App


A simple, well-organized collection of **Workout of the Day (WOD) ideas** for fitness enthusiasts, trainers, and athletes. Now featuring a modern **Streamlit web app** for browsing, searching, and filtering workouts! This repository is strictly for storing and sharing workout ideas, not for logging completed workouts or tracking personal fitness history.
## 🚀 WOD Browser App (Streamlit)

Browse, search, and filter all WOD ideas in a beautiful web interface!

### Quick Start

1. **Install dependencies** (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the app:**
   ```bash
   streamlit run main.py
   ```
3. Open your browser to the URL shown (usually http://localhost:8501)

### Features
- Browse all workouts by category, equipment, tags, and search
- Enhanced card layout for easy reading
- Filter and sort workouts
- Pagination for large collections
- (Optional) View statistics and RSS feed browser

### Project Structure (App Code)

```
main.py              # App entry point (orchestrates everything)
src/
  app.py             # App logic: data loading, filtering, sorting
  ui.py              # UI orchestration: layout, page structure
  ui/components.py   # Reusable UI components (cards, filters, etc.)
  config.py          # App configuration
  ...
```


## 🎯 Purpose

This repository serves as a shared resource where the fitness community can:
- **Browse** inspiring WOD ideas organized by category and type
- **Discover** new workout variations and challenges
- **Contribute** creative workout ideas for others to enjoy
- **Find** workouts suitable for different fitness levels and equipment availability


## 📂 Repository Structure (WOD Ideas)

```
/
├── README.md           # This file - explains purpose and usage
├── LICENSE             # Content license information
└── ideas/              # WOD idea files organized by category
    ├── endurance/      # Cardio and endurance-focused workouts
    ├── strength/       # Strength and power-focused workouts
    ├── mixed-modal/    # Mixed workouts combining multiple fitness domains
    └── bodyweight/     # Bodyweight-only workouts (no equipment needed)
```

## 🏋️ Browse WOD Ideas

Find workout inspiration in the `ideas/` folder! Each category has its own directory with individual WOD files:

- **[Endurance](ideas/endurance/)** - Cardio-focused workouts for building aerobic capacity
- **[Strength](ideas/strength/)** - Power and strength-focused workouts
- **[Mixed-Modal](ideas/mixed-modal/)** - Workouts combining strength, cardio, and skill
- **[Bodyweight](ideas/bodyweight/)** - No equipment needed - perfect for home workouts


## 🤝 Contributing

### Add a WOD Idea

We welcome new workout ideas! Here's how to contribute:

1. **Choose the right category** - Add your idea as a new file in the appropriate directory under `ideas/`
2. **Create a new file** - Name it descriptively (e.g., `my-awesome-workout.md`) in the category folder
3. **Follow the format** - Use the existing format for consistency:
   ```markdown
   # [Your Creative Workout Name]

   **Equipment:** [List equipment needed, or "None" for bodyweight]
   **Time Cap:** [Suggested time limit, if applicable]
   **Scaling:** [Brief scaling options for different fitness levels]

   **Workout:**
   - [Exercise 1 with reps/time]
   - [Exercise 2 with reps/time]
   - [Additional exercises...]

   **Notes:** [Any additional tips or variations]
   ```
4. **Submit a pull request** - Describe your new WOD idea in the PR
5. **Be creative** - Original workout names and creative combinations are encouraged!


### Contribute to the App

Pull requests for UI/UX improvements, bug fixes, or new features are welcome! Please keep logic, UI, and configuration in their respective modules as described above.

---
## 📝 License

This repository is licensed under the [Creative Commons Attribution 4.0 International License](LICENSE). You are free to use, share, and adapt these workout ideas with proper attribution.

## 🏷️ Topics

`workout-ideas` `WOD` `fitness` `crossfit` `exercise` `training`

---

**Disclaimer:** Always consult with a healthcare provider before starting any new exercise program. Modify workouts according to your fitness level and any physical limitations.