import ollama
from pathlib import Path
import os

PROMPT_TEMPLATE = """
Generate an ideal GitHub Action for a Terraform application following best practices.

Requirements:
1. Run the workflow on these branches: {BRANCH}. If the branch is 'main', trigger only on pull requests.
2. Set permissions:
   contents: read
   pull-requests: write
3. Inside the job, do the following:
   a. Create environment variables for GitHub token and cloud credentials: {CREDENTIALS}, and specify the Terraform working directory: {TF_DIR}.
   b. Set verbosity for Terraform logs.
   c. Run the following steps in order:
      - checkout
      - setup Terraform
      - terraform fmt
      - terraform sec scan
      - terraform lint
      - terraform validate
      - terraform plan
   d. For `terraform plan`, if `github.event_name == 'pull_request'`, run a script that:
      - collects the outputs of each Terraform step
      - formats them into a comment
      - uses `github.rest.issues.createComment` to post the result back to the pull request
"""

def get_credentials(cloud):
    """Return credentials required for a given cloud provider"""
    cloud = cloud.strip().lower()
    cloud_cred = {
        'aws': 'AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY',
        'azure': 'ARM_CLIENT_ID, ARM_CLIENT_SECRET, ARM_SUBSCRIPTION_ID, and ARM_TENANT_ID',
        'google': 'GOOGLE_CREDENTIALS as JSON',
    }
    return cloud_cred.get(cloud, 'Unknown credentials (please update mapping)')

def generate_githubaction(cloud, branch, tf_dir="."):
    """Generate GitHub Action YAML using Ollama"""
    credentials = get_credentials(cloud)
    if "Unknown" in credentials:
        print(f"Unsupported cloud: {cloud}")
        return None

    prompt = PROMPT_TEMPLATE.format(
        CREDENTIALS=credentials,
        BRANCH=branch,
        TF_DIR=tf_dir
    )

    try:
        api_key_env = os.getenv("GEMINI_API_KEY")
        if not api_key_env:
            print("❌ GEMINI_API_KEY environment variable not set.")
            return None

        genai.configure(api_key=api_key_env)
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(
            [prompt],
            generation_config={
                'temperature': 0.2,
                'max_output_tokens': 100,
            }
        )
        
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        print(f" Error generating commit message using Gemini: {e}")
        return None

def save_yamlfile(content, path='.'):
    """Save generated YAML file"""
    yamlfile_path = Path(path) / 'terraform.yml'
    try:
        with open(yamlfile_path, 'w') as f:
            f.write(content)
        print(f"\n YAML file saved to: {yamlfile_path.resolve()}")
    except Exception as e:
        print(f" Error saving YAML file: {e}")

def main():
    print("GitHub Action Terraform Generator using Ollama")
    print("Steps: terraform fmt → lint → sec → validate → plan\n")

    cloud = input("Enter the Cloud Provider (AWS, Azure, Google): ").strip()
    while not cloud:
        print("Cloud cannot be empty!")
        cloud = input("Enter the Cloud Provider: ").strip()

    branch = input("Enter the branch(es) to trigger on (comma-separated): ").strip()
    if not branch:
        branch = "main"

    tf_dir = input("Enter the Terraform directory path [default: '.']: ").strip() or '.'

    print("\n Generating GitHub Action YAML...")
    yamlfile = generate_githubaction(cloud, branch, tf_dir)

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
    main()
