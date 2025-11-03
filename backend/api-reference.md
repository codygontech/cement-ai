# Backend API Reference

Complete REST API documentation for the JK Cement AI Optimization System.

---

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Authentication

Currently, the API uses simple client identification and rate limiting. Future versions will include:
- JWT token-based authentication
- OAuth 2.0 integration
- API key management

### Rate Limits

- **100 requests/minute** per IP address
- **10,000 AI tokens/day** per client
- Custom limits per endpoint

---

## AI Chat Endpoints

### POST `/ai-chat/chat`

Send a message to the AI agent and receive a response.

**Request Body:**
```json
{
  "message": "What is the current kiln temperature?",
  "session_id": "optional-session-id",
  "history": [
    {
      "role": "user",
      "content": "Previous message",
      "timestamp": "2025-11-03T10:00:00Z"
    }
  ]
}
```

**Response:**
```json
{
  "message": "The current kiln burning zone temperature is 1450°C, which is within the optimal range of 1400-1500°C.",
  "session_id": "session-123",
  "timestamp": "2025-11-03T10:00:00Z",
  "recommendations": [
    "Maintain current temperature",
    "Monitor oxygen levels"
  ]
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid request
- `429`: Rate limit exceeded
- `500`: Server error

---

### POST `/ai-chat/stream`

Stream AI responses in real-time.

**Request Body:**
```json
{
  "message": "Analyze the last 24 hours of kiln operations",
  "session_id": "optional-session-id"
}
```

**Response:** Server-Sent Events (SSE)
```
data: {"type": "token", "content": "Based"}
data: {"type": "token", "content": " on"}
data: {"type": "token", "content": " the"}
...
data: {"type": "complete", "message": "Full response"}
```

---

### WebSocket `/ai-chat/ws/{client_id}`

Real-time bidirectional communication with the AI agent.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ai-chat/ws/client-123');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'message',
    content: 'What is the current status?'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

**Message Types:**

Send:
```json
{
  "type": "message",
  "content": "Your message here"
}
```

Receive:
```json
{
  "type": "response",
  "content": "AI response",
  "timestamp": "2025-11-03T10:00:00Z"
}
```

---

### GET `/ai-chat/recommendations`

Get AI-generated recommendations for plant optimization.

**Query Parameters:**
- `process_area` (optional): Filter by process area
- `priority` (optional): Minimum priority level (1-5)
- `limit` (optional): Number of recommendations (default: 10)

**Response:**
```json
{
  "recommendations": [
    {
      "id": 1,
      "process_area": "kiln_operations",
      "priority": 5,
      "description": "Reduce coal feed rate by 5% to improve efficiency",
      "estimated_savings_kwh": 1500,
      "estimated_savings_cost": 15000,
      "timestamp": "2025-11-03T10:00:00Z"
    }
  ],
  "count": 10
}
```

---

## Data Endpoints

### GET `/data/raw-materials`

Get raw material feed data.

**Query Parameters:**
- `hours` (optional): Hours of historical data (default: 24)
- `limit` (optional): Maximum records (default: 100)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "timestamp": "2025-11-03T10:00:00Z",
      "limestone_feed_rate": 150.5,
      "clay_feed_rate": 45.2,
      "iron_ore_feed_rate": 12.8,
      "gypsum_feed_rate": 8.5,
      "moisture_content_pct": 2.5
    }
  ],
  "count": 100,
  "timestamp": "2025-11-03T10:00:00Z"
}
```

---

### GET `/data/kiln-operations`

Get kiln operations data.

**Query Parameters:**
- `hours` (optional): Hours of historical data (default: 24)
- `limit` (optional): Maximum records (default: 100)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "timestamp": "2025-11-03T10:00:00Z",
      "burning_zone_temp": 1450,
      "preheater_temp": 850,
      "cooler_temp": 120,
      "coal_feed_rate": 25.5,
      "alternative_fuel_rate": 5.2,
      "kiln_speed": 3.5,
      "feed_rate": 180,
      "clinker_production": 160,
      "o2_pct": 3.2,
      "co_ppm": 150,
      "nox_ppm": 450
    }
  ],
  "count": 100
}
```

---

### GET `/data/grinding-operations`

Get grinding operations data.

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "timestamp": "2025-11-03T10:00:00Z",
      "cement_mill_speed": 18.5,
      "separator_speed": 850,
      "clinker_feed_rate": 120,
      "gypsum_feed_rate": 8,
      "fineness_blaine": 3500,
      "residue_90_micron": 8.5,
      "power_consumption": 450,
      "cement_production": 110
    }
  ],
  "count": 100
}
```

