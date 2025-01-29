import streamlit as st
import pandas as pd
import math
from data_generator import DataGenerator

def flatten_dict(d, parent_key='', sep='_'):
    """Flatten nested dictionaries, keeping arrays intact."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def convert_to_dataframe(data, parent_key=''):
    """Convert nested JSON data to pandas DataFrame with improved type handling."""
    if isinstance(data, dict):
        if all(not isinstance(v, (dict, list)) for v in data.values()):
            processed_data = {k: str(v) if isinstance(v, (int, float)) else v 
                            for k, v in data.items()}
            return pd.DataFrame([processed_data])
        
        rows = []
        for key, value in data.items():
            if isinstance(value, dict):
                flattened = flatten_dict(value)
                flattened['id'] = key
                rows.append(flattened)
            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    df = pd.DataFrame(value)
                    df['parent_id'] = key
                    return df
                else:
                    return pd.DataFrame({key: [str(x) for x in value]})
        
        if rows:
            return pd.DataFrame(rows)
        
    elif isinstance(data, list):
        if data and isinstance(data[0], dict):
            flattened_data = [flatten_dict(item) for item in data]
            return pd.DataFrame(flattened_data)
        return pd.DataFrame({parent_key: [str(x) for x in data]})
    
    return None

def create_grid_layout(items_list):
    """Create a grid layout with 2 columns."""
    n_rows = math.ceil(len(items_list) / 2)
    
    for row in range(n_rows):
        cols = st.columns(2)
        for col in range(2):
            idx = row * 2 + col
            if idx < len(items_list):
                key, value = items_list[idx]
                with cols[col]:
                    with st.expander(f"📊 {key.title()}", expanded=True):
                        try:
                            df = convert_to_dataframe(value, key)
                            if df is not None:
                                df = df.astype(str)
                                st.dataframe(df, use_container_width=True)
                            else:
                                st.json(value)
                        except Exception as e:
                            st.error(f"Error displaying {key}: {str(e)}")
                            st.json(value)

def display_data_tab(data, use_case, tools, functions):
    """Display the data view tab content."""
    
    # Create two columns for main content and data management
    main_col, mgmt_col = st.columns([4, 1])
    
    with main_col:
        # Display the data
        st.subheader("Sample Data")
        st.info("Sample Data simulating Databases and External connections. The AI Agents will have access to this data and the ability to update it.")
        items_list = list(st.session_state.context.items())
        create_grid_layout(items_list)
        
   
        
    with mgmt_col:
        # Data management controls in the right column
        st.markdown("### Data Management")
        st.info("Refresh the Data Tables or add more datapoints.")
        if st.button("↻ Refresh Data", use_container_width=True):
            st.rerun()
        num_items = st.number_input(
            "Number of datapoints to generate",
            min_value=1,
            max_value=10,
            value=1,
            help="Number of items to generate per table"
        )
        data_generator = DataGenerator(st.session_state.get('client'))
        if st.button("Generate More Data", use_container_width=True):
            with st.spinner("Generating new data..."):
                updated_data = data_generator.generate_more_data(st.session_state.context, num_items)
                if updated_data:
                    st.session_state.context = updated_data
                    st.rerun()
    

    # Display tools below the data
    st.markdown("---")
    st.subheader("Available Tools")
    with st.expander("🔧 Functions available to the AI Agents", expanded=True):
        st.info("A list of functions that the AI Agents can use to manipulate the data above or handle connections with external systems (APIs, AI Search etc.).")
        cols = st.columns(2)
        with cols[0]:
            simplified_tools = [
                {
                    "name": tool["function"]["name"],
                    "description": tool["function"]["description"]
                }
                for tool in tools
                if tool.get("type") == "function" and "function" in tool
            ]
            
            tools_md = "\n".join([
                f"\n**`{tool['name']}`**  \n{tool['description']}\n"
                for tool in simplified_tools
            ])
            with st.container(height=400):
                st.markdown(tools_md)

        with cols[1]:
            with st.container(height=400):
                st.code(functions, language="python")
        
        