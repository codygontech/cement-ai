"""
JK Cement AI Optimization Agent using LangGraph and Google Gemini
Provides intelligent analysis, recommendations, and insights for JK Cement India plants
Optimized for Indian cement manufacturing standards and best practices
"""

from typing import List, Dict, Any, TypedDict, Annotated, AsyncGenerator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from pydantic import SecretStr
import asyncio
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.logging_config import logger
from sqlalchemy import text
from app.db.session import AsyncSessionLocal


class AgentState(TypedDict):
    """State for the agent graph"""
    messages: Annotated[List[BaseMessage], add_messages]
    context: Dict[str, Any]


# Initialize Gemini model with Google AI Studio (Free tier!)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.7,
    api_key=SecretStr(settings.GOOGLE_API_KEY) if settings.GOOGLE_API_KEY else None,
    convert_system_message_to_human=True,
)


# Define tools for the agent
@tool
async def get_realtime_plant_data(table_name: str, hours_back: int = 1, limit: int = 50) -> Dict[str, Any]:
    """
    Fetch real-time process data from the cement plant database.
    
    Args:
        table_name: The table to query (raw_material_feed, kiln_operations, grinding_operations, quality_control)
        hours_back: Number of hours of historical data to fetch
        limit: Maximum number of records to return
        
    Returns:
        Dictionary containing the fetched data
    """
    try:
        async with AsyncSessionLocal() as session:
            query = text(f"""
                SELECT * FROM {table_name}
                WHERE timestamp >= NOW() - INTERVAL '{hours_back} hours'
                ORDER BY timestamp DESC
                LIMIT {limit}
            """)
            
            result = await session.execute(query)
            rows = result.fetchall()
            columns = result.keys()
            
            data = [dict(zip(columns, row)) for row in rows]
            
            return {
                "table": table_name,
                "records_count": len(data),
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Error fetching plant data: {e}")
        return {"error": str(e)}


@tool
async def calculate_efficiency_metrics(process_type: str, hours_back: int = 24) -> Dict[str, Any]:
    """
    Calculate key efficiency metrics for cement plant processes.
    
    Args:
        process_type: Type of process (raw_material, kiln, grinding, quality)
        hours_back: Hours of data to analyze
        
    Returns:
        Calculated efficiency metrics and recommendations
    """
    try:
        async with AsyncSessionLocal() as session:
            if process_type == "kiln":
                query = text(f"""
                    SELECT 
                        AVG(burning_zone_temp) as avg_temp,
                        AVG(coal_feed_rate) as avg_coal,
                        AVG(alternative_fuel_rate) as avg_alt_fuel,
                        AVG(clinker_production) as avg_production,
                        AVG(o2_pct) as avg_o2
                    FROM kiln_operations
                    WHERE timestamp >= NOW() - INTERVAL '{hours_back} hours'
                """)
                result = await session.execute(query)
                data = result.fetchone()
                
                if data:
                    # Convert Decimal to float for calculations
                    avg_temp = float(data[0]) if data[0] else 0
                    avg_coal = float(data[1]) if data[1] else 0
                    avg_alt_fuel = float(data[2]) if data[2] else 0
                    avg_production = float(data[3]) if data[3] else 0
                    avg_o2 = float(data[4]) if data[4] else 0
                    
                    thermal_efficiency = (avg_production * 1.6) / (avg_coal + avg_alt_fuel) if (avg_coal + avg_alt_fuel) > 0 else 0
                    alt_fuel_rate = (avg_alt_fuel / (avg_coal + avg_alt_fuel) * 100) if (avg_coal + avg_alt_fuel) > 0 else 0
                    
                    return {
                        "process": "Kiln Operations",
                        "thermal_efficiency": round(thermal_efficiency, 2),
                        "alternative_fuel_rate_pct": round(alt_fuel_rate, 2),
                        "avg_temperature": round(avg_temp, 2),
                        "avg_production_tph": round(avg_production, 2),
                        "recommendations": [
                            f"Current alt fuel rate: {alt_fuel_rate:.1f}% - Target: >30%" if alt_fuel_rate < 30 else "Alt fuel rate optimal",
                            f"O2 level: {avg_o2:.1f}% - Target: 2-4%" if avg_o2 else "Check O2 sensors"
                        ]
                    }
            
            elif process_type == "grinding":
                query = text(f"""
                    SELECT 
                        AVG(power_consumption) as avg_power,
                        AVG(feed_rate) as avg_feed,
                        AVG(product_fineness) as avg_fineness
                    FROM grinding_operations
                    WHERE timestamp >= NOW() - INTERVAL '{hours_back} hours'
                """)
                result = await session.execute(query)
                data = result.fetchone()
                
                if data and data[1] and float(data[1]) > 0:
                    # Convert Decimal to float for calculations
                    avg_power = float(data[0]) if data[0] else 0
                    avg_feed = float(data[1]) if data[1] else 0
                    avg_fineness = float(data[2]) if data[2] else 0
                    
                    specific_energy = avg_power / avg_feed
                    
                    return {
                        "process": "Grinding Operations",
                        "specific_energy_kwh_per_ton": round(specific_energy, 2),
                        "avg_fineness": round(avg_fineness, 2),
                        "efficiency_score": max(0, min(100, (50 - specific_energy) * 2)),
                        "recommendations": [
                            "Energy consumption optimal" if specific_energy < 35 else f"High energy consumption: {specific_energy:.1f} kWh/t - Target: <35 kWh/t",
                            f"Fineness: {avg_fineness:.0f} cm²/g" if avg_fineness else "Check fineness measurements"
                        ]
                    }
            
            return {"process": process_type, "message": "Analysis completed"}
            
    except Exception as e:
        logger.error(f"Error calculating metrics: {e}")
        return {"error": str(e)}


@tool
async def get_ai_recommendations(module: str, limit: int = 10) -> Dict[str, Any]:
    """
    Retrieve AI-generated recommendations for a specific module.
    
    Args:
        module: The module to get recommendations for (kiln, grinding, quality, fuel, etc.)
        limit: Maximum number of recommendations to return
        
    Returns:
        List of AI recommendations with priorities and estimated savings
    """
    try:
        async with AsyncSessionLocal() as session:
            query = text("""
                SELECT 
                    recommendation_type,
                    description,
                    priority,
                    estimated_savings,
                    confidence_score,
                    timestamp
                FROM ai_recommendations
                WHERE module = :module
                ORDER BY timestamp DESC, priority DESC
                LIMIT :limit
            """)
            
            result = await session.execute(query, {"module": module, "limit": limit})
            rows = result.fetchall()
            
            recommendations = [
                {
                    "type": row[0],
                    "description": row[1],
                    "priority": row[2],
                    "estimated_savings": row[3],
                    "confidence": row[4],
                    "timestamp": row[5].isoformat() if row[5] else None
                }
                for row in rows
            ]
            
            return {
                "module": module,
                "recommendations": recommendations,
                "count": len(recommendations)
            }
    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}")
        return {"error": str(e)}


