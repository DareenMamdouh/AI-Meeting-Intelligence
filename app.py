import json
import time
import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Meeting Intelligence", page_icon="📝", layout="wide")

SAMPLE = """Sara: Good morning everyone. Today we need to finalize the launch plan for the mobile app.
Ahmed: The backend is almost ready. I think we can launch on 20 May.
Sara: Agreed, let's go with 20 May as the launch date.
Mona: We should also move the database to the cloud before launch.
Sara: Okay, decision made, we will use the cloud database.
Ahmed: I will finish the backend APIs by Friday.
Mona: I'll migrate the database by next Tuesday.
Sara: I'll prepare the launch presentation by Monday and someone should test the app.
Omar: I can do the testing, I'll finish it before 18 May.
"""

# ---------------- Sidebar ----------------
st.sidebar.header("Backend settings")
backend_url = st.sidebar.text_input("ngrok URL", placeholder="https://xxxx.ngrok-free.app")
api_key = st.sidebar.text_input("API key", value="secret123", type="password")
st.sidebar.caption("Run the Kaggle notebook first, then paste the public URL it prints.")

# ---------------- Main ----------------
st.title("📝 AI Meeting Intelligence")
st.write("Paste a meeting transcript and get a summary, decisions, and tasks with owners and deadlines.")

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

col_a, col_b = st.columns([1, 1])
with col_a:
    if st.button("Load sample transcript"):
        st.session_state.transcript = SAMPLE
with col_b:
    uploaded = st.file_uploader("...or upload a .txt transcript", type=["txt"])
    if uploaded is not None:
        st.session_state.transcript = uploaded.read().decode("utf-8", errors="ignore")

transcript = st.text_area("Meeting transcript", key="transcript", height=280)

if st.button("Analyze meeting", type="primary"):
    if not backend_url:
        st.error("Please add the ngrok URL in the sidebar.")
    elif not transcript.strip():
        st.error("Please enter a transcript.")
    else:
        url = backend_url.rstrip("/") + "/analyze"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "ngrok-skip-browser-warning": "true",
        }
        base = backend_url.rstrip("/")
        try:
            res = requests.post(url, headers=headers, json={"transcript": transcript}, timeout=60)
            if res.status_code != 200:
                st.error(f"Backend error {res.status_code}: {res.text[:300]}")
            else:
                job_id = res.json()["job_id"]
                status_box = st.empty()
                start = time.time()
                while time.time() - start < 1200:  # wait up to 20 minutes
                    r = requests.get(f"{base}/result/{job_id}", headers=headers, timeout=60)
                    if r.status_code != 200:
                        st.error(f"Backend error {r.status_code}: {r.text[:300]}")
                        break
                    job = r.json()
                    if job["status"] == "done":
                        st.session_state.result = job["result"]
                        status_box.empty()
                        break
                    if job["status"] == "error":
                        status_box.empty()
                        st.error("The model failed. Check the Kaggle notebook output.")
                        st.code(job.get("error", "")[-1500:])
                        break
                    status_box.info(f"Status: {job['status']} ... {int(time.time() - start)}s elapsed")
                    time.sleep(3)
                else:
                    st.error("Timed out waiting for the model.")
        except Exception as e:
            st.error(f"Could not reach the backend: {e}")

result = st.session_state.get("result")
if result:
    st.divider()
    st.subheader("Meeting Summary")
    st.info(result.get("summary", ""))

    st.subheader("Decisions")
    decisions = result.get("decisions", [])
    if decisions:
        for d in decisions:
            st.markdown(f"- {d}")
    else:
        st.write("No decisions found.")

    st.subheader("Tasks")
    tasks = result.get("tasks", [])
    if tasks:
        df = pd.DataFrame(tasks)
        df = df.rename(columns={"task": "Task", "owner": "Owner", "deadline": "Deadline"})
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.write("No tasks found.")

    st.download_button(
        "Download result (JSON)",
        data=json.dumps(result, indent=2, ensure_ascii=False),
        file_name="meeting_analysis.json",
        mime="application/json",
    )
