// Nav active-state tracking
function setActive(el) {
  document.querySelectorAll('.nav-links button').forEach(b => b.classList.remove('is-active'));
  el.classList.add('is-active');
}

function setActiveByLabel(label) {
  document.querySelectorAll('.nav-links button').forEach(b => {
    b.classList.toggle('is-active', b.textContent.trim() === label);
  });
}

function scrollToMount() {
  document.getElementById('mount').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Project card head: toggles the hidden detail panel. The "live"
// and "GitHub" badges inside the head/detail are real <a> tags with
// their own stopPropagation, so clicking them opens the link instead
// of toggling.
function toggleProject(headEl) {
  const article = headEl.closest('.project');
  const detail = article.querySelector('.project-detail');
  if (detail.hasAttribute('hidden')) {
    detail.removeAttribute('hidden');
  } else {
    detail.setAttribute('hidden', '');
  }
}

// Mark "about" active on first load (it's server-rendered into #mount directly).
document.addEventListener('DOMContentLoaded', () => {
  setActiveByLabel('about');
});
