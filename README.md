# DevopsGPT
Automation of various Github Action and DockerFile using LLM 



This project leverages Large Language Models (LLMs) from multiple providers to **automatically generate DevOps assets** like Dockerfiles, GitHub Actions CI/CD pipelines, and commit messages. It supports:

- 🧠 **Local LLMs** via [Ollama](https://ollama.com/)
- ☁️ **AWS Bedrock**
- ☁️ **Azure AI Foundry**
- ☁️ **Google Gemini**

---

## 🚀 Features

- 🔁 **GitHub Actions Generator** for Terraform, Docker etc
- 🐳 **Secure Dockerfile Generator** based on language and dependencies
- ✏️ **AI-Generated Commit Messages** from actual Git diffs


---

## 🧠 Supported Providers

| Provider       | Path         | Notes |
|----------------|--------------|-------|
| Local LLM      | `local_llm/` | Powered by Ollama, supports models like LLaMA3 |
| AWS Bedrock    | `/AWS/`      | Uses `boto3` and supports Titan, Claude, Mistral |
| Azure Foundry  | `/Azure/`    | Inference via Azure ML endpoints (e.g., Phi-3, LLaMA2) |
| Google Gemini  | `/Google/`   | Uses Gemini Pro via REST API |

---

