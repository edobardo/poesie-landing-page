(()=>{
 const languages=['it','en','de','es','fr','pt','ru','ar','ja','ko','zh'];
 const select=document.getElementById('language-select');
 // Each URL keeps its language for all visitors, including the Italian root.
 // Change language only when the visitor uses the selector or a language link.
 if(select)select.addEventListener('change',()=>{
  const url=new URL(select.value,location.origin);
  const match=url.pathname.match(/^\/(?:privacy\/|terms\/)?([a-z]{2})(?:\/|\.html)$/);
  if(url.pathname==='/'||(match&&languages.includes(match[1]))){
   if(!url.pathname.includes('.html'))url.hash=location.hash;
   location.assign(url.href);
  }
 });
})();
// Flag picker uses ordinary links, so navigation also works without JavaScript.
(()=>{
 const picker=document.querySelector('.language-picker');if(!picker)return;
 picker.querySelectorAll('a[data-lang]').forEach(link=>link.addEventListener('click',()=>{
  if(!link.getAttribute('href').includes('.html')){const url=new URL(link.href);url.hash=location.hash;link.href=url.href}
 }));
 document.addEventListener('click',e=>{if(!picker.contains(e.target))picker.open=false});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&picker.open){picker.open=false;picker.querySelector('summary').focus()}});
})();
