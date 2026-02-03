import os
import sys
import argparse
import json

def generate_tasks_yaml(prompt):
    """
    Generates a YAML string for tasks based on the prompt using LLM.
    Defaults to GEMINI_API_KEY, falls back to OPENAI_API_KEY.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if not gemini_key and not openai_key:
        print("Error: Neither GEMINI_API_KEY nor OPENAI_API_KEY environment variables are set.", file=sys.stderr)
        sys.exit(1)

    system_instruction = (
        "You are a helper that generates task lists in YAML format. "
        "The output must be a valid YAML document starting with 'tasks:' key. "
        "Each task has a 'heading' and a 'description'. "
        "Description can contain markdown. "
        "Do not include markdown fences (```yaml) in the output, just the raw YAML."
    )
    
    user_message = f"Generate a list of tasks for: {prompt}"

    # Default to Gemini if available
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Combine system instruction into the prompt for Gemini if system_instruction param not strictly used
            # newer gemini versions support system_instruction in constructor, sticking to prompt concat for safety or simple usage
            full_prompt = f"{system_instruction}\n\nUser Request: {prompt}"
            
            response = model.generate_content(full_prompt)
            return clean_response(response.text)
        except Exception as e:
            if openai_key:
                 # Fallback/alternative if Gemini fails but key was present (though logic says default to Gemini)
                 # But typically if key exists we try it. If it fails, maybe we shouldn't switch unless requested.
                 # But sticking to "uses either... default to GEMINI"
                 print(f"Gemini generation failed: {e}. Trying OpenAI...", file=sys.stderr)
            else:
                 print(f"Gemini generation failed: {e}", file=sys.stderr)
                 sys.exit(1)

    # Use OpenAI if Gemini key missing or failed (and we reached here)
    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_message}
                ]
            )
            return clean_response(response.choices[0].message.content)
        except Exception as e:
            print(f"OpenAI generation failed: {e}", file=sys.stderr)
            sys.exit(1)

def clean_response(text):
    """Remove markdown code blocks if present."""
    text = text.strip()
    if text.startswith("```yaml"):
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
    
    yaml_output = generate_tasks_yaml(args.prompt)
    print(yaml_output)
