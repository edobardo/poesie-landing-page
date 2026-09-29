from pathlib import Path
from lxml import html
from urllib.parse import urlsplit,unquote
import json
P=Path(__file__).parent;D=P/'docs';langs=list(json.loads((P/'content/ui.json').read_text()))
count=0
for file in D.rglob('*.html'):
 r=html.fromstring(file.read_bytes());lang=r.get('lang');assert lang in langs,file
 assert r.get('dir')==('rtl' if lang=='ar' else 'ltr'),file
 opts=r.xpath('//select[@id="language-select"]/option');assert len(opts)==11,file
 selected=[x for x in opts if 'selected' in x.attrib];assert len(selected)==1,file
 for x in r.xpath('//*[@src or @href]'):
  for attr in ['src','href']:
   v=x.get(attr,'');u=urlsplit(v)
   if not v or u.scheme or v.startswith('//'):continue
   target=(D/unquote(u.path).lstrip('/')) if u.path.startswith('/') else file.parent/unquote(u.path)
   if not u.path:target=file
   if target.is_dir():target=target/'index.html'
   assert target.exists(),(file,v,target)
 for opt in opts:
  target=D/opt.get('value').lstrip('/');target=target/'index.html' if target.is_dir() else target
  assert target.exists(),(file,opt.get('value'))
 links=r.xpath('//footer//a/@href');assert f'/privacy/{lang}.html' in links and f'/terms/{lang}.html' in links
 assert 'https://www.instagram.com/poesie_app/' in links and 'mailto:support@poesieapp.it' in links
 if '/privacy/' in str(file):
  old=html.fromstring((P/'content/original-privacy'/file.name).read_bytes())
  newtext=' '.join(r.xpath('//section[contains(@class,"privacy-article")]//text()')).split()
  oldtext=' '.join(old.xpath('//section[contains(@class,"privacy-article")]//text()')).split()
  assert oldtext==newtext,('Privacy text changed',lang)
 if '/terms/' in str(file):assert len(r.xpath('//main/section'))==7
 count+=1
print(f'PASS: {count} pages; all 11 languages, language selectors, local links, assets, privacy text preservation and separate terms verified.')
