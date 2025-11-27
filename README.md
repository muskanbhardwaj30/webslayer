# ⚔️ WebSlayer

**WebSlayer** is an AI-powered, enterprise-grade Gradio application that crawls any public webpage, transforms its content into structured Markdown, and lets users chat with it as if the website had a built-in human assistant.

Built for developers, researchers, and businesses that need contextual insights from any webpage — fast, accurate, and conversational.

---

## 🔥 Features

- **Real-time Web Ingestion**: Crawl and extract data from any URL using a robust, customizable scraping pipeline.
- **Markdown Conversion & Caching**: Convert raw HTML to readable Markdown with reusable cache to avoid redundant fetches.
- **AI Chatbot with Memory**: Use Google’s Gemini AI to interact with website content naturally, accurately, and informatively.
- **Gradio UI Interface**: Clean, fast, modern chat UI using Gradio’s `Blocks` and `Chatbot` components.
- **Structured Logs**: Industrial-strength logging with timestamps, warning traces, and LLM response tracking.
- **Enterprise Modularity**: Organized codebase following scalable architecture principles.

---

## 🧠 Use Case

Imagine you visit a website, and instead of reading through pages of text, you just _ask_:

> "Does this site offer free trials?"

Or:

> "What services does this company provide?"

**WebSlayer** will fetch the content, understand it, and answer you like a well-trained support agent.

---

## 🌐 Live Demo

> Will be hosted soon on [HuggingFace Spaces](https://huggingface.co/spaces) or \[Gradio Share Link]

---

## 📁 Project Structure

```bash
├── app.py             # Gradio app controller
├── scraper.py         # Crawler and markdown processor
├── llm_client.py      # Gemini-based AI response system
├── utils.py           # Logger, hasher, URL cleaner
├── requirements.txt   # Python dependencies
├── .env               # Environment variables
├── .cache/            # Markdown cache storage
└── logs/              # Structured logging
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/himanshumahajan138/webslayer.git
cd webslayer
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Add Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_genai_key_here
```

### 5. Run the App

```bash
python app.py
```

Visit: `http://localhost:7860`

---

## 🛠️ Tech Stack

| Component | Tech                          |
| --------- | ----------------------------- |
| UI        | Gradio Blocks + Chatbot       |
| Crawler   | Advertools (custom settings)  |
| Parser    | markdownify + mdformat        |
| AI Model  | Google Generative AI (Gemini) |
| Logging   | Python’s logging module       |
| Language  | Python 3.10                   |

---

## 🧪 Dev & Testing Tips

- Use dummy URLs during development to avoid rate-limiting.
- Tail logs in real-time:

  ```bash
  tail -f logs/app.log
  ```

- Mock Gemini API in `llm_client.py` for offline dev.
- Consider using `pytest` for unit and integration tests.

---

## 🔒 Security Notes

- Do **not** commit `.env` or API keys.
- Use domain whitelisting if deploying publicly.
- Validate user inputs strictly to avoid SSRF or DoS.

---

## 📦 Deployment (Docker)

### Dockerfile

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
```

### Run

```bash
docker build -t webslayer .
docker run -p 7860:7860 webslayer
```

---

## 🙌 Contributing

We welcome contributions!

```bash
git checkout -b feature/your-feature
# make changes
git commit -m "✨ Add your feature"
git push origin feature/your-feature
```

Then open a Pull Request!

---

## 🧾 License

This project is licensed under the [MIT License](LICENSE).

---

### ✨ Project Maintainer

**Himanshu Mahajan**
🔗 [GitHub](https://github.com/himanshumahajan138)
✉️ Feel free to connect!

---

**WebSlayer**: Crawl. Convert. Converse.

> When websites speak, you listen.
