import streamlit as st
from humanize import naturaltime
from datetime import datetime
import random

from api.notebook_service import notebook_service
from pages.stream_app.utils import setup_page
from pages.components.navigation import create_vscode_navigation, create_vscode_sidebar

# Try setting page config directly instead of using setup_page
st.set_page_config(
    page_title="Open Notebook",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Still need to check migration and auth
from pages.stream_app.utils import check_migration
from pages.stream_app.auth import check_password
check_password()
check_migration()

# Handle navigation from sidebar
page_param = st.query_params.get("page")
if page_param:
    if page_param == "notebooks":
        st.switch_page("pages/2_📒_Notebooks.py")
    elif page_param == "search":
        st.switch_page("pages/3_🔍_Ask_and_Search.py")
    elif page_param == "models":
        st.switch_page("pages/7_🤖_Models.py")
    elif page_param == "transformations":
        st.switch_page("pages/8_💱_Transformations.py")
    elif page_param == "settings":
        st.switch_page("pages/10_⚙️_Settings.py")

# Apply VS Code styling
create_vscode_navigation()

# Create VS Code sidebar layout
create_vscode_sidebar()

# Main content area - no wrapper div to avoid empty space

# Welcome section - simplified
st.title("📒 Open Notebook")
st.caption("Your AI-powered research and note-taking companion")

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
                
                # Create notebook card with darker blue gradient
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
                    padding: 16px;
                    border-radius: 8px;
                    color: white;
                    margin-bottom: 12px;
                    cursor: pointer;
                    transition: all 0.2s ease-in-out;
                    border: 1px solid #1e1b4b;
                    box-shadow: 0 2px 8px rgba(49, 46, 129, 0.2);
                " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 16px rgba(49, 46, 129, 0.4)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(49, 46, 129, 0.2)'">
                    <h4 style="margin: 0 0 6px 0; font-size: 1.1rem;">{notebook.name}</h4>
                    <p style="margin: 0 0 6px 0; opacity: 0.9; font-size: 0.9rem;">{notebook.description or 'No description'}</p>
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
    <div style="text-align: center; padding: 16px; background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); border-radius: 8px; margin: 4px; border: 1px solid #1e1b4b; box-shadow: 0 2px 8px rgba(49, 46, 129, 0.2);">
        <div style="font-size: 3rem; margin-bottom: 8px;">🤖</div>
        <h4 style="color: white; margin: 0 0 6px 0;">AI-Powered</h4>
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">Leverage advanced AI models for intelligent insights and content generation</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 16px; background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); border-radius: 8px; margin: 4px; border: 1px solid #1e1b4b; box-shadow: 0 2px 8px rgba(49, 46, 129, 0.2);">
        <div style="font-size: 3rem; margin-bottom: 8px;">📚</div>
        <h4 style="color: white; margin: 0 0 6px 0;">Organized</h4>
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">Keep your research organized with notebooks, sources, and notes</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 16px; background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); border-radius: 8px; margin: 4px; border: 1px solid #1e1b4b; box-shadow: 0 2px 8px rgba(49, 46, 129, 0.2);">
        <div style="font-size: 3rem; margin-bottom: 8px;">🔍</div>
        <h4 style="color: white; margin: 0 0 6px 0;">Searchable</h4>
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">Find information quickly with powerful search capabilities</p>
    </div>
    """, unsafe_allow_html=True)

# Removed wrapper div closing tags to eliminate empty space
