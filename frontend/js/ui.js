// UI helpers: toasts, loader, badges, progress
(function(scope){
  function qs(sel, root=document){ return root.querySelector(sel); }

  function showToast(message, variant='primary', autohide=true){
    const container = qs('#toastContainer') || (()=>{
      const el = document.createElement('div');
      el.id = 'toastContainer';
      el.className = 'toast-container position-fixed top-0 end-0 p-3';
      document.body.appendChild(el);
      return el;
    })();

    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-bg-${variant} border-0`;
    toastEl.setAttribute('role','alert');
    toastEl.setAttribute('aria-live','assertive');
    toastEl.setAttribute('aria-atomic','true');
    toastEl.innerHTML = `<div class="d-flex">
      <div class="toast-body">${message}</div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>`;
    container.appendChild(toastEl);
    const toast = new bootstrap.Toast(toastEl, { delay: 3500, autohide });
    toast.show();
    toastEl.addEventListener('hidden.bs.toast', ()=> toastEl.remove());
  }

  function showLoading(text='Processing…'){
    let el = qs('#loadingOverlay');
    if(!el){
      el = document.createElement('div');
      el.id = 'loadingOverlay';
      el.innerHTML = `<div class="sra-overlay-backdrop"></div>
        <div class="sra-overlay-card shadow-lg">
          <div class="spinner-border" role="status" aria-hidden="true"></div>
          <div class="ms-3"><div class="fw-semibold">${text}</div><small class="text-secondary">Please wait</small></div>
        </div>`;
      document.body.appendChild(el);
    }
    el.classList.add('active');
  }
  function hideLoading(){ const el = document.getElementById('loadingOverlay'); if(el) el.classList.remove('active'); }

  function setProgress(id, value){
    const bar = qs(id); if(!bar) return;
    const val = Math.max(0, Math.min(100, Number(value)||0));
    bar.style.width = val + '%'; bar.setAttribute('aria-valuenow', String(val));
    const label = qs('#atsScoreLabel'); if(label) label.textContent = val + '%';
    bar.classList.remove('bg-danger','bg-warning','bg-success');
    bar.classList.add(val >= 80 ? 'bg-success' : val >= 50 ? 'bg-warning' : 'bg-danger');
  }

  function renderBadges(containerSel, items, type='matched'){
    const el = qs(containerSel); if(!el) return; el.innerHTML = '';
    (items || []).forEach(txt => {
      const b = document.createElement('span');
      b.className = 'badge me-2 mb-2 ' + (type==='matched' ? 'text-bg-success' : 'text-bg-danger');
      b.textContent = txt; el.appendChild(b);
    });
  }

  function toggleOtherRole(selectSel, inputSel){
    const sel = qs(selectSel), input = qs(inputSel); if(!sel || !input) return;
    const toggle = ()=>{ if(sel.value.toLowerCase()==='other'){ input.classList.remove('d-none'); input.focus(); } else { input.classList.add('d-none'); } };
    sel.addEventListener('change', toggle); toggle();
  }

  scope.SRA_UI = { qs, showToast, showLoading, hideLoading, setProgress, renderBadges, toggleOtherRole };
})(window);
