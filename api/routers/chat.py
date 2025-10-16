from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from loguru import logger

from api.models import (
    ChatSessionCreate,
    ChatSessionUpdate,
    ChatSessionResponse,
    ChatMessageCreate,
    ChatMessageResponse,
)
from open_notebook.domain.notebook import ChatSession, ChatMessage, Notebook
from open_notebook.exceptions import DatabaseOperationError, InvalidInputError

router = APIRouter()


@router.get("/notebooks/{notebook_id}/chat-sessions", response_model=List[ChatSessionResponse])
async def get_chat_sessions(notebook_id: str):
    """Get all chat sessions for a notebook (without messages for performance)."""
    try:
        # Verify notebook exists
        notebook = await Notebook.get(notebook_id)
        if not notebook:
            raise HTTPException(status_code=404, detail="Notebook not found")

        # Get chat sessions
        chat_sessions = await notebook.get_chat_sessions()
        
        # Convert to response format (without messages for performance)
        sessions_response = []
        for session in chat_sessions:
            sessions_response.append(
                ChatSessionResponse(
                    id=session.id,
                    title=session.title or "Untitled Chat",
                    created=str(session.created),
                    updated=str(session.updated),
                    messages=[],  # Don't load messages for list view
                )
            )
        
        return sessions_response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching chat sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching chat sessions: {str(e)}")


@router.post("/notebooks/{notebook_id}/chat-sessions", response_model=ChatSessionResponse)
async def create_chat_session(notebook_id: str, session_data: ChatSessionCreate):
    """Create a new chat session for a notebook."""
    try:
        # Verify notebook exists
        notebook = await Notebook.get(notebook_id)
        if not notebook:
            raise HTTPException(status_code=404, detail="Notebook not found")

        # Create chat session
        chat_session = ChatSession(title=session_data.title)
        await chat_session.save()
        
        # Relate to notebook
        await chat_session.relate_to_notebook(notebook_id)
        
        return ChatSessionResponse(
            id=chat_session.id,
            title=chat_session.title,
            created=str(chat_session.created),
            updated=str(chat_session.updated),
            messages=[],
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating chat session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating chat session: {str(e)}")


@router.get("/chat-sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(session_id: str):
    """Get a specific chat session with its messages."""
    try:
        chat_session = await ChatSession.get(session_id)
        if not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found")

        # Get messages
        messages = await chat_session.get_messages()
        messages_response = [
            ChatMessageResponse(
                id=msg.id,
                role=msg.role,
                mode=msg.mode,
                content=msg.content,
                created=str(msg.created),
            )
            for msg in messages
        ]
        
        return ChatSessionResponse(
            id=chat_session.id,
            title=chat_session.title or "Untitled Chat",
            created=str(chat_session.created),
            updated=str(chat_session.updated),
            messages=messages_response,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching chat session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching chat session: {str(e)}")


@router.put("/chat-sessions/{session_id}", response_model=ChatSessionResponse)
async def update_chat_session(session_id: str, session_data: ChatSessionUpdate):
    """Update a chat session."""
    try:
        chat_session = await ChatSession.get(session_id)
        if not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found")

        # Update fields
        if session_data.title is not None:
            chat_session.title = session_data.title
        
        await chat_session.save()
        
        # Get messages
        messages = await chat_session.get_messages()
        messages_response = [
            ChatMessageResponse(
                id=msg.id,
                role=msg.role,
                mode=msg.mode,
                content=msg.content,
                created=str(msg.created),
            )
            for msg in messages
        ]
        
        return ChatSessionResponse(
            id=chat_session.id,
            title=chat_session.title or "Untitled Chat",
            created=str(chat_session.created),
            updated=str(chat_session.updated),
            messages=messages_response,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating chat session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating chat session: {str(e)}")


@router.delete("/chat-sessions/{session_id}")
async def delete_chat_session(session_id: str):
    """Delete a chat session and all its messages."""
    try:
        chat_session = await ChatSession.get(session_id)
        if not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found")

        # Delete all messages first
        messages = await chat_session.get_messages()
        for message in messages:
            await message.delete()
        
        # Delete the session
        await chat_session.delete()
        
        return {"message": "Chat session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting chat session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting chat session: {str(e)}")


@router.post("/chat-sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def add_message_to_session(session_id: str, message_data: ChatMessageCreate):
    """Add a message to a chat session."""
    try:
        chat_session = await ChatSession.get(session_id)
        if not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found")

        # Create message
        message = ChatMessage(
            role=message_data.role,
            mode=message_data.mode,
            content=message_data.content,
            chat_session_id=session_id,
        )
        await message.save()
        
        # Relate to chat session
        await message.relate_to_chat_session(session_id)
        
        return ChatMessageResponse(
            id=message.id,
            role=message.role,
            mode=message.mode,
            content=message.content,
            created=str(message.created),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding message to chat session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding message to chat session: {str(e)}")
