window.READING_ROOM_STATIC=true;
window.readingRoomAPI=async function(path,data){
  const load=async file=>{const r=await fetch(new URL(file,document.baseURI));if(!r.ok)throw Error('This page is not available yet. Please reconnect once to download it.');return r.json();};
  if(path==='/api/library')return load('data/library.json');
  if(path.startsWith('/api/book/'))return load('data/book-'+path.slice('/api/book/'.length)+'.json');
  if(path==='/api/recordings')return load('data/recordings.json');
  if(path==='/api/voices')return load('data/voices.json');
  if(path==='/api/status')return {status:'idle'};
  if(path==='/api/extract'){
    if(!/\.(txt|md)$/i.test(data.name))throw Error('On the phone, open a TXT or Markdown draft. Word files can be opened in the laptop reader.');
    const bytes=Uint8Array.from(atob(data.data),c=>c.charCodeAt(0));return {text:new TextDecoder('utf-8',{fatal:true}).decode(bytes),name:data.name};
  }
  if(path==='/api/speak')throw Error('New narration is prepared on the laptop. Leave a note asking for a recording; it can be added here afterward.');
  throw Error('This action needs the laptop reader.');
};
