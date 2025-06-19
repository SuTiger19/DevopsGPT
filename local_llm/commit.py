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
# Main flow
diff_text = get_full_git_diff()
if diff_text:
    commit_msg = create_commit_message(diff_text)
    if commit_msg:
        print("\nSuggested Commit Message:\n", commit_msg)
else:
    print("No diff found or git command failed.")
