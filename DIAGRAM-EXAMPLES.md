# System Architecture Diagrams

Visual documentation of the JK Cement AI system architecture, data flows, and components.

---

## System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        A[Web Browser]
        B[Mobile Device]
    end
    
    subgraph "Application Layer - Frontend"
        C[Next.js 15<br/>React 19]
        C1[App Router]
        C2[Server Components]
        C3[Client Components]
        C --> C1
        C --> C2
        C --> C3
    end
    
    subgraph "Application Layer - Backend"
        D[FastAPI Backend]
        D1[API Routers]
        D2[Business Logic]
        D3[LangGraph Agent]
        D --> D1
        D --> D2
        D --> D3
    end
    
    subgraph "Google Cloud Platform"
        E[(Cloud SQL<br/>PostgreSQL)]
        F[Cloud Storage<br/>Buckets]
        G[Vertex AI<br/>Gemini 2.0]
        H[Cloud Vision<br/>API]
        I[Cloud Logging]
    end
    
    A --> C
    B --> C
    C --> D
    D --> D3
    D3 --> E
    D3 --> F
    D3 --> G
    D --> H
    D --> I
    
    style C fill:#4285F4,stroke:#1967D2,stroke-width:2px,color:#fff
    style D fill:#4285F4,stroke:#1967D2,stroke-width:2px,color:#fff
    style D3 fill:#FFA000,stroke:#F57C00,stroke-width:2px,color:#fff
    style G fill:#34A853,stroke:#137333,stroke-width:2px,color:#fff
    style E fill:#34A853,stroke:#137333,stroke-width:2px,color:#fff
```

---

## Data Flow - AI Chat

```mermaid
sequenceDiagram
    participant U as User
    participant F as Next.js Frontend
    participant A as FastAPI Backend
    participant L as LangGraph Agent
    participant G as Gemini 2.0
    participant D as Cloud SQL
    
    U->>F: Enter query: "What is kiln temp?"
    F->>A: POST /ai-chat/chat
    A->>L: run_agent(query)
    L->>L: Analyze intent
    L->>G: Request LLM reasoning
    G-->>L: Tool: get_realtime_data
    L->>D: SELECT * FROM kiln_operations
    D-->>L: Latest data
    L->>G: Generate response with data
    G-->>L: Formatted answer
    L-->>A: Stream response
    A-->>F: SSE stream
    F-->>U: Display: "Temp is 1450°C ✅"
    
    Note over L,G: LangGraph orchestrates<br/>multi-step reasoning
```

---

## AI Agent State Machine

```mermaid
stateDiagram-v2
    [*] --> ReceiveQuery
    ReceiveQuery --> AnalyzeIntent
    AnalyzeIntent --> SelectTools
    
    SelectTools --> FetchData: Need data
    SelectTools --> Calculate: Need computation
    SelectTools --> Generate: Direct response
    
    FetchData --> ProcessResults
    Calculate --> ProcessResults
    
    ProcessResults --> Generate
    Generate --> StreamResponse
    StreamResponse --> [*]
    
    note right of AnalyzeIntent
        Gemini 2.0 determines
        which tools to use
    end note
    
    note right of FetchData
        Query Cloud SQL
        Get real-time data
    end note
