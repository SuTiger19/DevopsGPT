import ollama
from pathlib import Path
import os

PROMPT_TEMPLATE = """
Generate an ideal Dockerfile for a {language} application following best practices.
The application {has_dependencies} dependencies.

Requirements:
1. Speical Reqiuremnt or No : {extra_requirement}, if no , then continue with rest of reqiurment 
2. Use the most appropriate official base image
3. {dependency_instructions}
4. Set proper working directory
5. Copy only necessary files
6. Use multi-stage build if beneficial
7. Follow security best practices
8. Expose necessary ports if it's a web application
9. Include proper cleanup to minimize image size

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

def generate_dockerfile(language, extra_requirement):
    """Generate Dockerfile using Ollama"""
    dep_info = get_dependency_info(language)
    """ Understanding dependency relate to Programming Lanangue, so it make sure include that in Docker File """
    prompt = PROMPT_TEMPLATE.format(
        language=language,
        has_dependencies="has" if dep_info['has_dependencies'] else "doesn't have",
        dependency_instructions=dep_info['instructions'],
        extra_requirement = extra_requirement
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

def save_dockerfile(content, path='.'):
    """Save generated Dockerfile"""
    dockerfile_path = Path(path) / 'Dockerfile'
    try:
        with open(dockerfile_path, 'w') as f:
            f.write(content)
        print(f"\nDockerfile saved to: {dockerfile_path.resolve()}")
    except Exception as e:
        print(f"Error saving Dockerfile: {e}")

def main():
    print("Dockerfile Generator using Ollama")
    print("--------------------------------")
    
    language = input("Enter the programming language (e.g., Python, Node, Java): ").strip()
    while not language:
        print("Language cannot be empty!")
        language = input("Enter the programming language: ").strip()
    extra_requirement = input( "Is there any extra requirement for your dockerfile, if not please type no:")


    print("\nGenerating Dockerfile...")
    dockerfile = generate_dockerfile(language, extra_requirement)
    
    if dockerfile:
        print("\nGenerated Dockerfile:\n")
        print(dockerfile)
        
        save = input("\nSave to Dockerfile? (y/n): ").lower()
        if save == 'y':
            path = input(f"Enter directory path [current: {os.getcwd()}]: ").strip()
            save_dockerfile(dockerfile, path or '.')
    else:
        print("Failed to generate Dockerfile")

if __name__ == '__main__':
    main()