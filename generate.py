from pathlib import Path
from lxml import html,etree
import json,copy
P=Path(__file__).parent; D=P/'docs'; C=P/'content'
language_names=json.loads((C/'language-names.json').read_text())
names=json.loads((C/'app-names.json').read_text())
ui=json.loads((C/'ui.json').read_text()); terms=json.loads((C/'terms.json').read_text())
keys=['native','brand','eyebrow','hero','intro','fine','artLabel','artText','bottom','nextVerse','manifesto','manifestoSub','experienceLabel','experienceTitle','experienceSub','privacyLabel','privacyTitle','galleryLabel','galleryTitle','gallerySub','scroll','faqLabel','closingLabel','closingTitle','language','close','prev','next','enlarge','home','writing','collections','covers','export','stats','lock','settings','contact','draft','updated','back']
for lang,vals in ui.items():assert len(vals)==len(keys),(lang,len(vals),len(keys))
U={l:dict(zip(keys,v)) for l,v in ui.items()}
files=['Homepage','WritePoem','Collection','CollectionSettings','ExportCollection','Statistics','Lockpage','Settings']
def node(s):return html.fragment_fromstring(s)
def sethtml(el,s):
 for child in list(el):el.remove(child)
 el.text=None
 for part in html.fragments_fromstring(s):
  if isinstance(part,str):el.text=(el.text or '')+part
  else:el.append(part)
def text(el,s):
 for child in list(el):el.remove(child)
 el.text=s

def language_select(lang,kind='landing'):
 u=U[lang];box=etree.Element('div',{'class':'language-control'})
 sel=etree.SubElement(box,'select',{'id':'language-select','aria-label':u['language'],'hidden':'hidden'})
 picker=etree.SubElement(box,'details',{'class':'language-picker'})
 summary=etree.SubElement(picker,'summary',{'aria-label':u['language']+': '+language_names[lang][lang]})
 etree.SubElement(summary,'img',src=f'/assets/flags/{lang}.png',alt='',width='22',height='16')
 code_label=etree.SubElement(summary,'span',{'class':'language-code'});code_label.text='US' if lang=='en' else lang.upper()
 native=etree.SubElement(summary,'span',{'class':'language-name'});native.text=language_names[lang][lang]
 chevron=etree.SubElement(summary,'span',{'class':'language-chevron','aria-hidden':'true'});chevron.text='⌄'
 menu=etree.SubElement(picker,'div',{'class':'language-options','aria-label':u['language']})
 for code in ui:
  url=f'/{code}/' if kind=='landing' else f'/{kind}/{code}.html'
  op=etree.SubElement(sel,'option',value=url)
  if code==lang:op.set('selected','selected')
  op.text=('US' if code=='en' else code.upper())+' · '+language_names[lang][code]
  a=etree.SubElement(menu,'a',href=url,lang=lang,hreflang=code,**{'data-lang':code})
  if code==lang:a.set('aria-current','true')
  etree.SubElement(a,'img',src=f'/assets/flags/{code}.png',alt='',width='22',height='16')
  c=etree.SubElement(a,'span',{'class':'language-code'});c.text='US' if code=='en' else code.upper()
  n=etree.SubElement(a,'span');n.text=language_names[lang][code]
 return box

