
import ollama
from pathlib import Path
import os


def get_dependency_info(language):
    """Determine if project has dependencies and how to install them"""
    dep_files = {
        'python': 'requirements.txt',
        'javascript': 'package.json',
        'java': 'pom.xml',
        'golang': 'go.mod',
        'ruby': 'Gemfile',
        'php': 'composer.json'
    }


    

def generate_dockerfile(language):
    """Generate Dockerfile using Ollama"""

    # Understanding dependency relate to Programming Lanangue, so it make sure include that in Docker File
    dep_info = get_dependency_info(language)
    

    # Prompt which will be input into LLM -  It using ollama module with llama3 in our case. Can switch model there.
    prompt = PROMPT_TEMPLATE.format(
        language=language,
        has_dependencies="has" if dep_info['has_dependencies'] else "doesn't have",
        dependency_instructions=dep_info['instructions']
    )
    
    try:
        response = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.2}
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error generating Dockerfile: {e}")
        return None



def main():
    print("Dockerfile Generator using Local LLM : Ollama")
    print("--------------------------------")
    
    language = input("Enter the programming language (e.g., Python, Node, Java): ").strip()
    while not language:
        print("Language cannot be empty!")
        language = input("Enter the programming language: ").strip()
            
    print("\nGenerating Dockerfile...")
    dockerfile = generate_dockerfile(language)

if __name__ == '__main__':
    main()

