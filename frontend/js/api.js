// Fetch helpers for backend APIs
(function(scope){
  const BASE = () => window.SRA_CONFIG.BASE_URL.replace(/\/$/, '');
  const USE_MOCKS = () => !!window.SRA_CONFIG.USE_MOCKS;

  async function http(path, opts = {}){
    const url = `${BASE()}${path.startsWith('/') ? path : '/'+path}`;
    const res = await fetch(url, opts);
    let body;
    const ctype = res.headers.get('content-type') || '';
    if(ctype.includes('application/json')) body = await res.json();
    else body = await res.text();
    if(!res.ok){
      const msg = (body && body.error) ? body.error : (typeof body === 'string' ? body : res.statusText);
      const err = new Error(msg || `HTTP ${res.status}`);
      err.status = res.status; err.body = body;
      throw err;
    }
    return body;
  }

  async function uploadResume(file){
    const form = new FormData();
    form.append('file', file);
    try{
      return await http('/api/upload', { method: 'POST', body: form });
    }catch(err){
      if(USE_MOCKS()){
        console.warn('[SRA] Mocking /api/upload', err);
        return { fileName: file?.name || 'mock.pdf', extractedText: 'Mock extracted resume text...', resumeId: 1 };
      }
      throw err;
    }
  }

  async function analyzeResume({ resumeText, jobDescription, jobRole }){
    try{
      return await http('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resumeText, jobDescription, jobRole })
      });
    }catch(err){
      if(USE_MOCKS()){
        const resp = await fetch('/mocks/analyze.json'); return await resp.json();
      }
      throw err;
    }
  }

  async function getResult(id){
    try{
      return await http(`/api/result/${id}`);
    }catch(err){
      if(USE_MOCKS()){
        const resp = await fetch('/mocks/result.json'); return await resp.json();
      }
      throw err;
    }
  }

  async function getReports(limit=8){
    try{
      return await http(`/api/reports?limit=${encodeURIComponent(limit)}`);
    }catch(err){
      if(USE_MOCKS()){
        return [{
          id: 102,
          role: 'Backend Developer',
          ats_score: 75,
          summaryHeadline: 'Partial Alignment',
          createdAt: '2026-04-02T13:35:00',
          shareUrl: 'https://resumeai-abe3m.web.app/results.html?id=102'
        }];
      }
      throw err;
    }
  }

  async function getRewriteSuggestions(id){
    try{
      return await http(`/api/result/${id}/rewrite`);
    }catch(err){
      if(USE_MOCKS()){
        return {
          role: 'Backend Developer',
          summaryRewrite: 'Backend-focused Python developer with hands-on FastAPI experience building reliable APIs and improving delivery quality through clean service design and practical cloud exposure.',
          headlineOptions: [
            'Python Backend Developer | FastAPI | AWS',
            'Backend Engineer | Python APIs | Cloud-Ready Systems',
            'FastAPI Developer | Python | Scalable Backend Projects'
          ],
          suggestions: [
            {
              title: 'Project Bullet Upgrade',
              before: 'Built backend APIs using Python.',
              after: 'Built Python and FastAPI APIs for core application workflows, improving response consistency and accelerating feature delivery.',
              rationale: 'Adds stack specificity and stronger ownership language.'
            },
            {
              title: 'Infrastructure Signal',
              before: 'Worked on deployment tasks.',
              after: 'Supported deployment workflows and improved backend release readiness through environment setup, testing, and cloud-focused configuration work.',
              rationale: 'Makes production support sound more concrete without overstating scope.'
            }
          ]
        };
      }
      throw err;
    }
  }

  scope.SRA_API = { uploadResume, analyzeResume, getResult, getReports, getRewriteSuggestions };
})(window);
