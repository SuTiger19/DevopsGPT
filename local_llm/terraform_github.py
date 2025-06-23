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
