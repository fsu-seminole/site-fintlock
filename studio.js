(() => {
  'use strict';
  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
  const projects = {
    fintley: { name: 'Fintley', category: 'REAL ESTATE / NATIVE IPHONE', description: 'An address becomes a structured investment report. Fintley brings property value, rent, comparable sales, cash flow, and a Forecast score into one iPhone experience. The Deal Lab helps users explore the assumptions behind a potential investment.', platform: 'Native iPhone · SwiftUI', focus: 'Clarity in complex decisions', href: 'https://fintley.app' },
    plants: { name: 'Plants in Pocket', category: 'PLANT CARE / NATIVE IPHONE', description: 'Identify a plant from a photo, check its health, and understand what to do next. Plants in Pocket brings identification, practical care guidance, and planning into an approachable everyday app.', platform: 'Native iPhone', focus: 'Useful everyday guidance', href: 'https://fintlock.com/work.html#plants-in-pocket' }
  };
  const dialog = document.getElementById('project-dialog');
  let opener = null;
  document.querySelectorAll('[data-project]').forEach(button => button.addEventListener('click', () => {
    const project = projects[button.dataset.project];
    if (!project) return;
    opener = button;
    document.getElementById('dialog-title').textContent = project.name;
    document.getElementById('dialog-category').textContent = project.category;
    document.getElementById('dialog-description').textContent = project.description;
    const facts = document.getElementById('dialog-facts');
    facts.replaceChildren();
    for (const [label, value] of [['Platform', project.platform], ['Designed around', project.focus]]) {
      const item = document.createElement('div');
      const caption = document.createElement('span');
      const text = document.createElement('strong');
      caption.textContent = label; text.textContent = value;
      item.append(caption, text); facts.append(item);
    }
    document.getElementById('dialog-link').href = project.href;
    document.body.classList.add('dialog-open');
    dialog.showModal();
  }));
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => { document.body.classList.remove('dialog-open'); opener?.focus(); });
})();
