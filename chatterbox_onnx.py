"""Local CPU inference adapted from ResembleAI/chatterbox-turbo-ONNX's example.

Uses the official q4 graphs, a synthetic Kokoro reference voice, and no network.
"""
import pathlib
import numpy as np
import onnxruntime as rt
import soundfile as sf
from tokenizers import Tokenizer

class ChatterboxONNX:
    sr=24000
    def __init__(self,model_dir,reference):
        root=pathlib.Path(model_dir)
        options=rt.SessionOptions(); options.intra_op_num_threads=2; options.inter_op_num_threads=1
        options.execution_mode=rt.ExecutionMode.ORT_SEQUENTIAL
        options.log_severity_level=3
        def session(name): return rt.InferenceSession(str(root/'onnx'/f'{name}_q4.onnx'),sess_options=options,providers=['CPUExecutionProvider'])
        self.encoder=session('speech_encoder')
        self.embeddings=session('embed_tokens')
        self.language=session('language_model')
        self.decoder=session('conditional_decoder')
        self.tokenizer=Tokenizer.from_file(str(root/'tokenizer.json'))
        samples,rate=sf.read(str(reference),dtype='float32')
        if rate!=self.sr or samples.ndim!=1: raise ValueError('Reference must be mono 24 kHz')
        self.condition,self.prompt,self.speaker,self.features=self.encoder.run(None,{'audio_values':samples[np.newaxis,:]})
        # The speech encoder is needed once for the fixed synthetic narrator.
        del self.encoder
        self.cache_inputs=[i for i in self.language.get_inputs() if 'past_key_values' in i.name]

    def create(self,text):
        ids=np.array([self.tokenizer.encode(text).ids],dtype=np.int64)
        if ids.size==0: raise ValueError('No text tokens')
        embeds=self.embeddings.run(None,{'input_ids':ids})[0]
        embeds=np.concatenate((self.condition,embeds),axis=1)
        batch,length,_=embeds.shape
        cache={i.name:np.zeros([batch,16,0,64],dtype=np.float16 if i.type=='tensor(float16)' else np.float32) for i in self.cache_inputs}
        attention=np.ones((batch,length),dtype=np.int64)
        positions=np.arange(length,dtype=np.int64).reshape(1,-1)
        generated=np.array([[6561]],dtype=np.int64)
        stopped=False
        for index in range(1024):
            logits,*present=self.language.run(None,{'inputs_embeds':embeds,'attention_mask':attention,'position_ids':positions,**cache})
            scores=logits[:,-1,:].copy()
            repeated=np.take_along_axis(scores,generated,axis=1)
            repeated=np.where(repeated<0,repeated*1.2,repeated/1.2)
            np.put_along_axis(scores,generated,repeated,axis=1)
            token=np.argmax(scores,axis=-1,keepdims=True).astype(np.int64)
            generated=np.concatenate((generated,token),axis=-1)
            if int(token[0,0])==6562:
                stopped=True; break
            attention=np.concatenate((attention,np.ones((batch,1),dtype=np.int64)),axis=1)
            positions=positions[:,-1:]+1
            cache={i.name:present[j] for j,i in enumerate(self.cache_inputs)}
            embeds=self.embeddings.run(None,{'input_ids':token})[0]
        if not stopped: raise ValueError('Turbo reached its speech-token limit. Use a shorter passage segment.')
        speech=np.concatenate((self.prompt,generated[:,1:-1],np.full((batch,3),4299,dtype=np.int64)),axis=1)
        output=self.decoder.run(None,{'speech_tokens':speech,'speaker_embeddings':self.speaker,'speaker_features':self.features})[0]
        return output.squeeze().astype(np.float32),self.sr