def footer(lang,t):
 u=U[lang];el=etree.Element('footer');brand=node('<a class="brand"><img src="/assets/appicon.webp" alt="" width="36" height="36">Poesie</a>');brand.set('href',f'/{lang}/');el.append(brand)
 p=etree.SubElement(el,'p');p.text=t['footer.desc']
 links=etree.SubElement(el,'div',{'class':'footer-links'})
 for title,url in [(t['footer.privacy'],f'/privacy/{lang}.html'),(t['footer.terms'],f'/terms/{lang}.html'),('Instagram','https://www.instagram.com/poesie_app/'),(u['contact'],'mailto:support@poesieapp.it')]:
  a=etree.SubElement(links,'a',href=url)
  svg=etree.SubElement(a,'svg',{'viewBox':'0 0 24 24','fill':'none','stroke':'currentColor','stroke-width':'1.6','stroke-linecap':'round','stroke-linejoin':'round','aria-hidden':'true','focusable':'false'})
  if '/privacy/' in url:
   etree.SubElement(svg,'path',d='M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6l-8-3Z');etree.SubElement(svg,'path',d='m8.5 12 2.5 2.5 4.5-5')
  elif '/terms/' in url:
   etree.SubElement(svg,'path',d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6Z');etree.SubElement(svg,'path',d='M14 2v6h6M8 13h8M8 17h6')
  elif 'instagram' in url:
   etree.SubElement(svg,'rect',x='3',y='3',width='18',height='18',rx='5');etree.SubElement(svg,'circle',cx='12',cy='12',r='4');etree.SubElement(svg,'circle',cx='17.5',cy='6.5',r='.7',fill='currentColor',stroke='none')
  else:
   etree.SubElement(svg,'rect',x='3',y='5',width='18',height='14',rx='2');etree.SubElement(svg,'path',d='m3 6 9 7 9-7')
  label=etree.SubElement(a,'span');label.text=title
  if url.startswith('https:'):a.set('target','_blank');a.set('rel','noopener noreferrer')
 s=etree.SubElement(el,'span');s.text=t['footer.rights'];return el

def common(root,lang,t,kind='landing'):
 root.set('lang',lang);root.set('dir','rtl' if lang=='ar' else 'ltr');u=U[lang]
 head=root.find('head');
 head.append(etree.Comment(' DO NOT REMOVE THIS TAGS'))
 for token in ['Uz_2xZmj4eRsIGz32dD3gQFCJSBnB3cIXKuSc_0gP8I','1PDc-eL9C9IMY2hQkHI3f17UTA2OM1Es9PY1jmA8l8w']:
  etree.SubElement(head,'meta',name='google-site-verification',content=token)
 head.append(etree.Comment(' DO NOT REMOVE THIS TAGS'))
 for alt in head.xpath('link[@rel="alternate"]'):head.remove(alt)
 for code in ui:
  href=f'/{code}/' if kind=='landing' else f'/{kind}/{code}.html'
  etree.SubElement(head,'link',rel='alternate',hreflang=code,href=href)
 for el in root.xpath('//*[@src or @href]'):
  for attr in ['src','href']:
   val=el.get(attr,'')
   if val=='assets/logo.png':val='assets/appicon.webp'
   if val.startswith('assets/') or val in ['style.css','app.js']:el.set(attr,'/'+val)
 for a in root.xpath('//a[contains(@href,"play.google.com")]'):a.set('href','https://play.google.com/store/apps/details?id=com.edobardo.poesie&hl='+lang)
 header=root.find('.//header');header.append(language_select(lang,kind))
 for a in header.xpath('.//a[starts-with(@href,"#")]'):
  if kind!='landing':a.set('href',f'/{lang}/'+a.get('href'))
 old=root.find('.//footer');old.getparent().replace(old,footer(lang,t))
 b=root.find('body');b.set('data-language',lang)
 scr=etree.SubElement(b,'script',src='/language.js');scr.set('defer','defer')

for lang in ui:
 u=U[lang];t=json.loads((C/'original-locales'/f'{lang}.json').read_text(encoding='utf-8-sig'))
 root=html.document_fromstring((C/'landing-template.html').read_text())
 def at(xpath):return root.xpath(xpath)[0]
 def put(xpath,value):sethtml(at(xpath),value)
 full_name='Poesie – '+names[lang]
 put('//title',full_name);at('//meta[@name="description"]').set('content',full_name+'. '+u['intro'])
 etree.SubElement(root.find('head'),'meta',property='og:title',content=full_name)
 etree.SubElement(root.find('head'),'meta',property='og:description',content=full_name+'. '+u['intro'])
 put('//header//a[@class="brand"]/span',names[lang])
 store_label=etree.Element('p',{'class':'app-store-name'});store_label.text=full_name
 at('//div[@class="hero-actions"]').addprevious(store_label)
 for a,key in zip(root.xpath('//header/nav/a'),['nav.features','nav.app','nav.faq']):text(a,t[key])
 at('//header/nav').set('aria-label',t['nav.app']);put('//header/a[contains(@class,"button")]',t['btn.download'])
 put('//div[@class="hero-copy"]/p[@class="eyebrow"]',u['eyebrow']);put('//h1',u['hero']);put('//p[@class="intro"]',u['intro'])
 put('//div[@class="hero-actions"]/a[1]',t['hero.btn_download']);put('//div[@class="hero-actions"]/a[2]',t['hero.btn_discover']);put('//p[@class="fine"]',u['fine'])
 put('//div[@class="art-note"]/span',u['artLabel']);put('//div[@class="art-note"]/p',u['artText'])
 put('//div[@class="hero-bottom"]/span[1]',u['bottom']);put('//div[@class="hero-bottom"]/span[2]',u['nextVerse'])
 put('//div[contains(@class,"manifesto")]/p',u['manifesto']);put('//div[contains(@class,"manifesto")]/span',u['manifestoSub'])
 put('//div[contains(@class,"section-head")]/p[1]',u['experienceLabel']);put('//div[contains(@class,"section-head")]/h2',u['experienceTitle']);put('//div[contains(@class,"section-head")]/p[2]',u['experienceSub'])
 for f,prefix in zip(root.xpath('//button[contains(@class,"feature")]'),['feat1','feat2','export','stats']):text(f.find('.//h3'),t[prefix+'.heading']);text(f.find('.//p'),t[prefix+'.text'])
 at('//div[@class="feature-list"]').set('aria-label',t['nav.features'])
 put('//section[contains(@class,"privacy")]/div[1]/p[1]',u['privacyLabel']);put('//section[contains(@class,"privacy")]/div[1]/h2',t['sec.heading']);put('//section[contains(@class,"privacy")]/div[1]/p[2]',t['sec.text'])
 for el,key in zip(root.xpath('//div[@class="privacy-tags"]/span'),['sec.card1_title','sec.card2_title','sec.card3_title']):text(el,t[key])
 put('//div[@class="privacy-detail"]/h3',u['privacyTitle']);put('//div[@class="privacy-detail"]/p',t['sec.card2_desc'])
 put('//div[contains(@class,"gallery-heading")]/div/p',u['galleryLabel']);put('//div[contains(@class,"gallery-heading")]/div/h2',u['galleryTitle']);put('//div[contains(@class,"gallery-heading")]/p',u['gallerySub'])
 at('//div[@class="gallery"]').set('aria-label',u['gallerySub']);put('//div[@class="gallery-foot"]/span',u['scroll'])
 for id,key in [('prev','prev'),('next','next')]:text(at(f'//*[@id="{id}"]'),u[key]);at(f'//*[@id="{id}"]').set('aria-label',u[key])
 # Reuse established translations for the three supporting feature notes.
 for el,vals in zip(root.xpath('//section[contains(@class,"details")]/div'),[(t['nav.features'],t['feat1.item2'],t['feat1.text']),(t['nav.export'],t['export.item4'],t['export.text']),(t['nav.stats'],t['stats.item4'],t['stats.text'])]):
  for child,value in zip([el.find('span'),el.find('h3'),el.find('p')],vals):text(child,value)
 put('//section[@id="domande"]/div[1]/p',u['faqLabel']);put('//section[@id="domande"]/div[1]/h2',t['faq.title'])
 for i,det in enumerate(root.xpath('//div[@class="questions"]/details'),1):text(det.find('summary'),t[f'faq.q{i}']);text(det.find('p'),t[f'faq.a{i}'])
 put('//section[contains(@class,"closing")]/div/p',u['closingLabel']);put('//section[contains(@class,"closing")]/div/h2',u['closingTitle']);put('//section[contains(@class,"closing")]/div/a',t['cta.btn'])
 at('//dialog/button').set('aria-label',u['close']);at('//dialog').set('aria-label',u['gallerySub'])
 for img in root.xpath('//img[not(@alt="")]'):img.set('alt',t['nav.app']+' — Poesie')
 at('//*[@id="feature-img"]').set('alt',t['feat1.heading'])
 gallery=[{'file':f,'title':u[k]} for f,k in zip(files,['home','writing','collections','covers','export','stats','lock','settings'])]
 conf=etree.Element('script');conf.text='window.POESIE='+json.dumps({'gallery':gallery,'enlarge':u['enlarge']},ensure_ascii=False).replace('<','\\u003c')+';'
 app=at('//script[@src="app.js"]');app.addprevious(conf)
 common(root,lang,t)
 target=D/lang/'index.html';target.parent.mkdir(exist_ok=True);target.write_bytes(html.tostring(root,encoding='utf-8',doctype='<!doctype html>'))
 if lang=='it':(D/'index.html').write_bytes(html.tostring(root,encoding='utf-8',doctype='<!doctype html>'))
 # Legal pages share the new design, with original privacy body text retained.
 for kind in ['privacy','terms']:
  legal=html.document_fromstring('<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title></title><link rel="icon" href="/assets/appicon.webp"><link rel="stylesheet" href="/style.css"></head><body><main class="legal-page"></main><footer></footer></body></html>')
  header=copy.deepcopy(root.find('.//header'));header.remove(header.find('.//div[@class="language-control"]'));legal.find('body').insert(0,header)
  main=legal.find('.//main');a=etree.SubElement(main,'a',{'class':'legal-back','href':f'/{lang}/'});a.text=u['back']
  title=t['footer.'+kind];legal.find('.//title').text=title+' — '+full_name
  if kind=='privacy':
   source=html.document_fromstring((C/'original-privacy'/f'{lang}.html').read_text(encoding='utf-8-sig'))
   for cls in ['privacy-hero','privacy-article']:
    els=source.xpath(f'//section[contains(concat(" ",normalize-space(@class)," ")," {cls} ")]');assert els,(lang,cls)
    main.append(copy.deepcopy(els[0]))
   # Remove old decorative SVGs, animated presentation, and old inline styles; preserve legal prose and links.
   for x in main.xpath('.//svg | .//script | .//style'):x.getparent().remove(x)
   for x in main.iter():
    for att in ['style','data-i18n','data-split']:
     x.attrib.pop(att,None)
  else:
   h=etree.SubElement(main,'h1');h.text=title
   p=etree.SubElement(main,'p',{'class':'legal-date'});p.text=u['updated']
   p=etree.SubElement(main,'p',{'class':'draft-notice'});p.text=u['draft']
   for heading,body in terms[lang]:
    sec=etree.SubElement(main,'section');h=etree.SubElement(sec,'h2');h.text=heading;p=etree.SubElement(sec,'p');p.text=body
   p=etree.SubElement(main,'p');a=etree.SubElement(p,'a',href=f'/privacy/{lang}.html');a.text=t['footer.privacy']
   p=etree.SubElement(main,'p');a=etree.SubElement(p,'a',href='mailto:support@poesieapp.it');a.text='support@poesieapp.it'
  common(legal,lang,t,kind)
  target=D/kind/f'{lang}.html';target.parent.mkdir(exist_ok=True);target.write_bytes(html.tostring(legal,encoding='utf-8',doctype='<!doctype html>'))
print('Generated 11 landing pages, 11 privacy pages, 11 terms pages and Italian root.')
