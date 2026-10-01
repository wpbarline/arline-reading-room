# Read, listen, and request changes

Phone site: https://wpbarline.github.io/arline-reading-room/

## Install

- iPhone: open the link in Safari, use Share, then Add to Home Screen.
- Android: open the link in Chrome or Edge, then choose Install app or Add to Home screen.
- This laptop: use the Arline Reading Room desktop shortcut, which opens Edge in an app window. For Edge’s formal installation, open the site in Edge and choose Apps → Install this site as an app.

## Arline’s notes

1. Open a passage. Optionally select the words you want to mark.
2. Tap **Note a change**. Write the request; preferred replacement wording is optional.
3. Tap **Save note**. The note stays with that passage and survives closing the app on that device.
4. Tap **Send request to GitHub**, sign in as needed, and submit the prefilled issue. The request goes to the original book project, preserving the passage identity and source version. Ask Codex to review those requests when ready.

**Save a copy of my notes** exports a JSON backup. **Share my notes** can share that file on a phone. **Restore notes from a file** merges exported notes rather than replacing them. Notes do not automatically sync between devices; GitHub submissions or exported files are how to transfer them. Browser storage can be cleared, so keep backups of important notes. Typed, unfinished notes are also saved as drafts on that device.

The public site includes the full recovered draft collection, with alternate scenes and notes intact. Copyright remains attributed to Hazel Arline Hunter. Anyone with internet access can read the deployed material; the original private book repository has not been made public.

## Updates

Website working text is in `content/`. After requested edits, run `build_phone_site.py`, commit both the source and generated `docs/`, and push to `main`. Pages is configured to serve `/docs`. New narration is generated on the laptop and included by the builder. Existing recordings stay valid only for their exact text hash and narrator; an edited passage needs a new recording.

GitHub stores application source and public website assets. Python environments, model files, local logs, credentials, and private author-note backups remain on the laptop. A fresh laptop installation requires separately setting up the Python and neural narrator runtimes described in README.md.
