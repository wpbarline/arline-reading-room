"""Export the authorized public phone reader; no model/runtime files are published."""
import datetime,hashlib,json,pathlib,shutil
ROOT=pathlib.Path(__file__).resolve().parent
SITE=ROOT/'docs';SITE.mkdir(exist_ok=True)
DATA=SITE/'data';DATA.mkdir(exist_ok=True)
def write_json(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
html=(ROOT/'index.html').read_text(encoding='utf-8')
html=html.replace('href="/manifest.webmanifest"','href="./manifest.webmanifest"').replace('href="/icons/','href="./icons/').replace('href="/annotations.css"','href="./annotations.css"').replace('src="/annotations.js"','src="./annotations.js"')
html=html.replace('<script>','<script src="./phone-platform.js"></script><script>',1)
html=html.replace("navigator.serviceWorker.register('/sw.js')","navigator.serviceWorker.register('./sw.js')")
html=html.replace('Private, on your laptop · Your place is remembered automatically','Arline’s public draft library · Your place is remembered on this device')
html=html.replace('Prepare this passage once. Its recording will be here when you return.','Play saved readings here. New recordings are prepared on Arline’s laptop and added to this library.')
html=html.replace('Your narrators work privately on this laptop, offline.','Saved narration plays on your phone, including offline after it has downloaded.')
html=html.replace("async function poll(){if(polling)return;","async function poll(){if(window.READING_ROOM_STATIC){$('prepare').disabled=$('player').hidden;return;}if(polling)return;")
html=html.replace("Your chosen narrator works privately on this laptop. Longer passages may take time; progress is saved.","There is no saved recording of this passage with this narrator yet. You can leave a note requesting one, or choose another narrator.")
html=html.replace("$('prepare').textContent='Prepare read-aloud'","$('prepare').textContent='Recording not ready'")
html=html.replace('</main></div>', '<p class="install-help">Install on iPhone: open this site in Safari, tap Share, then Add to Home Screen. On Android: use Install app or your browser’s Add to Home screen menu.</p></main></div>')
html=html.replace('</style>','.install-help{color:var(--muted);line-height:1.6;font-size:14px;padding:18px 0}</style>',1)
html=html.replace('accept=".txt,.md,.docx"','accept=".txt,.md"')
(SITE/'index.html').write_text(html,encoding='utf-8')
for file in ['annotations.js','annotations.css','phone-platform.js']:shutil.copyfile(ROOT/file,SITE/file)
shutil.copytree(ROOT/'icons',SITE/'icons',dirs_exist_ok=True)
manifest=json.loads((ROOT/'manifest.webmanifest').read_text(encoding='utf-8'))
manifest.update(id='./',start_url='./',scope='./',description='Arline’s stories, saved readings, and author change requests.')
for icon in manifest['icons']:icon['src']='./'+icon['src'].lstrip('/')
write_json(SITE/'manifest.webmanifest',manifest)
(SITE/'.nojekyll').write_text('')
paths={'story':ROOT.parent/'The-AI-Stands-Accused'/'RECOVERED-STORY.md','guide':ROOT.parent/'The-AI-Stands-Accused'/'STORY-BEATS.md','premise':ROOT.parent/'The-AI-Stands-Accused-review'/'notes'/'2026-09-30-arline-brenda-consciousness-prison-premise.md'}
content=ROOT/'content';content.mkdir(exist_ok=True)
for key,path in list(paths.items()):
    working=content/path.name
    if not working.exists():shutil.copyfile(path,working)
    paths[key]=working
library=[{'id':'story','title':'The AI Stands Accused','subtitle':'Recovered scenes, drafts & author notes'},{'id':'guide','title':'The story at a glance','subtitle':'A short guide to the recovered plot'},{'id':'premise','title':'Brenda: consciousness & prison','subtitle':'Arline’s preserved story notes'}]
write_json(DATA/'library.json',{'books':library})
for key,path in paths.items():write_json(DATA/f'book-{key}.json',{'text':path.read_text(encoding='utf-8'),'name':path.name})
recordings=[];audio_dir=SITE/'audio';audio_dir.mkdir(exist_ok=True)
for file in sorted((ROOT/'results').glob('*/recording.json'),reverse=True):
    wav=file.parent/'read-aloud.wav'
    if not wav.exists():continue
    row=json.loads(file.read_text(encoding='utf-8'));row['audio']='./audio/'+file.parent.name+'.wav'
    recordings.append(row);shutil.copyfile(wav,audio_dir/(file.parent.name+'.wav'))
write_json(DATA/'recordings.json',{'recordings':recordings})
write_json(DATA/'voices.json',{'voices':[{'id':'chatterbox:builtin','label':'Chatterbox Turbo · saved readings'},{'id':'kokoro:af_heart','label':'Kokoro Heart · saved readings'},{'id':'windows:zira','label':'Windows Zira · saved readings'}]})
revision=hashlib.sha256(''.join((SITE/f).read_text(encoding='utf-8') for f in ['index.html','annotations.js','phone-platform.js']).encode()+b''.join((DATA/f).read_bytes() for f in ['book-story.json','recordings.json'])).hexdigest()[:12]
shell=['./','./index.html','./manifest.webmanifest','./annotations.js','./annotations.css','./phone-platform.js','./icons/icon-192.png','./icons/icon-512.png']+['./data/'+p.name for p in sorted(DATA.glob('*.json'))]
sw=(ROOT/'phone-sw.js').read_text(encoding='utf-8').replace('__REVISION__',revision).replace('__SHELL__',json.dumps(shell))
(SITE/'sw.js').write_text(sw,encoding='utf-8')
write_json(DATA/'release.json',{'revision':revision,'built':datetime.datetime.now(datetime.timezone.utc).isoformat(),'publication':'Full recovered drafts publicly shared at Scott’s request; competing drafts are preserved, not adopted as a final manuscript.'})
print(f'Phone site built: {SITE}; {len(recordings)} recordings; revision {revision}')
