# Flash Tasks

A Flask-based web application that displays interactive task cards sourced from a YAML file. Each card features a heading and description with minimize and close functionality.

![Flash Tasks UI](https://github.com/user-attachments/assets/30061cf9-1aa6-4f57-8e8b-60561f333031)

## Features

- **Dynamic Card Loading**: Tasks are loaded from a YAML configuration file.
- **Markdown Support**: Task descriptions support Markdown rendering, including bold, italics, lists, and more.
- **Syntax Highlighting**: Code blocks are properly formatted and highlighted (`fenced_code` and `codehilite`).
- **Smart Layout**: Cards containing code blocks or long descriptions are automatically adjusted to a wider layout for better readability.
- **Interactive UI**: Each card can be minimized or closed.
- **Responsive Design**: Built with Tailwind CSS for a modern, responsive layout.
- **shadcn-inspired Design**: Clean and professional UI following shadcn design patterns.

## Installation

### Using uv (Recommended)

This project uses `uv` for dependency management.

1. Clone the repository:
   ```bash
   git clone https://github.com/darenr/flash-tasks.git
   cd flash-tasks
   ```

2. Sync dependencies:
   ```bash
   uv sync
   ```

3. Run the application:
   ```bash
   uv run app.py
   ```

### Using pip

1. Clone the repository:
   ```bash
   git clone https://github.com/darenr/flash-tasks.git
   cd flash-tasks
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:
   ```bash
   # If using pip/python directly
   python app.py
   
   # If using uv
   uv run app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Configuration

### Application Settings

The application can be configured using environment variables:

- `FLASK_DEBUG`: Enable debug mode (default: `False`)
- `FLASK_HOST`: Host to bind to (default: `127.0.0.1`)
- `FLASK_PORT`: Port to run on (default: `5000`)

Example with custom configuration:
```bash
FLASK_DEBUG=true FLASK_HOST=0.0.0.0 FLASK_PORT=8080 python app.py
```

### Task Configuration

Tasks are defined in `tasks.yaml`. You can add new tasks by following this structure:

```yaml
tasks:
  - id: 1
    heading: "Task Title"
    description: |
      You can use **Markdown** here.
      
      ```python
      def hello():
          print("Hello World")
      ```
```

- **heading**: The title of the task card.
- **description**: The body of the card (supports Markdown). Card width will automatically expand for long text or code blocks.

## Card Controls

Each card has two control buttons in the top-right corner:

- **Minimize** (−): Collapses the card to show only the heading
- **Close** (×): Removes the card from view

## Project Structure

```
flash-tasks/
├── app.py              # Main Flask application
├── tasks.yaml          # Task definitions
├── pyproject.toml      # Project configuration and dependencies
├── requirements.txt    # Python dependencies (legacy)
├── templates/
│   └── index.html      # Main HTML template
└── static/
    └── css/
        └── pygments.css # Syntax highlighting styles
```

## Technologies Used

- **Flask**: Python web framework
- **PyYAML**: YAML parsing library
- **Markdown**: Text-to-HTML conversion tool
- **Pygments**: Syntax highlighting
- **Tailwind CSS**: Utility-first CSS framework (loaded via CDN)

## License

See [LICENSE](LICENSE) file for details.
