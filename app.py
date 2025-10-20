"""
Streamlit AI Agent for MongoDB querying via MCP tools.
Run with: streamlit run app.py

The AI calling logic is separated into the MongoDBAgent class which can be
used independently for evaluation with pydantic_evals.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from mongodb_agent import MongoDBAgent


# Load environment variables
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

# ============================================================================
# STREAMLIT UI
# ============================================================================

def init_streamlit_ui():
    """Initialize Streamlit UI components. Only called when running as Streamlit app."""
    import streamlit as st
    
    # Page configuration
    st.set_page_config(
        page_title="MongoDB AI Agent",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            margin-bottom: 1rem;
        }
        .tool-call {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            border-left: 4px solid #1f77b4;
        }
        .success {
            color: #28a745;
        }
        .error {
            color: #dc3545;
        }
        .iteration-header {
            background-color: #e9ecef;
            padding: 0.5rem;
            border-radius: 0.3rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main Streamlit application entry point."""
    import streamlit as st
    
    # Header
    st.markdown('<div class="main-header">🤖 MongoDB AI Agent</div>', unsafe_allow_html=True)
    st.markdown("Ask questions about your MongoDB data in natural language, and let AI figure out the right queries!")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Check environment variables
        has_mongodb = bool(os.getenv("MDB_MCP_CONNECTION_STRING") and os.getenv("MDB_MCP_DATABASE"))
        has_openai = bool(os.getenv("OPENAI_API_KEY"))
        
        if has_mongodb:
            st.success("✅ MongoDB configured")
            database_name = os.getenv("MDB_MCP_DATABASE")
            st.info(f"📊 Database: `{database_name}`")
        else:
            st.error("❌ MongoDB not configured")
            st.info("Add to .env file:\n- MDB_MCP_CONNECTION_STRING\n- MDB_MCP_DATABASE")
        
        if has_openai:
            st.success("✅ OpenAI API configured")
        else:
            st.error("❌ OpenAI API not configured")
            st.info("Add OPENAI_API_KEY to .env file")
        
        st.markdown("---")
        st.header("📝 Example Queries")
        st.markdown("""
        - Show all visitors who checked in past week
        - Count total events in the database
        - List all collections
        - Find documents created in the last month
        - Aggregate data by event type
        """)
        
        st.markdown("---")
        st.header("🔧 MCP Server Status")
        mcp_status = st.empty()
        
        try:
            # Try to check if MCP server is running (basic check)
            mcp_status.success("✅ Ready to connect")
        except:
            mcp_status.warning("⚠️ Make sure MCP server is running on localhost:3000")
    
    # Main content
    if not (has_mongodb and has_openai):
        st.warning("⚠️ Please configure environment variables in .env file to use the app")
        
        with st.expander("📋 Setup Instructions"):
            st.code("""
# Create .env file with:
MDB_MCP_CONNECTION_STRING=mongodb+srv://user:pass@cluster.mongodb.net/
MDB_MCP_DATABASE=your_database_name
OPENAI_API_KEY=sk-your-openai-api-key
            """)
        return
    
    # Query input
    st.markdown("### 💬 Ask a Question")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_query = st.text_input(
            "Enter your query:",
            placeholder="e.g., Show all visitors who checked out in the past 2 weeks",
            label_visibility="collapsed"
        )
    
    with col2:
        submit_button = st.button("🚀 Run Query", type="primary", use_container_width=True)
    
    # Quick examples
    st.markdown("**Quick examples:**")
    example_cols = st.columns(3)
    with example_cols[0]:
        if st.button("📊 List collections", use_container_width=True):
            user_query = "List all collections in the database"
            submit_button = True
    with example_cols[1]:
        if st.button("📈 Count events", use_container_width=True):
            user_query = "Count how many documents are in the events collection"
            submit_button = True
    with example_cols[2]:
        if st.button("🔍 Recent data", use_container_width=True):
            user_query = "Show the most recent 5 documents from the events collection"
            submit_button = True
    
    # Execute query
    if submit_button and user_query:
        with st.spinner("🔄 Processing your query..."):
            try:
                # Initialize MongoDB Agent
                agent = MongoDBAgent()
                
                # Run query
                query_result = agent.query_sync(user_query)
                
                # Display results
                st.markdown("---")
                st.markdown("### 🎯 Query Results")
                
                # Show extracted query
                if query_result.get("collection") and query_result.get("filter"):
                    st.markdown("**📋 Extracted MongoDB Query:**")
                    st.json({
                        "collection": query_result["collection"],
                        "filter": query_result["filter"]
                    })
                
                # Show iterations
                for result in query_result.get("iterations", []):
                    with st.expander(f"🔄 Iteration {result['iteration']}", expanded=True):
                        if result['tool_calls']:
                            st.markdown("**🔧 Tool Calls:**")
                            for tool_call in result['tool_calls']:
                                if tool_call['success']:
                                    st.success(f"✅ {tool_call['name']}")
                                else:
                                    st.error(f"❌ {tool_call['name']}")
                                
                                with st.container():
                                    st.json({
                                        "arguments": tool_call['arguments'],
                                        "result": tool_call['result'][:1000] + "..." if len(str(tool_call['result'])) > 1000 else tool_call['result']
                                    })
                        
                        if result.get('final_answer'):
                            st.markdown("**💡 Final Answer:**")
                            st.markdown(result['final_answer'])
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.exception(e)

if __name__ == "__main__":
    init_streamlit_ui()
    main()

