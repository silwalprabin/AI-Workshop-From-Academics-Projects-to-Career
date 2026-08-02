# Troubleshooting — Top 30 Errors

A fast reference for the problems students hit most in this workshop. Each entry has **Problem → Reason → Solution**. Skim the headings, find your error, apply the fix.

> Official docs for deeper digging: Python https://docs.python.org/3/ · Ollama API https://github.com/ollama/ollama/blob/main/docs/api.md · Chroma https://docs.trychroma.com/ · Streamlit https://docs.streamlit.io/ · LangGraph https://langchain-ai.github.io/langgraph/ · Docker https://docs.docker.com/ · Git https://git-scm.com/doc

---

## Environment & Python

### 1. `python` is not recognized / command not found
- **Problem:** Terminal can't find Python.
- **Reason:** Python isn't on `PATH`, or you're using the wrong command name.
- **Solution:** On Windows, reinstall from python.org with **"Add python.exe to PATH"** checked and open a new terminal. On macOS/Linux use `python3`. Verify with `python --version` / `python3 --version`.

### 2. `pip` is not recognized
- **Problem:** `pip` command fails even though Python works.
- **Reason:** `pip`'s Scripts dir isn't on PATH.
- **Solution:** Use the module form: `python -m pip install ...` (or `python3 -m pip ...`). This always works when Python is on PATH.

### 3. venv activation blocked on Windows (execution policy)
- **Problem:** `Activate.ps1` errors: *"running scripts is disabled on this system"*.
- **Reason:** PowerShell's execution policy blocks local scripts by default.
- **Solution:** Run once per user:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  ```
  Then re-run `.\.venv\Scripts\Activate.ps1`. Or use `cmd.exe` with `\.venv\Scripts\activate.bat`.

### 4. `ModuleNotFoundError: No module named '...'`
- **Problem:** Import fails at runtime.
- **Reason:** The venv isn't activated, or the package wasn't installed into the active environment.
- **Solution:** Activate the venv, confirm with `which python` / `where python`, then `pip install -r requirements.txt`. Install into the *same* interpreter you run the app with (`python -m pip install <pkg>`).

### 5. SSL / certificate errors during `pip install`
- **Problem:** `SSLError` / `CERTIFICATE_VERIFY_FAILED` when installing.
- **Reason:** Corporate proxy/firewall, outdated certs, or a clock that's wrong.
- **Solution:** Upgrade pip (`python -m pip install --upgrade pip`), fix system date/time, and on macOS run the bundled **"Install Certificates.command"** from the Python folder. If behind a proxy, configure it per your org's docs. Avoid `--trusted-host` on untrusted networks.

### 6. UnicodeDecodeError / encoding error reading a file
- **Problem:** Reading a PDF/text file throws a decode error.
- **Reason:** File isn't UTF-8, or you opened a binary file in text mode.
- **Solution:** Open text with `open(path, encoding="utf-8", errors="replace")`. For PDFs use a PDF library (extract bytes, not `open(...).read()`). On Windows set `PYTHONUTF8=1` if needed.

### 7. Import works in the Python REPL but not in the app
- **Problem:** `python -c "import x"` works, but the app says module not found.
- **Reason:** The app runs under a different interpreter/venv than your shell, or a local file **shadows** the package (e.g. a file named `streamlit.py`).
- **Solution:** Run the app with the venv's interpreter (`python -m streamlit run app.py`). Rename any local file/module that collides with a package name and delete stale `__pycache__`.

---

## Ollama & models

### 8. Ollama connection refused (`localhost:11434`)
- **Problem:** Requests to the Ollama API fail with connection refused.
- **Reason:** The Ollama service isn't running.
- **Solution:** Launch the Ollama app (menu bar/system tray) or run `ollama serve`. Verify with `curl http://localhost:11434/api/tags` or `ollama list`.

