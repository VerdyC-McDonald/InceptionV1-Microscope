"""Resumable mirror of the source manifest's public, non-hidden resources."""
import asyncio, aiohttp, json, time, hashlib, io
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / 'dist/source'
BASE = 'https://already-clean.goodfire.com/microscope/inceptionv1/'
META = json.loads((ROOT/'meta.json').read_text())
JOBS=[]
for layer in META['layers']:
    name=layer['name']
    for n in json.loads((ROOT/layer['data']).read_text())['neurons']:
        c=n['c']
        JOBS.append(f'conn/{name}/{c}.json')
        for slot,status in zip(META['fvSlots'],n['fv']):
            if status=='1': JOBS.append(f'fv/{slot}/{name}/{c}.png')
        if not n.get('hid'):
            JOBS.extend([f'sheets/{name}/{c}.jpg',f'thumbs/{name}/{c}.jpg',f'heat/{name}/{c}.bin'])

def validate(path,b):
    if path.endswith('.bin'):
        assert len(b)==META['heatmaps']['size']**2*META['heatmaps']['mapsPerNeuron']
    elif path.endswith('.json'):
        d=json.loads(b);assert isinstance(d,dict) and 'prev' in d and 'next' in d
    else:
        with Image.open(io.BytesIO(b)) as im: im.verify()

async def main():
    started=time.time(); q=asyncio.Queue(); results={};failed={};done=0
    for p in JOBS:q.put_nowait(p)
    connector=aiohttp.TCPConnector(limit=160)
    async with aiohttp.ClientSession(connector=connector,timeout=aiohttp.ClientTimeout(total=75),trust_env=True) as session:
        async def worker():
            nonlocal done
            while not q.empty():
                p=await q.get(); dest=ROOT/p
                try:
                    if dest.exists():
                        b=dest.read_bytes();validate(p,b)
                    else:
                        for attempt in range(4):
                            try:
                                async with session.get(BASE+p) as r:
                                    r.raise_for_status();b=await r.read()
                                validate(p,b);break
                            except Exception:
                                if attempt==3:raise
                                await asyncio.sleep(1+attempt*2)
                        dest.parent.mkdir(parents=True,exist_ok=True)
                        tmp=dest.with_suffix(dest.suffix+'.part');tmp.write_bytes(b);tmp.replace(dest)
                    results[p]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
                except Exception as e:failed[p]=str(e)
                done+=1;q.task_done()
        tasks=[asyncio.create_task(worker()) for _ in range(160)]
        while any(not t.done() for t in tasks):
            await asyncio.wait(tasks,timeout=10)
            report={'expected':len(JOBS),'verified':len(results),'failed':len(failed),'processed':done,'seconds':round(time.time()-started)}
            (ROOT/'download-progress.json').write_text(json.dumps(report))
            print(json.dumps(report),flush=True)
        await asyncio.gather(*tasks)
    (ROOT/'asset-verification.json').write_text(json.dumps({'source':BASE,'files':results,'failures':failed},separators=(',',':')))
    index=json.loads((ROOT/'index.json').read_text())
    index.update(assets=[p for p in results if not p.startswith('conn/')],connection_records=sum(p.startswith('conn/') for p in results),expected_assets=len(JOBS),verified_files=len(results),failures=failed)
    (ROOT/'index.json').write_text(json.dumps(index,separators=(',',':')))
    connections={p.split('/')[1]+':'+Path(p).stem:json.loads((ROOT/p).read_text()) for p in results if p.startswith('conn/')}
    (ROOT/'connections.json').write_text(json.dumps(connections,separators=(',',':')))
    print('FINISHED',len(results),'verified;',len(failed),'failures',flush=True)

if __name__=='__main__':asyncio.run(main())
