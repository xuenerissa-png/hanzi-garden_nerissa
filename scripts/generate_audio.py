import asyncio,json,hashlib
from pathlib import Path
import edge_tts
root=Path(__file__).resolve().parent.parent; data=json.loads((root/'dist/data.js').read_text()[11:-1]);items=[x for g in data for x in g]+[{'c':c,'w':'小花朵' if i<3 else '宝宝'}for i,c in enumerate('小花朵宝宝')]
texts=set(x['c']for x in items)
texts.update(x['c'] if x['w']==x['c'] else x['c']+'，'+x['w']+'。'for x in items)
texts.update(['小朋友，你好呀。我们一起种小花吧。','打出来啦！','找对啦！','小花开啦！','五朵小花都开啦。小朋友，看看你的花园。'])
out=root/'dist/audio';out.mkdir(exist_ok=True);mapping={};fail=[];sem=asyncio.Semaphore(5);done=0
async def one(t):
 global done
 name=hashlib.sha256(t.encode()).hexdigest()[:16]+'.mp3';path=out/name
 async with sem:
  for attempt in range(3):
   try:
    if not path.exists() or path.stat().st_size<1000:await asyncio.wait_for(edge_tts.Communicate(t,'zh-CN-XiaoxiaoNeural',rate='-5%').save(str(path)),40)
    mapping[t]='audio/'+name;done+=1
    if done%30==0:print(f'{done}/{len(texts)}',flush=True)
    return
   except Exception as e:
    if attempt==2:fail.append((t,type(e).__name__))
    else:await asyncio.sleep(1)
async def main():
 await asyncio.gather(*(one(t)for t in sorted(texts)))
 (root/'dist/audio-map.js').write_text('const AUDIO_MAP='+json.dumps(mapping,ensure_ascii=False)+';')
 print(json.dumps({'success':len(mapping),'failed':fail},ensure_ascii=False),flush=True)
 if fail:raise SystemExit(1)
asyncio.run(main())