@tool
async def analyze_quality_trends(days_back: int = 7) -> Dict[str, Any]:
    """
    Analyze quality metrics trends over time.
    
    Args:
        days_back: Number of days to analyze
        
    Returns:
        Quality trend analysis and predictions
    """
    try:
        async with AsyncSessionLocal() as session:
            query = text(f"""
                SELECT 
                    AVG(compressive_strength_28d) as avg_strength,
                    AVG(fineness) as avg_fineness,
                    AVG(so3) as avg_so3,
                    COUNT(CASE WHEN status != 'Pass' THEN 1 END) as defect_count,
                    COUNT(*) as total_samples
                FROM quality_control
                WHERE timestamp >= NOW() - INTERVAL '{days_back} days'
            """)
            
            result = await session.execute(query)
            data = result.fetchone()
            
            if data:
                defect_rate = (data[3] / data[4] * 100) if data[4] > 0 else 0
                
                return {
                    "period_days": days_back,
                    "avg_compressive_strength_mpa": round(float(data[0]), 2) if data[0] else 0,
                    "avg_fineness_cm2_per_g": round(float(data[1]), 2) if data[1] else 0,
                    "avg_so3_pct": round(float(data[2]), 2) if data[2] else 0,
                    "defect_rate_pct": round(defect_rate, 2),
                    "total_samples": data[4],
                    "quality_status": "Excellent" if defect_rate < 1 else "Good" if defect_rate < 5 else "Needs Attention",
                    "recommendations": [
                        "Quality metrics within target range" if defect_rate < 1 else f"Defect rate at {defect_rate:.1f}% - investigate causes",
                        f"Strength: {data[0]:.1f} MPa - Target: >42.5 MPa" if data[0] else "Check strength testing",
                        f"Fineness: {data[1]:.0f} cm²/g - Target: 3200-3600 cm²/g" if data[1] else "Check fineness measurements"
                    ]
                }
            
            return {"message": "No quality data available for analysis"}
            
    except Exception as e:
        logger.error(f"Error analyzing quality trends: {e}")
        return {"error": str(e)}


