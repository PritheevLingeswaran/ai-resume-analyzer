(function(api, ui){
  const { qs, showToast, setProgress } = ui;
  const RESULT_SCHEMA_VERSION = '4';

  function asList(value){
    if(Array.isArray(value)) return value.filter(Boolean);
    return [];
  }

  function splitSuggestions(text){
    if(!text) return [];
    return text
      .split(/(?<=[.!?])\s+/)
      .map(item => item.trim())
      .filter(Boolean);
  }

  function renderList(containerSel, items, emptyText){
    const el = qs(containerSel); if(!el) return;
    const list = asList(items);
    if(!list.length){
      el.innerHTML = `<li class="text-secondary">${emptyText}</li>`;
      return;
    }
    el.innerHTML = list.map(item => `<li>${item}</li>`).join('');
  }

  function renderSkillGroups(containerSel, groups, emptyText, tone='success'){
    const el = qs(containerSel); if(!el) return;
    const list = asList(groups);
    if(!list.length){
      el.innerHTML = `<div class="small text-secondary">${emptyText}</div>`;
      return;
    }
    el.innerHTML = list.map(group => `
      <div class="sra-group-card">
        <div class="sra-group-title">${group.title}</div>
        <div class="mt-2">
          ${(group.items || []).map(item => `<span class="badge me-2 mb-2 ${tone === 'danger' ? 'text-bg-danger' : 'text-bg-success'}">${item}</span>`).join('')}
        </div>
      </div>
    `).join('');
  }

  function renderBreakdown(breakdown){
    const el = qs('#breakdownGrid'); if(!el) return;
    const metrics = [
      ['Keyword Coverage', breakdown?.keywordCoverage],
      ['Section Quality', breakdown?.sectionScore],
      ['Impact Score', breakdown?.impactScore],
      ['Formatting', breakdown?.formattingScore]
    ];
    el.innerHTML = metrics.map(([label, value]) => {
      const score = Math.max(0, Math.min(100, Number(value) || 0));
      return `
        <div class="sra-breakdown-item">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="small fw-semibold">${label}</span>
            <span class="small text-secondary">${score.toFixed(0)}%</span>
          </div>
          <div class="progress sra-mini-progress">
            <div class="progress-bar ${score >= 80 ? 'bg-success' : score >= 50 ? 'bg-warning' : 'bg-danger'}" style="width:${score}%"></div>
          </div>
        </div>
      `;
    }).join('');
  }

  function renderScoreCommentary(entries){
    const el = qs('#scoreCommentary'); if(!el) return;
    const list = asList(entries);
    el.innerHTML = list.map(entry => `
      <div class="sra-commentary-item">
        <div class="d-flex justify-content-between align-items-center">
          <span class="fw-semibold small">${entry.title}</span>
          <span class="small text-secondary">${formatScore(entry.score)} / 100</span>
        </div>
        <p class="small text-secondary mb-0 mt-1">${entry.commentary}</p>
      </div>
    `).join('');
  }

  function formatScore(value){
    return Math.max(0, Math.min(100, Number(value) || 0)).toFixed(0);
  }

  function hydrate(result){
    if(!result){ showToast('No analysis found. Run analysis first.', 'warning'); return; }
    setProgress('#atsProgress', result.ats_score ?? result.atsScore ?? 0);
    renderSkillGroups('#matchedGroups', result.audit?.matchedGroups || [], 'No grouped strengths available yet.', 'success');
    renderSkillGroups('#missingGroups', result.audit?.missingGroups || [], 'No grouped gaps available yet.', 'danger');
    const sum = qs('#summary'); if(sum) sum.textContent = result.summary || '';
    const verdict = qs('#finalVerdict'); if(verdict) verdict.textContent = result.audit?.finalVerdict || '';
    const headline = qs('#summaryHeadline'); if(headline) headline.textContent = result.audit?.summaryHeadline || 'AI + ATS Insights';
    const gapHeadline = qs('#priorityGapHeadline'); if(gapHeadline) gapHeadline.textContent = result.audit?.priorityGapHeadline || '';
    const riskBadge = qs('#riskBadge'); if(riskBadge){
      const risk = result.audit?.atsRiskLevel || 'ATS Risk';
      riskBadge.textContent = risk;
      riskBadge.className = 'badge ' + (risk.includes('Low') ? 'text-bg-success' : risk.includes('Moderate') ? 'text-bg-warning text-dark' : 'text-bg-danger');
    }
    renderList('#quickWinsList', result.audit?.quickWins || [], 'No quick improvements generated yet.');
    renderList('#suggestionsList', result.audit?.suggestionBullets?.length ? result.audit.suggestionBullets : splitSuggestions(result.suggestions || ''), 'No specific suggestions generated yet.');
    renderList('#strengthsList', result.audit?.strengthHighlights?.length ? result.audit.strengthHighlights : result.strengths || [], 'Strength indicators will appear here when available.');
    renderList('#risksList', result.audit?.riskHighlights?.length ? result.audit.riskHighlights : result.risks || [], 'No major risks detected in the current analysis.');
    renderBreakdown(result.breakdown || {});
    renderScoreCommentary(result.audit?.scoreExplanations || []);
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
    const css = `<style>body{{font-family:Arial; padding:24px; color:#111827;}} .badge{{display:inline-block;margin:4px 6px 0 0;padding:6px 10px;border-radius:999px;background:#eee}} ul{{padding-left:20px}} .metric{{margin-bottom:10px}}</style>`;
    w.document.write(`<!doctype html><html><head><meta charset="utf-8"><title>SRA Analysis</title>${css}</head><body>`);
    w.document.write(`<h1>AI Resume Analyzer — Results</h1>`);
    w.document.write(`<p><strong>ATS Score:</strong> ${(data.ats_score ?? 0)}%</p>`);
    w.document.write(`<h2>Matched Skills</h2><div>${(data.matchedSkills||[]).map(s=>`<span class='badge'>${s}</span>`).join('')}</div>`);
    w.document.write(`<h2>Missing Skills</h2><div>${(data.missingSkills||[]).map(s=>`<span class='badge'>${s}</span>`).join('')}</div>`);
    w.document.write(`<h2>Final Verdict</h2><p>${(data.audit?.finalVerdict||'')}</p>`);
    w.document.write(`<h2>Executive Summary</h2><p>${(data.summary||'')}</p>`);
    w.document.write(`<h2>Quick Improvements</h2><ul>${(data.audit?.quickWins||[]).map(s=>`<li>${s}</li>`).join('')}</ul>`);
    w.document.write(`<h2>Priority Suggestions</h2><ul>${(data.audit?.suggestionBullets?.length ? data.audit.suggestionBullets : splitSuggestions(data.suggestions||'')).map(s=>`<li>${s}</li>`).join('')}</ul>`);
    w.document.write(`<h2>Strengths</h2><ul>${((data.audit?.strengthHighlights?.length ? data.audit.strengthHighlights : data.strengths)||[]).map(s=>`<li>${s}</li>`).join('')}</ul>`);
    w.document.write(`<h2>Risks</h2><ul>${((data.audit?.riskHighlights?.length ? data.audit.riskHighlights : data.risks)||[]).map(s=>`<li>${s}</li>`).join('')}</ul>`);
    w.document.write(`<h2>Score Breakdown</h2>`);
    w.document.write(`<div class='metric'><strong>Keyword Coverage:</strong> ${formatScore(data.breakdown?.keywordCoverage)}%</div>`);
    w.document.write(`<div class='metric'><strong>Section Quality:</strong> ${formatScore(data.breakdown?.sectionScore)}%</div>`);
    w.document.write(`<div class='metric'><strong>Impact Score:</strong> ${formatScore(data.breakdown?.impactScore)}%</div>`);
    w.document.write(`<div class='metric'><strong>Formatting:</strong> ${formatScore(data.breakdown?.formattingScore)}%</div>`);
    w.document.write(`</body></html>`); w.document.close(); w.print();
  }

  document.addEventListener('DOMContentLoaded', async ()=>{
    const params = new URLSearchParams(location.search);
    const id = params.get('id');
    try{
      let result = null;
      if(id){ result = await api.getResult(id); }
      else {
        const version = sessionStorage.getItem('SRA_RESULT_SCHEMA_VERSION');
        const cached = sessionStorage.getItem('SRA_LAST_RESULT');
        if(cached && version === RESULT_SCHEMA_VERSION) result = JSON.parse(cached);
        else if(cached){
          sessionStorage.removeItem('SRA_LAST_RESULT');
          sessionStorage.removeItem('SRA_RESULT_SCHEMA_VERSION');
          showToast('Stored analysis was outdated. Please run analysis again to load the latest ATS logic.', 'warning');
        }
      }
      hydrate(result);
    }catch(err){
      console.error(err); showToast('Failed to load results: ' + (err.message||'Unknown error'), 'danger');
    }
    qs('#btnDownloadJSON')?.addEventListener('click', downloadJSON);
    qs('#btnDownloadPDF')?.addEventListener('click', downloadPDF);
  });
})(window.SRA_API, window.SRA_UI);
