import streamlit as st
from src.ui.components import UIComponents

def render_ui(app_logic):
    # Inject custom CSS for global style improvements
    st.markdown(
        '''<link href="https://fonts.googleapis.com/css2?family=Inter:wght@700;900&display=swap" rel="stylesheet">
        <link rel="icon" type="image/png" href="/favicon.ico">
        <style>
        /* App header band */
        .main > div:first-child { background: linear-gradient(90deg, #2EC4B6 0%, #4361ee 100%); border-radius: 0 0 24px 24px; padding: 2.5rem 2rem 1.5rem 2rem; margin-bottom: 2.5rem; }
        .main > div:first-child h1 { font-family: 'Inter', sans-serif; font-size: 2.6rem !important; font-weight: 900; letter-spacing: -1px; color: #fff; margin-bottom: 0.2em; }
        .main > div:first-child p { font-size: 1.18rem; color: #e0f7fa; }
        /* Section header band */
        .section-band { background: #f1f6fb; border-radius: 12px; padding: 0.7rem 1.2rem; margin-bottom: 1.5rem; font-size: 1.25rem; font-weight: 900; color: #4361ee; letter-spacing: 0.5px; border-left: 6px solid #2EC4B6; }
        /* Card improvements */
        .wod-card { background: #fff; border-radius: 22px; box-shadow: 0 6px 24px rgba(30,41,59,0.13); border: 2.5px solid #2EC4B6; margin-bottom: 36px; padding: 36px 36px 24px 36px; }
        .wod-title { font-family: 'Inter', sans-serif; font-size: 1.7rem; font-weight: 900; color: #22223b; margin-bottom: 0.7em; letter-spacing: -0.5px; }
        .wod-meta-label { font-weight: 800; color: #4361ee; font-size: 1.13em; }
        .wod-meta-value { font-weight: 700; color: #22223b; }
        .wod-section { margin-top: 1.3em; margin-bottom: 0.9em; font-size: 1.13em; font-weight: 800; color: #1976d2; }
        .wod-workout-list { margin-left: 1.4em; margin-bottom: 0.7em; }
        .wod-scaling { background: #e0f7fa; border-left: 6px solid #00b4d8; padding: 14px 20px; border-radius: 10px; margin: 0.8em 0 1.1em 0; color: #005f73; font-weight: 600; }
        .wod-notes { background: #fff3cd; border-left: 6px solid #ffd166; padding: 14px 20px; border-radius: 10px; margin: 0.8em 0 1.1em 0; color: #7c4700; font-weight: 600; }
        .wod-tags { margin-top: 0.4em; }
        .wod-tag { display: inline-block; background: #e1f5fe; color: #1976d2; border-radius: 16px; padding: 4px 14px; font-size: 1.05em; margin: 4px 8px 4px 0; font-weight: 800; box-shadow: 0 1px 4px rgba(67,97,238,0.08); border: 1.5px solid #b2e0fc; }
        /* Sidebar improvements */
        section[data-testid="stSidebar"] h2, .sidebar-section-header { font-size: 1.18rem; font-weight: 900; color: #1976d2; margin-top: 2.1em; margin-bottom: 0.7em; letter-spacing: 0.5px; }
        .sidebar-section { margin-bottom: 2.1em; }
        .sidebar-clear-btn button { background: #fff; color: #d32f2f; border: 2.5px solid #d32f2f; border-radius: 12px; font-weight: 900; padding: 10px 26px; margin-top: 14px; font-size: 1.13em; transition: background 0.2s, color 0.2s, box-shadow 0.2s; }
        .sidebar-clear-btn button:hover { background: #d32f2f; color: #fff; box-shadow: 0 2px 8px rgba(211,47,47,0.12); }
        .sidebar-section .stMultiSelect, .sidebar-section .stTextInput { margin-bottom: 1.2em; }
        /* Button polish */
        .stButton > button { border-radius: 12px !important; font-weight: 900; font-size: 1.13em; padding: 0.7em 2.2em; background: linear-gradient(90deg, #2EC4B6 0%, #4361ee 100%); color: #fff; border: none; transition: background 0.2s, color 0.2s, box-shadow 0.2s; }
        .stButton > button:hover { background: linear-gradient(90deg, #4361ee 0%, #2EC4B6 100%); color: #fff; box-shadow: 0 2px 8px rgba(67,97,238,0.12); }
        .secondary-btn { background: #fff !important; color: #4361ee !important; border: 2px solid #4361ee !important; border-radius: 12px !important; font-weight: 900 !important; font-size: 1.13em !important; padding: 0.7em 2.2em !important; margin-left: 1em; transition: background 0.2s, color 0.2s, box-shadow 0.2s !important; }
        .secondary-btn:hover { background: #4361ee !important; color: #fff !important; box-shadow: 0 2px 8px rgba(67,97,238,0.12) !important; }
        /* Empty state */
        .empty-state { text-align: center; color: #888; margin: 3em 0; font-size: 1.3em; }
        </style>''', unsafe_allow_html=True)

    # Colored band for main header
    st.markdown(f'<div class="section-band">{app_logic.APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(app_logic.APP_DESCRIPTION)

    # Navigation bar with color contrast and active tab highlight
    nav_tabs = ["Browse", "Favorites", "Stats"]
    if "active_tab" not in st.session_state:
        st.session_state["active_tab"] = nav_tabs[0]
    nav_html = '<div style="display:flex;gap:1.2em;margin-bottom:2em;">'
    for tab in nav_tabs:
        active = tab == st.session_state["active_tab"]
        nav_html += f'<div style="padding:0.7em 2em;border-radius:16px;font-weight:900;font-size:1.13em;cursor:pointer;background:{'#4361ee' if active else '#e1f5fe'};color:{'#fff' if active else '#4361ee'};box-shadow:{'0 2px 8px rgba(67,97,238,0.12)' if active else 'none'};border:2px solid #4361ee;margin-right:0.5em;" onclick="window.location.hash=\'{tab}\'">{tab}</div>'
    nav_html += '</div>'
    st.markdown(nav_html, unsafe_allow_html=True)
    # Update active tab from hash (simulate tab click)
    import streamlit_javascript
    tab_hash = streamlit_javascript.st_javascript("window.location.hash.substring(1)")
    if tab_hash in nav_tabs:
        st.session_state["active_tab"] = tab_hash

    st.markdown('<div class="section-band">All Matching Workouts</div>', unsafe_allow_html=True)

    # Action buttons row (Random Workout, Export Results)
    st.markdown('<div style="display:flex;justify-content:center;margin-bottom:2em;">', unsafe_allow_html=True)
    st.markdown('<style>.random-btn-large {font-size:1.45em !important;padding:1.2em 3.5em !important;border-radius:18px !important;background:linear-gradient(90deg,#2EC4B6 0%,#4361ee 100%) !important;color:#fff !important;font-weight:900 !important;box-shadow:0 4px 16px rgba(67,97,238,0.13) !important;margin-bottom:1em !important;}</style>', unsafe_allow_html=True)
    st.button("🎲 Random Workout", help="Show a random workout", key="random-btn", use_container_width=True, type="primary")
    st.markdown('<script>document.querySelector("button[data-testid=\'baseButton-random-btn\']").classList.add("random-btn-large")</script>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.button("⬇️ Export Results", help="Click to download workout list", key="export-btn")
    st.markdown('<style>.element-container button[data-testid="baseButton-export-btn"]{margin-left:0;}.element-container button[data-testid="baseButton-export-btn"].secondary-btn{margin-left:0;}</style>', unsafe_allow_html=True)

    # Sidebar filters
    categories = app_logic.get_categories()
    equipment = app_logic.get_equipment()
    tags = app_logic.get_tags()
    selected_categories, selected_equipment, selected_tags, search_term = UIComponents.display_filters_sidebar(categories, equipment, tags)
    use_card_layout, sort_selection = UIComponents.display_sorting_options()

    # Filter and sort workouts
    filtered_workouts = app_logic.filter_workouts(selected_categories, selected_equipment, selected_tags, search_term, sort_selection)
    total_workouts = len(filtered_workouts)
    start_idx, end_idx = UIComponents.display_pagination(total_workouts, app_logic.ITEMS_PER_PAGE)

    # Display active filter chips
    active_filters = []
    if selected_categories:
        active_filters += [f'<span class="wod-tag">{c}</span>' for c in selected_categories]
    if selected_equipment:
        active_filters += [f'<span class="wod-tag">{e}</span>' for e in selected_equipment]
    if selected_tags:
        active_filters += [f'<span class="wod-tag">{t}</span>' for t in selected_tags]
    if search_term:
        active_filters.append(f'<span class="wod-tag">🔍 {search_term}</span>')
    if active_filters:
        st.markdown('<div class="wod-tags">' + ' '.join(active_filters) + '</div>', unsafe_allow_html=True)

    # Display workouts or empty state
    if total_workouts == 0:
        st.markdown('''<div class="empty-state" style="display:flex;flex-direction:column;align-items:center;justify-content:center;">
            <div style="font-size:3.5rem;">🗂️</div>
            <div style="font-size:1.5rem;font-weight:700;margin-top:0.5em;">No workouts found</div>
            <div style="color:#888;margin-top:0.3em;">Try adjusting your filters or search terms.</div>
        </div>''', unsafe_allow_html=True)
    else:
        # Responsive grid: 2 columns on desktop, 1 on mobile
        import streamlit as st
        num_cols = 2
        try:
            from streamlit_javascript import st_javascript
            width = st_javascript("window.innerWidth")
            if width and isinstance(width, int) and width < 700:
                num_cols = 1
        except Exception:
            pass
        cols = st.columns(num_cols)
        for idx, workout in enumerate(filtered_workouts[start_idx:end_idx]):
            with cols[idx % num_cols]:
                UIComponents.display_workout(workout, use_card_layout=use_card_layout)

    # Optionally, add statistics or RSS browser
    # app_logic.display_statistics()
    # app_logic.display_rss_browser()
