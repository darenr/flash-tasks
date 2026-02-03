from flask import Flask, render_template
import yaml
import os
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
import argparse
import glob
import re
from loguru import logger


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if info:
            lang = info.split()[0]
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except:
                lexer = get_lexer_by_name("text", stripall=True)
        else:
            lexer = get_lexer_by_name("text", stripall=True)

        formatter = html.HtmlFormatter(cssclass="codehilite")
        return highlight(code, lexer, formatter)


app = Flask(__name__)


def slugify(text):
    """Create a URL/ID safe slug from text."""
    text = str(text).lower().strip()
    text = re.sub(r"[\W_]+", "-", text)
    return text.strip("-")


def process_task(task):
    """Process a single task to render markdown and determine layout."""
    # Use heading as primary key/id
    if "heading" in task:
        task["id"] = slugify(task["heading"])
    else:
        task["id"] = "unknown"

    task_id = task["id"]
    logger.debug(f"Processing task {task_id}")

    if "description" in task:
        raw_desc = task["description"]
        markdown = mistune.create_markdown(
            renderer=HighlightRenderer(),
            plugins=["table", "task_lists", "url", "strikethrough"],
            hard_wrap=True,
        )
        html_desc = markdown(raw_desc)
        task["description"] = html_desc

        # Determine if card should be wide
        # Check for code blocks or long descriptions (> 200 chars)
        has_code = "<pre>" in html_desc
        is_long = len(raw_desc.split()) > 100
        task["is_wide"] = has_code or is_long
        logger.debug(
            f"Task {task_id}: is_wide={task['is_wide']} (code={has_code}, long={is_long})"
        )

    return task


def load_from_file(file_path):
    """Load tasks from a single YAML file."""
    logger.info(f"Loading tasks from {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
            tasks = data.get("tasks", [])
            logger.info(f"Found {len(tasks)} tasks in {file_path}")
            return [process_task(task) for task in tasks]
    except FileNotFoundError:
        logger.warning(f"Warning: {file_path} not found.")
        return []
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML in {file_path}: {e}")
        return []


def load_tasks():
    """Load tasks from the configured source."""
    source_path = app.config.get("TASKS_SOURCE", "tasks")
    logger.info(f"Loading tasks from source: {source_path}")

    all_tasks = []

    if os.path.isdir(source_path):
        # Find all .yaml and .yml files
        yaml_files = glob.glob(os.path.join(source_path, "*.yaml")) + glob.glob(
            os.path.join(source_path, "*.yml")
        )
        yaml_files.sort()  # Consistent order
        logger.debug(f"Found {len(yaml_files)} YAML files in directory")
        for file_path in yaml_files:
            all_tasks.extend(load_from_file(file_path))
    else:
        all_tasks = load_from_file(source_path)

    logger.info(f"Total tasks loaded: {len(all_tasks)}")
    return all_tasks


@app.route("/")
def index():
    """Render the main page with task cards."""
    logger.info("Serving index page")
    tasks = load_tasks()
    title = app.config.get("PAGE_TITLE", "Flash Tasks")
    return render_template("index.html", tasks=tasks, title=title)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flash Tasks Server")
    parser.add_argument(
        "input_path",
        nargs="?",
        default="tasks/example.yaml",
        help="Path to a tasks.yaml file or a directory containing YAML files",
    )
    args = parser.parse_args()

    # Configure app based on args
    input_path = os.path.abspath(args.input_path)
    app.config["TASKS_SOURCE"] = input_path

    # Determine a nice title
    title_source = os.path.basename(input_path)
    # If it's a file, strip extension
    if os.path.isfile(input_path):
        title_source = os.path.splitext(title_source)[0]

    # Capitalize and replace separators
    clean_title = title_source.replace("-", " ").replace("_", " ").title()
    if not clean_title:
        clean_title = "Flash Tasks"

    app.config["PAGE_TITLE"] = clean_title

    # Get configuration from environment variables
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "5000"))

    logger.info("Starting Flash Tasks server")
    logger.info(f"Loading tasks from: {input_path}")
    logger.info(f"Bind: {host}:{port}, Debug: {debug_mode}")

    app.run(debug=debug_mode, host=host, port=port)
