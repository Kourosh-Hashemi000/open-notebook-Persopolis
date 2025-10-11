import streamlit as st
from humanize import naturaltime
from datetime import datetime
import random

from api.notebook_service import notebook_service
from pages.stream_app.utils import setup_page

setup_page("NotebookLM", sidebar_state="collapsed")

# Custom CSS for NotebookLM-style interface
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header styling */
    .main-header {
        background-color: #1a1a1a;
        padding: 1rem 2rem;
        border-bottom: 1px solid #333;
        margin-bottom: 2rem;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .logo-icon {
        font-size: 1.5rem;
        color: #4CAF50;
    }
    
    .nav-tabs {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .nav-tab {
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .nav-tab.active {
        background-color: #1f77b4;
        color: white;
    }
    
    .nav-tab:hover {
        background-color: #333;
    }
    
    .header-controls {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-left: auto;
    }
    
    .notebook-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        position: relative;
        overflow: hidden;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .notebook-card:hover {
        transform: translateY(-2px);
    }
    
    .notebook-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        transform: translate(30px, -30px);
    }
    
    .notebook-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .notebook-meta {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .create-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .create-button:hover {
        transform: translateY(-1px);
    }
    
    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0 1rem 0;
    }
    
    .see-all-link {
        color: #1f77b4;
        text-decoration: none;
        font-weight: 500;
    }
    
    .see-all-link:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

def create_notebook_card(notebook, gradient_colors=None):
    """Create a NotebookLM-style notebook card"""
    if gradient_colors is None:
        gradients = [
            "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
            "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
            "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
            "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)",
            "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)"
        ]
        gradient = random.choice(gradients)
    else:
        gradient = gradient_colors
    
    # Get source count for the notebook
    from api.sources_service import sources_service
    sources = sources_service.get_all_sources(notebook_id=notebook.id)
    source_count = len(sources)
    
    # Format date
    if notebook.created:
        try:
            # Try to parse the date if it's a string
            if isinstance(notebook.created, str):
                from datetime import datetime
                created_date = datetime.fromisoformat(notebook.created.replace('Z', '+00:00')).strftime("%b %d, %Y")
            else:
                created_date = notebook.created.strftime("%b %d, %Y")
        except:
            created_date = "Unknown"
    else:
        created_date = "Unknown"
    
    # Create a clickable card using Streamlit columns
    col1, col2 = st.columns([1, 0.1])
    
    with col1:
        st.markdown(f"""
        <div class="notebook-card" style="background: {gradient};">
            <div class="notebook-title">{notebook.name}</div>
            <div class="notebook-meta">{created_date} • {source_count} sources</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("→", key=f"open_{notebook.id}", help=f"Open {notebook.name}"):
            st.session_state["current_notebook_id"] = notebook.id
            st.switch_page("pages/2_📒_Notebooks.py")

def main():
    # Header Section
    st.markdown("""
    <div class="main-header">
        <div class="logo-section">
            <span class="logo-icon">📒</span>
            <h1 style="margin: 0; color: white;">NotebookLM</h1>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="nav-tabs">
                <div class="nav-tab active">All</div>
                <div class="nav-tab">Featured notebooks</div>
                <div class="nav-tab">Shared with me</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create new button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("+ Create new", key="create_new_btn", type="primary", use_container_width=True):
            st.switch_page("pages/2_📒_Notebooks.py?create_new=true")
    
    # Check for create new action
    if st.query_params.get("create_new") == "true":
        st.switch_page("pages/2_📒_Notebooks.py")
        return
    
    # Check for notebook selection
    if st.query_params.get("notebook_id"):
        st.session_state["current_notebook_id"] = st.query_params.get("notebook_id")
        st.switch_page("pages/2_📒_Notebooks.py")
        return
    
    # Featured Notebooks Section
    st.markdown("""
    <div class="section-header">
        <h2 style="margin: 0; color: white;">Featured notebooks</h2>
        <a href="#" class="see-all-link">See all ></a>
    </div>
    """, unsafe_allow_html=True)
    
    # Get all notebooks
    notebooks = notebook_service.get_all_notebooks(order_by="updated desc")
    
    # Show featured notebooks (first 3)
    if notebooks:
        featured_col1, featured_col2, featured_col3 = st.columns(3)
        
        with featured_col1:
            if len(notebooks) > 0:
                create_notebook_card(notebooks[0], "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)")
        
        with featured_col2:
            if len(notebooks) > 1:
                create_notebook_card(notebooks[1], "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)")
        
        with featured_col3:
            if len(notebooks) > 2:
                create_notebook_card(notebooks[2], "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)")
    
    # Recent Notebooks Section
    st.markdown("""
    <div class="section-header">
        <h2 style="margin: 0; color: white;">Recent notebooks</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Show recent notebooks in a grid
    if notebooks:
        # Create a grid layout for recent notebooks
        cols = st.columns(3)
        for i, notebook in enumerate(notebooks[3:9]):  # Show up to 6 more notebooks
            with cols[i % 3]:
                create_notebook_card(notebook)
    
    # If no notebooks exist, show empty state
    if not notebooks:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; color: #666;">
            <h3>No notebooks yet</h3>
            <p>Create your first notebook to get started with NotebookLM</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