---

### GET `/data/quality-metrics`

Get quality control metrics.

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "timestamp": "2025-11-03T10:00:00Z",
      "sample_id": "QC-2025-1103-001",
      "compressive_strength_3day": 18.5,
      "compressive_strength_7day": 28.2,
      "compressive_strength_28day": 45.8,
      "setting_time_initial_min": 125,
      "setting_time_final_min": 185,
      "consistency_pct": 28,
      "free_lime_pct": 1.2,
      "loss_on_ignition_pct": 2.5
    }
  ],
  "count": 100
}
```

---

### GET `/data/alternative-fuels`

Get alternative fuel usage data.

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "timestamp": "2025-11-03T10:00:00Z",
      "fuel_type": "Refuse Derived Fuel",
      "calorific_value_mj_kg": 18.5,
      "consumption_rate_tph": 5.2,
      "moisture_content_pct": 15,
      "chlorine_content_pct": 0.5,
      "cost_per_ton": 1200,
      "substitution_rate_pct": 25
    }
  ],
  "count": 100
}
```

---

## Analytics Endpoints

### GET `/analytics/efficiency`

Calculate process efficiency metrics.

**Query Parameters:**
- `process_type`: `raw_material`, `kiln`, `grinding`, `quality`
- `hours`: Hours of data to analyze (default: 24)

**Response:**
```json
{
  "process_type": "kiln",
  "period_hours": 24,
  "metrics": {
    "avg_temperature": 1445,
    "avg_coal_consumption": 25.2,
    "avg_production": 158.5,
    "efficiency_score": 87.5,
    "fuel_efficiency": 92.3
  },
  "recommendations": [
    "Consider reducing coal feed rate by 3%",
    "Optimize preheater temperature"
  ],
  "timestamp": "2025-11-03T10:00:00Z"
}
```

---

### GET `/analytics/trends`

Get trend analysis for specified metrics.

**Query Parameters:**
- `metric`: Metric name (e.g., `clinker_production`)
- `days`: Days to analyze (default: 7)
- `table`: Data table name

**Response:**
```json
{
  "metric": "clinker_production",
  "period_days": 7,
  "trend": {
    "direction": "increasing",
    "change_pct": 5.2,
    "avg_value": 158.5,
    "min_value": 145.2,
    "max_value": 172.8,
    "std_dev": 8.3
  },
  "data_points": [
    {"date": "2025-11-01", "value": 155.2},
    {"date": "2025-11-02", "value": 158.5},
    {"date": "2025-11-03", "value": 162.3}
  ]
}
```

---

### POST `/analytics/anomaly-detection`

Detect anomalies in process data.

**Request Body:**
```json
{
  "process_type": "kiln",
  "hours": 24,
  "threshold": 2.5
}
```

**Response:**
```json
{
  "anomalies_found": 3,
  "anomalies": [
    {
      "timestamp": "2025-11-03T08:15:00Z",
      "parameter": "burning_zone_temp",
      "value": 1520,
      "expected_range": [1400, 1500],
      "severity": "medium",
      "description": "Temperature spike detected"
    }
  ]
}
```

---

## Plant Locations Endpoints

### GET `/locations/plants`

Get all plant locations.

**Query Parameters:**
- `state` (optional): Filter by state
- `type` (optional): Filter by plant type
- `status` (optional): Filter by status

**Response:**
```json
{
  "plants": [
    {
      "id": 1,
      "plant_name": "JK Cement Nimbahera",
      "location": "Nimbahera, Rajasthan",
      "state": "Rajasthan",
      "latitude": 24.6238,
      "longitude": 74.6843,
      "capacity_mtpa": 2.7,
      "plant_type": "Integrated",
      "commissioning_year": 1975,
      "status": "Operational",
      "cement_types": ["OPC", "PPC", "PSC"]
    }
  ],
  "count": 10
}
```

---

### GET `/locations/plants/{plant_id}`

Get specific plant details.

