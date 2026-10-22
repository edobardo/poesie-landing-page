from pathlib import Path
from lxml import html,etree
import json,copy
P=Path(__file__).parent; D=P/'docs'; C=P/'content'
language_names=json.loads((C/'language-names.json').read_text(encoding='utf-8'))
names=json.loads((C/'app-names.json').read_text(encoding='utf-8'))
ui=json.loads((C/'ui.json').read_text(encoding='utf-8')); terms=json.loads((C/'terms.json').read_text(encoding='utf-8'))
keys=['native','brand','eyebrow','hero','intro','fine','artLabel','artText','bottom','nextVerse','manifesto','manifestoSub','experienceLabel','experienceTitle','experienceSub','privacyLabel','privacyTitle','galleryLabel','galleryTitle','gallerySub','scroll','faqLabel','closingLabel','closingTitle','language','close','prev','next','enlarge','home','writing','collections','covers','export','stats','lock','settings','contact','draft','updated','back']
for lang,vals in ui.items():assert len(vals)==len(keys),(lang,len(vals),len(keys))
U={l:dict(zip(keys,v)) for l,v in ui.items()}
SITE='https://poesieapp.it'
landing=json.loads((C/'landing.json').read_text(encoding='utf-8'))
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
 u=U[lang];el=etree.Element('footer')
 brand=node('<a class="brand"><img src="/assets/appicon.webp" alt="" width="36" height="36"><bdi class="footer-app-name"></bdi></a>')
 brand.find('bdi').text='Poesie - '+names[lang]
 brand.set('href',f'/{lang}/');el.append(brand)
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
  href=landing_path(code) if kind=='landing' else f'/{kind}/{code}.html'
  etree.SubElement(head,'link',rel='alternate',hreflang=code,href=SITE+href)
 canonical=SITE+(landing_path(lang) if kind=='landing' else f'/{kind}/{lang}.html')
 etree.SubElement(head,'link',rel='canonical',href=canonical)
 etree.SubElement(head,'link',rel='alternate',hreflang='x-default',href=SITE+('/' if kind=='landing' else f'/{kind}/it.html'))
 etree.SubElement(head,'meta',property='og:url',content=canonical)
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

def landing_path(lang):
    return '/' if lang == 'it' else f'/{lang}/'


def render_copy(root, copy, lang):
    for element in root.xpath('//*[@data-copy]'):
        key = element.attrib.pop('data-copy')
        if 'data-html' in element.attrib:
            element.attrib.pop('data-html')
            sethtml(element, copy[key])
        else:
            text(element, copy[key])
    for element in root.xpath('//*[@data-alt]'):
        element.set('alt', copy[element.attrib.pop('data-alt')])
    for element in root.xpath('//*[@data-list]'):
        for item in copy[element.attrib.pop('data-list')]:
            etree.SubElement(element, 'li').text = item
    for anchor in root.xpath('//*[@data-poster]'):
        poster = anchor.attrib.pop('data-poster')
        title = copy[anchor.attrib.pop('data-title')]
        anchor.set('href', f'/assets/showcase/{poster}-960.webp')
        anchor.set('class', 'poster-link')
        anchor.set('aria-label', U[lang]['enlarge'] + ': ' + title)
        anchor.set('data-lightbox', title)
        image = etree.SubElement(anchor, 'img', src=f'/assets/showcase/{poster}-480.webp', alt=title,
            width='480', height='860', decoding='async')
        image.set('srcset', f'/assets/showcase/{poster}-480.webp 480w, /assets/showcase/{poster}-960.webp 960w')
        image.set('sizes', '(max-width: 700px) 85vw, (max-width: 1100px) 40vw, 380px')
        if poster == 'share':
            image.set('fetchpriority', 'high')
        else:
            image.set('loading', 'lazy')
    for element in root.xpath('//*[@data-faq]'):
        element.attrib.pop('data-faq')
        for question, answer in copy['faq']:
            detail = etree.SubElement(element, 'details')
            etree.SubElement(detail, 'summary').text = question
            etree.SubElement(detail, 'p').text = answer


