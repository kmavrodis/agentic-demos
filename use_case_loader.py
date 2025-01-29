import json
import importlib.util
import sys
from pathlib import Path
from typing import Dict, Any, Tuple, List
import inspect

class UseCaseLoader:
    def __init__(self, base_path: str = "use_cases"):
        self.base_path = Path(base_path)
        
    def load_use_cases(self) -> List[str]:
        """Load all available use cases from the use_cases directory."""
        use_cases = []
        
        if self.base_path.exists():
            for folder in self.base_path.iterdir():
                if folder.is_dir():
                    data_file = folder / "data.json"
                    if data_file.exists():
                        use_cases.append(folder.name)
        
        return sorted(use_cases)

    def import_module(self, use_case: str, module_name: str) -> Any:
        """Dynamically import a Python module from a use case directory."""
        module_path = self.base_path / use_case / f"{module_name}.py"
        
        if not module_path.exists():
            raise FileNotFoundError(f"Module {module_name}.py not found in {use_case}")
            
        spec = importlib.util.spec_from_file_location(
            f"{use_case}.{module_name}", 
            str(module_path)
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    def load_use_case_components(self, use_case: str) -> Dict[str, Any]:
        """Load all components for a specific use case."""
        try:
            # Load JSON data
            data_path = self.base_path / use_case / "data.json"
            with open(data_path, 'r') as f:
                data = json.load(f)
            
            # Import Python modules
            tools_module = self.import_module(use_case, "tools")
            functions_module = self.import_module(use_case, "functions")
            
            return {
                'data': data,
                'tools': getattr(tools_module, 'TOOLS', []),
                'function_mapping': getattr(functions_module, 'FUNCTION_MAPPING', {}),
                'sample_scenarios': getattr(functions_module, 'SAMPLE_SCENARIOS', []),
                'functions': inspect.getsource(functions_module)
            }
            
        except Exception as e:
            raise Exception(f"Error loading use case {use_case}: {str(e)}")

    def validate_use_case(self, use_case: str) -> bool:
        """Validate that a use case has all required files."""
        required_files = ['data.json', 'tools.py', 'functions.py']
        use_case_path = self.base_path / use_case
        
        if not use_case_path.exists():
            return False
            
        return all((use_case_path / file).exists() for file in required_files)