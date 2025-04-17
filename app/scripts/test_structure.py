# scripts/test_structure.py
import os

# Get the absolute path of the current script
script_path = os.path.abspath(__file__)
print(f"Script path: {script_path}")

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(script_path))
print(f"Project root: {project_root}")

# Check if data/generators directory exists
data_generators_path = os.path.join(project_root, "data", "generators")
print(f"data/generators path: {data_generators_path}")
print(f"Exists: {os.path.exists(data_generators_path)}")

# Check if app/data/generators directory exists
app_data_generators_path = os.path.join(project_root, "app", "data", "generators")
print(f"app/data/generators path: {app_data_generators_path}")
print(f"Exists: {os.path.exists(app_data_generators_path)}")

# List all directories in project root
print("\nDirectories in project root:")
for item in os.listdir(project_root):
    if os.path.isdir(os.path.join(project_root, item)):
        print(f"- {item}")