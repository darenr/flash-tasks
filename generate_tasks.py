import os
import sys
import argparse
import json


def generate_tasks_yaml(prompt):
    """
    Generates a YAML string for tasks based on the prompt using LLM.
    Returns a tuple (filename, yaml_content).
    Defaults to GEMINI_API_KEY, falls back to OPENAI_API_KEY.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if not gemini_key and not openai_key:
        print(
            "Error: Neither GEMINI_API_KEY nor OPENAI_API_KEY environment variables are set.",
            file=sys.stderr,
        )
        sys.exit(1)

    system_instruction = (
        "You are a helper that generates task lists like flash cards in YAML format. Approach the task generation creatively and ensure detail and variety in the tasks. Use markdown for formatting, tasks can be short or long, mix things up. for the description use multiple lines in the yaml for readability, as in description: |\nline 1\nline 2\n\n"
        "Provide the output as a JSON object with two keys:\n"
        "1. 'filename': A short, appropriate filename for these tasks ending in .yaml (e.g., 'interview-prep.yaml'). "
        "Ensure the filename is safe for file systems (lowercase, dashes instead of spaces).\n"
        "2. 'content': The valid YAML string starting with 'tasks:', containing 'heading' and 'description' keys. "
        "Description can contain markdown.\n"
        "Return ONLY the raw JSON object, no markdown formatting."
    )

    user_message = f"Generate a list of tasks for: {prompt}"

    response_text = ""

    # Default to Gemini if available
    if gemini_key:
        try:
            from google import genai

            client = genai.Client(api_key=gemini_key)

            full_prompt = f"{system_instruction}\n\nUser Request: {prompt}"

            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=full_prompt
            )
            response_text = response.text
        except Exception as e:
            if openai_key:
                print(f"Gemini generation failed: {e}. Trying OpenAI...", file=sys.stderr)
            else:
                print(f"Gemini generation failed: {e}", file=sys.stderr)
                sys.exit(1)

    # Use OpenAI if Gemini key missing or failed (and we reached here)
    if openai_key and not response_text:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=openai_key)

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_message},
                ],
                response_format={"type": "json_object"},
            )
            response_text = response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI generation failed: {e}", file=sys.stderr)
            sys.exit(1)

    return parse_response(response_text)


def parse_response(text):
    """Parse the JSON response to extract filename and content."""
    text = clean_response(text)
    try:
        data = json.loads(text)
        return data.get("filename", "generated_tasks.yaml"), data.get("content", "")
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON response from LLM.", file=sys.stderr)
        print(f"Raw response: {text[:100]}...", file=sys.stderr)
        return "error_generated.yaml", text


def clean_response(text):
    """Remove markdown code blocks if present."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```yaml"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate tasks YAML from a prompt.")
    parser.add_argument("prompt", help="The prompt to generate tasks for.")
    args = parser.parse_args()

    filename, yaml_output = generate_tasks_yaml(args.prompt)

    # Sanitize filename just in case
    filename = os.path.basename(filename)
    if not filename.endswith(".yaml"):
        filename += ".yaml"

    full_path = os.path.join("tasks", filename)

    # Ensure tasks directory exists
    os.makedirs("tasks", exist_ok=True)

    with open(full_path, "w") as f:
        f.write(yaml_output)

    print(f"Tasks generated and saved to {full_path}")
    print(yaml_output)
