import ollama
from pathlib import Path
import os

PROMPT_TEMPLATE = """
Generate an ideal Dockerfile for a {language} application following best practices.
The application {has_dependencies} dependencies.

Requirements:
1. Use the most appropriate official base image
    a.Choose minimal and secure base images (e.g., alpine, slim, or distroless if possible). - python:3.12-slim, node:20-alpine, golang:1.21-alpine.
2. Install required dependencies only {dependency_instructions}
    a.Avoid unnecessary tools or build packages in the final image.
    b.Use --no-cache or remove package manager caches.
    c. For Node: npm ci instead of npm install.
3.Set a proper working directory
    a.Use WORKDIR /app or a relevant directory name to isolate app files.
4.Copy only necessary files
    a.Use .dockerignore to exclude files like .git, node_modules, tests, etc.
    b.Copy only what's needed for build, then source code.
5.Use multi-stage builds when beneficial
    a.Separate build and runtime environments to reduce size. Like: use a builder stage with compilers/tools, then copy the built artifacts to a minimal runtime image.
6.Follow security best practices
    a.Avoid running as root: create and use a non-root user.
    b.Keep dependencies updated.
    c.Use image scanners like Trivy or Docker Scout.
    d.Minimize attack surface (no shell tools in production image).
7.Expose only necessary ports (for web apps)
    a.Use EXPOSE relevant PORT .
    b.Do not expose ports unnecessarily.
8.Include proper cleanup to minimize image size
    a.Remove temp build files, caches, logs after use.
    b.Combine commands using && to reduce layers.
    c. Use rm -rf /path/to/temp when needed.

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