# DevopsGPT - Automation of various Github Action and DockerFile using LLM 
---


**DevOpsGPT** is an AI-powered automation tool that leverages Large Language Models (LLMs) to generate:
-  Dockerfiles tailored to your application's language and structure
-  GitHub Actions for CI/CD pipelines (Terraform, Docker)
-  Intelligent Git commit messages from Git diffs

---

##  LLM Providers Supported

This tool supports generating DevOps assets using the following LLM backends:

| Provider         | Folder        | Description |
|------------------|---------------|-------------|
|  Local LLMs     | `local_llm/`   | Powered by Ollama – supports open models like LLaMA3 |
|  AWS Bedrock    | `AWS/`         | Titan, Claude, Mistral via Bedrock Runtime |
|  Azure Foundry  | `Azure/`       | Microsoft-hosted models (Phi-3, LLaMA2) via Azure AI Studio |
|  Google Gemini  | `Google/`      | Gemini 1.5 Pro via REST API |

Each folder contains model-specific logic and usage guides.

---

##  What Each Script Does

| Script         | Description |
|----------------|-------------|
| `commit.py`    | Generates a meaningful commit message from recent `git diff` |
| `docker.py`    | Creates an optimized Dockerfile based on language and project setup |
| `docker_cicd.py` | Generates GitHub Actions workflow for Docker CI/CD |
| `terraform_github.py` | Generates GitHub Actions workflow for Terraform deployments |

---

## ⚙️ Switching Between Providers

Each folder uses the same base script structure, but routes prompts through the respective API (Ollama, Bedrock, Azure, Gemini).  
The main logic (prompting, formatting, saving) remains consistent across providers — making it easy to switch backends.

---

##  Setup Instructions

Each provider folder contains its own `README.md` with:

- Required environment variables
- How to get API keys or credentials
- Example CLI usage

 Please refer to:
- `AWS/README.md` for Bedrock setup
- `Azure/README.md` for Azure AI Studio setup
- `Google/README.md` for Gemini setup
- `local_llm/README.md` for Ollama local inference

---

##  Example Use Cases

-  Spin up a Terraform pipeline on push to `main`
-  Generate a secure multi-stage Dockerfile for Node, Python, or Go
-  Create Docker CI/CD GitHub Actions to build and push to Docker Hub
-  Automatically generate a commit message like:  
  `"fix: optimize Docker build and remove unnecessary layers"`

---