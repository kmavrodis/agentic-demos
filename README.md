# O1 Multi-Industry Agentic Demos

A Streamlit application that demonstrates the use of AI agents (powered by OpenAI O1) to automate business processes and execute complex scenarios across multiple industries.

## Overview

This application provides a framework for creating and executing AI-powered workflows, where:
- O1-Mini generates strategic plans for handling complex scenarios
- GPT-4o executes these plans using predefined tools and functions
- Business data and processes can be simulated and managed in real-time

## Features

- 🏗️ **Dynamic Use Case Management**
  - Create new use cases with custom data structures and tools
  - Delete existing use cases
  - Generate sample data for testing

- 📊 **Interactive Data Visualization**
  - View and manage sample data in a grid layout
  - Generate additional test data on demand
  - Monitor data changes in real-time

- 🤖 **AI-Powered Workflow Execution**
  - Process predefined or custom scenarios
  - Watch the AI plan and execute solutions step by step
  - Track execution metrics and performance

- 🔧 **Extensible Tool Framework**
  - Define custom tools and functions for each use case
  - Monitor tool usage and execution results
  - Handle errors and provide detailed feedback
## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API access (including O1 model access)
- Azure OpenAI Service deployment

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/o1-agentic-demos.git
cd o1-agentic-demos
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy the sample environment file:
     ```bash
     cp .env.sample .env
     ```
   - Open `.env` and replace the placeholder values with your actual API keys and endpoints

4. Run the application:
```bash
streamlit run app.py
```


## Project Structure

```
├── app.py                 # Main application entry point
├── data_generator.py      # Handles sample data generation
├── data_view.py           # Data visualization components
├── prompts.py             # AI system prompts
├── scenario_processor.py  # Scenario execution logic
├── use_case_loader.py     # Use case management utilities
├── use_case_manager.py    # Use case creation/deletion
└── use_cases/             # Directory containing use case definitions
    └── [use_case_name]/
        ├── data.json      # Sample data
        ├── tools.py       # Available tools
        └── functions.py   # Function implementations
```

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables (see above)
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Select a Use Case**
   - Choose from existing use cases in the sidebar
   - Create new use cases with custom data and tools

2. **View Sample Data**
   - Examine the current data structure
   - Generate additional sample data
   - Monitor available tools and functions

3. **Execute Scenarios**
   - Select from sample scenarios or create custom ones
   - Watch the AI generate and execute plans
   - Review execution metrics and results

## Creating New Use Cases

1. Click "Create New" in the Use Case Management section
2. Provide:
   - Use case name (letters and underscores only)
   - Description of the use case
   - Template to base it on
3. The system will generate:
   - Sample data structure
   - Required tools and functions
   - Example scenarios


## Disclaimer

All sample data in this repository has been generated with Generative AI.


## Contributing

Contributions are welcome! Please feel free to submit pull requests, create issues, or suggest improvements.


