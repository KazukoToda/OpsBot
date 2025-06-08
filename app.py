import streamlit as st
import pandas as pd
import json
import os
from typing import List, Dict, Any
import plotly.express as px
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🌐 OpsBot - AI System Status Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize OpenAI client
@st.cache_resource
def init_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API Key not found. Please set OPENAI_API_KEY in your environment variables.")
        return None
    return OpenAI(api_key=api_key)

# Load system data
@st.cache_data
def load_system_data():
    try:
        with open('systems.json', 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except FileNotFoundError:
        st.error("systems.json file not found. Please ensure the file exists in the application directory.")
        return pd.DataFrame()
    except json.JSONDecodeError:
        st.error("Error reading systems.json. Please check the file format.")
        return pd.DataFrame()

# Query OpenAI for intent extraction and response generation
def query_openai(client, user_question: str, systems_data: pd.DataFrame) -> str:
    if client is None:
        return "OpenAI client is not available. Please check your API key configuration."
    
    # Convert dataframe to string for context
    systems_context = systems_data.to_string(index=False)
    
    system_prompt = f"""You are an AI assistant for a system monitoring dashboard. 
    You have access to the following system data:
    
    {systems_context}
    
    Answer user questions about system status, CPU usage, memory usage, and provide helpful insights.
    Be conversational and provide specific details from the data when relevant.
    If asked about systems that are down or stopped, mention which ones specifically.
    For numerical queries (like "over 80%"), provide exact values and system names.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using gpt-4o-mini for cost efficiency
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error querying OpenAI: {str(e)}"

# Filter systems based on query type
def filter_systems(df: pd.DataFrame, query_type: str) -> pd.DataFrame:
    if "down" in query_type.lower() or "stopped" in query_type.lower():
        return df[df['status'] == 'stopped']
    elif "high memory" in query_type.lower() or "memory over" in query_type.lower():
        return df[df['memory'] > 80]
    elif "high cpu" in query_type.lower() or "cpu over" in query_type.lower():
        return df[df['cpu'] > 80]
    elif "running" in query_type.lower():
        return df[df['status'] == 'running']
    else:
        return df

# Create visualizations
def create_system_chart(df: pd.DataFrame, chart_type: str = "bar"):
    if df.empty:
        return None
    
    if chart_type == "bar":
        fig = px.bar(df, x='name', y=['cpu', 'memory'], 
                     title="System CPU and Memory Usage",
                     barmode='group',
                     color_discrete_map={'cpu': '#ff6b6b', 'memory': '#4ecdc4'})
        fig.update_layout(xaxis_tickangle=-45)
        return fig
    elif chart_type == "status":
        status_counts = df['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, 
                     title="System Status Distribution",
                     color_discrete_map={'running': '#51cf66', 'stopped': '#ff6b6b'})
        return fig
    
    return None

# Simulate system updates
def simulate_system_updates(df: pd.DataFrame) -> pd.DataFrame:
    import random
    
    updated_df = df.copy()
    
    # Randomly update some systems
    for idx in updated_df.index:
        if random.random() < 0.3:  # 30% chance to update each system
            # Random CPU change
            if updated_df.loc[idx, 'status'] == 'running':
                updated_df.loc[idx, 'cpu'] = max(0, min(100, 
                    updated_df.loc[idx, 'cpu'] + random.randint(-10, 10)))
                updated_df.loc[idx, 'memory'] = max(0, min(100,
                    updated_df.loc[idx, 'memory'] + random.randint(-5, 15)))
            
            # Random status change (small chance)
            if random.random() < 0.1:
                if updated_df.loc[idx, 'status'] == 'running':
                    updated_df.loc[idx, 'status'] = 'stopped'
                    updated_df.loc[idx, 'cpu'] = 0
                    updated_df.loc[idx, 'memory'] = 0
                else:
                    updated_df.loc[idx, 'status'] = 'running'
                    updated_df.loc[idx, 'cpu'] = random.randint(10, 90)
                    updated_df.loc[idx, 'memory'] = random.randint(20, 80)
    
    return updated_df

# Main application
def main():
    st.title("🌐 OpsBot - AI-powered System Status Dashboard")
    st.markdown("Ask me anything about your system status!")
    
    # Initialize OpenAI client
    client = init_openai_client()
    
    # Load system data
    if 'systems_df' not in st.session_state:
        st.session_state.systems_df = load_system_data()
    
    if st.session_state.systems_df.empty:
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Controls")
        
        # System update simulation
        if st.button("🔄 Simulate System Updates", use_container_width=True):
            st.session_state.systems_df = simulate_system_updates(st.session_state.systems_df)
            st.rerun()
        
        # Data view options
        st.header("📊 Data Views")
        view_type = st.selectbox("Select View:", ["Table", "CPU/Memory Chart", "Status Chart"])
        
        # Sample questions
        st.header("💡 Sample Questions")
        sample_questions = [
            "Which servers are down?",
            "Show me the CPU usage of all systems",
            "Any service with memory usage over 80%?",
            "What's the status of the database server?",
            "Which systems are running normally?"
        ]
        
        for question in sample_questions:
            if st.button(f"💬 {question}", use_container_width=True, key=f"sample_{question}"):
                st.session_state.user_input = question
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat interface
        st.header("💬 Ask OpsBot")
        
        # Initialize chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # User input
        user_input = st.text_input("Your question:", 
                                  value=st.session_state.get('user_input', ''),
                                  placeholder="e.g., Which servers are down?",
                                  key="user_question")
        
        # Clear the session state input after displaying
        if 'user_input' in st.session_state:
            del st.session_state.user_input
        
        if st.button("🚀 Ask", use_container_width=True) and user_input:
            with st.spinner("🤔 Thinking..."):
                # Get AI response
                response = query_openai(client, user_input, st.session_state.systems_df)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "question": user_input,
                    "response": response
                })
        
        # Display chat history
        if st.session_state.chat_history:
            st.header("📜 Chat History")
            for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
                with st.expander(f"💬 {chat['question']}", expanded=(i == 0)):
                    st.write(chat['response'])
    
    with col2:
        # Data visualization
        st.header("📊 System Overview")
        
        if view_type == "Table":
            st.dataframe(st.session_state.systems_df, use_container_width=True)
        
        elif view_type == "CPU/Memory Chart":
            chart = create_system_chart(st.session_state.systems_df, "bar")
            if chart:
                st.plotly_chart(chart, use_container_width=True)
        
        elif view_type == "Status Chart":
            chart = create_system_chart(st.session_state.systems_df, "status")
            if chart:
                st.plotly_chart(chart, use_container_width=True)
        
        # System summary
        st.header("📈 Quick Stats")
        total_systems = len(st.session_state.systems_df)
        running_systems = len(st.session_state.systems_df[st.session_state.systems_df['status'] == 'running'])
        stopped_systems = total_systems - running_systems
        avg_cpu = st.session_state.systems_df[st.session_state.systems_df['status'] == 'running']['cpu'].mean()
        avg_memory = st.session_state.systems_df[st.session_state.systems_df['status'] == 'running']['memory'].mean()
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("✅ Running", running_systems)
            st.metric("📊 Avg CPU", f"{avg_cpu:.1f}%" if not pd.isna(avg_cpu) else "N/A")
        with col_b:
            st.metric("❌ Stopped", stopped_systems)
            st.metric("💾 Avg Memory", f"{avg_memory:.1f}%" if not pd.isna(avg_memory) else "N/A")

if __name__ == "__main__":
    main()