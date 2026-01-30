# Flash Tasks

A Flask-based web application that displays interactive task cards sourced from a YAML file. Each card features a heading and description with minimize and close functionality.

![Flash Tasks UI](https://github.com/user-attachments/assets/30061cf9-1aa6-4f57-8e8b-60561f333031)

## Features

- **Dynamic Card Loading**: Tasks are loaded from a YAML configuration file
- **Interactive UI**: Each card can be minimized or closed
- **Responsive Design**: Built with Tailwind CSS for a modern, responsive layout
- **shadcn-inspired Design**: Clean and professional UI following shadcn design patterns

## Installation

1. Clone the repository:
```bash
git clone https://github.com/darenr/flash-tasks.git
cd flash-tasks
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

### Configuration

The application can be configured using environment variables:

- `FLASK_DEBUG`: Enable debug mode (default: `False`)
- `FLASK_HOST`: Host to bind to (default: `127.0.0.1`)
- `FLASK_PORT`: Port to run on (default: `5000`)

Example with custom configuration:
```bash
FLASK_DEBUG=true FLASK_HOST=0.0.0.0 FLASK_PORT=8080 python app.py
```

**Security Note**: Never run with `FLASK_DEBUG=true` in production environments.

## Configuration

Tasks are defined in `tasks.yaml`. Each task should have the following structure:

```yaml
tasks:
  - id: 1
    heading: "Task Title"
    description: "Task description goes here."
  
  - id: 2
    heading: "Another Task"
    description: "Another task description."
```

### YAML Structure

- `tasks`: Root array containing all task objects
- `id`: Unique identifier for each task (integer)
- `heading`: Task title (string)
- `description`: Detailed task description (string)

## Card Controls

Each card has two control buttons in the top-right corner:

- **Minimize** (−): Collapses the card to show only the heading
- **Close** (×): Removes the card from view

## Project Structure

```
flash-tasks/
├── app.py              # Main Flask application
├── tasks.yaml          # Task definitions
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Main HTML template
└── static/            # Static assets (currently empty)
```

## Technologies Used

- **Flask**: Python web framework
- **PyYAML**: YAML parsing library
- **Tailwind CSS**: Utility-first CSS framework (loaded via CDN)

## License

See [LICENSE](LICENSE) file for details.
