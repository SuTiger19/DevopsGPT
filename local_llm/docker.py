
import ollama
from pathlib import Path
import os



PROMPT_TEMPLATE = """
Generate an ideal Dockerfile for a {language} application following best practices.
The application {has_dependencies} dependencies.

Requirements:
1. Use the most appropriate official base image
2. {dependency_instructions}
3. Set proper working directory
4. Copy only necessary files
5. Use multi-stage build if beneficial
6. Follow security best practices
7. Expose necessary ports if it's a web application
8. Include proper cleanup to minimize image size

Output ONLY the Dockerfile content with no additional explanation or commentary.
"""



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

    dep_file = dep_files.get(language.lower())
    if dep_file and os.path.exists(dep_file):
        with open(dep_file) as f:
            content = f.read()
            return {
                'has_dependencies': True,
                'instructions': f"Install dependencies from {dep_file}"
            }
    return {
        'has_dependencies': False,
        'instructions': "No specific dependency installation needed"
    }
def save_dockerfile(content, path='.'):
    """Save generated Dockerfile"""
    dockerfile_path = Path(path) / 'Dockerfile'
    try:
        with open(dockerfile_path, 'w') as f:
            f.write(content)
        print(f"\nDockerfile saved to: {dockerfile_path.resolve()}")
    except Exception as e:
        print(f"Error saving Dockerfile: {e}")




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

