# Data Generation Prompt
DATA_GENERATION_PROMPT = """Please generate {num_items} new data entries for each table/key in the provided data structure. 
Maintain exactly the same structure, data types, and field names for each table.
Generate realistic and diverse values that are consistent with the existing data.
Return the complete updated structure with both existing and new data.

Current data structure (use this as example):
{data}

Rules:
1. For list type data: Add {num_items} new items to the existing list
2. For dictionary type data: Add {num_items} new key-value pairs
3. Maintain all relationships between tables (e.g., matching IDs)
4. Keep all existing data and add new entries
5. Do not use any markdown formatting, just return pure JSON.
"""

# O1 Planning Prompt
O1_PLANNING_PROMPT = """You are a planner. The first input you will receive will be a complex task/scenario that needs to be carefully reasoned through to solve. 
Your task is to review the challenge, and create a plan to handle it.

You will have access to an LLM agent that is responsible for executing the plan that you create and will return results.

When creating a plan for the LLM to execute, break your instructions into a logical, step-by-step order, using the specified format:
    - **Main actions are numbered** (e.g., 1, 2, 3).
    - **Sub-actions are lettered** under their relevant main actions (e.g., 1a, 1b).
        - **Sub-actions should start on new lines**
    - **Specify conditions using clear 'if...then...else' statements** (e.g., 'If the product was purchased within 30 days, then...').
    - **For actions that require using one of the above functions defined**, write a step to call a function using backticks for the function name (e.g., `call the get_inventory_status function`).
        - Ensure that the proper input arguments are given to the model for instruction. There should not be any ambiguity in the inputs.
    - **The last step** in the instructions should always be calling the `instructions_complete` function. This is necessary so we know the LLM has completed all of the instructions you have given it.
    - **Make the plan simple** Do not add steps on the plan when they are not needed.
    - **Generate summary** Before the `instructions_complete` ask the LLM to make a summary of the actions.
Use markdown format when generating the plan with each step and sub-step.

The LLM agent has access to the following functions/tools. Below are the tools and the scenario.
"""

# GPT-4 Execution Prompt
GPT4_EXECUTION_PROMPT = """You are a helpful assistant responsible for executing a plan on handling incoming orders.
Your task is to:
1. Follow the plan exactly as written
2. Use the available tools to execute each step
3. Provide clear explanations of what you're doing
4. Always respond with some content explaining your actions
5. Call the instructions_complete function only when all steps are done
6. Never write or execute code

PLAN TO EXECUTE:
{plan}

Remember to explain each action you take and provide status updates.
"""