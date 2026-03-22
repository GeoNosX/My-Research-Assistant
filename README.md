# 🔬 AI Multi-Agent Research Assistant

An autonomous, multi-agent AI research system that dynamically generates a team of specialized AI experts to investigate any given topic. Built with LangGraph and powered by Meta's Llama 3.1 70B, the agents conduct independent web searches, compile their findings, and synthesize a massive, multi-perspective final report.

## 🚀 Features

* **Dynamic AI Personas:** Input a topic, and the system automatically generates a customized team of researchers with unique roles, backgrounds, and perspectives.
* **Autonomous Web Research:** Agents utilize Google Serper, Tavily, and Wikipedia to hunt down real-time, factual information.
* **Multi-Perspective Synthesis:** The system aggregates individual agent reports into one comprehensive master document.
* **Fully Containerized:** Runs flawlessly on any machine using Docker and Docker Compose.
* **Automated CI/CD:** Protected by GitHub Actions with automated Pytest runs and Docker build verifications.

## 🛠️ Tech Stack

* **Frontend:** Vanilla HTML, CSS, JavaScript (served via Nginx)
* **Backend:** Python 3.11, FastAPI, Uvicorn
* **AI Orchestration:** LangGraph, LangChain
* **LLM:** Meta Llama 3.1 70B Instruct (via Nvidia Inference API)
* **Tools:** Google Serper API, Tavily Search API, Wikipedia
* **Infrastructure:** Docker, Docker Compose, GitHub Actions

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
* Docker Desktop
* Git

You will also need API keys for the following services:
* **Nvidia API** (For Llama 3.1 inference)
* **Tavily API** (For AI-optimized search)
* **Serper API** (For Google Search results)

## ⚙️ Installation & Setup

**1. Clone the repository:**

git clone https://github.com/GeoNosX/My-Research-Assistant
cd My-Research-Assistant

**2. Set up your Environment Variables:**
Create a .env file in the root directory and add your API keys:

Απόσπασμα κώδικα
NVIDIA_API_KEY=your_nvidia_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
SERPER_API_KEY=your_serper_api_key_here

**3. Build and run the application using Docker:**

```bash
docker compose up --build

**4. Access the App:**
Open your web browser and navigate to: http://localhost:3000

## 🧪 Testing

This project uses pytest for backend testing and GitHub Actions for continuous integration. The testing suite mocks the LLM responses to ensure the FastAPI routing and LangGraph logic function correctly without consuming API credits.

To run the tests locally (outside of Docker):

```bash
pip install -r requirements.txt
pytest backend/test_main.py

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.


