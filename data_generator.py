import json
from pathlib import Path
from typing import Dict, Any
from openai import AzureOpenAI
import streamlit as st

class DataGenerator:
    def __init__(self, client: AzureOpenAI):
        self.client = client

    def generate_more_data(self, data: Dict[str, Any], num_items: int) -> Dict[str, Any]:
        """Generate more data using OpenAI for all tables in a single call."""
        try:
            from prompts import DATA_GENERATION_PROMPT
            
            prompt = DATA_GENERATION_PROMPT.format(
                num_items=num_items,
                data=json.dumps(data, indent=2)
            )

            response = self.client.chat.completions.create(
                model=self.client.deployment_name,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant that generates realistic data. Only respond with valid JSON data that follows the exact same structure as the input."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            # Parse the generated data
            generated_data = json.loads(response.choices[0].message.content)
            
            # Ensure we have all the original keys
            for key in data:
                if key not in generated_data:
                    generated_data[key] = data[key]
            
            # Update session state context instead of file
            st.session_state.context = generated_data
            
            return generated_data
            
        except Exception as e:
            st.error(f"Error generating data: {str(e)}")
            return None

    def update_session_state(self, data: Dict[str, Any]) -> None:
        """Update the session state with new data."""
        try:
            st.session_state.context = data
        except Exception as e:
            st.error(f"Error updating session state: {str(e)}")