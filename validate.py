"""Validate deployable pages, translations, image variants and legal text."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from urllib.robotparser import RobotFileParser
import json
import re
from lxml import html, etree

P = Path(__file__).resolve().parent
D = P / 'docs'
SITE = 'https://poesieapp.it'
robots = RobotFileParser()
robots.parse((D/'robots.txt').read_text(encoding='utf-8').splitlines())
langs = list(json.loads((P/'content/ui.json').read_text(encoding='utf-8')))
copy = json.loads((P/'content/landing.json').read_text(encoding='utf-8'))
assert set(copy) == set(langs), 'Missing landing translations'
for lang in langs:
    assert set(copy[lang]) == set(copy['it']), ('Incomplete translation', lang)
    serialized = json.dumps(copy[lang], ensure_ascii=False)
    assert '??' not in serialized and '\ufffd' not in serialized, ('Damaged text encoding', lang)
    assert len(copy[lang]['faq']) == 6, lang
    assert len(copy[lang]['freeFeatures']) == 4 and len(copy[lang]['paidFeatures']) == 5, lang
    scripts = {'ru': r'[\u0400-\u04ff]', 'ar': r'[\u0600-\u06ff]',
               'ja': r'[\u3040-\u30ff]', 'ko': r'[\uac00-\ud7af]', 'zh': r'[\u4e00-\u9fff]'}
    if lang in scripts:
        for key in ('hero', 'intro', 'writeTitle', 'createTitle', 'bookTitle', 'spaceTitle'):
            assert re.search(scripts[lang], copy[lang][key]), ('Expected language script missing', lang, key)


def local_target(file, value):
    url = urlsplit(value)
    if url.scheme or value.startswith('//'):
        if not value.startswith(SITE + '/'):
            return None
    path = unquote(url.path)
    target = D/path.lstrip('/') if path.startswith('/') else file.parent/path
    if not path:
        target = file
    if target.is_dir():
        target = target/'index.html'
    assert target.exists(), (file.relative_to(D), value, target)
    if url.fragment and target.suffix == '.html':
        parsed = html.fromstring(target.read_bytes())
        assert parsed.xpath('//*[@id=$id]', id=unquote(url.fragment)), (file, value, 'missing anchor')
    return target


def page_path(lang, kind='landing'):
    return (('/' if lang == 'it' else f'/{lang}/') if kind == 'landing'
            else f'/{kind}/{lang}.html')


def expected_alternates(kind):
    return {**{lang: SITE + page_path(lang, kind) for lang in langs},
            'x-default': SITE + page_path('it', kind)}


count = 0
canonical_urls = set()
for file in D.rglob('*.html'):
    r = html.fromstring(file.read_bytes())
    lang = r.get('lang')
    assert lang in langs, file
    assert r.get('dir') == ('rtl' if lang == 'ar' else 'ltr'), file
    kind = file.parent.name if file.parent.name in ('privacy', 'terms') else 'landing'
    expected = page_path(lang, kind)
    assert robots.can_fetch('Googlebot', SITE + expected), ('Googlebot blocked by robots.txt', file)
    for meta in r.xpath('//meta[@name]'):
        if meta.get('name', '').lower() in ('robots', 'googlebot'):
            directives = set(re.split(r'[\s,]+', meta.get('content', '').lower()))
            assert not directives.intersection({'noindex', 'none'}), ('Indexing blocked by meta tag', file)
    assert not r.xpath('//*[@data-copy or @data-alt or @data-poster or @data-list or @data-faq or @data-store]'), ('Unresolved template', file)
    opts = r.xpath('//select[@id="language-select"]/option')
    assert len(opts) == 11, file
    selected = [x for x in opts if 'selected' in x.attrib]
    assert len(selected) == 1, file
    assert selected[0].get('value') == expected, file
    assert [x.get('value') for x in opts] == [page_path(code, kind) for code in langs], file
    for anchor in r.xpath('//a[@href]'):
        assert urlsplit(anchor.get('href')).path not in ('/it/', '/it/index.html'), ('Noncanonical Italian link', file)
    for element in r.xpath('//*[@src or @href or @srcset]'):
        for attr in ['src', 'href']:
            value = element.get(attr, '')
            if value:
                local_target(file, value)
        for candidate in element.get('srcset', '').split(','):
            if candidate.strip():
                local_target(file, candidate.strip().split()[0])
    for opt in opts:
        local_target(file, opt.get('value'))
    canonicals = r.xpath('//link[@rel="canonical"]/@href')
    assert len(canonicals) == 1, ('Canonical missing or repeated', file)
    assert canonicals[0] == SITE + expected, (file, canonicals)
    canonical_urls.add(canonicals[0])
    alternates = r.xpath('//link[@rel="alternate"]')
    assert {x.get('hreflang') for x in alternates} == set(langs) | {'x-default'}, file
    assert len(alternates) == 12, file
    assert {x.get('hreflang'): x.get('href') for x in alternates} == expected_alternates(kind), ('Incorrect language alternates', file)
    for alt in alternates:
        assert alt.get('href').startswith(SITE + '/'), file
        local_target(file, alt.get('href'))
    links = r.xpath('//footer//a/@href')
    assert f'/privacy/{lang}.html' in links and f'/terms/{lang}.html' in links, file
    assert 'https://www.instagram.com/poesie_app/' in links and 'mailto:support@poesieapp.it' in links, file
    if kind == 'privacy':
        old = html.fromstring((P/'content/original-privacy'/file.name).read_bytes())
        newtext = ' '.join(r.xpath('//section[contains(@class,"privacy-article")]//text()')).split()
        oldtext = ' '.join(old.xpath('//section[contains(@class,"privacy-article")]//text()')).split()
        assert oldtext == newtext, ('Privacy differs from current source', lang)
        assert r.xpath('//div[contains(@class,"privacy-badge")]/text()') == old.xpath('//div[contains(@class,"privacy-badge")]/text()'), ('Privacy date differs from source', lang)
    elif kind == 'terms':
        assert not r.xpath('//p[@class="draft-notice"]'), file
        original = json.loads((P/'content/terms.json').read_text(encoding='utf-8'))[lang]
        sections = r.xpath('//main/section')
        assert len(sections) == 7, file
        for section, (heading, body) in zip(sections, original):
            assert section.find('h2').text == heading and section.find('p').text == body, ('Terms text changed', lang)
    else:
        assert len(r.xpath('//h1')) == 1, file
        posters = r.xpath('//a[@data-lightbox]')
        assert len(posters) == 6, ('Static showcase missing', file)
        for anchor in posters:
            image = anchor.find('img')
            assert image is not None and image.get('alt'), file
            assert image.get('width') and image.get('height') and image.get('srcset'), file
        assert len(r.xpath('//img[@fetchpriority="high"]')) == 1, file
        assert len(r.xpath('//div[@class="questions"]/details')) == 6, file
        assert r.xpath('//meta[@property="og:image"]/@content') == [SITE+'/assets/showcase/feature-1024.png'], file
        assert r.xpath('//meta[@name="twitter:card"]/@content') == ['summary_large_image'], file
        assert r.xpath('//meta[@name="google-site-verification"]'), file
    # Retain coverage if a future template introduces dynamic gallery data again.
    for script in r.xpath('//script[not(@src)]'):
        source = script.text or ''
        if source.strip().startswith('window.POESIE='):
            conf = json.loads(source.strip().removeprefix('window.POESIE=').rstrip(';'))
            for item in conf.get('gallery', []):
                local_target(file, '/assets/' + item['file'] + '.webp')
    for key in r.xpath('//*[@data-image]/@data-image'):
        local_target(file, '/assets/' + key + '.webp')
    count += 1
for match in re.findall(r'url\([\'\"]?([^\)\'\"]+)', (D/'style.css').read_text(encoding='utf-8-sig')):
    local_target(D/'index.html', match)
assert count == 34, count
assert (D/'index.html').read_bytes() == (D/'it/index.html').read_bytes()
assert (D/'robots.txt').exists()
assert f'Sitemap: {SITE}/sitemap.xml' in (D/'robots.txt').read_text(encoding='utf-8')
assert (D/'sitemap.xml').exists()
sitemap_root = etree.fromstring((D/'sitemap.xml').read_bytes())
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'xhtml': 'http://www.w3.org/1999/xhtml'}
sitemap_entries = sitemap_root.xpath('sm:url', namespaces=ns)
locations = [entry.find('sm:loc', ns).text for entry in sitemap_entries]
assert len(locations) == len(set(locations)) == 33
assert set(locations) == canonical_urls, 'Sitemap must contain exactly the canonical URLs'
for entry, location in zip(sitemap_entries, locations):
    path = urlsplit(location).path
    kind = path.split('/')[1] if path.startswith(('/privacy/', '/terms/')) else 'landing'
    alternates = entry.xpath('xhtml:link', namespaces=ns)
    assert len(alternates) == 12, location
    assert all(x.get('rel') == 'alternate' for x in alternates), location
    assert {x.get('hreflang'): x.get('href') for x in alternates} == expected_alternates(kind), ('Incorrect sitemap alternates', location)
print(f'PASS: {count} pages; 11 complete translations, responsive assets, anchors, canonicals, hreflang, static showcase, Premium sections, sitemap.xml, robots.txt and legal content matching current sources.')
