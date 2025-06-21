

# 🧠 Git Commit Message Generator using Ollama + LLaMA 3

This Python script automatically generates meaningful commit messages by analyzing your latest code changes using `git diff` and summarizing them with the help of a local `llama3` model via the `ollama` API.

##  Features

- Extracts the latest Git diff between the current and previous commit (`HEAD~1` to `HEAD`)
- Uses `llama3` via Ollama to generate a concise commit message
- Minimal, human-readable, and context-aware suggestions