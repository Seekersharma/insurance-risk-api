# OpenAI Skills Explorer

> Production-ready examples demonstrating **OpenAI Skills** with **Azure AI Foundry** and the **Azure OpenAI Responses API**.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Azure AI Foundry](https://img.shields.io/badge/Azure-AI%20Foundry-0078D4)
![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-0078D4)
![Responses API](https://img.shields.io/badge/OpenAI-Responses%20API-green)


---

# Overview

This project demonstrates how to build applications using **OpenAI Skills** instead of embedding large business prompts directly inside application code.

The examples cover:

* ✅ Azure AI Foundry
* ✅ Azure OpenAI Responses API
* ✅ Inline Skills
* ✅ Local Skills (`SKILL.md`)
* ✅ GitHub Skills
* ✅ Skill Routing
* ✅ Real Token Usage Metrics
* ✅ Real Latency Comparison

The goal is to provide a clean, production-quality reference implementation that is easy to understand, extend, and demonstrate.

---

# Why Skills?

Traditional applications often place all business instructions inside a single prompt.

```
Application
     │
     ▼

Large Prompt
 ├── Role
 ├── Rules
 ├── Formatting
 ├── Examples
 └── Business Logic

     │
     ▼

LLM Response
```

As prompts grow, they become difficult to maintain, duplicate across applications, and harder to version.

OpenAI Skills move reusable business logic into dedicated assets.

```
Application
      │
      ▼

Azure OpenAI Responses API

      │
      ▼

Skill (SKILL.md)

      │
      ▼

Reusable Business Logic

      │
      ▼

LLM Response
```

Benefits:

* Reusable business logic
* Cleaner application code
* Version-controlled instructions
* Easier maintenance
* Consistent AI behavior

---

# Project Structure

```
openai-skills-explorer/

├── 01_create_skill/
├── 02_manage_skills/
├── 03_use_skills/
├── 04_compare/
├── 05_metrics/
├── 06_sample_skills/
├── 07_sample_data/
├── 08_docs/
│
├── config.py
├── requirements.txt
├── .env.example
└── README.md
```

---

# Sample Skills

## Claims Analysis

Analyzes insurance claims and produces:

* Risk assessment
* Key observations
* Recommended actions
* Executive summary

---

## Executive Summary

Converts long business documents into concise executive-level summaries.

Output includes:

* Key points
* Business impact
* Risks
* Next steps

---

## Insurance Assistant

Provides structured responses for insurance-related questions using predefined business guidelines.

---

# Examples

## 1. Basic Response

```
python 03_use_skills/01_basic_response.py
```

Demonstrates a standard Azure OpenAI Responses API call without Skills.

---

## 2. Inline Skill

```
python 03_use_skills/02_inline_skill.py
```

Business instructions are defined directly inside the request.

---

## 3. Local Skill

```
python 03_use_skills/03_local_skill.py
```

Uses:

```
claims_analysis/

├── SKILL.md
├── README.md
└── example.md
```

---

## 4. GitHub Skill

```
python 03_use_skills/04_github_skill.py
```

Loads a reusable Skill maintained in a GitHub repository.

---

## 5. Skill Router

```
python 03_use_skills/05_skill_router.py
```

Routes user requests to the appropriate Skill based on business intent.

Example:

```
Input

Summarize this executive email.

↓

Skill Selected

executive_summary

↓

Response
```

---

# Performance Comparison

The project includes a real comparison between:

* Standard prompting
* Prompting with Skills

Metrics are collected directly from:

```
response.usage
```

and measured application latency.

Example output:

```
==================================================

WITHOUT SKILL

Input Tokens : 1199
Output Tokens: 1610
Total Tokens : 2809

Latency      : 28.7 sec

==================================================

WITH SKILL

Input Tokens : 1318
Output Tokens: 1319
Total Tokens : 2637

Latency      : 24.4 sec

==================================================

Total Tokens Saved : 6%

Output Tokens Saved: 18%

Latency Improvement: 15%

==================================================
```

> Metrics shown above are examples. Actual values depend on the prompt, model, and Skill used.

---

# Architecture

```
                 User Request
                       │
                       ▼

          Azure OpenAI Responses API

                       │

        ┌──────────────┼──────────────┐

        ▼              ▼              ▼

  Inline Skill    Local Skill    GitHub Skill

        │              │              │

        └──────────────┼──────────────┘

                       ▼

               LLM Reasoning

                       ▼

                response.output

                       ▼

          response.usage + latency

                       ▼

            Performance Comparison
```

---

# Installation

Clone the repository:

```
git clone <repository-url>

cd openai-skills-explorer
```

Create a virtual environment:

```
python -m venv .venv

source .venv/bin/activate

# Windows

.venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file.

```
AZURE_OPENAI_ENDPOINT=

AZURE_OPENAI_API_KEY=

AZURE_OPENAI_API_VERSION=

AZURE_OPENAI_DEPLOYMENT=
```

---

# Technologies

* Python
* Azure AI Foundry
* Azure OpenAI
* OpenAI Responses API
* OpenAI Skills
* GitHub
* Markdown

---

# Business Value

| Traditional Prompting                  | OpenAI Skills               |
| -------------------------------------- | --------------------------- |
| Business logic inside application code | Business logic externalized |
| Duplicate prompts                      | Reusable Skills             |
| Difficult maintenance                  | Centralized updates         |
| Hard to version                        | Git-managed assets          |
| Inconsistent behavior                  | Standardized AI responses   |

---

# Future Enhancements

* Hosted Skills
* Enterprise Skill Catalog
* Multi-agent orchestration
* Automated Skill evaluation
* Observability dashboards
* CI/CD validation for Skills

---

