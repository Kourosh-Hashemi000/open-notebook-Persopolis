import streamlit as st
from humanize import naturaltime
from datetime import datetime
import random

from api.notebook_service import notebook_service
from pages.stream_app.utils import setup_page
from pages.components.navigation import create_vscode_navigation, create_navigation_menu

setup_page("Open Notebook", sidebar_state="collapsed")

# Apply VS Code styling
create_vscode_navigation()

# Create navigation menu
create_navigation_menu()

# Main content area
st.markdown("""
<div style="padding: 20px; background-color: #1e1e1e; min-height: 100vh;">
    <div style="max-width: 1200px; margin: 0 auto;">
""", unsafe_allow_html=True)

# Welcome section
st.markdown("""
<div style="text-align: center; margin-bottom: 40px;">
    <h1 style="color: #cccccc; font-size: 2.5rem; margin-bottom: 10px;">📒 Open Notebook</h1>
    <p style="color: #6a6a6a; font-size: 1.2rem;">Your AI-powered research and note-taking companion</p>
</div>
""", unsafe_allow_html=True)

# Quick actions
st.markdown("### Quick Actions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📚 Create Notebook", key="create_notebook_quick", use_container_width=True):
        st.session_state["create_new_notebook"] = True
        st.switch_page("pages/2_📒_Notebooks.py")

with col2:
    if st.button("🔍 Search", key="search_quick", use_container_width=True):
        st.switch_page("pages/3_🔍_Ask_and_Search.py")

with col3:
    if st.button("🤖 Models", key="models_quick", use_container_width=True):
        st.switch_page("pages/7_🤖_Models.py")

with col4:
    if st.button("⚙️ Settings", key="settings_quick", use_container_width=True):
        st.switch_page("pages/10_⚙️_Settings.py")

st.markdown("---")

# Recent notebooks section
st.markdown("### Recent Notebooks")

try:
    notebooks = notebook_service.get_all_notebooks(order_by="updated desc")
    
    if not notebooks:
        st.info("No notebooks found. Click 'Create Notebook' to get started!")
    else:
        # Display notebooks in a grid
        cols = st.columns(3)
        for i, notebook in enumerate(notebooks[:6]):  # Show max 6 notebooks
            with cols[i % 3]:
                # Get source count
                from api.sources_service import sources_service
                sources = sources_service.get_all_sources(notebook_id=notebook.id)
                source_count = len(sources)
                
                # Format date
                if notebook.created:
                    try:
                        if isinstance(notebook.created, str):
                            created_date = datetime.fromisoformat(notebook.created.replace('Z', '+00:00')).strftime("%b %d, %Y")
                        else:
                            created_date = notebook.created.strftime("%b %d, %Y")
                    except:
                        created_date = "Unknown"
                else:
                    created_date = "Unknown"
                
                # Create notebook card
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    border-radius: 8px;
                    color: white;
                    margin-bottom: 16px;
                    cursor: pointer;
                    transition: transform 0.2s ease-in-out;
                " onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                    <h4 style="margin: 0 0 8px 0; font-size: 1.1rem;">{notebook.name}</h4>
                    <p style="margin: 0 0 8px 0; opacity: 0.9; font-size: 0.9rem;">{notebook.description or 'No description'}</p>
                    <p style="margin: 0; font-size: 0.8rem; opacity: 0.8;">{created_date} • {source_count} sources</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Open", key=f"open_notebook_{notebook.id}", use_container_width=True):
                    st.session_state["current_notebook_id"] = notebook.id
                    st.switch_page("pages/2_📒_Notebooks.py")

except Exception as e:
    st.error(f"Error loading notebooks: {str(e)}")

# Features section
st.markdown("---")
st.markdown("### Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 3rem; margin-bottom: 10px;">🤖</div>
        <h4 style="color: #cccccc;">AI-Powered</h4>
        <p style="color: #6a6a6a;">Leverage advanced AI models for intelligent insights and content generation</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 3rem; margin-bottom: 10px;">📚</div>
        <h4 style="color: #cccccc;">Organized</h4>
        <p style="color: #6a6a6a;">Keep your research organized with notebooks, sources, and notes</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 3rem; margin-bottom: 10px;">🔍</div>
        <h4 style="color: #cccccc;">Searchable</h4>
        <p style="color: #6a6a6a;">Find information quickly with powerful search capabilities</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)