### 9. Model not found
- **Problem:** *"model '...' not found"* when calling a model.
- **Reason:** The model isn't pulled, or the name/tag is misspelled.
- **Solution:** `ollama pull <model>` first (e.g. `ollama pull llama3.2:3b`). Match the exact tag from https://ollama.com/library and confirm with `ollama list`.

### 10. Ollama slow on the first call
- **Problem:** First request takes many seconds; later ones are fast.
- **Reason:** The model is being loaded into RAM/VRAM (cold start).
- **Solution:** Expected behavior. Warm the model once at app startup with a tiny prompt. Keep it resident by reusing it; smaller/quantized models load faster.

### 11. Out of memory when running a model
- **Problem:** Model crashes, the machine swaps, or generation stalls.
- **Reason:** The model is too big for available RAM/VRAM.
- **Solution:** Use a smaller or more-quantized model (e.g. a 3B instead of 8B). Close other apps. See the sizing table in `INSTALLATION_GUIDE.md`.

### 12. Wrong embeddings — you used a chat model to embed
- **Problem:** Retrieval returns nonsense, or the embed call errors/returns odd dimensions.
- **Reason:** A chat/generate model was used where an **embedding model** is required.
- **Solution:** Pull and use a dedicated embedding model (e.g. `ollama pull nomic-embed-text`) and call the **embeddings** endpoint, not chat. Never mix embedding models between indexing and querying.

### 13. Context length exceeded
- **Problem:** The model truncates input or errors on long prompts.
- **Reason:** Prompt + retrieved context exceeds the model's context window.
- **Solution:** Retrieve fewer/smaller chunks (lower `top_k`), summarize context, shrink chunk size, or choose a model with a larger context window.

---

## RAG, embeddings & data

### 14. PDF text is empty (scanned document)
- **Problem:** PDF extraction returns an empty string.
- **Reason:** The PDF is a scanned image with no text layer.
- **Solution:** Use a text-based PDF, or run OCR to create a text layer before ingesting. Detect and warn when extracted text is empty instead of indexing nothing.

