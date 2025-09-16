"""
RBI Guidelines Chatbot - Minimal Professional Interface
Clean, minimalist design for RBI risk management guidelines assistant
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="RBI Assistant",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Minimal styling
st.markdown("""
<style>
    .main { padding-top: 2rem; }
    .stTitle { text-align: center; font-weight: 300; }
    .chat-message { 
        padding: 1rem; 
        margin: 0.5rem 0; 
        border-radius: 8px; 
        border-left: 3px solid #0066cc;
        color: #2c3e50;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .user-message { 
        background-color: #f8f9fa; 
        border-left-color: #0066cc;
        color: #2c3e50;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.15);
    }
    .assistant-message { 
        background-color: #ffffff; 
        border-left-color: #28a745;
        color: #2c3e50;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.15);
        border: 1px solid #e9ecef;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    .stButton > button {
        border-radius: 20px;
        border: none;
        background: linear-gradient(90deg, #0066cc, #004499);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Ollama API class
class OllamaChat:
    def __init__(self, model="tinyllama", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        
    def generate(self, prompt, stream=False):
        """Generate response from Ollama using chat API"""
        if stream:
            return self._generate_stream(prompt)
        else:
            return self._generate_normal(prompt)
    
    def _generate_normal(self, prompt):
        """Generate non-streaming response"""
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 500
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if "message" in result and "content" in result["message"]:
                        content = result["message"]["content"].strip()
                        if content:
                            return content
                        else:
                            return "Error: Empty content in response"
                    else:
                        return f"Error: Invalid response format. Keys: {list(result.keys())}"
                except json.JSONDecodeError as e:
                    return f"Error: Failed to parse JSON response: {e}"
            else:
                return f"Error: API returned status {response.status_code}: {response.text}"
                
        except requests.exceptions.Timeout:
            return "Error: Request timed out after 60 seconds"
        except requests.exceptions.ConnectionError:
            return "Error: Could not connect to Ollama. Is it running?"
        except requests.exceptions.RequestException as e:
            return f"Error: Request failed: {e}"
        except Exception as e:
            return f"Error: Unexpected error: {e}"
    
    def _generate_stream(self, prompt):
        """Generate streaming response"""
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": True,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 500
                    }
                },
                stream=True,
                timeout=60
            )
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if "message" in data and "content" in data["message"]:
                            chunk = data["message"]["content"]
                            full_response += chunk
                            yield chunk
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
            return full_response
            
        except Exception as e:
            yield f"Error: {e}"
    
    def is_available(self):
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "ollama" not in st.session_state:
    st.session_state.ollama = OllamaChat()

# Main interface
st.title("🏦 RBI Guidelines Assistant")
st.markdown("<p style='text-align: center; color: #666; margin-bottom: 2rem;'>Professional AI assistant for Reserve Bank of India guidelines</p>", unsafe_allow_html=True)

# Status indicator
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.session_state.ollama.is_available():
        st.success("🟢 Connected to Ollama")
    else:
        st.error("🔴 Ollama not available - Please start Ollama service")

# Chat interface
chat_container = st.container()

# Display chat history
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>Assistant:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)

# Input area
st.markdown("---")
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Ask about RBI guidelines...",
        placeholder="e.g., What are operational risk management requirements?",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("Send", use_container_width=True)

# Handle input
if send_button and user_input.strip():
    if not st.session_state.ollama.is_available():
        st.error("Ollama is not available. Please start the Ollama service.")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate response
        with st.spinner("Thinking..."):
            # Create context-aware prompt
            prompt = f"""You are a professional assistant specializing in Reserve Bank of India (RBI) guidelines and risk management. 
            
User question: {user_input}

Please provide a clear, professional response about RBI guidelines. If the question is outside RBI guidelines scope, politely redirect to RBI-related topics."""
            
            try:
                response = st.session_state.ollama.generate(prompt)
                
                if response and isinstance(response, str):
                    if response.startswith("Error:"):
                        st.error(response)
                    elif len(response.strip()) > 0:
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    else:
                        st.error("Received empty response from Ollama")
                else:
                    st.error(f"Invalid response type from Ollama: {type(response)}")
                    
            except Exception as e:
                st.error(f"Error generating response: {e}")
        
        st.rerun()

# Quick actions
if not st.session_state.messages:
    st.markdown("### Quick Questions")
    
    quick_questions = [
        "What are operational risk management requirements?",
        "How should banks monitor credit risk?",
        "What are capital adequacy guidelines?",
        "What are technology risk controls?"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(quick_questions):
        with cols[i % 2]:
            if st.button(question, key=f"quick_{i}"):
                st.session_state.messages.append({"role": "user", "content": question})
                
                with st.spinner("Thinking..."):
                    prompt = f"""You are a professional assistant specializing in Reserve Bank of India (RBI) guidelines and risk management. 
                    
User question: {question}

Please provide a clear, professional response about RBI guidelines."""
                    
                    response = st.session_state.ollama.generate(prompt)
                    
                    if response and isinstance(response, str) and not response.startswith("Error") and not response.startswith("Connection error"):
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    else:
                        st.error(f"Failed to get response for quick question: {response}")
                
                st.rerun()

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
