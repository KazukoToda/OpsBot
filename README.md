🌐 Ops Bot: AI-powered System Status Dashboard
🎯 Objective
Build a web-based dashboard (using Streamlit) that shows the status of multiple virtual systems or applications.
Users can ask natural language questions like:

"Which server is down?"
"Show me the CPU usage of all systems"
"Any service with memory usage over 80%?"
The system should respond using a conversational AI model (OpenAI GPT-4o or similar), and query local JSON/CSV data for system metrics.

📊 Sample System Data
Each system has the following attributes:

name (e.g. "web-server-1")
status (e.g. "running", "stopped")
cpu (e.g. 75%)
memory (e.g. 62%)
This data should be simulated in a file like systems.json.

🛠️ Features
Streamlit-based UI with chat-style input
Uses OpenAI API to extract intent and filter system data
Displays results in human-readable format
JSON or CSV file as data source
🌱 Stretch Goals
Add a button to simulate system updates
Add ability to switch between data views (table/chart)
Pre-load 3–5 sample questions
🚧 Tech Stack
Python
Streamlit
OpenAI (GPT API)
Pandas
JSON file (or CSV)
📎 Notes
This project is for a hackathon. It should be functional but simple. Focus on core features and clear UX.