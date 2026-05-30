![Python](https://img.shields.io/badge/Python-3.14-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![n8n](https://img.shields.io/badge/n8n-Automation-orange)
![GitHub](https://img.shields.io/badge/GitHub-Version%20Control-black)
![Status](https://img.shields.io/badge/Status-Active%20Development-green)


# UrbanOps AI Builder

AI-powered automation platform that generates, packages, and delivers web projects automatically using Streamlit, n8n, Python, and Gmail integrations.

---

# Overview

UrbanOps AI Builder is an experimental AI automation system designed to:

- Generate landing page projects
- Package project files automatically
- Compress builds into ZIP archives
- Send completed projects through Gmail
- Integrate Streamlit frontends with n8n workflows
- Create scalable AI-powered development pipelines

The system combines:
- Python
- Streamlit
- n8n
- GitHub
- Gmail automation
- AI orchestration workflows

---

# Features

## Automated Workflow

The current workflow pipeline:

1. Streamlit receives project request
2. Project files are generated
3. Files are copied into staging directory
4. n8n workflow activates
5. Files are compressed into ZIP archive
6. Gmail sends completed package
7. Webhook responds with success status

---

# Current n8n Workflow

Webhook  
→ Read/Write Files from Disk  
→ Compression  
→ Gmail Send Message  
→ Respond to Webhook

---

# Technologies Used

- Python
- Streamlit
- n8n
- Git
- GitHub
- Gmail API
- PowerShell
- HTML/CSS/JavaScript

---

# Security

Sensitive files are protected using `.gitignore`.

Excluded items include:

- `.env`
- `.venv`
- generated ZIP files
- temporary project outputs
- n8n local storage

---

# Installation

## Clone Repository

```bash
git clone https://github.com/cano1362/urbanops-ai-builder.git
```

## Enter Project Folder

```bash
cd urbanops-ai-builder
```

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate Environment

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

# Run Streamlit

```bash
streamlit run app.py
```

---

# Future Roadmap

- AI multi-agent orchestration
- Automated deployment system
- SaaS dashboard
- User authentication
- Stripe integration
- Docker support
- Cloud deployment
- Project templates marketplace
- AI code generation agents
- Enterprise workflow automation

---

# Author

Leonardo Vega  
Founder of UrbanOps

---

# Status

Active Development
