(function(api, ui){
  const { qs, showToast, setProgress, renderBadges } = ui;

  function hydrate(result){
    if(!result){ showToast('No analysis found. Run analysis first.', 'warning'); return; }
    setProgress('#atsProgress', result.ats_score ?? result.atsScore ?? 0);
    renderBadges('#matchedList', result.matchedSkills || [], 'matched');
    renderBadges('#missingList', result.missingSkills || [], 'missing');
    const sug = qs('#suggestions'); if(sug) sug.textContent = result.suggestions || '';
    const sum = qs('#summary'); if(sum) sum.textContent = result.summary || '';
  }

  function downloadJSON(){
    const data = sessionStorage.getItem('SRA_LAST_RESULT');
    if(!data) return showToast('Nothing to download.', 'warning');
    const blob = new Blob([data], { type: 'application/json' });
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'sra-analysis.json'; a.click();
    URL.revokeObjectURL(a.href);
  }

  function downloadPDF(){
    const data = JSON.parse(sessionStorage.getItem('SRA_LAST_RESULT') || '{}');
    const w = window.open('', '_blank');
    const css = `<style>body{{font-family:Arial; padding:24px;}} .badge{{display:inline-block;margin:4px 6px 0 0;padding:6px 10px;border-radius:999px;background:#eee}}</style>`;
    w.document.write(`<!doctype html><html><head><meta charset="utf-8"><title>SRA Analysis</title>${css}</head><body>`);
    w.document.write(`<h1>Smart Resume Analyzer — Results</h1>`);
    w.document.write(`<p><strong>ATS Score:</strong> ${(data.ats_score ?? 0)}%</p>`);
    w.document.write(`<h2>Matched Skills</h2><div>${(data.matchedSkills||[]).map(s=>`<span class='badge'>${s}</span>`).join('')}</div>`);
    w.document.write(`<h2>Missing Skills</h2><div>${(data.missingSkills||[]).map(s=>`<span class='badge'>${s}</span>`).join('')}</div>`);
    w.document.write(`<h2>Suggestions</h2><p>${(data.suggestions||'')}</p>`);
    w.document.write(`<h2>Summary</h2><p>${(data.summary||'')}</p>`);
    w.document.write(`</body></html>`); w.document.close(); w.print();
  }

  document.addEventListener('DOMContentLoaded', async ()=>{
    const params = new URLSearchParams(location.search);
    const id = params.get('id');
    try{
      let result = null;
      if(id){ result = await api.getResult(id); }
      else {
        const cached = sessionStorage.getItem('SRA_LAST_RESULT');
        if(cached) result = JSON.parse(cached);
      }
      hydrate(result);
    }catch(err){
      console.error(err); showToast('Failed to load results: ' + (err.message||'Unknown error'), 'danger');
    }
    qs('#btnDownloadJSON')?.addEventListener('click', downloadJSON);
    qs('#btnDownloadPDF')?.addEventListener('click', downloadPDF);
  });
})(window.SRA_API, window.SRA_UI);
