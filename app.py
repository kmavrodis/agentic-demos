import streamlit as st
from data_view import display_data_tab
from scenario_processor import display_scenario_tab
from use_case_loader import UseCaseLoader
from use_case_manager import add_use_case_manager
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables at startup
load_dotenv()

def get_openai_client(key, endpoint, deployment):
    """Initialize an OpenAI client with the given credentials."""
    client = AzureOpenAI(
        api_key=os.getenv(key),
        api_version="2024-12-01-preview",
        azure_endpoint=os.getenv(endpoint)
    )
    client.deployment_name = os.getenv(deployment)
    return client

def initialize_clients():
    """Initialize OpenAI clients and store them in session state."""
    if 'client' not in st.session_state:
        st.session_state.client = get_openai_client(
            "4o_OPENAI_API_KEY", 
            "4o_OPENAI_ENDPOINT", 
            "4o_OPENAI_DEPLOYMENT_NAME"
        )
    
    if 'o1_client' not in st.session_state:
        st.session_state.o1_client = get_openai_client(
            "O1_OPENAI_API_KEY", 
            "O1_OPENAI_ENDPOINT", 
            "O1_OPENAI_DEPLOYMENT_NAME"
        )
    
    if 'o1_mini_client' not in st.session_state:
        st.session_state.o1_mini_client = get_openai_client(
            "O1_MINI_OPENAI_API_KEY", 
            "O1_MINI_OPENAI_ENDPOINT", 
            "O1_MINI_OPENAI_DEPLOYMENT_NAME"
        )

def main():
    # Check for environment variables
    required_env_vars = [
        "4o_OPENAI_API_KEY", "4o_OPENAI_ENDPOINT", "4o_OPENAI_DEPLOYMENT_NAME",
        "O1_OPENAI_API_KEY", "O1_OPENAI_ENDPOINT", "O1_OPENAI_DEPLOYMENT_NAME",
        "O1_MINI_OPENAI_API_KEY", "O1_MINI_OPENAI_ENDPOINT", "O1_MINI_OPENAI_DEPLOYMENT_NAME"
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        st.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        return

    st.set_page_config(layout="wide", page_title="Agentic Demos with O1", page_icon="🥷")
    
    # Initialize OpenAI clients
    try:
        initialize_clients()
    except Exception as e:
        st.error(f"Error initializing OpenAI clients: {str(e)}")
        return
    
    # Initialize the use case loader
    loader = UseCaseLoader()
    use_cases = loader.load_use_cases()
    
    if not use_cases:
        st.error("No use cases found.")
        return
    
    # Sidebar
    with st.sidebar:
        st.title("🥷 O1 Multi-Industry Demos")
        
        st.markdown("""
        ### About
        Build agentic demos to automate your business processes and execute complex scenarios. This app uses OpenAI O1 to plan an agentic workflow and GPT 4o to execute it.
        
        ### Quick Start
        1. Select a use case below
        2. Choose the first tab to view sample data and tools
        3. Choose the second tab to execute an agentic workflow
        4. Generate a new use case directly in the sidebar
        """)
        
        st.markdown("---")
        st.header("Select a Use Case")
        st.markdown("After selecting a Use Case below, use the tabs on the right to view sample data and tools, and run an agentic workflow.")
        selected_use_case = st.selectbox(
            "Select Use Case",
            use_cases,
            help="Choose a use case to view its data"
        )

    try:
        # Validate and load use case components
        if not loader.validate_use_case(selected_use_case):
            st.error(f"Invalid use case structure for {selected_use_case}")
            return
            
        components = loader.load_use_case_components(selected_use_case)
        
        # Initialize session state
        if 'current_use_case' not in st.session_state or st.session_state.current_use_case != selected_use_case:
            st.session_state.current_use_case = selected_use_case
            st.session_state.context = components['data']
            st.session_state.initial_context = components['data'].copy()
            st.session_state.messages = []

        # Create tabs
        tab1, tab2 = st.tabs([
            "| 📈 1. Sample Data and Tools |",
            "| 🧠 2. Run Agentic Workflow |"
        ])
        
        with tab1:
            display_data_tab(
                data=st.session_state.context,
                use_case=selected_use_case,
                tools=components['tools'],
                functions=components['functions']
            )
            
        with tab2:
            display_scenario_tab(
                tools=components['tools'],
                function_mapping=components['function_mapping'],
                sample_scenarios=components['sample_scenarios']
            )
            


        add_use_case_manager(st, st.session_state.o1_client)

    except Exception as e:
        st.error(f"Error loading use case components: {str(e)}")

if __name__ == "__main__":
    main()