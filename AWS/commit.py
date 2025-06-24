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
        print(f"Bedrock- Git Commit Error: {e}")
        return None
# Main flow
diff_text = get_full_git_diff()
if diff_text:
    commit_msg = create_commit_message(diff_text)
    if commit_msg:
        print("\nSuggested Commit Message:\n", commit_msg)
else:
    print("No diff found or git command failed.")
