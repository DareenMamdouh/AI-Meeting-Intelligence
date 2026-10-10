# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Internship (August–October) 2026

> 🎓 This project was built during the [ **Tips Hindawi** ](https://www.tipshindawi.com/) **Internship (August–October) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        | Dareen                               |
| Project Name     | AI Meeting Intelligence              |
| GitHub Username  | DareenMamdouh                 |
| Internship Batch | August–October 2026                  |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en)                         |

---

# 📖 Project Overview

**AI Meeting Intelligence** analyzes meeting transcripts automatically. The user pastes (or uploads) a transcript in a Streamlit web app, and an open-source LLM (Mistral from Hugging Face) turns it into:

- a short **meeting summary**
- the **decisions** the team agreed on
- a list of **tasks**, each with an **owner** and a **deadline**

The project combines **RAG (Retrieval-Augmented Generation)** with **LangChain Output Parsers**. The model runs on a Kaggle GPU and is exposed through a **FastAPI** server and an **ngrok** tunnel, while the **Streamlit** UI runs on the user's own computer and talks to it over HTTP.

---

# ✨ Features

* Three separate chains: **Summarize Meeting**, **Extract Decisions**, **Extract Tasks**
* RAG: the transcript is split into chunks, embedded, and stored in FAISS so each chain only reads the relevant parts
* Structured output through `StructuredOutputParser` (task / owner / deadline), with a JSON fallback if the model's answer is messy
* Long transcripts are handled with a map-reduce style summary
* Streamlit UI: paste text, upload a `.txt` file, or load a sample transcript
* Results shown as a summary, a decisions list, and a tasks table, with a **JSON download** button
* Background jobs with polling, so long model runs do not break the ngrok connection
* API key protection (`Bearer` token) on the backend

---

# 🛠️ Technologies Used

| Area | Tools |
| ---- | ----- |
| Language | Python 3 |
| LLM | Mistral (`Mistral-Nemo-Instruct-2407`) via Hugging Face Transformers |
| RAG | LangChain, FAISS, `sentence-transformers/all-MiniLM-L6-v2` |
| Output parsing | LangChain `StructuredOutputParser` + `ResponseSchema` |
| Backend | FastAPI, Uvicorn, pyngrok |
| Frontend | Streamlit, Pandas, Requests |
| Platform | Kaggle notebook (GPU T4 x2) |

---

# ⚙️ Installation

### Project files

```
.
├── kaggle_backend.py   
├── app.py              # Streamlit UI (runs on your computer)
├── requirements.txt    # libraries for the UI
└── README.md
```

### 1) Backend (Kaggle)

1. Create a new Kaggle notebook. Set **Accelerator = GPU T4 x2** and **Internet = On**.
2. Copy each `# %% CELL` block of `kaggle_backend.py` into its own notebook cell.
3. Create a free account at [ngrok.com](https://ngrok.com), copy your **Authtoken**, and put it in `NGROK_TOKEN` in cell 6. Change `API_KEY` to your own secret.
4. Run cells 1 to 5 (install, load model, RAG, parsers, chains).



### 2) Frontend (your computer)

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/ai-meeting-intelligence.git
cd ai-meeting-intelligence
pip install -r requirements.txt
```

---

# 🚀 Usage

1. In Kaggle, run **cell 6**. It prints a public URL like `https://xxxx.ngrok-free.app`. Keep the notebook running.
2. On your computer, start the UI:
   ```bash
   streamlit run app.py
   ```
   It opens at `http://localhost:8501`.
3. In the sidebar, paste the **ngrok URL** (without `/analyze`) and your **API key**.
4. Paste a meeting transcript, upload a `.txt` file, or click **Load sample transcript**.
5. Click **Analyze meeting** and wait. The page shows the job status while the model works.
6. Read the **Summary**, **Decisions**, and **Tasks** (with owner and deadline), or download the JSON.

### How it works

```
Streamlit UI  --HTTP via ngrok-->  FastAPI (Kaggle)
                                       |
        transcript -> chunks -> embeddings -> FAISS  (RAG)
                                       |
   Chain 1: Summary   -> Output Parser -> summary
   Chain 2: Decisions -> Output Parser -> decisions
   Chain 3: Tasks     -> Output Parser -> task, owner, deadline
                                       |
                     structured JSON -> shown in the UI
```

### API endpoints

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| POST | `/analyze` | Send `{"transcript": "..."}`, returns a `job_id` |
| GET | `/result/{job_id}` | Returns `status` (`queued`, `running`, `done`, `error`) and the `result` |
| POST | `/generate` | Raw text generation from a prompt |
| GET | `/health` | Simple health check |

All endpoints except `/health` need the header `Authorization: Bearer <API_KEY>`.

---

# 📸 Demo

Add your screenshots to a `screenshots/` folder and link them here:

```md
![Home page](screenshots/home.png)
![Results](screenshots/results.png)
```

---

# 📈 Results

For a transcript like this:

```
Sara: Let's go with 20 May as the launch date.
Ahmed: I will finish the backend APIs by Friday.
```

the app returns a structured result in this shape:

```json
{
  "summary": "The team agreed on a launch date ...",
  "decisions": ["Launch on 20 May"],
  "tasks": [
    { "task": "Finish the backend APIs", "owner": "Ahmed", "deadline": "Friday" }
  ]
}
```
![alt text](image.png)

![alt text](image-1.png)

The project shows how RAG and output parsers can turn long, unstructured meeting text into clean, usable data (summary, decisions, tasks, owners, deadlines) using only open-source models.

---

# 🔮 Future Improvements

* Support audio input with speech-to-text (for example Whisper) so recordings can be analyzed directly
* Export results to PDF, Word, or a task manager
* Detect speakers and dates automatically, and resolve phrases like "next Tuesday" into real dates
* Add an Arabic transcript option
* Deploy the backend permanently instead of a Kaggle notebook

---

# 📚 About the Internship

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Internship (August–October) 2026**, and it will be showcased on the official [Tips Hindawi](https://www.tipshindawi.com/) website.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the internship encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the internship, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.
