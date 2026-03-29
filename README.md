# Project Synapse - Agentic Last-Mile Coordinator

**GrabHack: Campus Edition**  
**Team Chai and Biscuit** | Divyanshi Gupta & Arnav Bharti | BITS Pilani

---

## Table of Contents
- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Technical Stack](#technical-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Presentation Materials](#presentation-materials)
- [Skills Demonstrated](#skills-demonstrated)

---

## Overview

Project Synapse is an autonomous AI agent designed to resolve complex last-mile delivery disruptions across Grab's ecosystem (GrabFood, GrabMart, GrabExpress, GrabCar). The system uses advanced reasoning, dynamic tool orchestration, and continuous learning to autonomously coordinate solutions for real-time delivery challenges.

---

## Problem Statement

Last-mile delivery operations face a **15-20% failure rate** due to unpredictable disruptions that rigid, rule-based systems cannot effectively handle.

![Problem Analysis](./docs/images/problem_statement.png)
<img width="1158" height="652" alt="Screenshot 2026-03-29 at 3 20 26 PM" src="https://github.com/user-attachments/assets/8ec3582d-453a-460b-83bb-a2d3ed32a2b1" />


### Key Challenges

**Pain Points:**
- Regional inefficiency
- Performance gaps
- Infrastructure challenges
- Customer expectations

**Disruption Types:**
- Route blockages (traffic jams, road closures)
- Incorrect addresses (customer location errors)
- Merchant unavailability (restaurant overload, store closures)
- Customer unavailability (recipient not present)

**Current AI Limitations:**
- No contextual understanding of root causes
- Cannot generate autonomous resolution strategies
- No adaptive learning capabilities
- Lack of multi-factor reasoning
- Require human approval for execution

---

## Solution

Project Synapse is an autonomous AI agent that reasons through delivery disruptions and executes multi-step solutions using 15+ specialized logistics tools.

### Core Capabilities

1. **Autonomous Reasoning**: Chain-of-thought analysis of complex scenarios
2. **Dynamic Tool Orchestration**: Intelligent selection and execution of appropriate APIs
3. **Context-Aware Intelligence**: Service-specific handling for GrabFood, GrabMart, GrabExpress, GrabCar
4. **Continuous Learning**: Feedback-driven improvement through memory persistence
5. **Driver Protection**: Evidence-based fault assessment to prevent unfair blame

### Comparison with Traditional Systems

| Aspect | Traditional Systems | Project Synapse |
|--------|-------------------|-----------------|
| Response | Rule-based flags | Autonomous reasoning |
| Tool Usage | Manual selection | Dynamic orchestration |
| Learning | Static rules | Feedback-driven |
| Context | Generic | Product-specific |
| Driver Protection | Manual review | Automated evidence analysis |
| Interface | Complex dashboards | Conversational chat |

---

## Key Features

![Feature Overview](./docs/images/features.png)
<img width="1215" height="685" alt="Screenshot 2026-03-29 at 3 20 52 PM" src="https://github.com/user-attachments/assets/b663b31a-384a-40c3-9449-9aeaf55c8a48" />


### Intelligent Reasoning Engine
- Chain-of-thought processing with transparent decision-making
- Context-aware understanding for each Grab service vertical
- Stakeholder impact analysis (customer, driver, merchant)
- Evidence-based fault attribution

### Dynamic Tool System
- 15+ specialized tools simulating real Grab logistics APIs
- Context-driven tool selection based on scenario analysis
- Error-resilient execution with graceful degradation
- Structured success/failure handling

### Memory & Learning
- Conversation history storage for context continuity
- User feedback integration (star ratings, improvement suggestions)
- Mistake prevention through pattern recognition
- Session state management

### Driver Protection Logic
- Systematic evaluation of driver responsibility in every scenario
- Default assumption of driver professionalism
- Automated `exonerate_driver()` function when evidence supports innocence
- Fair resolution framework balancing all stakeholder interests

### Multi-Service Support

**GrabFood**: Restaurant delays, damaged packaging, merchant coordination  
**GrabMart**: Stock-outs, product substitutions, store closures, bulk orders  
**GrabExpress**: Recipient unavailability, valuable packages, secure delivery alternatives  
**GrabCar**: Traffic disruptions, route optimization, airport coordination

### User Experience
- Natural language input for scenario description
- Product-specific example scenarios
- Interactive feedback system
- Follow-up question capability
- One-click conversation restart


---

## System Architecture

### High-Level Flow
```
User Input (Disruption Scenario)
    ↓
Service Selection (GrabFood/Mart/Express/Car)
    ↓
AI Agent (Reasoning + Tool Selection + Memory)
    ↓
Tool Execution (15+ Specialized APIs)
    ↓
Structured Output (Analysis + Action Plan + Code)
```

### System Components

**1. Input Processing**
- Natural language scenario parsing
- Service context selection
- Historical conversation memory integration

**2. AI Agent Core**
- Chain-of-thought reasoning engine
- Dynamic tool selection logic
- Driver protection and bias prevention
- Evidence-based decision making

**3. Tool Execution Layer**
- 15+ specialized API simulations
- Real-time data gathering
- Error handling with fallback strategies
- Structured result processing

**4. Output Generation**
- Situational analysis
- Transparent reasoning chain
- Step-by-step action plans
- Executable code generation
- Follow-up guidance

---

## Technical Stack

### Core Technologies
- **Python 3.8+** - Primary programming language
- **Streamlit** - Real-time chat interface with session state management
- **LangChain** - Agentic workflows, tool binding, message management
- **Google Gemini 1.5 Flash** - Fast reasoning with native tool-calling capabilities

### Key Libraries
- **dotenv** - Environment variable management
- **langchain-google-genai** - Gemini integration
- **langchain-core** - Message handling and agent primitives

### Architecture Patterns
- ReAct (Reasoning + Acting) agent pattern
- Error-resilient tool execution framework
- Context-aware prompt engineering
- Modular tool system design

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- pip package manager

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/div7521/GrabHackathon.git
cd GrabHackathon

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Create a .env file in the root directory
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env

# Run the application
streamlit run main.py
```

The application will launch at `http://localhost:8501`

---

## Usage

### Getting Started

1. Select a Grab service (GrabFood, GrabMart, GrabExpress, or GrabCar)
2. Describe a delivery disruption scenario in natural language or select from example scenarios
3. Review the AI's situational analysis and reasoning chain
4. Observe tool execution and results
5. Provide feedback through the rating system

### Example Scenarios

**GrabFood - Restaurant Overload**
```
Restaurant restaurant_002 is overloaded with 40-minute prep time. 
Customer CUST_123 has an urgent order and is getting impatient. 
The driver DRIVER_456 is waiting idle. What should we do?
```

**GrabExpress - Recipient Unavailable**
```
Driver arrived at destination but recipient is unavailable for a 
valuable $200 electronics package. Package requires secure handling. 
What are the delivery options?
```

**GrabCar - Airport Rush**
```
Passenger is heading to airport with flight SQ123 departing at 3 PM. 
Major accident detected on route_002 causing 30-minute delay. 
Current time is 1:30 PM. What should we do?
```

---

## Project Structure

```
GrabHackathon/
├── main.py                  # Streamlit application entry point
├── prompt.py                # System prompts and agent instructions
├── tools.py                 # Tool definitions and implementations
├── logging_config.py        # Logging configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in repo)
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
└── docs/
    ├── slides_problem.pdf   # Problem statement presentation
    ├── slides_solution.pdf  # Solution architecture presentation
    └── images/              # Documentation images
        ├── problem_statement.png
        └── features.png
```

---

## Presentation Materials

### Slide Decks

**Problem Statement & Analysis**
- Comprehensive analysis of last-mile delivery challenges
- Current AI maturity landscape
- Identified gaps and limitations

**Solution Architecture & Implementation**
- Framework architecture and design patterns
- Engineering techniques and prompt strategies
- Feature implementation details
- System architecture diagrams

### Repository
- **GitHub**: [https://github.com/div7521/GrabHackathon](https://github.com/div7521/GrabHackathon)

---

## Skills Demonstrated

### Technical Skills
- LangChain framework for agentic workflows
- Streamlit development for interactive applications
- Prompt engineering and context-aware instruction design
- API integration and tool orchestration
- Error handling and graceful degradation
- State management and session persistence
- Large language model integration (Gemini API)

### AI/ML Skills
- Agent design and autonomous reasoning systems
- Dynamic tool calling and function selection
- Chain-of-thought reasoning implementation
- Memory integration and feedback loops
- Context switching and product-specific adaptation

### Software Architecture
- Multi-layer system design
- Component-based modular architecture
- Solution architecture for end-to-end systems
- User experience design for conversational interfaces

### Domain Expertise
- Logistics operations and last-mile delivery
- Business process design and stakeholder coordination
- Problem-solving methodologies and structured analysis

---

## Contact

**Team Chai and Biscuit**

Divyanshi Gupta & Arnav Bharti  
BITS Pilani

**Project Repository**: [https://github.com/div7521/GrabHackathon](https://github.com/div7521/GrabHackathon)

---

Built for GrabHack: Campus Edition
