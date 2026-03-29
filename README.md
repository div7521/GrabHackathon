# 🚀 Project Synapse - Agentic Last-Mile Coordinator

[![GrabHack Campus Edition](https://img.shields.io/badge/GrabHack-Campus%20Edition-green)](https://github.com/div7521/GrabHackathon)
[![BITS Pilani](https://img.shields.io/badge/BITS-Pilani-blue)](https://www.bits-pilani.ac.in/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-orange)](https://langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)](https://streamlit.io/)

**Team Chai and Biscuit** | Divyanshi Gupta & Arnav Bharti

---

## 📋 Table of Contents
- [Overview](#overview)
- [The Problem](#the-problem)
- [Our Solution](#our-solution)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Demo & Presentation](#demo--presentation)
- [Skills Learned](#skills-learned)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 🎯 Overview

**Project Synapse** is an autonomous AI agent designed to revolutionize last-mile delivery coordination across Grab's ecosystem. It intelligently resolves complex delivery disruptions in real-time using advanced reasoning, dynamic tool orchestration, and continuous learning from feedback.

### 🏆 Built for GrabHack: Campus Edition

This project addresses the critical challenge of **unpredictable real-time disruptions** in last-mile delivery that traditional rule-based systems cannot handle effectively.

---

## ❌ The Problem

Last-mile delivery faces a **15-20% failure rate** due to:

- **Route Blockages**: Sudden traffic jams, road closures
- **Incorrect Addresses**: Customer location errors, incomplete details
- **Merchant Unavailability**: Restaurant overload, store closures, stock-outs
- **Customer Unavailability**: Recipient not present for delivery
- **Package Issues**: Damage disputes, wrong items, quality concerns

**Current AI systems** have critical limitations:
- ❌ No contextual understanding of root causes
- ❌ Cannot generate resolution strategies autonomously
- ❌ No adaptive learning from outcomes
- ❌ Lack multi-factor reasoning capabilities
- ❌ Need human approval for every action

---

## ✅ Our Solution

**Project Synapse** is an intelligent agentic coordinator that:

1. **Analyzes** disruption scenarios using Chain-of-Thought reasoning
2. **Selects** appropriate tools from 15+ specialized logistics APIs
3. **Executes** multi-step action plans autonomously
4. **Learns** from user feedback to continuously improve
5. **Protects** drivers from false blame through evidence-based decisions

### 🎨 What Makes Us Different

| Feature | Traditional Systems | Project Synapse |
|---------|-------------------|-----------------|
| **Response Type** | Rule-based flags | Autonomous reasoning |
| **Tool Usage** | Manual selection | Dynamic orchestration |
| **Learning** | Static rules | Feedback-driven improvement |
| **Context** | Generic | Product-specific (Food/Mart/Express/Car) |
| **Driver Protection** | Manual review | Automated evidence analysis |
| **User Experience** | Complex dashboards | Conversational chat interface |

---

## ⚡ Key Features

### 🧠 **Intelligent Reasoning Engine**
- Chain-of-thought processing with transparent decision-making
- Context-aware understanding for each Grab service
- Evidence-based fault attribution and stakeholder impact analysis

### 🔧 **Dynamic Tool Orchestration**
- 15+ specialized tools mimicking real Grab logistics APIs
- Smart tool selection based on scenario context
- Error-resilient execution with fallback strategies

### 💾 **Memory & Learning System**
- Stores conversation history for context continuity
- Feedback loop with rating system and improvement suggestions
- Learns from mistakes and prevents repeated errors

### 🛡️ **Driver Protection Logic**
- Systematic bias prevention with default driver professionalism assumption
- Automated `exonerate_driver()` evaluation in every dispute
- Evidence-based decision making for fair outcomes

### 🎯 **Multi-Service Support**
- **GrabFood**: Restaurant delays, damaged packaging, merchant coordination
- **GrabMart**: Stock-outs, substitutions, store closures, bulk orders
- **GrabExpress**: Recipient unavailability, valuable packages, secure drops
- **GrabCar**: Traffic disruptions, airport rushes, passenger urgency

### 🎨 **User Experience Excellence**
- Conversational chat interface for natural interaction
- Product-specific examples and scenarios
- Interactive feedback with star ratings
- Follow-up question capability
- One-click conversation restart

---

## 🏗️ Architecture

### System Flow
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

### Core Components

#### 1️⃣ **Input Processing**
- Natural language disruption scenarios
- Service context selection
- Historical conversation memory integration

#### 2️⃣ **AI Agent Core**
- Chain-of-thought reasoning engine
- Dynamic tool selection logic
- Driver protection and bias prevention
- Evidence-based decision making

#### 3️⃣ **Tool Execution Layer**
- 15+ specialized API simulations
- Real-time data gathering
- Error handling with fallback strategies
- Success/failure result processing

#### 4️⃣ **Output Generation**
- Situational analysis (bullet points)
- Transparent reasoning chain
- Step-by-step action plans
- Executable code generation
- Follow-up interaction guidance

---

## 🛠️ Tech Stack

### **Frontend**
- **Streamlit** - Real-time chat interface with session state management

### **AI/ML Framework**
- **LangChain** - Agentic workflows, tool binding, message management
- **Google Gemini 1.5 Flash** - Fast, cost-effective reasoning with tool-calling

### **Backend**
- **Python 3.8+** - Core programming language
- **dotenv** - Environment variable management
- **Custom Logging** - Tool execution tracking and debugging

### **Architecture Patterns**
- ReAct (Reasoning + Acting) agent pattern
- Error-resilient tool execution framework
- Context-aware prompt engineering
- Modular tool system design

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/div7521/GrabHackathon.git
cd GrabHackathon
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the root directory:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 4: Run the Application
```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 🎮 Usage

### Getting Started

1. **Select Grab Service**: Choose from GrabFood, GrabMart, GrabExpress, or GrabCar
2. **Describe Scenario**: Enter a delivery disruption in natural language or use example scenarios
3. **Review Analysis**: See the AI's situational analysis and reasoning chain
4. **Execute Actions**: Watch as the agent selects and executes appropriate tools
5. **Provide Feedback**: Rate the response and suggest improvements

### Example Scenarios

#### GrabFood - Restaurant Overload
```
Restaurant restaurant_002 is overloaded with 40-minute prep time. 
Customer CUST_123 has an urgent order and is getting impatient. 
The driver DRIVER_456 is waiting idle. What should we do?
```

#### GrabExpress - Recipient Unavailable
```
Driver arrived at destination but recipient is unavailable for a 
valuable $200 electronics package. Package requires secure handling. 
What are the delivery options?
```

#### GrabCar - Airport Rush
```
Passenger is heading to airport with flight SQ123 departing at 3 PM. 
Major accident detected on route_002 causing 30-minute delay. 
Current time is 1:30 PM. What should we do?
```

---

## 📁 Project Structure

```
GrabHackathon/
├── main.py                  # Streamlit application entry point
├── prompt.py                # System prompts and agent instructions
├── tools.py                 # Tool definitions and implementations
├── logging_config.py        # Logging configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in repo)
├── .gitignore              # Git ignore file
├── README.md               # This file
└── docs/
    ├── slides_problem.pdf   # Problem statement slides
    └── slides_solution.pdf  # Solution architecture slides
```

---

## 🎥 Demo & Presentation

### 📊 Presentation Slides

**Problem Statement & Context**
- [View Problem Analysis Slides](./docs/slides_problem.pdf)
- Covers: Pain points, current AI limitations, disruption types

**Solution Architecture & Implementation**
- [View Solution Slides](./docs/slides_solution.pdf)
- Covers: Framework, features, engineering techniques, architecture

### 🎬 Key Highlights

- **Autonomous Problem Solving**: No human intervention required
- **Transparent Reasoning**: Clear chain-of-thought visible to users
- **Error Resilience**: Continues operation even when tools fail
- **Fair Outcomes**: Driver protection through evidence-based decisions
- **Continuous Learning**: Improves from user feedback

---

## 🎓 Skills Learned

### Technical Skills
- **LangChain Framework** - Agentic workflows and tool orchestration
- **Streamlit Development** - Interactive web applications
- **Prompt Engineering** - Context-aware AI instruction design
- **API Integration** - Tool binding and execution patterns
- **Error Handling** - Graceful degradation strategies
- **State Management** - Session persistence and memory systems
- **Large Language Models** - Gemini API integration

### AI/ML Skills
- **Agent Design** - Autonomous reasoning systems
- **Tool Calling** - Dynamic function selection
- **Chain-of-Thought** - Multi-step reasoning implementation
- **Memory Integration** - Feedback loops and learning
- **Context Switching** - Product-specific adaptation

### Software Architecture
- **System Design** - Multi-layer architecture
- **Component Architecture** - Modular design patterns
- **Solution Architecture** - End-to-end system thinking
- **UX Design** - Conversational interfaces

---

## 🚀 Future Enhancements

### Phase 1: Enhanced Intelligence
- [ ] Multi-agent collaboration for complex scenarios
- [ ] Predictive disruption detection using historical data
- [ ] Real-time optimization of action sequences

### Phase 2: Production Integration
- [ ] Connect to real Grab APIs
- [ ] Deploy on cloud infrastructure (AWS/GCP)
- [ ] Add authentication and user management
- [ ] Implement comprehensive monitoring and analytics

### Phase 3: Advanced Features
- [ ] Voice interface for drivers
- [ ] Multilingual support for regional expansion
- [ ] Mobile app integration
- [ ] Dashboard for operations teams

### Phase 4: ML Improvements
- [ ] Fine-tune LLM on Grab-specific data
- [ ] Reinforcement learning from outcomes
- [ ] Automated A/B testing of strategies

---

## 📄 License

This project was created for **GrabHack: Campus Edition** by Team Chai and Biscuit (Divyanshi Gupta & Arnav Bharti) from BITS Pilani.

---

## 🙏 Acknowledgments

- **Grab** for organizing GrabHack: Campus Edition
- **BITS Pilani** for supporting student innovation
- **Google** for Gemini API access
- **LangChain** and **Streamlit** communities for excellent frameworks

---

## 📞 Contact

**Team Chai and Biscuit**

- **Divyanshi Gupta** - [GitHub](https://github.com/div7521)
- **Arnav Bharti** - [GitHub](https://github.com/div7521)
- **Institution**: BITS Pilani

**Project Repository**: [https://github.com/div7521/GrabHackathon](https://github.com/div7521/GrabHackathon)

---

<div align="center">

### ⭐ If you found this project interesting, please star the repository!

**Built with ❤️ for GrabHack: Campus Edition**

</div>
