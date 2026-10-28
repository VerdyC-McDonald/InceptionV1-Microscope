from pathlib import Path
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import json,hashlib
root=Path(__file__).resolve().parents[1];src=root/'dist/source';raw=root/'original-source'
raw.mkdir(exist_ok=True)
for folder in ['fv','sheets','thumbs']:
    if not (raw/folder).exists():(src/folder).rename(raw/folder)
files=[p for folder in ['sheets','thumbs'] for p in (raw/folder).rglob('*') if p.is_file()]
def convert(p):
    original=p.relative_to(raw).as_posix();path=Path(original).with_suffix('.avif').as_posix();out=src/path
    out.parent.mkdir(parents=True,exist_ok=True)
    with Image.open(p) as im:
        im=im.resize((1024,192) if original.startswith('sheets/') else (128,128),Image.Resampling.LANCZOS)
        im.save(out,'AVIF',quality=35 if original.startswith('sheets/') else 45,speed=10,max_threads=1)
        with Image.open(out) as check:assert check.size==im.size;check.load()
    b=out.read_bytes();return original,path,len(b),hashlib.sha256(b).hexdigest()
mapping=json.loads((src/'index.json').read_text())['asset_paths'];verification=json.loads((src/'display-verification.json').read_text())
with ThreadPoolExecutor(max_workers=12) as pool:
    for i,(original,path,size,sha) in enumerate(pool.map(convert,files)):
        mapping[original]=path;verification[path]={'bytes':size,'sha256':sha}
        if i%2000==0:print('CONVERTED',i+1,'/',len(files),flush=True)
idx=json.loads((src/'index.json').read_text());idx['asset_paths']=mapping;idx['display_images']={'format':'AVIF','feature_vis_dimensions':'original','dataset_cell_pixels':64,'thumbnail_pixels':128,'original_files':'original-source/ in source repository'}
(src/'index.json').write_text(json.dumps(idx,separators=(',',':')))
(src/'display-verification.json').write_text(json.dumps(verification,separators=(',',':')))
print('DONE',len(mapping),'images',sum(v['bytes'] for v in verification.values()),'bytes',flush=True)