### 15. `json.loads` fails on model output
- **Problem:** Parsing the model's JSON raises `JSONDecodeError`.
- **Reason:** The model wrapped JSON in prose or markdown fences, or emitted trailing text.
- **Solution:** Prompt for JSON only, request structured/format-constrained output where supported, strip ```` ```json ```` fences, and extract the first `{...}` block. Always wrap `json.loads` in try/except and retry on failure.

### 16. Chroma index is empty (no results)
- **Problem:** Queries return nothing.
- **Reason:** Documents were never added, the collection name differs between write and read, or an in-memory client reset on restart.
- **Solution:** Confirm documents were added (`collection.count()`), reuse the **same** collection name, and use a **persistent** client with a path so data survives restarts.

---

## Streamlit

### 17. `streamlit: command not found` / not recognized
- **Problem:** `streamlit run app.py` fails.
- **Reason:** Streamlit isn't installed in the active venv, or its Scripts dir isn't on PATH.
- **Solution:** Activate the venv, `pip install streamlit`, and run `python -m streamlit run app.py`.

### 18. Streamlit port already in use
- **Problem:** *"Port 8501 is already in use."*
- **Reason:** A previous Streamlit process is still running.
- **Solution:** Use a different port `streamlit run app.py --server.port 8502`, or stop the old process (find and kill the PID on that port).

### 19. App re-runs everything on every click (slow)
- **Problem:** Expensive work (model loads, indexing) repeats on each interaction.
- **Reason:** Streamlit reruns the whole script top-to-bottom on every widget change.
- **Solution:** Cache with `@st.cache_resource` (clients/models) and `@st.cache_data` (data). Store cross-run values in `st.session_state`.

---

## Git & GitHub

### 20. `git clone` fails
- **Problem:** Clone errors with permission denied or "repository not found".
- **Reason:** Wrong URL, private repo without access, or SSH key not set up.
- **Solution:** Use the HTTPS URL for public repos. For private/SSH, add an SSH key or use a Personal Access Token per https://docs.github.com/en/authentication. Double-check the org/repo name.

### 21. `git push` rejected (non-fast-forward)
- **Problem:** Push rejected: *"Updates were rejected because the remote contains work you do not have."*
- **Reason:** The remote branch has commits you don't have locally.
- **Solution:** `git pull --rebase origin <branch>`, resolve any conflicts, then `git push`. Never force-push shared branches without agreement.

### 22. `.env` not loaded
- **Problem:** Env vars come back as `None`.
- **Reason:** `load_dotenv()` wasn't called, the file isn't named `.env`, or it's in the wrong directory.
- **Solution:** `from dotenv import load_dotenv; load_dotenv()` at startup, place `.env` in the project root, and read with `os.getenv("KEY")`. Provide a committed `.env.example` (no secrets).

### 23. Committed `.env` by mistake
- **Problem:** Secrets got pushed to GitHub.
- **Reason:** `.env` wasn't in `.gitignore` before the commit.
- **Solution:** Add `.env` to `.gitignore`, then `git rm --cached .env` and commit. **Rotate any exposed secret immediately** — it may already be public. Removing from history requires a history rewrite (see GitHub's official guide).

---

## LangGraph

### 24. Graph won't compile (`START`/`END` wiring)
- **Problem:** Compile fails or the graph never runs a node.
- **Reason:** Missing entry/finish edges, or nodes not connected to `START`/`END`.
- **Solution:** Add an edge from `START` to your first node and from your last node to `END`. Ensure every node is reachable. See https://langchain-ai.github.io/langgraph/.

### 25. Findings get overwritten (need a reducer)
- **Problem:** Only the last node's output survives; earlier findings vanish.
- **Reason:** State fields overwrite by default; parallel/successive writes clobber each other.
- **Solution:** Annotate the accumulating field with a reducer (e.g. `Annotated[list, operator.add]`) so writes **append** instead of replace.

### 26. Graph runs forever (infinite loop)
- **Problem:** The agent loops without stopping.
- **Reason:** A conditional edge always routes back with no exit condition.
- **Solution:** Add a loop counter in state and a conditional edge to `END` when a max is reached. Set a `recursion_limit` when invoking as a safety net.

---

## Docker

### 27. Docker daemon is not running
- **Problem:** `docker` commands fail: *"Cannot connect to the Docker daemon."*
- **Reason:** Docker Desktop/engine isn't started.
- **Solution:** Start Docker Desktop (wait for the whale icon) or `sudo systemctl start docker` on Linux. Verify with `docker run hello-world`.

### 28. Container can't reach Ollama on the host
- **Problem:** Code in a container gets connection refused to `localhost:11434`.
- **Reason:** Inside a container, `localhost` is the container, not your host machine.
- **Solution:** Point the client at `http://host.docker.internal:11434` (Windows/macOS Docker Desktop). On Linux, run with `--add-host=host.docker.internal:host-gateway` or use the host's IP / host networking.

### 29. `docker build` is slow (bad layer order)
- **Problem:** Every build reinstalls all dependencies.
- **Reason:** Source is copied before dependencies, so any code change busts the dependency cache.
- **Solution:** Copy `requirements.txt` and `pip install` **before** `COPY . .`, and add a `.dockerignore` (exclude `.venv`, `__pycache__`, `.git`, data). Dependency layers then stay cached.

### 30. Port mapping fails / app unreachable
- **Problem:** You can't open the app in the browser, or the port is already allocated.
- **Reason:** Missing/incorrect `-p host:container` mapping, the app binds to `127.0.0.1` inside the container, or the host port is taken.
- **Solution:** Publish the port (`docker run -p 8501:8501 ...`), bind the server to `0.0.0.0` inside the container, and pick a free host port if the chosen one is in use.
