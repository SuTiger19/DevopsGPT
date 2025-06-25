import subprocess
import os
from google import genai

def get_full_git_diff():
    try:
        result = subprocess.run(
            ['git', 'diff', 'HEAD~1', 'HEAD'],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("❌ Error running git diff:", e)
        return None

def create_commit_message(diff_text):
    if not diff_text:
        return None

    prompt = (
        "Based on the following Git diff, generate a concise and meaningful commit message:\n\n"
        f"{diff_text}"
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

# Main flow
diff_text = get_full_git_diff()

if diff_text:
    commit_msg = create_commit_message(diff_text)
    if commit_msg:
        print("\n Suggested Commit Message:\n", commit_msg)
    else:
        print(" Failed to generate commit message.")
else:
    print(" No diff found or git command failed.")
