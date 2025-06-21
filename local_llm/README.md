

# 🧠 Git Commit Message Generator using Ollama + LLaMA 3

This Python script automatically generates meaningful commit messages by analyzing your latest code changes using `git diff` and summarizing them with the help of a local `llama3` model via the `ollama` API.

##  Features

- Extracts the latest Git diff between the current and previous commit (`HEAD~1` to `HEAD`)
- Uses `llama3` via Ollama to generate a concise commit message
- Minimal, human-readable, and context-aware suggestions

##  Requirements

- Python 3.7+
- [Ollama](https://ollama.com/) installed and running locally
- A Git repository initialized and containing at least one commit


## 📦 Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/your-username/git-commit-ai.git
   cd git-commit-ai
    ```

2. **Install dependencies:**

   ```bash
   pip install ollama
   ```

3. **Ensure Ollama is running:**

   Start your local Ollama server and ensure the `llama3` ( Can choice your own Model, just need update code with model name) model is pulled:

   ```bash
   ollama run llama3
   ```

   ```bash
   ollama run  {YOUR MODEL}
   ```

##  Usage

Simply run the script from the root of your Git repository:

```bash
python generate_commit_msg.py
```

If there are changes between the last two commits, it will output a suggested commit message based on those changes.

