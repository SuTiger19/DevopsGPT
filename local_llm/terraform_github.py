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
    yamlfile_path = Path(path) / 'terraform.yml'
    try:
        with open(yamlfile_path, 'w') as f:
            f.write(content)
        print(f"\n YAML file saved to: {yamlfile_path.resolve()}")
    except Exception as e:
        print(f"❌ Error saving YAML file: {e}")


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

    print("\n🚀 Generating GitHub Action YAML...")
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