**Response:**
```json
{
  "id": 1,
  "plant_name": "JK Cement Nimbahera",
  "location": "Nimbahera, Rajasthan",
  "state": "Rajasthan",
  "latitude": 24.6238,
  "longitude": 74.6843,
  "capacity_mtpa": 2.7,
  "plant_type": "Integrated",
  "commissioning_year": 1975,
  "status": "Operational",
  "cement_types": ["OPC", "PPC", "PSC"],
  "recent_metrics": {
    "production_today": 158.5,
    "efficiency": 87.5,
    "quality_score": 95.2
  }
}
```

---

### GET `/locations/stats`

Get aggregate statistics for all plants.

**Response:**
```json
{
  "total_plants": 10,
  "total_capacity_mtpa": 27.5,
  "avg_capacity_mtpa": 2.75,
  "operational_plants": 9,
  "by_state": {
    "Rajasthan": 3,
    "Gujarat": 2,
    "Andhra Pradesh": 2,
    "Uttar Pradesh": 3
  },
  "by_type": {
    "Integrated": 7,
    "Grinding Unit": 3
  }
}
```

---

## Vision API Endpoints

### POST `/vision/analyze-quality`

Analyze cement quality from image using Cloud Vision API.

**Request:** Multipart form data
- `file`: Image file (JPEG, PNG)
- `sample_id` (optional): Sample identifier
- `expected_grade` (optional): Expected cement grade

**Response:**
```json
{
  "analysis_id": "vision-2025-1103-001",
  "sample_id": "QC-001",
  "quality_score": 92.5,
  "color_consistency": 95.0,
  "defects_detected": 0,
  "analysis": {
    "dominant_color": "#C0C0C0",
    "color_variance": 0.05,
    "texture_score": 88.5,
    "uniformity": 94.2
  },
  "recommendations": [
    "Quality meets standards",
    "Color consistency excellent"
  ],
  "image_url": "gs://bucket/images/vision-2025-1103-001.jpg",
  "timestamp": "2025-11-03T10:00:00Z"
}
```

---

### GET `/vision/history`

Get history of vision API analyses.

**Query Parameters:**
- `limit` (optional): Maximum records (default: 50)
- `min_score` (optional): Minimum quality score filter

**Response:**
```json
{
  "analyses": [
    {
      "analysis_id": "vision-2025-1103-001",
      "sample_id": "QC-001",
      "quality_score": 92.5,
      "timestamp": "2025-11-03T10:00:00Z",
      "image_url": "gs://bucket/images/..."
    }
  ],
  "count": 50
}
```

---

## Health Check Endpoints

### GET `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-03T10:00:00Z",
  "version": "1.0.0",
  "database": "connected",
  "google_cloud": "connected"
}
```

---

### GET `/metrics`

Get API usage metrics.

**Response:**
```json
{
  "total_requests": 15432,
  "requests_last_hour": 523,
  "avg_response_time_ms": 125,
  "error_rate_pct": 0.5,
  "ai_tokens_used_today": 25000,
  "websocket_connections": 12
}
```

---

## Error Responses

All endpoints follow a consistent error format:

```json
{
  "error": "Error message",
  "detail": "Detailed error information",
  "status_code": 400,
  "timestamp": "2025-11-03T10:00:00Z"
}
```

### Common Status Codes

- **200**: Success
- **201**: Created
- **400**: Bad Request - Invalid parameters
- **401**: Unauthorized - Authentication required
- **403**: Forbidden - Insufficient permissions
- **404**: Not Found - Resource doesn't exist
- **429**: Too Many Requests - Rate limit exceeded
- **500**: Internal Server Error
- **503**: Service Unavailable

---

## Rate Limiting Headers

All API responses include rate limiting headers:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1699012800
```

---

## Pagination

For endpoints returning lists, use pagination parameters:

**Query Parameters:**
- `limit`: Records per page (default: 100, max: 1000)
- `offset`: Number of records to skip (default: 0)

**Response includes pagination metadata:**
```json
{
  "data": [...],
  "pagination": {
    "total": 1523,
    "limit": 100,
    "offset": 0,
    "has_more": true
  }
}
```

---

## CORS Configuration

Default CORS origins:
- `http://localhost:3000`
- `http://localhost:3001`

Configure additional origins via `CORS_ORIGINS` environment variable.

---

## Next Steps

- **[WebSocket API](../api/websocket.md)** - Real-time communication
- **[Authentication Guide](../api/authentication.md)** - Security implementation
- **[Backend Implementation](./overview.md)** - Backend architecture
- **[AI Agent Details](./ai-agent.md)** - LangGraph agent system

---

**Last Updated**: November 2025
