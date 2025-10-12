import streamlit as st

def create_vscode_navigation():
    """Create VS Code-style navigation with activity bar and sidebar"""
    
    # VS Code-style CSS
    st.markdown("""
    <style>
    /* VS Code Dark Theme Colors */
    :root {
        --vscode-background: #1e1e1e;
        --vscode-sidebar-background: #252526;
        --vscode-activitybar-background: #333333;
        --vscode-titlebar-background: #3c3c3c;
        --vscode-text-foreground: #cccccc;
        --vscode-text-disabled: #6a6a6a;
        --vscode-border: #3c3c3c;
        --vscode-focus-border: #007acc;
        --vscode-button-background: #0e639c;
        --vscode-button-hover: #1177bb;
        --vscode-input-background: #3c3c3c;
        --vscode-input-foreground: #cccccc;
        --vscode-input-border: #3c3c3c;
    }
    
    /* Main container */
    .vscode-container {
        display: flex;
        height: 100vh;
        background-color: var(--vscode-background);
        color: var(--vscode-text-foreground);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Activity Bar */
    .activity-bar {
        width: 48px;
        background-color: var(--vscode-activitybar-background);
        border-right: 1px solid var(--vscode-border);
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 8px 0;
    }
    
    .activity-item {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 4px 0;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.2s;
        color: var(--vscode-text-disabled);
    }
    
    .activity-item:hover {
        background-color: var(--vscode-input-background);
    }
    
    .activity-item.active {
        background-color: var(--vscode-focus-border);
        color: white;
    }
    
    /* Sidebar */
    .sidebar {
        width: 300px;
        background-color: var(--vscode-sidebar-background);
        border-right: 1px solid var(--vscode-border);
        display: flex;
        flex-direction: column;
    }
    
    .sidebar-header {
        padding: 12px 16px;
        border-bottom: 1px solid var(--vscode-border);
        font-weight: 600;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--vscode-text-disabled);
    }
    
    .sidebar-content {
        flex: 1;
        padding: 8px 0;
        overflow-y: auto;
    }
    
    .sidebar-item {
        padding: 8px 16px;
        cursor: pointer;
        transition: background-color 0.2s;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .sidebar-item:hover {
        background-color: var(--vscode-input-background);
    }
    
    .sidebar-item.active {
        background-color: var(--vscode-focus-border);
        color: white;
    }
    
    /* Main content area */
    .main-content {
        flex: 1;
        background-color: var(--vscode-background);
        overflow: hidden;
    }
    
    /* Title bar */
    .title-bar {
        height: 35px;
        background-color: var(--vscode-titlebar-background);
        border-bottom: 1px solid var(--vscode-border);
        display: flex;
        align-items: center;
        padding: 0 16px;
        font-size: 13px;
        color: var(--vscode-text-foreground);
    }
    
    /* VS Code-style buttons */
    .vscode-button {
        background-color: var(--vscode-button-background);
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 2px;
        font-size: 13px;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .vscode-button:hover {
        background-color: var(--vscode-button-hover);
    }
    
    .vscode-button.secondary {
        background-color: transparent;
        color: var(--vscode-text-foreground);
        border: 1px solid var(--vscode-border);
    }
    
    .vscode-button.secondary:hover {
        background-color: var(--vscode-input-background);
    }
    
    /* VS Code-style inputs */
    .vscode-input {
        background-color: var(--vscode-input-background);
        color: var(--vscode-input-foreground);
        border: 1px solid var(--vscode-input-border);
        padding: 6px 8px;
        border-radius: 2px;
        font-size: 13px;
    }
    
    .vscode-input:focus {
        outline: none;
        border-color: var(--vscode-focus-border);
    }
    
    /* Hide Streamlit default elements */
    .main .block-container {
        padding: 0;
        max-width: none;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--vscode-sidebar-background);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--vscode-border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--vscode-text-disabled);
    }
    
    /* Navigation Menu */
    .nav-menu {
        background-color: #252526;
        border-bottom: 1px solid #3c3c3c;
        padding: 0;
        margin: 0;
        display: flex;
        align-items: center;
    }
    
    .nav-item {
        padding: 8px 16px;
        color: #cccccc;
        text-decoration: none;
        font-size: 13px;
        border: none;
        background: none;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .nav-item:hover {
        background-color: #3c3c3c;
        color: white;
    }
    
    .nav-item.active {
        background-color: #007acc;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def create_navigation_menu():
    """Create a horizontal navigation menu using Streamlit buttons"""
    # Create navigation buttons in a horizontal layout
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.switch_page("pages/1_🏠_Home.py")
    
    with col2:
        if st.button("📚 Notebooks", key="nav_notebooks", use_container_width=True):
            st.switch_page("pages/2_📒_Notebooks.py")
    
    with col3:
        if st.button("🔍 Search", key="nav_search", use_container_width=True):
            st.switch_page("pages/3_🔍_Ask_and_Search.py")
    
    with col4:
        if st.button("🤖 Models", key="nav_models", use_container_width=True):
            st.switch_page("pages/7_🤖_Models.py")
    
    with col5:
        if st.button("💱 Transformations", key="nav_transformations", use_container_width=True):
            st.switch_page("pages/8_💱_Transformations.py")
    
    with col6:
        if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
            st.switch_page("pages/10_⚙️_Settings.py")
    
    st.markdown("---")
