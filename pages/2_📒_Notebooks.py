import streamlit as st
from humanize import naturaltime

from api.notebook_service import notebook_service
from api.notes_service import notes_service
from api.sources_service import sources_service
from open_notebook.domain.notebook import Notebook
from pages.stream_app.chat import chat_sidebar
from pages.stream_app.note import add_note, note_card
from pages.stream_app.source import add_source, source_card
from pages.stream_app.utils import setup_page, setup_stream_state
from pages.components.navigation import create_vscode_navigation, create_vscode_sidebar

setup_page("📒 Open Notebook", only_check_mandatory_models=True, sidebar_state="expanded")

# Handle navigation from sidebar
page_param = st.query_params.get("page")
if page_param:
    if page_param == "home":
        st.switch_page("pages/1_🏠_Home.py")
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

# Create navigation menu
create_vscode_sidebar()


def notebook_header(current_notebook: Notebook):
    """
    Defines the header of the notebook page, including the ability to edit the notebook's name and description.
    """
    c1, c2, c3 = st.columns([8, 2, 2])
    c1.header(current_notebook.name)
    if c2.button("Back to the list", icon="🔙"):
        st.session_state["current_notebook_id"] = None
        st.switch_page("pages/1_🏠_Home.py")

    if c3.button("Refresh", icon="🔄"):
        st.rerun()
    current_description = current_notebook.description
    with st.expander(
        current_notebook.description
        if len(current_description) > 0
        else "click to add a description"
    ):
        notebook_name = st.text_input("Name", value=current_notebook.name)
        notebook_description = st.text_area(
            "Description",
            value=current_description,
            placeholder="Add as much context as you can as this will be used by the AI to generate insights.",
        )
        c1, c2, c3 = st.columns([1, 1, 1])
        if c1.button("Save", icon="💾", key="edit_notebook"):
            current_notebook.name = notebook_name
            current_notebook.description = notebook_description
            notebook_service.update_notebook(current_notebook)
            st.rerun()
        if not current_notebook.archived:
            if c2.button("Archive", icon="🗃️"):
                current_notebook.archived = True
                notebook_service.update_notebook(current_notebook)
                st.toast("Notebook archived", icon="🗃️")
        else:
            if c2.button("Unarchive", icon="🗃️"):
                current_notebook.archived = False
                notebook_service.update_notebook(current_notebook)
                st.toast("Notebook unarchived", icon="🗃️")
        if c3.button("Delete forever", type="primary", icon="☠️"):
            notebook_service.delete_notebook(current_notebook)
            st.session_state["current_notebook_id"] = None
            st.rerun()


def notebook_page(current_notebook: Notebook):
    # Guarantees that we have an entry for this notebook in the session state
    if current_notebook.id not in st.session_state:
        st.session_state[current_notebook.id] = {"notebook": current_notebook}

    # sets up the active session
    current_session = setup_stream_state(
        current_notebook=current_notebook,
    )

    sources = sources_service.get_all_sources(notebook_id=current_notebook.id)
    notes = notes_service.get_all_notes(notebook_id=current_notebook.id)

    # NotebookLM-style header
    st.markdown("""
    <style>
        .notebook-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            color: white;
        }
        .notebook-title {
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .notebook-description {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        .back-button {
            background: rgba(255,255,255,0.2);
            border: none;
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;
            color: white;
            cursor: pointer;
            margin-bottom: 1rem;
        }
        .back-button:hover {
            background: rgba(255,255,255,0.3);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to notebooks", key="back_to_notebooks"):
        st.session_state["current_notebook_id"] = None
        st.switch_page("pages/1_🏠_Home.py")
        st.rerun()
    
    # Notebook header
    st.markdown(f"""
    <div class="notebook-header">
        <div class="notebook-title">{current_notebook.name}</div>
        <div class="notebook-description">{current_notebook.description or 'No description provided'}</div>
    </div>
    """, unsafe_allow_html=True)

    # Three-column layout like NotebookLM
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("### 📚 Sources")
        with st.container(border=True, height=600):
            if st.button("+ Add Source", key="add_source_btn"):
                add_source(current_notebook.id)
            st.markdown("---")
            for source in sources:
                source_card(source=source, notebook_id=current_notebook.id)
                st.markdown("---")

    with col2:
        st.markdown("### 📝 Notes")
        with st.container(border=True, height=600):
            if st.button("+ Write a Note", key="add_note_btn"):
                add_note(current_notebook.id)
            st.markdown("---")
            for note in notes:
                note_card(note=note, notebook_id=current_notebook.id)
                st.markdown("---")

    with col3:
        st.markdown("### 💬 Chat")
        with st.container(border=True, height=600):
            chat_sidebar(current_notebook=current_notebook, current_session=current_session)


def notebook_list_item(notebook):
    with st.container(border=True):
        st.subheader(notebook.name)
        st.caption(
            f"Created: {naturaltime(notebook.created)}, updated: {naturaltime(notebook.updated)}"
        )
        st.write(notebook.description)
        if st.button("Open", key=f"open_notebook_{notebook.id}"):
            st.session_state["current_notebook_id"] = notebook.id
            st.switch_page("pages/2_📒_Notebooks.py")


if "current_notebook_id" not in st.session_state:
    st.session_state["current_notebook_id"] = None

# Check if we're in create new mode
if st.session_state.get("create_new_notebook", False):
    st.title("📒 Create New Notebook")
    st.caption(
        "Notebooks are a great way to organize your thoughts, ideas, and sources. You can create notebooks for different research topics and projects, to create new articles, etc. "
    )

    with st.form("create_notebook_form"):
        new_notebook_title = st.text_input("New Notebook Name", placeholder="Enter notebook name")
        new_notebook_description = st.text_area(
            "Description",
            placeholder="Explain the purpose of this notebook. The more details the better.",
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Create Notebook", type="primary", use_container_width=True):
                if new_notebook_title:
                    notebook = notebook_service.create_notebook(
                        name=new_notebook_title, description=new_notebook_description
                    )
                    st.session_state["current_notebook_id"] = notebook.id
                    st.session_state["create_new_notebook"] = False
                    st.toast("Notebook created successfully", icon="📒")
                    st.rerun()
                else:
                    st.error("Please enter a notebook name")
        
        with col2:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state["create_new_notebook"] = False
                st.switch_page("pages/1_🏠_Home.py")
    
    st.stop()

# todo: get the notebook, check if it exists and if it's archived
if st.session_state["current_notebook_id"]:
    current_notebook: Notebook = notebook_service.get_notebook(st.session_state["current_notebook_id"])
    if not current_notebook:
        st.error("Notebook not found")
        st.stop()
    notebook_page(current_notebook)
    st.stop()

# If no notebook is selected and not creating new, redirect to home
st.switch_page("pages/1_🏠_Home.py")
