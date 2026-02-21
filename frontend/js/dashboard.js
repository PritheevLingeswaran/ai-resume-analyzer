(function(api, ui){
  const { qs, showToast, showLoading, hideLoading, toggleOtherRole } = ui;

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
        window.location.href = 'results.html';
      }catch(err){
        console.error(err); showToast('Analysis failed: ' + (err.message||'Unknown error'), 'danger');
      }finally{ hideLoading(); }
    });
  }

  document.addEventListener('DOMContentLoaded', ()=>{ wireUploader(); wireAnalyze(); });
})(window.SRA_API, window.SRA_UI);
