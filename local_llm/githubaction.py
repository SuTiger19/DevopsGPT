
import ollama
from pathlib import Path
import os

def generate_docker_ci(branch, app_dir, dockerhub_user, image_name):
    """Generate GitHub Actions YAML for Docker build and push"""
    prompt = PROMPT_TEMPLATE.format(
        BRANCH=branch,
        APP_DIR=app_dir,
        DOCKERHUB_USERNAME=dockerhub_user,
        IMAGE_NAME=image_name
    )

    try:
        response = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.2}
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error generating GitHub Action YAML: {e}")
        return None
    
    

def save_yamlfile(content, path='.'):
    """Save generated YAML file"""
    yamlfile_path = Path(path) / 'docker-ci.yml'
    try:
        with open(yamlfile_path, 'w') as f:
            f.write(content)
        print(f"\n YAML file saved to: {yamlfile_path.resolve()}")
    except Exception as e:
        print(f" Error saving YAML file: {e}")



def main():
    print("GitHub Action Docker CI Generator using Ollama")
    print("Steps: login → build → tag → push\n")

    branch = input("Enter the branch(es) to trigger on (comma-separated): ").strip()
    if not branch:
        branch = "main"

    app_dir = input("Enter the application directory containing the Dockerfile [default: '.']: ").strip() or '.'
    dockerhub_user = input("Enter your Docker Hub username: ").strip()
    image_name = input("Enter the Docker image name: ").strip()

    if not dockerhub_user or not image_name:
        print(" Docker Hub username and image name are required.")
        return

    print("\n🚀 Generating GitHub Action YAML for Docker...")
    yamlfile = generate_docker_ci(branch, app_dir, dockerhub_user, image_name)

    if yamlfile:
        print("\n--- Generated YAML ---\n")
        print(yamlfile)

        save = input("\n Save this YAML to file? (y/n): ").lower()
        if save == 'y':
            path = input(f"Enter directory path [default: {os.getcwd()}]: ").strip()
            save_yamlfile(yamlfile, path or '.')
    else:
        print(" Failed to generate the GitHub Action YAML")

if __name__ == '__main__':
    main(