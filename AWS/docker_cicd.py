
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
        client = boto3.client('bedrock-runtime', region_name='us-east-1')
        body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "temperature": 0.2,
                "maxTokenCount": 800
            }
        }
        response = client.invoke_model(
            modelId='amazon.titan-text-express-v1',
            body=json.dumps(body),
            contentType='application/json'
        )
        result = json.loads(response['body'].read())
        return result['results'][0]['outputText']
    except ClientError as e:
        print(f"Bedrock- Github_Action Error: {e}")
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