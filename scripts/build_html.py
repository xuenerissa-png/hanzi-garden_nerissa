from pathlib import Path
import base64,json,re
root=Path(__file__).resolve().parent.parent
html=(root/'dist/index.html').read_text(); data=(root/'dist/data.js').read_text();audio_js=(root/'dist/audio-map.js').read_text();mapping=json.loads(audio_js[len('const AUDIO_MAP='):].strip().removesuffix(';'));embedded={}
for text,path in mapping.items():
 audio=root/'dist'/path
 assert audio.stat().st_size>1000,path
 embedded[text]='data:audio/mpeg;base64,'+base64.b64encode(audio.read_bytes()).decode()
html=html.replace('<script src="data.js"></script>','<script>'+data+'</script>').replace('<script src="audio-map.js"></script>','<script>const AUDIO_MAP='+json.dumps(embedded,ensure_ascii=False)+';</script>')
out=root/'hanzi-garden.html';out.write_text(html)
print('本地单文件已更新，内置配音',len(mapping),'段，大小',round(out.stat().st_size/1024/1024,2),'MB')