# Define agent tools
tools = [
    get_realtime_plant_data,
    calculate_efficiency_metrics,
    get_ai_recommendations,
    analyze_quality_trends,
]

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)


def should_continue(state: AgentState):
    """Determine if the agent should continue or end"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # If there are no tool calls, end the conversation
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return "end"
    return "continue"


async def call_model(state: AgentState):
    """Call the model with the current state"""
    messages = state["messages"]
    
    # Add system message if not present
    if not messages or not isinstance(messages[0], SystemMessage):
        system_message = SystemMessage(content="""You are an expert AI assistant for JK Cement India plant optimization.

You specialize in optimizing cement manufacturing operations across JK Cement's plants in India, following Indian standards (IS 269, IS 4031, IS 12089) and best practices.

You have access to real-time plant data and can analyze:
- Raw material feed composition and quality (limestone, clay, iron ore, gypsum)
- Kiln operations and thermal efficiency (targeting 750-780 kcal/kg clinker)
- Grinding operations and energy consumption (targeting <30 kWh/ton)
- Quality control metrics for JK Super Cement, JK Lakshmi, and premium brands
- Alternative fuel utilization and TSR optimization (targeting >30% AFR)
- AI-generated recommendations for cost savings in INR

Your role is to:
1. Analyze current JK Cement plant operations using available tools
2. Identify optimization opportunities with savings estimated in Indian Rupees (₹)
3. Provide actionable recommendations following JK Cement's operational excellence standards
4. Ensure compliance with Indian environmental and quality standards
5. Support JK Cement's sustainability and cost reduction initiatives

Always use tools to fetch current data before making recommendations. Report all costs and savings in INR.
Focus on practical implementations suitable for JK Cement's operational context.""")
        messages = [system_message] + messages
    
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}


# Create the agent graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# Set entry point
workflow.set_entry_point("agent")

# Add edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

workflow.add_edge("tools", "agent")

# Compile the graph
agent_graph = workflow.compile()


async def run_agent(message: str, chat_history: List[Dict[str, str]] = None) -> AsyncGenerator[str, None]:
    """
    Run the agent with streaming response
    
    Args:
        message: User message
        chat_history: Previous conversation history
        
    Yields:
        Streamed response chunks
    """
    try:
        # Convert chat history to messages
        messages = []
        if chat_history:
            for msg in chat_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        
        # Add current message
        messages.append(HumanMessage(content=message))
        
        # Run the agent
        async for event in agent_graph.astream(
            {"messages": messages, "context": {}},
            stream_mode="values"
        ):
            if "messages" in event and event["messages"]:
                last_message = event["messages"][-1]
                if isinstance(last_message, AIMessage):
                    yield last_message.content
                    
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        yield f"Error: {str(e)}"


from typing import AsyncGenerator


async def generate_recommendations(message: str, response: str, chat_history: List[Dict[str, str]] = None) -> List[str]:
    """
    Generate context-aware follow-up recommendations based on the conversation.
    
    Args:
        message: User's last message
        response: AI's response
        chat_history: Previous conversation history
        
    Returns:
        List of recommended follow-up questions
    """
    try:
        # Build context from conversation
        context = f"User asked: {message}\nAI responded: {response[:500]}"  # Limit response length
        
        # Create a prompt for generating recommendations
        recommendation_prompt = f"""Based on this cement plant conversation:
{context}

Generate 5 short, specific follow-up questions (max 60 characters each) that would help the user:
1. Dive deeper into the current topic
2. Explore related plant operations
3. Get actionable insights
4. Optimize different processes
5. Check other important metrics

Format: Return ONLY the questions, one per line, without numbering or extra text."""

        # Use the LLM to generate recommendations
        messages = [HumanMessage(content=recommendation_prompt)]
        response_msg = await llm.ainvoke(messages)
        
        # Parse the recommendations
        recommendations = [
            q.strip() 
            for q in response_msg.content.strip().split('\n') 
            if q.strip() and len(q.strip()) > 10
        ][:5]  # Limit to 5 recommendations
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        # Return default recommendations as fallback
        return [
            "What's the current kiln efficiency?",
            "Show me quality metrics",
            "Check for process anomalies",
            "Analyze grinding operations",
            "What are optimization opportunities?"
        ]

