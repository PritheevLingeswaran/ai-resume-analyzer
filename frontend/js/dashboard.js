(function(api, ui){
  const { qs, showToast, showLoading, hideLoading, toggleOtherRole } = ui;
  const RESULT_SCHEMA_VERSION = '6';

  function wireUploader(){
    const input = qs('#resumeFile');
    const preview = qs('#resumePreview');
    const btn = qs('#uploadBtn');
    if(!input || !btn) return;

    btn.addEventListener('click', async (e)=>{
      e.preventDefault();
      const file = input.files && input.files[0];
      if(!file){ showToast('Please choose a PDF or DOCX resume.', 'warning'); return; }
      if(!/\.(pdf|docx)$/i.test(file.name)){ showToast('Only .pdf or .docx allowed.', 'warning'); return; }
      try{
        showLoading('Uploading & extracting…');
        const res = await api.uploadResume(file);
        if(preview){ preview.value = res.extractedText || ''; }
        localStorage.setItem('SRA_LAST_RESUME_TEXT', res.extractedText || '');
        showToast(`Uploaded: ${res.fileName || file.name}`, 'success');
      }catch(err){
        console.error(err); showToast('Upload failed: ' + (err.message||'Unknown error'), 'danger');
      }finally{ hideLoading(); }
    });
  }

  function wireAnalyze(){
    const btn = qs('#analyzeBtn');
    const roleSel = qs('#jobRole');
    const roleOther = qs('#customRole');
    const jdInput = qs('#jobDescription');
    const preview = qs('#resumePreview');
    if(!btn) return;

    toggleOtherRole('#jobRole', '#customRole');

    btn.addEventListener('click', async (e)=>{
      e.preventDefault();
      const resumeText = (preview?.value || '').trim() || localStorage.getItem('SRA_LAST_RESUME_TEXT') || '';
      const jobDescription = (jdInput?.value || '').trim();
      let jobRole = roleSel?.value || '';
      if(jobRole.toLowerCase()==='other') jobRole = (roleOther?.value || '').trim();
      if(!resumeText || !jobDescription){ showToast('Resume text or JD is empty.', 'warning'); return; }

      try{
        showLoading('Analyzing…');
        const result = await api.analyzeResume({ resumeText, jobDescription, jobRole });
        sessionStorage.setItem('SRA_LAST_RESULT', JSON.stringify(result));
        sessionStorage.setItem('SRA_LAST_ROLE', jobRole);
        sessionStorage.setItem('SRA_RESULT_SCHEMA_VERSION', RESULT_SCHEMA_VERSION);
        window.location.href = 'results.html';
      }catch(err){
        console.error(err); showToast('Analysis failed: ' + (err.message||'Unknown error'), 'danger');
      }finally{ hideLoading(); }
    });
  }

  async function loadRecentReports(){
    const container = qs('#recentReports');
    if(!container) return;
    try{
      const reports = await api.getReports(6);
      if(!reports.length){
        container.innerHTML = `<div class="text-secondary small">No saved reports yet. Run your first analysis to populate history.</div>`;
        return;
      }
      container.innerHTML = reports.map(report => `
        <a class="sra-recent-item" href="/results.html?id=${report.id}">
          <div>
            <div class="fw-semibold">${report.role || 'Untitled Role'}</div>
            <div class="small text-secondary">${report.summaryHeadline}</div>
          </div>
          <div class="text-end">
            <div class="fw-semibold">${report.ats_score}%</div>
            <div class="small text-secondary">${new Date(report.createdAt).toLocaleDateString()}</div>
          </div>
        </a>
      `).join('');
    }catch(err){
      container.innerHTML = `<div class="text-secondary small">Recent reports are unavailable right now.</div>`;
    }
  }

  document.addEventListener('DOMContentLoaded', ()=>{ wireUploader(); wireAnalyze(); loadRecentReports(); });
})(window.SRA_API, window.SRA_UI);
