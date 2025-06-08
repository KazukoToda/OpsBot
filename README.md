# 🌐 Ops Bot: AI-powered System Status Dashboard

## 🎯 Objective
Build a web-based dashboard (using Streamlit) that shows the status of multiple virtual systems or applications.  
Users can ask natural language questions like:

- "Which server is down?"
- "Show me the CPU usage of all systems"
- "Any service with memory usage over 80%?"

The system responds using a conversational AI model (OpenAI GPT-4o-mini) and queries local JSON data for system metrics.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API Key

### Installation
```bash
# Clone the repository
git clone https://github.com/KazukoToda/OpsBot.git
cd OpsBot

# Install dependencies
pip install -r requirements.txt

# Set up your OpenAI API key
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Running the Application

#### Option 1: Using the startup script (Easiest)
```bash
./start.sh
```

#### Option 2: Direct Python
```bash
streamlit run app.py
```

#### Option 3: Docker Compose (Recommended for production)
```bash
# Set your OpenAI API key in environment
export OPENAI_API_KEY=your_api_key_here

# Run with Docker Compose
docker-compose up -d
```

The dashboard will open in your browser at `http://localhost:8501`

## 📊 Sample System Data
Each system has the following attributes:
- `name` (e.g. "web-server-1")
- `status` (e.g. "running", "stopped")
- `cpu` (e.g. 75%)
- `memory` (e.g. 62%)

Sample data is provided in `systems.json` with 8 virtual systems.

## 🛠️ Features
✅ **Implemented:**
- Streamlit-based UI with chat-style input
- OpenAI API integration for natural language processing
- Interactive system data visualization (tables and charts)
- Real-time system status overview
- Sample questions for easy interaction
- System update simulation

✅ **Stretch Goals Completed:**
- Button to simulate system updates
- Multiple data view options (table/chart)
- Pre-loaded sample questions

## 🚧 Tech Stack
- **Python** - Core language
- **Streamlit** - Web framework
- **OpenAI GPT-4o-mini** - AI conversational model
- **Pandas** - Data manipulation
- **Plotly** - Interactive charts
- **JSON** - Data storage

## 📝 Usage Examples

### Sample Questions You Can Ask:
- "Which servers are down?"
- "Show me the CPU usage of all systems"
- "Any service with memory usage over 80%?"
- "What's the status of the database server?"
- "Which systems are running normally?"

### Features:
- **Chat Interface**: Ask questions in natural language
- **Live Data**: View real-time system metrics
- **Interactive Charts**: Switch between table and chart views
- **System Simulation**: Update system states with one click
- **Quick Stats**: Overview of system health at a glance

## 🧪 Testing
Run the included test suite:
```bash
python test_opsbot.py
```

## 📎 Notes
This project was built for a hackathon with focus on core functionality and clean UX. The system uses simulated data but can be easily extended to connect to real monitoring systems.