"""
AI Chat API Router for JK Cement
Handles conversational AI interactions with the JK Cement plant optimization agent
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import json

from app.agents.cement_agent import run_agent, generate_recommendations
from app.core.logging_config import logger
from app.core.simple_protection import (
    check_rate_limit,
    validate_message,
    track_cost,
    estimate_tokens,
    get_client_id,
    get_stats
)
from app.db.session import AsyncSessionLocal
from sqlalchemy import text

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message model"""
    role: str
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    session_id: Optional[str] = None
    history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    message: str
    session_id: str
    timestamp: str
    recommendations: List[str] = []


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, http_request: Request):
    """
    Send a message to the AI agent and get a response
    With simple rate limiting and validation
    """
    try:
        # Get client ID
        client_id = get_client_id(http_request)
        
        # Check rate limit
        allowed, error_msg = check_rate_limit(client_id)
        if not allowed:
            raise HTTPException(status_code=429, detail=error_msg)
        
        # Validate message
        is_valid, error_msg = validate_message(request.message)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Clean message
        message = request.message.strip()
        
        session_id = request.session_id or f"session_{datetime.now().timestamp()}"
        
        # Convert history to dict format (keep last 10 only for efficiency)
        history = []
        if request.history:
            history = [{"role": msg.role, "content": msg.content} for msg in request.history[-10:]]
        
        # Get response from agent
        response_content = ""
        async for chunk in run_agent(message, history):
            response_content += chunk
        
        # Generate context-aware recommendations
        recommendations = await generate_recommendations(message, response_content, history)
        
        # Track tokens and cost
        total_tokens = estimate_tokens(message + response_content)
        if not track_cost(client_id, total_tokens):
            raise HTTPException(status_code=429, detail="Daily cost limit reached. Please try again tomorrow.")
        
        # Save to database
        try:
            async with AsyncSessionLocal() as session:
                # Save user message
                await session.execute(
                    text("""
                        INSERT INTO chat_history (session_id, role, content, timestamp)
                        VALUES (:session_id, 'user', :content, NOW())
                    """),
                    {"session_id": session_id, "content": message}
                )
                
                # Save assistant response
                await session.execute(
                    text("""
                        INSERT INTO chat_history (session_id, role, content, timestamp)
                        VALUES (:session_id, 'assistant', :content, NOW())
                    """),
                    {"session_id": session_id, "content": response_content}
                )
                
                await session.commit()
        except Exception as e:
            logger.warning(f"Failed to save chat history: {e}")
        
        return ChatResponse(
            message=response_content,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream AI responses in real-time
    """
    async def generate():
        try:
            history = []
            if request.history:
                history = [{"role": msg.role, "content": msg.content} for msg in request.history]
            
            async for chunk in run_agent(request.message, history):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
                
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            logger.error(f"Error in streaming chat: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@router.websocket("/chat/ws")
async def chat_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat
    """
    await websocket.accept()
    session_id = f"ws_session_{datetime.now().timestamp()}"
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message = data.get("message", "")
            history = data.get("history", [])
            
            # Send acknowledgment
            await websocket.send_json({"type": "ack", "message": "Processing..."})
            
            # Stream response
            async for chunk in run_agent(message, history):
                await websocket.send_json({
                    "type": "chunk",
                    "content": chunk,
                    "session_id": session_id
                })
            
            # Send completion
            await websocket.send_json({"type": "done", "session_id": session_id})
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.send_json({"type": "error", "message": str(e)})


@router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str, limit: int = 50):
    """
    Retrieve chat history for a session
    """


@router.get("/chat/stats")
async def get_chat_stats():
    """
    Get simple usage statistics (for hackathon monitoring)
    """
    return get_stats()
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT role, content, timestamp
                    FROM chat_history
                    WHERE session_id = :session_id
                    ORDER BY timestamp ASC
                    LIMIT :limit
                """),
                {"session_id": session_id, "limit": limit}
            )
            
            rows = result.fetchall()
            
            history = [
                {
                    "role": row[0],
                    "content": row[1],
                    "timestamp": row[2].isoformat() if row[2] else None
                }
                for row in rows
            ]
            
            return {"session_id": session_id, "history": history}
            
    except Exception as e:
        logger.error(f"Error fetching chat history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