```

---

## Database Schema

```mermaid
erDiagram
    RAW_MATERIAL_FEED ||--o{ KILN_OPERATIONS : feeds
    KILN_OPERATIONS ||--o{ GRINDING_OPERATIONS : produces_clinker
    GRINDING_OPERATIONS ||--o{ QUALITY_METRICS : produces_cement
    KILN_OPERATIONS ||--o{ QUALITY_METRICS : quality_tested
    ALTERNATIVE_FUELS ||--o{ KILN_OPERATIONS : used_in
    
    RAW_MATERIAL_FEED {
        int id PK
        timestamp timestamp
        float limestone_feed_rate
        float clay_feed_rate
        float iron_ore_feed_rate
        float moisture_content_pct
    }
    
    KILN_OPERATIONS {
        int id PK
        timestamp timestamp
        float burning_zone_temp
        float coal_feed_rate
        float alternative_fuel_rate
        float clinker_production
        float o2_pct
        int co_ppm
        int nox_ppm
    }
    
    GRINDING_OPERATIONS {
        int id PK
        timestamp timestamp
        float cement_mill_speed
        float separator_speed
        float fineness_blaine
        float power_consumption
        float cement_production
    }
    
    QUALITY_METRICS {
        int id PK
        timestamp timestamp
        string sample_id
        float compressive_strength_3day
        float compressive_strength_28day
        float setting_time_initial
        float consistency_pct
    }
    
    ALTERNATIVE_FUELS {
        int id PK
        timestamp timestamp
        string fuel_type
        float calorific_value
        float consumption_rate
        float substitution_rate_pct
    }
    
    AI_RECOMMENDATIONS {
        int id PK
        timestamp timestamp
        string process_area
        int priority_level
        string description
        float estimated_savings_kwh
    }
```

---

## Component Hierarchy - Frontend

```mermaid
graph TD
    A[cement-plant-app.tsx] --> B[main-layout.tsx]
    B --> C[header.tsx]
    B --> D[sidebar.tsx]
    B --> E[Module Content]
    
    E --> F[executive-dashboard.tsx]
    E --> G[ai-chat.tsx]
    E --> H[kiln-operations.tsx]
    E --> I[quality-control.tsx]
    E --> J[plant-locations.tsx]
    
    G --> K[use-api-data hook]
    H --> K
    I --> K
    
    K --> L[api-client.ts]
    L --> M[FastAPI Backend]
    
    style A fill:#4285F4,color:#fff
    style B fill:#4285F4,color:#fff
    style G fill:#FFA000,color:#fff
    style K fill:#34A853,color:#fff
    style L fill:#34A853,color:#fff
```

---

## Deployment Architecture - Cloud Run

```mermaid
graph TB
    subgraph "Internet"
        A[Users]
    end
    
    subgraph "Google Cloud - Global"
        B[Cloud Load Balancer]
        C[Cloud CDN]
    end
    
    subgraph "Google Cloud - asia-south1"
        D[Cloud Run - Frontend<br/>Next.js Container]
        E[Cloud Run - Backend<br/>FastAPI Container]
        F[(Cloud SQL<br/>PostgreSQL)]
        G[Cloud Storage<br/>Images & Data]
    end
    
    subgraph "Google Cloud - AI Services"
        H[Vertex AI<br/>Gemini 2.0]
        I[Cloud Vision API]
    end
    
    subgraph "Observability"
        J[Cloud Logging]
        K[Cloud Monitoring]
    end
    
    A --> B
    B --> C
    C --> D
    D <--> E
    E --> F
    E --> G
    E --> H
    E --> I
    E --> J
    E --> K
    D --> J
    
    style D fill:#4285F4,stroke:#1967D2,stroke-width:2px,color:#fff
    style E fill:#4285F4,stroke:#1967D2,stroke-width:2px,color:#fff
    style H fill:#34A853,stroke:#137333,stroke-width:2px,color:#fff
    style F fill:#34A853,stroke:#137333,stroke-width:2px,color:#fff
```

---

## Process Monitoring Flow

```mermaid
flowchart LR
    A[Sensor Data] --> B[Data Collection]
    B --> C{Data Validation}
    C -->|Valid| D[Store in Cloud SQL]
    C -->|Invalid| E[Error Logging]
    D --> F[Real-time Dashboard]
    D --> G[AI Analysis]
    G --> H{Anomaly<br/>Detected?}
    H -->|Yes| I[Generate Alert]
    H -->|No| J[Continue Monitoring]
    I --> K[Notify Operators]
    I --> L[AI Recommendations]
    
    style G fill:#FFA000,color:#fff
    style H fill:#EA4335,color:#fff
    style I fill:#EA4335,color:#fff
    style L fill:#34A853,color:#fff
```

---

## API Request Flow

```mermaid
graph LR
    A[Client Request] --> B{Rate Limit<br/>Check}
    B -->|Exceeded| C[429 Error]
    B -->|OK| D{Authentication}
    D -->|Invalid| E[401 Error]
    D -->|Valid| F[Route Handler]
    F --> G{Request Type}
    G -->|Data Query| H[Database]
    G -->|AI Query| I[LangGraph Agent]
    G -->|Vision| J[Cloud Vision API]
    H --> K[Format Response]
    I --> K
    J --> K
    K --> L[Return to Client]
    
    style B fill:#FFA000,color:#fff
    style D fill:#FFA000,color:#fff
    style I fill:#34A853,color:#fff
```

---

## Class Diagram - Backend Core

```mermaid
classDiagram
    class CementAgent {
        +ChatGoogleGenerativeAI llm
        +List tools
        +StateGraph agent_graph
        +run_agent(message)
        +get_realtime_plant_data()
        +calculate_efficiency_metrics()
        +analyze_quality_metrics()
        +generate_recommendations()
    }
    
    class Settings {
        +str GOOGLE_CLOUD_PROJECT
        +str GOOGLE_API_KEY
        +str DATABASE_URL
        +str VERTEX_AI_LOCATION
        +List cors_origins_list
    }
    
    class AsyncSessionLocal {
        +execute(query)
        +commit()
        +rollback()
    }
    
    class APIRouter {
        +str prefix
        +List tags
        +get()
        +post()
        +websocket()
    }
    
    CementAgent --> Settings : uses
    CementAgent --> AsyncSessionLocal : queries
    APIRouter --> CementAgent : calls
    
    class AIChat {
        <<router>>
        +chat(request)
        +stream(request)
        +websocket(client_id)
    }
    
    class DataEndpoints {
        <<router>>
        +get_raw_materials()
        +get_kiln_operations()
        +get_quality_metrics()
    }
    
    AIChat --|> APIRouter
    DataEndpoints --|> APIRouter
```

---

## Technology Stack Layers

```mermaid
graph TB
    subgraph "Presentation Layer"
        A[Next.js 15]
        B[React 19]
        C[TypeScript]
        D[Tailwind CSS]
    end
    
    subgraph "Application Layer"
        E[FastAPI]
        F[Python 3.11+]
        G[LangChain]
        H[LangGraph]
    end
    
    subgraph "Data Layer"
        I[SQLAlchemy 2.0]
        J[PostgreSQL 14+]
        K[Cloud SQL]
    end
    
    subgraph "AI/ML Layer"
        L[Vertex AI]
        M[Gemini 2.0]
        N[Cloud Vision]
    end
    
    subgraph "Infrastructure"
        O[Docker]
        P[Cloud Run]
        Q[Cloud Storage]
    end
    
    A --> E
    B --> A
    C --> A
    D --> A
    E --> I
    F --> E
    G --> E
    H --> G
    I --> J
    J --> K
    E --> L
    L --> M
    E --> N
    E --> P
    P --> Q
    
    style A fill:#4285F4,color:#fff
    style E fill:#4285F4,color:#fff
    style K fill:#34A853,color:#fff
    style M fill:#34A853,color:#fff
```

---

## Development Workflow

```mermaid
gitGraph
    commit id: "Initial setup"
    branch develop
    checkout develop
    commit id: "Add AI agent"
    branch feature/vision-api
    checkout feature/vision-api
    commit id: "Implement Vision API"
    commit id: "Add tests"
    checkout develop
    merge feature/vision-api
    branch feature/dashboard
    checkout feature/dashboard
    commit id: "Create dashboard"
    commit id: "Add charts"
    checkout develop
    merge feature/dashboard
    checkout main
    merge develop tag: "v1.0.0"
    commit id: "Production release"
```

---

**Developed by**: Codygon Technologies Private Limited  
**Support**: support@codygon.com

© 2025 Codygon Technologies Private Limited. All rights reserved.
