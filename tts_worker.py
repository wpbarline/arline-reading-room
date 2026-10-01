"""CPU-only offline narration with resumable PCM segments."""
import argparse, hashlib, json, os, pathlib, re, time, wave
os.environ['HF_HUB_OFFLINE']='1'
os.environ['TRANSFORMERS_OFFLINE']='1'
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
os.environ['OMP_NUM_THREADS']='2'
os.environ['MKL_NUM_THREADS']='2'

def emit(**fields): print(json.dumps(fields),flush=True)
def split_text(text,limit=380):
    pieces=[]; buffer=''
    for sentence in re.split(r'(?<=[.!?])\s+|\n+',text):
        sentence=sentence.strip()
        while sentence:
            if len(buffer)+len(sentence)+1<=limit:
                buffer=(buffer+' '+sentence).strip(); break
            if buffer: pieces.append(buffer); buffer=''
            if len(sentence)<=limit: buffer=sentence; break
            cut=sentence.rfind(' ',0,limit)
            if cut<1: cut=limit
            pieces.append(sentence[:cut]); sentence=sentence[cut:].strip()
    if buffer: pieces.append(buffer)
    return pieces

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--engine',choices=['kokoro','chatterbox'],required=True)
    parser.add_argument('--voice',default='af_heart')
    parser.add_argument('--input',required=True)
    parser.add_argument('--folder',required=True)
    args=parser.parse_args()
    start=time.perf_counter()
    folder=pathlib.Path(args.folder); segment_dir=folder/'segments'; segment_dir.mkdir(parents=True,exist_ok=True)
    text=pathlib.Path(args.input).read_text(encoding='utf-8').strip()
    pieces=split_text(text)
    if not pieces: raise ValueError('No narration text')
    key=hashlib.sha256(json.dumps([args.engine,args.voice,text],ensure_ascii=False).encode()).hexdigest()
    manifest=folder/'segments.json'
    if manifest.exists() and json.loads(manifest.read_text())['sha256']!=key: raise ValueError('Segment source differs from saved job')
    manifest.write_text(json.dumps({'sha256':key,'sections':pieces},ensure_ascii=False,indent=2),encoding='utf-8')
    emit(message=f'Loading {"Kokoro" if args.engine=="kokoro" else "Chatterbox Turbo"} on this laptop',total=len(pieces),completed=0)
    import numpy as np
    import soundfile as sf
    if args.engine=='kokoro':
        import onnxruntime as rt
        from kokoro_onnx import Kokoro
        options=rt.SessionOptions(); options.intra_op_num_threads=2; options.inter_op_num_threads=1
        session=rt.InferenceSession(r'C:\models\kokoro\kokoro-v1.0.int8.onnx',sess_options=options,providers=['CPUExecutionProvider'])
        model=Kokoro.from_session(session,r'C:\models\kokoro\voices-v1.0.bin')
        if args.voice not in model.get_voices(): raise ValueError('Unknown Kokoro voice')
        def synthesize(part):
            return model.create(part,voice=args.voice,speed=0.95,lang='en-gb' if args.voice.startswith('b') else 'en-us')
    else:
        from chatterbox_onnx import ChatterboxONNX
        model=ChatterboxONNX(r'C:\models\chatterbox-turbo-onnx',r'C:\models\kokoro\narrator-reference.wav')
        def synthesize(part):
            return model.create(part)
    loaded=time.perf_counter()
    emit(message='Narrator is ready',load_seconds=round(loaded-start,2),total=len(pieces),completed=0)
    for index,part in enumerate(pieces,1):
        path=segment_dir/f'{index:05}.wav'
        valid=False
        if path.exists():
            try:
                with wave.open(str(path),'rb') as wav: valid=wav.getnframes()>0
            except (EOFError,wave.Error): pass
        if not valid:
            samples,rate=synthesize(part)
            samples=np.asarray(samples,dtype=np.float32).reshape(-1)
            if not len(samples) or not np.isfinite(samples).all(): raise ValueError('Narrator produced invalid audio')
            temporary=segment_dir/f'{index:05}.tmp.wav'
            sf.write(str(temporary),samples,rate,subtype='PCM_16')
            temporary.replace(path)
        emit(message=f'Preparing narration: section {index} of {len(pieces)}',total=len(pieces),completed=index)
    final=folder/'read-aloud.tmp.wav'; duration=0
    with wave.open(str(final),'wb') as output:
        rate=None
        for index in range(1,len(pieces)+1):
            with wave.open(str(segment_dir/f'{index:05}.wav'),'rb') as section:
                if rate is None:
                    rate=section.getframerate(); output.setparams((1,2,rate,0,'NONE','not compressed'))
                if (section.getnchannels(),section.getsampwidth(),section.getframerate())!=(1,2,rate): raise ValueError('Unexpected segment audio format')
                while True:
                    frames=section.readframes(16384)
                    if not frames: break
                    output.writeframesraw(frames)
                duration+=section.getnframes()/rate
                if index<len(pieces): output.writeframesraw(b'\0\0'*int(rate*.18)); duration+=.18
    final.replace(folder/'read-aloud.wav')
    timing={'engine':args.engine,'voice':args.voice,'load_seconds':round(loaded-start,2),'elapsed_seconds':round(time.perf_counter()-start,2),'duration_seconds':round(duration,2),'sections':len(pieces)}
    (folder/'timing.json').write_text(json.dumps(timing,indent=2),encoding='utf-8')
    emit(message='Recording saved',**timing)

if __name__=='__main__': main()