for lang in ui:
    u = U[lang]
    t = json.loads((C/'original-locales'/f'{lang}.json').read_text(encoding='utf-8-sig'))
    copytext = landing[lang]
    root = html.document_fromstring((C/'landing-template.html').read_text(encoding='utf-8-sig'))
    render_copy(root, copytext, lang)
    full_name = 'Poesie – ' + names[lang]
    hero_text = html.fromstring('<span>'+copytext['hero'].replace('<br>', ' ')+'</span>').text_content()
    root.find('.//title').text = full_name + ' | ' + hero_text
    head = root.find('head')
    description = copytext['intro']
    head.xpath('meta[@name="description"]')[0].set('content', description)
    for property, value in [('og:title', full_name), ('og:description', description),
            ('og:type', 'website'), ('og:site_name', 'Poesie'),
            ('og:image', SITE+'/assets/showcase/feature-1024.png'),
            ('og:image:width', '1024'), ('og:image:height', '500'),
            ('og:image:alt', copytext['featureAlt'])]:
        etree.SubElement(head, 'meta', property=property, content=value)
    for name, value in [('twitter:card', 'summary_large_image'), ('twitter:title', full_name),
            ('twitter:description', description), ('twitter:image', SITE+'/assets/showcase/feature-1024.png'),
            ('twitter:image:alt', copytext['featureAlt'])]:
        etree.SubElement(head, 'meta', name=name, content=value)
    root.xpath('//header//a[@class="brand"]/span')[0].text = names[lang]
    root.xpath('//header/nav')[0].set('aria-label', t['nav.app'])
    for element in root.xpath('//*[@data-app-name]'):
        element.attrib.pop('data-app-name')
        element.text = names[lang]
    for anchor in root.xpath('//*[@data-store]'):
        anchor.attrib.pop('data-store')
        anchor.set('href', 'https://play.google.com/store/apps/details?id=com.edobardo.poesie&hl='+lang)
        anchor.set('target', '_blank')
        anchor.set('rel', 'noopener noreferrer')
    root.xpath('//dialog/button')[0].set('aria-label', u['close'])
    root.xpath('//dialog')[0].set('aria-label', u['enlarge'])
    common(root, lang, t)
    target = D/lang/'index.html'
    target.parent.mkdir(exist_ok=True)
    content = html.tostring(root, encoding='utf-8', doctype='<!doctype html>', pretty_print=True)
    target.write_bytes(content)
    if lang == 'it':
        (D/'index.html').write_bytes(content)
    for kind in ['privacy', 'terms']:
        legal = html.document_fromstring('<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title></title><link rel="icon" href="/assets/appicon.webp"><link rel="stylesheet" href="/style.css"></head><body><main class="legal-page" id="main"></main><footer></footer></body></html>')
        header = copy.deepcopy(root.find('.//header'))
        header.remove(header.find('.//div[@class="language-control"]'))
        legal.find('body').insert(0, header)
        main = legal.find('.//main')
        a = etree.SubElement(main, 'a', {'class': 'legal-back', 'href': f'/{lang}/'})
        a.text = u['back']
        title = t['footer.'+kind]
        legal.find('.//title').text = title+' — '+full_name
        if kind == 'privacy':
            source = html.document_fromstring((C/'original-privacy'/f'{lang}.html').read_text(encoding='utf-8-sig'))
            for cls in ['privacy-hero', 'privacy-article']:
                elements = source.xpath(f'//section[contains(concat(" ",normalize-space(@class)," ")," {cls} ")]')
                assert elements, (lang, cls)
                main.append(copy.deepcopy(elements[0]))
            for element in main.xpath('.//svg | .//script | .//style'):
                element.getparent().remove(element)
            for element in main.iter():
                for attribute in ['style', 'data-i18n', 'data-split']:
                    element.attrib.pop(attribute, None)
        else:
            etree.SubElement(main, 'h1').text = title
            etree.SubElement(main, 'p', {'class': 'legal-date'}).text = u['updated']
            # Published terms omit the old source draft label in every language.
            for heading, body in terms[lang]:
                section = etree.SubElement(main, 'section')
                etree.SubElement(section, 'h2').text = heading
                etree.SubElement(section, 'p').text = body
            p = etree.SubElement(main, 'p')
            etree.SubElement(p, 'a', href=f'/privacy/{lang}.html').text = t['footer.privacy']
            p = etree.SubElement(main, 'p')
            etree.SubElement(p, 'a', href='mailto:support@poesieapp.it').text = 'support@poesieapp.it'
        common(legal, lang, t, kind)
        target = D/kind/f'{lang}.html'
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(html.tostring(legal, encoding='utf-8', doctype='<!doctype html>', pretty_print=True))
print('Generated 11 landing pages, 11 privacy pages, 11 terms pages and Italian root.')
