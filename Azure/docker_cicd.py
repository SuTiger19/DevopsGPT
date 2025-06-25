
import ollama
from pathlib import Path
import os


PROMPT_TEMPLATE = """
Generate a GitHub Action YAML file that builds a Docker image from the application's Dockerfile and pushes it to Docker Hub.

Requirements:
1. The workflow should trigger on pushes to these branches: {BRANCH}.
2. The Dockerfile is located in this directory: {APP_DIR}
3. The job should:
   - Set up Docker Buildx
   - Log in to Docker Hub using secrets: `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`
   - Build the Docker image with the appropriate tag: `{DOCKERHUB_USERNAME}/{IMAGE_NAME}:latest`
   - Push the image to Docker Hub
4. Follow GitHub security and Docker best practices.
5. Output only the GitHub Actions YAML file.
"""




def generate_docker_ci(branch, app_dir, dockerhub_user, image_name):
    """Generate GitHub Actions YAML for Docker build and push"""
    prompt = PROMPT_TEMPLATE.format(
        BRANCH=branch,
        APP_DIR=app_dir,
        DOCKERHUB_USERNAME=dockerhub_user,
        IMAGE_NAME=image_name
    )
    try:
        endpoint = os.getenv("AZURE_AI_ENDPOINT")  
        token = os.getenv("AZURE_AI_TOKEN")        

        if not endpoint or not token:
            print(" AZURE_AI_ENDPOINT or AZURE_AI_TOKEN is not set.")
            return None

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "input_data": {
                "input_string": [prompt]
            }
        }

        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        output = response.json()

        return output["output"][0]  # Assumes response contains: { "output": ["response text"] }

    except Exception as e:
        print(f"Azure AI Foundry Error: {e}")
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