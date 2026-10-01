# Arline’s Reading Room

This repository contains the public PWA and laptop narration service. Scott authorized publishing the full recovered draft collection on October 1, 2026. It is a working collection with alternate scenes and author notes, not an approved final novel.

## Author change requests

- Author requests can be submitted as GitHub issues in `wpbarline/The-AI-Stands-Accused`, or supplied as exported `arline-change-notes` JSON. Laptop notes also have a local backup at `results/author-notes.json`.
- A note is a request, not an automatic manuscript edit. Apply only the specific changes requested by Arline or Scott; discuss ambiguous requests before altering established story facts.
- Locate the named passage, compare its SHA-256 with the request, and verify the quote and nearby context. If versions differ or a quote is ambiguous, resolve the location before changing wording. Never apply a broad replacement across competing drafts.
- Preserve original canonical archive files in the separate `The-AI-Stands-Accused` project unless separately authorized. The copies in `content/` are the website’s working drafts. Commit a checkpoint before substantive story edits and commit the requested changes afterward.
- Retain alternative drafts unless the author explicitly requests removing them. Do not silently assemble the collection into an approved manuscript.
- Rebuild with `build_phone_site.py` after changing content, code, or saved recordings. `docs/` is the deployed output. Commit and push the rebuilt output; GitHub Pages publishes `main:/docs`.
- Check deployment and the live page before claiming an update is published. Notes marked Applied should link to the change commit or be explained to the author; do not promise automatic monitoring of requests.

## Runtime and publication

- Never commit tokens, runtime environments, model weights, private notes, or local logs. `.gitignore` excludes these folders. Use GitHub CLI’s credential store.
- The phone app is static. It plays pre-generated audio; it cannot run the laptop’s TTS/model APIs. Preserve the distinction in UI and documentation.
- Notes persist on each device and do not automatically sync. GitHub submission, file export/share, and restore provide explicit transfer. Never place a GitHub access token in browser code or ask Arline to paste one into the app.
- Keep asset, manifest, service-worker, and audio URLs relative so project Pages paths work. Retain cached audio across app releases and preserve browser note storage.
