from flask import Flask, render_template
import yaml
import os

app = Flask(__name__)

def load_tasks():
    """Load tasks from the YAML file."""
    yaml_path = os.path.join(os.path.dirname(__file__), 'tasks.yaml')
    try:
        with open(yaml_path, 'r') as file:
            data = yaml.safe_load(file)
            return data.get('tasks', [])
    except FileNotFoundError:
        print(f"Warning: {yaml_path} not found. Using empty task list.")
        return []
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return []

@app.route('/')
def index():
    """Render the main page with task cards."""
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
