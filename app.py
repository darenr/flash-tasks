from flask import Flask, render_template
import yaml
import os
import markdown

app = Flask(__name__)


def load_tasks():
    """Load tasks from the YAML file."""
    yaml_path = os.path.join(os.path.dirname(__file__), "tasks.yaml")
    try:
        with open(yaml_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            tasks = data.get("tasks", [])
            # Convert markdown descriptions to HTML
            for task in tasks:
                if "description" in task:
                    raw_desc = task["description"]
                    html_desc = markdown.markdown(
                        raw_desc, extensions=["fenced_code", "codehilite"]
                    )
                    task["description"] = html_desc

                    # Determine if card should be wide
                    # Check for code blocks or long descriptions (> 200 chars)
                    has_code = "<pre>" in html_desc
                    is_long = len(raw_desc) > 200
                    task["is_wide"] = has_code or is_long
            return tasks
    except FileNotFoundError:
        print(f"Warning: {yaml_path} not found. Using empty task list.")
        return []
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return []


@app.route("/")
def index():
    """Render the main page with task cards."""
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    # Get configuration from environment variables
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "5000"))

    app.run(debug=debug_mode, host=host, port=port)
