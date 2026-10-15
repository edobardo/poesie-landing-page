(()=>{
 const languages=['it','en','de','es','fr','pt','ru','ar','ja','ko','zh'];
 const select=document.getElementById('language-select');
 const current=document.documentElement.lang;
 let saved=null;try{saved=localStorage.getItem('preferred_lang')}catch{}
 const isBot=/bot|googlebot|crawler|spider|robot|crawling|lighthouse/i.test(navigator.userAgent);
 if(!isBot&&(location.pathname==='/'||location.pathname==='/index.html')){
  const query=new URLSearchParams(location.search).get('lang');
  const preferred=languages.includes(query)?query:languages.includes(saved)?saved:(navigator.language||'it').slice(0,2);
  if(languages.includes(preferred)&&preferred!==current){location.replace('/'+preferred+'/'+location.hash);return}
 }
 if(select)select.addEventListener('change',()=>{
  const url=new URL(select.value,location.origin);
  const match=url.pathname.match(/^\/(?:privacy\/|terms\/)?([a-z]{2})(?:\/|\.html)$/);
  if(match&&languages.includes(match[1])){
   try{localStorage.setItem('preferred_lang',match[1])}catch{}
   if(!url.pathname.includes('.html'))url.hash=location.hash;
   location.assign(url.href);
  }
 });
})();
// Flag picker uses ordinary links, so navigation also works without JavaScript.
(()=>{
 const picker=document.querySelector('.language-picker');if(!picker)return;
 picker.querySelectorAll('a[data-lang]').forEach(link=>link.addEventListener('click',()=>{
  try{localStorage.setItem('preferred_lang',link.dataset.lang)}catch{}
  if(!link.getAttribute('href').includes('.html')){const url=new URL(link.href);url.hash=location.hash;link.href=url.href}
 }));
 document.addEventListener('click',e=>{if(!picker.contains(e.target))picker.open=false});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&picker.open){picker.open=false;picker.querySelector('summary').focus()}});
})();