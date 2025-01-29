import os
from pathlib import Path
import json
import shutil

def create_use_case_template(base_case: str) -> dict:
    """Load template files from an existing use case."""
    base_path = Path("use_cases") / base_case
    template = {}
    
    try:
        # Load data.json
        with open(base_path / "data.json", "r") as f:
            template["data"] = json.load(f)
            
        # Load tools.py
        with open(base_path / "tools.py", "r") as f:
            template["tools"] = f.read()
            
        # Load functions.py
        with open(base_path / "functions.py", "r") as f:
            template["functions"] = f.read()
            
        return template
    except Exception as e:
        raise Exception(f"Error loading template from {base_case}: {str(e)}")

def validate_use_case_name(use_case_name):
    # Check if string only contains letters and underscores
    return all(char.isalpha() or char == '_' for char in use_case_name)

def create_use_case_files(name: str, files_content: dict):
    """Create a new use case directory with generated files."""
    base_path = Path("use_cases") / name.lower()
    
    try:
        # Create directory
        base_path.mkdir(parents=True, exist_ok=False)
        
        # Create data.json
        with open(base_path / "data.json", "w") as f:
            json.dump(files_content["data"], f, indent=2)
            
        # Create tools.py
        with open(base_path / "tools.py", "w") as f:
            f.write(files_content["tools"])
            
        # Create functions.py
        with open(base_path / "functions.py", "w") as f:
            f.write(files_content["functions"])
            
    except Exception as e:
        # Clean up if anything fails
        if base_path.exists():
            for file in base_path.glob("*"):
                file.unlink()
            base_path.rmdir()
        raise Exception(f"Error creating use case files: {str(e)}")

def generate_use_case_content(description: str, template: dict, o1_client) -> dict:
    """Generate new use case files using O1."""
    prompt = f"""Given the following use case description and template files, generate a new set of files for this use case.

Description:
{description}

Template Files:
1. data.json (example structure):
{json.dumps(template['data'], indent=2)}

2. tools.py (example):
{template['tools']}

3. functions.py (example):
{template['functions']}

Please generate new versions of these files that implement the described use case while semantic cohesiveness.
Improvise and create the data and tools that you find appropriate for this use case.
Return the content as a JSON object with three keys: 'data', 'tools', and 'functions'.
The 'data' value should be a JSON object, while 'tools' and 'functions' should be strings containing the Python code.
The values True and False will also always be with a capital T and F respectively.
Sample scenarios are necessary definitions of tasks that can be performed using the functions and sample data (if ID is needed it needs to be present in Sample Data)
Function mapping is necessary.
Format your response as a valid JSON object.
"""

    response = o1_client.chat.completions.create(
        model=o1_client.deployment_name,
        messages=[{
            'role': 'user',
            'content': prompt
        }],
        response_format={ "type": "json_object" }
    )
    
    try:
        # Parse the response into a dictionary
        content = json.loads(response.choices[0].message.content)
        required_keys = {'data', 'tools', 'functions'}
        
        if not all(key in content for key in required_keys):
            raise ValueError("Generated content missing required keys")
            
        return content
    except Exception as e:
        raise Exception(f"Error parsing O1 response: {str(e)}")




def delete_use_case(use_case_name: str) -> bool:
    """
    Delete a use case directory and all its contents.
    
    Args:
        use_case_name (str): Name of the use case to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
        
    Raises:
        Exception: If there's an error during deletion
    """
    try:
        base_path = Path("use_cases") / use_case_name.lower()
        
        # Check if use case exists
        if not base_path.exists():
            raise Exception(f"Use case '{use_case_name}' does not exist")
            
        # Remove directory and all contents
        shutil.rmtree(base_path)
        return True
        
    except Exception as e:
        raise Exception(f"Error deleting use case: {str(e)}")

def add_use_case_manager(st, o1_client):
    """Add use case management UI elements to the sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.header("Generate a Use Case")
    st.sidebar.markdown("You can define your own agentic use case. O1 will use your description to generate the necessary sample data and functionality.")
    
    # Create tabs for Create and Delete operations
    create_tab, delete_tab = st.sidebar.tabs(["Create New", "Delete Existing"])
    
    # Get existing use cases
    existing_cases = [d.name for d in Path("use_cases").iterdir() if d.is_dir()]
    
    with create_tab:
        # Input fields for creation
        use_case_name = st.text_input(
            "Use Case Name",
            help="Enter a name for the new use case (letters and underscores only)"
        )
        
        use_case_description = st.text_area(
            "Use Case Description",
            help="Describe what this use case should do"
        )
        
        template_case = st.selectbox(
            "Template From",
            existing_cases,
            help="Select an existing use case to use as a template"
        )
        
        if st.button("Create Use Case", use_container_width=True):
            try:
                # Validate inputs
                if not use_case_name or not use_case_description:
                    st.error("Please provide both name and description")
                    return
                    
                if not validate_use_case_name(use_case_name):
                    st.error("Invalid use case name. Use only letters and underscores.")
                    return
                    
                # Check if use case already exists
                if (Path("use_cases") / use_case_name.lower()).exists():
                    st.error("Use case with this name already exists")
                    return
                
                with st.status("Creating new use case...") as status:
                    # Load template
                    template = create_use_case_template(template_case)
                    status.write("Template loaded...")
                    
                    # Generate new content
                    status.write("Generating content with O1...")
                    content = generate_use_case_content(use_case_description, template, o1_client)
                    status.write("Content generated...")
                    
                    # Create files
                    status.write("Creating files...")
                    create_use_case_files(use_case_name, content)
                    
                    status.update(label="✅ Use case created successfully!", state="complete")
                    st.toast("Use case created successfully! You can now select it from use case selector.")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error creating use case: {str(e)}")
    
    with delete_tab:
        # Delete functionality
        use_case_to_delete = st.selectbox(
            "Select Use Case to Delete",
            existing_cases,
            help="Select the use case you want to delete"
        )
        
        # Add confirmation checkbox
        confirm_delete = st.checkbox(
            "I understand this action cannot be undone",
            help="Please confirm you want to delete this use case"
        )
        
        if st.button("Delete Use Case", 
                    use_container_width=True,
                    disabled=not confirm_delete,
                    type="primary" if confirm_delete else "secondary"):
            try:
                with st.status("Deleting use case...") as status:
                    delete_use_case(use_case_to_delete)
                    status.update(label="✅ Use case deleted successfully!", state="complete")
                    st.rerun()
            except Exception as e:
                st.error(f"Error deleting use case: {str(e)}")

  