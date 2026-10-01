# Arline’s Reading Room

Public phone PWA: **https://wpbarline.github.io/arline-reading-room/**. Application repository: **https://github.com/wpbarline/arline-reading-room**. See [PUBLISHING.md](PUBLISHING.md) for installation, passage notes, GitHub change requests, and website updates. Public working drafts live in `content/`; the original book archive is preserved separately.

Open **Arline Reading Room** on the Windows desktop, or run `Start-Assistant.ps1`.
The reader opens at http://127.0.0.1:8765 and works without an internet connection.

Choose a story on the bookshelf, then a passage in Contents. **A+** makes the writing larger. **Evening mode** changes the page colors. **Open a draft** supports UTF-8 TXT, Markdown, and Word DOCX files.

Choose a **Narrator**, then **Prepare read-aloud**. Kokoro offers four voices; Chatterbox Turbo uses a synthetic Kokoro voice reference. Windows Zira remains available for quick recordings. All synthesis runs locally with network access disabled in the worker. You can close the window while preparation continues, provided the laptop stays awake. When it is ready, press Play. Recordings appear in **Your saved recordings** and remain on disk after restarting Windows. **Save recording** downloads a WAV that can also play in Windows Media Player. The browser remembers your passage, narrator, text size, appearance, listening speed, and audio position in the same browser profile.

Neural narration saves completed sections. After a restart, unfinished jobs resume automatically when the reading service starts. For a failed job, pressing Prepare again reuses its completed sections. Chatterbox temporarily stops the local language model to make more memory available and restarts it afterward if it was running. Keep the laptop plugged in and awake during long recordings.

## App window and offline use

The desktop shortcut opens a dedicated Edge app window and starts the local reading service. The service also starts at Windows sign-in. The app includes a manifest, icons, and a service worker that caches the bookshelf and pages. Previously played recordings can be cached for playback when the service is unavailable, subject to browser storage space. Preparing new audio requires the local service to be running, but no internet connection.

For Edge's formal PWA installation, open http://127.0.0.1:8765/ in Edge and choose **Install app** when offered, or **Settings and more → Apps → Install this site as an app**. Automated completion of Edge's installation dialog was blocked because the computer-use tool could not verify the browser URL. The desktop shortcut is already available independently of that installation.

## Neural narrator files

- Runtime: `runtime\kokoro\Scripts\python.exe` with Kokoro ONNX, ONNX Runtime, SoundFile, and Tokenizers. Both neural narrators use this CPU runtime.
- Kokoro: `C:\models\kokoro\kokoro-v1.0.int8.onnx` and `voices-v1.0.bin`, from the [Kokoro ONNX project](https://github.com/thewh1teagle/kokoro-onnx).
- Turbo: `C:\models\chatterbox-turbo-onnx`, the official [Resemble AI Chatterbox Turbo ONNX](https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX) q4 graphs and tokenizer.
- Reference: `C:\models\kokoro\narrator-reference.wav`, generated locally with Kokoro Heart; it is not a recording of a real person.
- `voices.json` enables only successfully tested narrators. `tts_worker.py` handles sections and WAV assembly; `chatterbox_onnx.py` adapts Resemble's published CPU inference example.

On this laptop, a 30-word demonstration produced 10.08 seconds of Turbo audio in 77.41 seconds (including 23.07 seconds loading), and 10.71 seconds of Kokoro audio in 133.39 seconds (including 5.88 seconds loading). These are short-sample measurements, not chapter benchmarks. Both outputs passed a local Whisper transcription check for sentence coverage; name spelling differed. Voice preference still needs listening. Long readings may take hours; saved audio plays normally afterward.

The book’s original files are preserved. The recovered collection contains alternate scenes and notes; the reader does not assemble them into an approved manuscript or rewrite them.

## Local folders

- `C:\github-projects\The-AI-Stands-Accused`: clean main checkout, including complete reachable history and all four remote branch references as of setup.
- `C:\github-projects\The-AI-Stands-Accused-review`: separate worktree on `edit/story-review`, with the later Brenda notes.
- `C:\github-projects\Solitaire-And-Friends`: GitHub repository is empty; its local Git repository has the correct origin.
- `C:\github-projects\local-writing-assistant\results`: saved WAV recordings, narration text, metadata, and model reports.

The private book repository was imported through the authorized GitHub connector because Windows Git has no GitHub login. All imported blobs, trees, and commits were checked against their original SHA-1 identities and `git fsck --full` passed. No remote files were changed. Future command-line pulls and pushes require signing Windows Git in to GitHub.

## Model and dictation tools

These are separate from the reading experience and are not required for narration.

- Qwen3.5-2B Q4_K_M runs under llama.cpp at `http://127.0.0.1:8080`, using the existing BonsaiService scheduled task. It uses the optimized Haswell Release build, two CPU threads, one request slot, and an 8,192-token context. A short CPU benchmark measured 6.83 generated tokens/s and 21.29 prompt tokens/s; longer tasks and a busy laptop can be slower.
- The local `/api/review` controller processes selected source lines in sections of at most 3,500 characters, with a 6,500-token input ceiling, a 650-token output ceiling, one request at a time, and at most 40 sections. It saves per-section JSON and Markdown reports and caches successful sections for reuse. Exact quote references are checked before findings are retained. Model interpretations and summaries still need human review. Continuity checks compare within each section, not across the whole novel.

The first constrained character-extraction smoke test returned an empty review. The controller now rejects empty responses. Model speed is verified, but dependable chapter analysis is not established; further prompt/model evaluation is needed before relying on this optional feature. The reading room and narration do not use the language model.
- Whisper.cpp v1.9.0 with `base.en` is installed for offline English speech recognition. The JFK sample (11 seconds) transcribed in about 5.9 seconds on this laptop. This does not establish accuracy for Arline’s microphone or voice. `/api/transcribe` accepts mono 16 kHz 16-bit PCM WAV clips up to 15 minutes; microphone recording is not part of this reader interface.

## Restarting or recovering

Closing the browser does not stop the hidden Python reader process. After a reboot, the desktop shortcut starts it again. Completed recordings remain available. If the computer powers off during preparation, that unfinished recording may need to be prepared again.

The reader binds only to localhost. Its page contains no external fonts, scripts, analytics, or cloud speech calls. A portable Python 3.12.10 runtime is included; no Python installation or pip packages are required.

Antigravity’s original model-start script and scheduled-task XML are backed up in `downloads`. The updated script is `C:\bin\start-bonsai-service.ps1`. Antigravity’s conversation/brain files remain at `C:\Users\Arline\.gemini\antigravity`.

References: [Qwen model card](https://huggingface.co/Qwen/Qwen3.5-2B), [Whisper.cpp](https://github.com/ggml-org/whisper.cpp), [Windows speech synthesis](https://learn.microsoft.com/en-us/dotnet/api/system.speech.synthesis.speechsynthesizer).
