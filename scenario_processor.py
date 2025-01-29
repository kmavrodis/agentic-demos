import streamlit as st
import time
import json
from typing import List, Dict, Tuple
from prompts import O1_PLANNING_PROMPT, GPT4_EXECUTION_PROMPT

def process_message(message_type: str, content: str, arguments: dict = None) -> None:
    """Add a message to the session state message log and display it."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        
    message = {
        'type': message_type,
        'content': content,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'arguments': arguments
    }
    
    st.session_state.messages.append(message)
    
    # Create layout if it doesn't exist
    if 'layout_container' not in st.session_state:
        st.session_state.layout_container = st.container()
        with st.session_state.layout_container:
            st.session_state.plan_col, st.session_state.exec_col = st.columns([1, 1])
            with st.session_state.plan_col:
                st.markdown("### Planning")
            with st.session_state.exec_col:
                st.markdown("### Execution")
    
    # Display message
    if message_type == 'plan':
        with st.session_state.plan_col:
            with st.expander(f"{message['timestamp']} - Plan", expanded=True):
                st.markdown(content)
    else:
        with st.session_state.exec_col:
            with st.expander(f"{message['timestamp']} - {message_type.upper()}", expanded=True):
                if message_type == 'function':
                    func_name, content = content.split(':', 1)
                    st.code(func_name.strip())
                    if arguments:
                        st.write("Input Arguments:")
                        st.json(arguments)
                    st.write("Output:")
                    st.json(json.loads(content))
                elif message_type == 'error':
                    st.error(content)
                    if arguments:
                        st.error("Error Details:")
                        if isinstance(arguments, dict):
                            if 'arguments' in arguments:
                                st.write("Function Arguments:")
                                st.json(arguments['arguments'])
                            if 'error_type' in arguments:
                                st.write(f"Error Type: {arguments['error_type']}")
                            if 'traceback' in arguments:
                                st.write("Full Traceback:")
                                st.code(arguments['traceback'], language='python')
                elif message_type == 'status':
                    st.info(content)
                else:
                    st.write(content)

def call_o1(scenario: str, o1_mini_client, tools) -> str:
    """Generate a plan using O1-Mini."""
    prompt = f"{O1_PLANNING_PROMPT}\n\nTools:\n{tools}\n\nScenario:\n{scenario}\n\nPlease provide the next steps in your plan."
    
    status_container = st.empty()
    with status_container.container():
        st.info("🤖 Calling O1-Mini for planning...")
        progress_bar = st.progress(0)
        
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
            
        response = o1_mini_client.chat.completions.create(
            model=o1_mini_client.deployment_name,
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        st.success("✅ Planning completed!")
        time.sleep(1)
    
    status_container.empty()
    plan = response.choices[0].message.content
    process_message('plan', plan)
    return plan

def call_gpt4o(plan: str, tools: List[Dict], client, function_mapping: Dict) -> List[Dict]:
    """Execute the plan using GPT-4."""
    messages = [{'role': 'system', 'content': GPT4_EXECUTION_PROMPT.format(plan=plan)}]
    step_counter = 1
    status_container = st.empty()
    
    while True:
        with status_container:
            st.info(f"🤖 Execution Step {step_counter}")
        
        response = client.chat.completions.create(
            model=client.deployment_name,
            messages=messages,
            tools=tools,
            parallel_tool_calls=False
        )
        
        assistant_message = response.choices[0].message
        messages.append({
            "role": "assistant", 
            "content": assistant_message.content, 
            "tool_calls": assistant_message.tool_calls
        })
        
        if assistant_message.content:
            process_message('assistant', assistant_message.content)

        if not assistant_message.tool_calls:
            continue

        # Process tool calls
        tool_responses = []
        for tool_call in assistant_message.tool_calls:
            if tool_call.function.name == 'instructions_complete':
                status_container.empty()
                return messages

            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            try:
                process_message('status', f"Executing function: {function_name}")
                function_response = function_mapping[function_name](**arguments)
                process_message(
                    'function', 
                    f"{function_name}: {json.dumps(function_response)}", 
                    arguments=arguments
                )
                
                tool_responses.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(function_response)
                })
                
            except Exception as e:
                import traceback
                error_details = {
                    'function': function_name,
                    'error_message': str(e),
                    'error_type': type(e).__name__,
                    'traceback': traceback.format_exc(),
                    'arguments': arguments
                }
                process_message(
                    'error', 
                    f"Error in {function_name}: {str(e)}", 
                    arguments=error_details
                )
                tool_responses.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps({"error": error_details})
                })

        messages.extend(tool_responses)
        step_counter += 1

def count_operations(messages: List[Dict]) -> Dict[str, int]:
    """Count different types of operations from the message history."""
    function_calls = 0
    assistant_messages = 0
    tool_messages = 0
    
    for msg in messages:
        if isinstance(msg, dict):
            role = msg.get('role', '')
            if role == 'assistant':
                assistant_messages += 1
            elif role == 'tool':
                tool_messages += 1
                function_calls += 1
    
    return {
        'function_calls': function_calls,
        'assistant_messages': assistant_messages,
        'tool_messages': tool_messages
    }

def add_scenario_selector(sample_scenarios: list) -> str:
    """Add a scenario selector to the Streamlit UI and return the selected scenario."""
    input_method = st.radio(
        "Choose input method",
        ["Select from samples", "Enter custom scenario"],
        horizontal=True
    )

    if input_method == "Select from samples":
        scenario = st.selectbox(
            "Select a sample scenario",
            sample_scenarios,
            key="sample_scenario"
        )
    else:
        scenario = st.text_input(
            "Enter your custom scenario",
            key="custom_scenario"
        )
        
    return scenario

def process_scenario(scenario: str, o1_mini_client, client, tools: List[Dict], 
                    function_mapping: Dict) -> Tuple[List[Dict], str]:
    """Process a scenario by generating and executing a plan."""
    process_container = st.empty()
    
    with process_container.container():
        # Planning phase
        process_message('status', 'Generating plan...')
        start_time = time.time()
        plan = call_o1(scenario, o1_mini_client, tools)
        planning_time = time.time() - start_time
        
        # Execution phase
        process_message('status', 'Executing plan...')
        start_time = time.time()
        messages = call_gpt4o(plan, tools, client, function_mapping)
        execution_time = time.time() - start_time
        
        # Count operations
        operation_counts = count_operations(messages)
        
        # Show completion summary
        st.success("✨ Processing Complete!")
        st.write("📊 Process Summary:")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Planning Time", f"{planning_time:.2f}s")
        with col2:
            st.metric("Execution Time", f"{execution_time:.2f}s")
        with col3:
            st.metric("Function Calls", operation_counts['function_calls'])
        with col4:
            st.metric("Assistant Messages", operation_counts['assistant_messages'])
        with col5:
            st.metric("Tool Messages", operation_counts['tool_messages'])
            
    process_message('status', 'Processing complete.')
    return messages, plan

def display_scenario_tab(tools: List[Dict], function_mapping: Dict, sample_scenarios: List[str]):
    """Display the scenario processing tab content."""
    st.subheader("Build and Execute an Agentic Workdlow")
    st.info("Select one of the pre-generated scenarios or create a custom new one. Click 'Process Scenario' to build and execute a workflow.")

    # Add scenario selector
    scenario = add_scenario_selector(sample_scenarios)
    
    # Reset the layout container when starting a new scenario
    if st.button("Process Scenario", key="process_scenario_button"):
        if 'layout_container' in st.session_state:
            del st.session_state.layout_container
        
        with st.spinner("Processing scenario..."):
            messages, plan = process_scenario(
                scenario=scenario,
                o1_mini_client=st.session_state.o1_mini_client,
                client=st.session_state.client,
                tools=tools,
                function_mapping=function_mapping
            )