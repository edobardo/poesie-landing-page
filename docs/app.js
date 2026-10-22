(() => {
  const dialog = document.querySelector('#lightbox');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  let opener = null;
  const close = () => {
    dialog.close();
  };
  document.querySelectorAll('a[data-lightbox]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = link;
      const img = dialog.querySelector('img');
      img.src = link.href;
      img.alt = link.dataset.lightbox;
      dialog.querySelector('p').textContent = link.dataset.lightbox;
      dialog.showModal();
    });
  });
  dialog.querySelector('.close').addEventListener('click', close);
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) close();
  });
  dialog.addEventListener('close', () => {
    if (opener) opener.focus({preventScroll: true});
  });
})();
