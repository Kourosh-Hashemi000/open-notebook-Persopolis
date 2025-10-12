import streamlit as st

def create_vscode_navigation():
    """Create VS Code-style navigation with activity bar and sidebar"""
    
    # VS Code-style CSS
    st.markdown("""
    <style>
    /* VS Code Dark Theme Colors with Darker Blue Hue */
    :root {
        --vscode-background: #0f0f23;
        --vscode-sidebar-background: #0a0a1a;
        --vscode-activitybar-background: #050510;
        --vscode-titlebar-background: #0d0d1f;
        --vscode-text-foreground: #c7d2fe;
        --vscode-text-disabled: #4c4c6a;
        --vscode-border: #1e1b4b;
        --vscode-focus-border: #312e81;
        --vscode-button-background: #1e1b4b;
        --vscode-button-hover: #312e81;
        --vscode-input-background: #1e1b4b;
        --vscode-input-foreground: #c7d2fe;
        --vscode-input-border: #1e1b4b;
    }
    
    /* Main container with collapsible sidebar */
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
        position: fixed;
        left: 0;
        top: 0;
        height: 100vh;
        z-index: 1000;
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
    
    /* Collapsible Sidebar */
    .sidebar {
        width: 300px;
        background-color: var(--vscode-sidebar-background);
        border-right: 1px solid var(--vscode-border);
        display: flex;
        flex-direction: column;
        position: fixed;
        left: 48px;
        top: 0;
        height: 100vh;
        z-index: 999;
        transition: transform 0.3s ease;
        transform: translateX(0);
    }
    
    .sidebar.collapsed {
        transform: translateX(-100%);
    }
    
    .sidebar-header {
        padding: 12px 16px;
        border-bottom: 1px solid var(--vscode-border);
        font-weight: 600;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--vscode-text-disabled);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .sidebar-toggle {
        background: none;
        border: none;
        color: var(--vscode-text-disabled);
        cursor: pointer;
        padding: 4px;
        border-radius: 2px;
        transition: background-color 0.2s;
    }
    
    .sidebar-toggle:hover {
        background-color: var(--vscode-input-background);
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
        color: var(--vscode-text-foreground);
        text-decoration: none;
    }
    
    .sidebar-item:hover {
        background-color: var(--vscode-input-background);
    }
    
    .sidebar-item.active {
        background-color: var(--vscode-focus-border);
        color: white;
    }
    
    /* Main content area with sidebar offset */
    .main-content {
        flex: 1;
        background-color: var(--vscode-background);
        overflow: hidden;
        margin-left: 48px;
        transition: margin-left 0.3s ease;
    }
    
    .main-content.sidebar-expanded {
        margin-left: 348px;
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
    
    /* Remove empty space at top */
    .main .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    .stApp > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    .stApp .main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Force sidebar to be visible - multiple selectors */
    .stSidebar,
    [data-testid="stSidebar"],
    .css-1d391kg,
    .css-1cypcdb,
    .css-17eq0hr {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        background-color: var(--vscode-sidebar-background) !important;
        border-right: 1px solid var(--vscode-border) !important;
    }
    
    /* Ensure sidebar container is visible */
    .stApp > div:first-child {
        display: flex !important;
    }
    
    /* Make sure sidebar takes up space */
    .stSidebar {
        width: 300px !important;
        min-width: 300px !important;
    }
    
    .css-1d391kg .stButton > button {
        background-color: transparent;
        color: var(--vscode-text-foreground);
        border: 1px solid transparent;
        border-radius: 4px;
        margin: 2px 0;
        width: 100%;
        text-align: left;
        padding: 8px 12px;
        transition: all 0.2s ease;
    }
    
    .css-1d391kg .stButton > button:hover {
        background-color: var(--vscode-input-background);
        border-color: var(--vscode-border);
        transform: translateX(2px);
    }
    
    /* Remove margins and gaps */
    .element-container {
        margin: 0;
        padding: 0;
    }
    
    .stButton > button {
        margin: 0;
        border-radius: 4px;
        border: 1px solid var(--vscode-border);
        background-color: var(--vscode-button-background);
        color: var(--vscode-text-foreground);
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: var(--vscode-button-hover);
        border-color: var(--vscode-focus-border);
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    /* Style input elements with blue hue */
    .stTextInput > div > div > input {
        background-color: var(--vscode-input-background);
        color: var(--vscode-input-foreground);
        border: 1px solid var(--vscode-input-border);
        border-radius: 4px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--vscode-focus-border);
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
    
    /* Style text areas */
    .stTextArea > div > div > textarea {
        background-color: var(--vscode-input-background);
        color: var(--vscode-input-foreground);
        border: 1px solid var(--vscode-input-border);
        border-radius: 4px;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--vscode-focus-border);
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
    
    /* Style select boxes */
    .stSelectbox > div > div > div {
        background-color: var(--vscode-input-background);
        color: var(--vscode-input-foreground);
        border: 1px solid var(--vscode-input-border);
        border-radius: 4px;
    }
    
    /* Style containers with blue hue */
    .stContainer {
        background-color: var(--vscode-sidebar-background);
        border: 1px solid var(--vscode-border);
        border-radius: 6px;
        padding: 12px;
        margin: 4px 0;
    }
    
    /* Style tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--vscode-sidebar-background);
        border-bottom: 1px solid var(--vscode-border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: var(--vscode-text-foreground);
        border: none;
        border-radius: 4px 4px 0 0;
        margin-right: 2px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--vscode-button-background);
        color: white;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--vscode-input-background);
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
    
    /* Navigation Menu with Blue Hue */
    .nav-menu {
        background-color: var(--vscode-sidebar-background);
        border-bottom: 1px solid var(--vscode-border);
        padding: 0;
        margin: 0;
        display: flex;
        align-items: center;
    }
    
    .nav-item {
        padding: 8px 16px;
        color: var(--vscode-text-foreground);
        text-decoration: none;
        font-size: 13px;
        border: none;
        background: none;
        cursor: pointer;
        transition: all 0.2s ease;
        border-radius: 4px;
        margin: 2px;
    }
    
    .nav-item:hover {
        background-color: var(--vscode-input-background);
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
    }
    
    .nav-item.active {
        background-color: var(--vscode-button-background);
        color: white;
        box-shadow: 0 2px 8px rgba(49, 46, 129, 0.4);
    }
    
    /* JavaScript for sidebar toggle */
    </style>
    
    <script>
    function toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        const mainContent = document.querySelector('.main-content');
        
        if (sidebar && mainContent) {
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('sidebar-expanded');
        }
    }
    
    // Initialize sidebar state - removed problematic code that was hiding sidebar
    </script>
    """, unsafe_allow_html=True)

def create_vscode_sidebar():
    """Create VS Code-style collapsible sidebar using Streamlit components"""
    # Create a sidebar with navigation
    with st.sidebar:
        st.markdown("### 📁 EXPLORER")
        st.markdown("---")
        
        # Navigation buttons with VS Code styling
        nav_items = [
            ("🏠", "Home", "pages/1_🏠_Home.py", "sidebar_home"),
            ("📚", "Notebooks", "pages/2_📒_Notebooks.py", "sidebar_notebooks"),
            ("🔍", "Search", "pages/3_🔍_Ask_and_Search.py", "sidebar_search"),
            ("🤖", "Models", "pages/7_🤖_Models.py", "sidebar_models"),
            ("💱", "Transformations", "pages/8_💱_Transformations.py", "sidebar_transformations"),
            ("⚙️", "Settings", "pages/10_⚙️_Settings.py", "sidebar_settings")
        ]
        
        for icon, name, page, key in nav_items:
            if st.button(f"{icon} {name}", key=key, use_container_width=True):
                st.switch_page(page)

def close_vscode_layout():
    """Close the VS Code layout - no longer needed with simplified approach"""
    pass

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

def close_vscode_layout():
    """Close the VS Code layout"""
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
