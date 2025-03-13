# 🏥 Appointment AI - Voice-Based Doctor Appointment Scheduler

🚀 **Appointment AI** is an AI-powered voice-based appointment scheduling system that integrates **STT (Whisper), TTS (Google TTS), RAG Retrieval (ChromaDB), and LLM (Gemini API)** to help patients book appointments efficiently.

---

## 📌 Features
- 😧 **Speech-to-Text (STT)**: Converts user queries from speech to text using **OpenAI Whisper**.
- 🤖 **LLM-powered AI Agent**: Understands queries, retrieves doctor schedules, and provides responses.
- 📚 **RAG-Based Retrieval**: Uses **ChromaDB** to fetch doctor schedules efficiently.
- 🔊 **Text-to-Speech (TTS)**: Reads AI responses aloud using **Google TTS**.
- 🗓 **Appointment Booking & CSV Management**: Updates doctor schedules dynamically.
- 🌐 **Deployed on Streamlit Cloud** for easy access.

---

## 📚 Project Structure
```
appointment_ai/
│── app.py               # Streamlit UI  
│── chat.py              # Handles chat session  
│── vector_db.py         # ChromaDB operations  
│── speech.py            # STT & TTS functions  
│── intent.py            # Intent detection & query processing  
│── history.py           # Chat history management  
│── appointment.py       # Appointment scheduling logic  
│── config.py            # API keys & constants  
│── requirements.txt     # Dependencies for deployment  
│── packages.txt         # Python version for Streamlit  
│── doctor_schedule.csv  # Sample doctor schedule file  
│── logs/                # Stores call logs  
│── README.md            # Project documentation  
```

---

## ⚡ Quick Start (Run Locally in VS Code / Colab)

**1️⃣ Clone the Repository**  
```sh
git clone https://github.com/yourusername/appointment-ai.git
cd appointment-ai
```

**2️⃣ Install Dependencies**  
```sh
pip install -r requirements.txt
```

**3️⃣ Set Up API Keys**  
Create a `.env` file and add:  
```ini
HF_SECRET=your_huggingface_token
GEMINI_API_KEY=your_gemini_api_key
```

**4️⃣ Run the Streamlit App**  
```sh
streamlit run app.py
```

---

## 🌐 Deploy on Streamlit Cloud

**1️⃣ Push to GitHub**  
```sh
git add .
git commit -m "Initial commit"
git push origin main
```

**2️⃣ Add Secrets to Streamlit**  
Go to **Streamlit Cloud** → **Manage App** → **Secrets Management**, and add:  
```
HF_SECRET=your_huggingface_token
GEMINI_API_KEY=your_gemini_api_key
```

**3️⃣ Deploy the App**  
- Go to **Streamlit Cloud** → **Create a new app**.  
- Select your **GitHub repository** and deploy.

---

## 🚀 Future Improvements
- 🔄 **Real-Time Voice Conversations**
- 🗓 **Multi-Doctor Scheduling**
- 🌐 **Multi-Language Support**

---

## 🤝 Contributing
1. **Fork** this repository.  
2. **Create a branch:**  
   ```sh
   git checkout -b feature-xyz
   ```
3. **Commit changes:**  
   ```sh
   git commit -m "Added new feature"
   ```
4. **Push to GitHub:**  
   ```sh
   git push origin feature-xyz
   ```
5. **Submit a pull request**.

---

## 🐟 License
This project is licensed under the **MIT License**.

---

## 💎 Contact
For issues or support, reach out via:
- 📩 Email: `saliimranz.email@example.com`
- 🌐 GitHub Issues: [Open an issue](https://github.com/saliimranz/appointment-ai/issues)

