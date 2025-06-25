import subprocess
import ollama

def get_full_git_diff():
    try:
        # Get the full unified diff (actual code changes)
        result = subprocess.run(
            ['git', 'diff', 'HEAD~1', 'HEAD'],
            capture_output=True, text=True, check=True
        )

        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        print("Error running git diff:", e)
        return None

def create_commit_message(diff_text):
    if not diff_text:
        return None

    prompt = (
        "Based on the following Git diff, generate a concise and meaningful commit message :\n\n"
        f"{diff_text}"
    )

    try:
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_KEY")
        deployment = os.getenv("AZURE_DEPLOYMENT_NAME")
        headers = {
            "api-key": api_key,
            "Content-Type": "application/json"
        }
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }
        response = requests.post(
            f"{azure_endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2023-07-01-preview",
            headers=headers, json=data
        )
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Azure Error: {e}")
        return None
# Main flow
diff_text = get_full_git_diff()
if diff_text:
    commit_msg = create_commit_message(diff_text)
    if commit_msg:
        print("\nSuggested Commit Message:\n", commit_msg)
else:
    print("No diff found or git command failed.")
