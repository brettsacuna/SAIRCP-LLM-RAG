// =============================================
// SAIRCP Frontend v2 — Institutional Theme
// =============================================

// Auto-detecta la URL de la API:
// - Si se accede via nginx (puerto 3000), usa la misma origin (proxy)
// - Si se abre el HTML directo (file://), usa localhost:8000
function getDefaultApiUrl() {
  const loc = window.location;
  if (loc.protocol === 'file:') return 'http://localhost:8000';
  // Nginx en el mismo host hace proxy de /api/ al backend
  return loc.origin;
}

const API = () => document.getElementById('apiUrl').value.replace(/\/+$/, '');
let analysisHistory = [];
let selectedFile = null;

// --- Navigation ---
function switchView(name) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.sub-nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('view-' + name)?.classList.add('active');
  document.querySelector(`[data-view="${name}"]`)?.classList.add('active');
  window.scrollTo(0, 0);
}

// --- Loading ---
function showLoading(text, sub) {
  document.getElementById('loadingText').textContent = text || 'Procesando...';
  document.getElementById('loadingSub').textContent = sub || '';
  document.getElementById('loadingOverlay').classList.add('active');
  animateSteps();
}
function hideLoading() {
  document.getElementById('loadingOverlay').classList.remove('active');
}
function animateSteps() {
  const steps = document.querySelectorAll('.loading-steps .step');
  let i = 0;
  const iv = setInterval(() => {
    steps.forEach(s => s.classList.remove('active'));
    if (i < steps.length) { steps[i].classList.add('active'); i++; }
    else clearInterval(iv);
  }, 2500);
}

// --- API calls ---
async function apiCall(endpoint, options = {}) {
  const url = API() + '/api/v1' + endpoint;
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw { status: res.status, data };
  return data;
}

// --- Health ---
async function checkHealth() {
  const dot = document.getElementById('statusDot');
  const label = document.getElementById('statusLabel');
  try {
    const data = await apiCall('/health');
    dot.className = 'status-dot online';
    label.textContent = `v${data.version} — Conectado`;
    return data;
  } catch {
    dot.className = 'status-dot offline';
    label.textContent = 'Sin conexión con la API';
    return null;
  }
}

function isHealthy(value) {
  const bad = ['error', 'down', 'not_initialized', 'failed', 'unhealthy'];
  return !bad.includes(value?.toLowerCase());
}

async function fetchHealth() {
  const c = document.getElementById('healthResult');
  c.style.display = 'block';
  try {
    const data = await apiCall('/health');
    const comps = Object.entries(data.components || {});
    c.innerHTML = `
      <div class="result-card">
        <div class="result-card-header">
          <strong>Estado del sistema</strong>
          <span class="risk-badge risk-badge--low">${data.status.toUpperCase()}</span>
        </div>
        <div class="result-card-body">
          <div class="result-meta">
            <div>Versión: <span>${data.version}</span></div>
            <div>Fecha: <span>${new Date(data.timestamp).toLocaleString('es-PE')}</span></div>
          </div>
          <div class="health-grid" style="margin-top:16px">
            ${comps.map(([k,v]) => `
              <div class="health-item">
                <div class="health-dot ${isHealthy(v)?'ok':'err'}"></div>
                <span class="health-label">${k}</span>
                <span class="health-value">${v}</span>
              </div>`).join('')}
          </div>
        </div>
      </div>
      <button class="toggle-json" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'block':'none'">{ } Ver JSON</button>
      <div class="json-view" style="display:none;margin-top:8px">${syntaxHL(data)}</div>`;
  } catch (e) {
    c.innerHTML = `<div class="error-msg">Error al conectar: ${e.message || JSON.stringify(e.data)}</div>`;
  }
}

// --- Analyze ---
async function handleAnalyze() {
  const content = document.getElementById('docContent').value;
  const docType = document.getElementById('docType').value;
  if (content.length < 50) return alert('El contenido debe tener al menos 50 caracteres.');
  showLoading('Analizando documento...', 'Pipeline: Analizador → Comparador → Investigador → Evaluador → Generador');
  try {
    const data = await apiCall('/analyze', {
      method: 'POST',
      body: JSON.stringify({
        content, document_type: docType,
        process_id: document.getElementById('processId').value || undefined,
        entity_name: document.getElementById('entityName').value || undefined,
      }),
    });
    hideLoading();
    addToHistory(data);
    renderResult('analyzeResult', data);
  } catch (err) {
    hideLoading();
    showError('analyzeResult', err);
  }
}

// --- Upload ---
function handleDrop(e) {
  e.preventDefault();
  document.getElementById('dropZone').classList.remove('dragover');
  if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0]);
}
function handleFileSelect(input) { if (input.files[0]) setFile(input.files[0]); }
function setFile(file) {
  selectedFile = file;
  document.getElementById('fileInfo').style.display = 'flex';
  document.getElementById('fileName').textContent = `${file.name} (${(file.size/1024).toFixed(1)} KB)`;
  document.getElementById('uploadBtn').disabled = false;
}
function clearFile() {
  selectedFile = null;
  document.getElementById('fileInfo').style.display = 'none';
  document.getElementById('fileInput').value = '';
  document.getElementById('uploadBtn').disabled = true;
}
async function handleUpload() {
  if (!selectedFile) return;
  showLoading('Procesando archivo...', `Extrayendo texto de ${selectedFile.name}`);
  const fd = new FormData();
  fd.append('file', selectedFile);
  try {
    const res = await fetch(API() + '/api/v1/analyze/upload', { method: 'POST', body: fd });
    const data = await res.json();
    hideLoading();
    if (!res.ok) throw { status: res.status, data };
    addToHistory(data);
    renderResult('uploadResult', data);
  } catch (err) { hideLoading(); showError('uploadResult', err); }
}

// --- Query ---
async function handleQuery() {
  const query = document.getElementById('queryInput').value;
  if (query.length < 5) return alert('La pregunta debe tener al menos 5 caracteres.');
  const topK = parseInt(document.getElementById('topK').value) || 5;
  showLoading('Consultando base de conocimiento...', 'Buscando documentos relevantes');
  try {
    const data = await apiCall('/query', { method: 'POST', body: JSON.stringify({ query, top_k: topK }) });
    hideLoading();
    const c = document.getElementById('queryResult');
    c.style.display = 'block';
    c.innerHTML = `
      <div class="result-card">
        <div class="result-card-header"><strong>Respuesta</strong></div>
        <div class="result-card-body">
          <div class="query-answer">${esc(data.response)}</div>
          <div class="result-meta" style="margin-top:14px">
            <div>Fuentes: <span>${data.sources.length}</span></div>
            <div>Tokens: <span>${data.tokens_used}</span></div>
            <div>Latencia: <span>${data.latency_ms.toFixed(0)}ms</span></div>
          </div>
          ${data.sources.length ? `<div style="margin-top:10px">${data.sources.map(s => `<span class="tag">${s.id}</span>`).join(' ')}</div>` : ''}
        </div>
      </div>
      <button class="toggle-json" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'block':'none'">{ } Ver JSON</button>
      <div class="json-view" style="display:none;margin-top:8px">${syntaxHL(data)}</div>`;
  } catch (err) { hideLoading(); showError('queryResult', err); }
}

// --- Ingest ---
async function handleIngest() {
  const raw = document.getElementById('ingestDocs').value;
  let docs;
  try { docs = JSON.parse(raw); if (!Array.isArray(docs)) docs = [docs]; }
  catch { return showError('ingestResult', { message: 'JSON no válido. Verifique el formato.' }); }
  showLoading('Ingresando documentos...', `${docs.length} documento(s)`);
  try {
    const data = await apiCall('/ingest', { method: 'POST', body: JSON.stringify({ documents: docs }) });
    hideLoading();
    const c = document.getElementById('ingestResult');
    c.style.display = 'block';
    c.innerHTML = `
      <div class="result-card">
        <div class="result-card-header"><strong>Ingesta completada</strong><span class="risk-badge risk-badge--low">${data.status.toUpperCase()}</span></div>
        <div class="result-card-body">
          <div class="result-meta">
            <div>Chunks indexados: <span>${data.indexed_docs}</span></div>
            <div>Errores: <span>${data.errors.length}</span></div>
          </div>
          ${data.errors.length ? `<div class="error-msg" style="margin-top:12px">${data.errors.join('<br>')}</div>` : ''}
        </div>
      </div>`;
  } catch (err) { hideLoading(); showError('ingestResult', err); }
}

// --- Render analysis result ---
function renderResult(containerId, data) {
  const c = document.getElementById(containerId);
  c.style.display = 'block';
  const rk = data.risk_level === 'BAJO' ? 'low' : data.risk_level === 'MEDIO' ? 'med' : 'high';
  const rc = rk === 'low' ? '#2E7D32' : rk === 'med' ? '#E65100' : '#C62828';
  const pct = Math.min(data.total_score, 100);
  const circ = 2 * Math.PI * 30;
  const off = circ - (pct / 100) * circ;

  c.innerHTML = `
    <div class="result-card">
      <div class="result-card-header">
        <div style="display:flex;align-items:center;gap:16px">
          <div class="score-ring">
            <svg viewBox="0 0 72 72">
              <circle cx="36" cy="36" r="30" fill="none" stroke="${rc}20" stroke-width="5"/>
              <circle cx="36" cy="36" r="30" fill="none" stroke="${rc}" stroke-width="5"
                stroke-dasharray="${circ}" stroke-dashoffset="${off}" stroke-linecap="round"/>
            </svg>
            <div class="score-ring-value" style="color:${rc}">${data.total_score}</div>
          </div>
          <div>
            <div style="font-weight:600;font-size:16px">Resultado del análisis</div>
            <div style="font-size:12px;color:var(--text-muted)">${data.analysis_id}</div>
          </div>
        </div>
        <span class="risk-badge risk-badge--${rk}">${data.risk_level}</span>
      </div>
      <div class="result-card-body">
        <div class="result-meta">
          <div>Tipo: <span>${data.document_type}</span></div>
          <div>Modelo: <span>${data.model_used}</span></div>
          <div>Tiempo: <span>${(data.processing_time_ms/1000).toFixed(1)}s</span></div>
          <div>Trace: <span style="font-family:monospace;font-size:11px">${data.trace_id?.substring(0,12)}...</span></div>
        </div>
        ${data.summary ? `<div class="result-section"><h3>Resumen ejecutivo</h3><div class="summary-text">${esc(data.summary)}</div></div>` : ''}
        ${data.alerts?.length ? `<div class="result-section"><h3>Alertas <span class="section-count">${data.alerts.length}</span></h3>${data.alerts.map(a => renderAlert(a)).join('')}</div>` : ''}
        ${data.requirements_found?.length ? `<div class="result-section"><h3>Requisitos encontrados <span class="section-count">${data.requirements_found.length}</span></h3><div>${data.requirements_found.map(r => `<span class="tag">${esc(r)}</span>`).join('')}</div></div>` : ''}
        ${data.potential_restrictions?.length ? `<div class="result-section"><h3>Restricciones potenciales <span class="section-count">${data.potential_restrictions.length}</span></h3><div>${data.potential_restrictions.map(r => `<span class="tag tag--danger">${esc(r)}</span>`).join('')}</div></div>` : ''}
        ${data.providers_found?.length ? `<div class="result-section"><h3>Proveedores <span class="section-count">${data.providers_found.length}</span></h3>${data.providers_found.map(p => `<div class="provider-row"><span class="provider-name">${esc(p.name||'N/A')}</span><span class="provider-ruc">${p.ruc||''}</span><span class="provider-source">${p.source||''}</span></div>`).join('')}</div>` : ''}
      </div>
    </div>
    <button class="toggle-json" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'block':'none'">{ } Ver JSON completo</button>
    <div class="json-view" style="display:none;margin-top:8px">${syntaxHL(data)}</div>`;
}

function renderAlert(a) {
  const rk = a.severity === 'BAJO' ? 'low' : a.severity === 'MEDIO' ? 'med' : 'high';
  return `<div class="alert-card">
    <div class="alert-card-header">
      <span class="alert-title">${esc(a.description)}</span>
      <span class="risk-badge risk-badge--${rk}" style="font-size:10px;padding:3px 10px">${a.severity}</span>
    </div>
    ${a.document_fragment ? `<div class="alert-fragment">"${esc(a.document_fragment)}"</div>` : ''}
    ${a.indicators?.length ? `<div>${a.indicators.map(i => `<span class="indicator-pill">${esc(i.indicator)} <span class="indicator-weight">${i.weight}pts</span></span>`).join('')}</div>` : ''}
    ${a.recommendation ? `<div class="alert-recommendation">${esc(a.recommendation)}</div>` : ''}
  </div>`;
}

// --- History & Dashboard ---
function addToHistory(result) {
  analysisHistory.unshift(result);
  updateDashboard();
}
function updateDashboard() {
  document.getElementById('statTotal').textContent = analysisHistory.length;
  document.getElementById('statLow').textContent = analysisHistory.filter(r => r.risk_level === 'BAJO').length;
  document.getElementById('statMed').textContent = analysisHistory.filter(r => r.risk_level === 'MEDIO').length;
  document.getElementById('statHigh').textContent = analysisHistory.filter(r => r.risk_level === 'ALTO').length;

  const list = document.getElementById('recentResults');
  if (!analysisHistory.length) return;
  list.innerHTML = analysisHistory.slice(0, 10).map(r => {
    const rk = r.risk_level === 'BAJO' ? 'low' : r.risk_level === 'MEDIO' ? 'med' : 'high';
    const rc = rk === 'low' ? 'var(--risk-low)' : rk === 'med' ? 'var(--risk-med)' : 'var(--risk-high)';
    return `<div class="result-list-item" onclick="showDetail('${r.analysis_id}')">
      <div class="rli-score" style="color:${rc}">${r.total_score}</div>
      <div class="rli-info"><div class="rli-title">${r.analysis_id} — ${r.document_type}</div><div class="rli-meta">${r.alerts?.length||0} alertas</div></div>
      <div class="rli-time">${new Date(r.timestamp).toLocaleTimeString('es-PE')}</div>
      <span class="risk-badge risk-badge--${rk}" style="font-size:10px;padding:3px 10px">${r.risk_level}</span>
    </div>`;
  }).join('');
}
function showDetail(id) {
  const r = analysisHistory.find(x => x.analysis_id === id);
  if (!r) return;
  switchView('analyze');
  renderResult('analyzeResult', r);
}

// --- Utils ---
function esc(s) { if (!s) return ''; const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
function showError(containerId, err) {
  const c = document.getElementById(containerId);
  c.style.display = 'block';
  const msg = err?.data?.detail ? (Array.isArray(err.data.detail) ? err.data.detail.map(d => `${d.loc?.join('.')} — ${d.msg}`).join('; ') : err.data.detail) : err?.message || JSON.stringify(err);
  c.innerHTML = `<div class="error-msg">Error: ${msg}</div>`;
}
function syntaxHL(obj) {
  return JSON.stringify(obj, null, 2).replace(
    /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+\.?\d*([eE][+-]?\d+)?)/g,
    m => { let c='json-number'; if (/^"/.test(m)) c=/:$/.test(m)?'json-key':'json-string'; else if (/true|false/.test(m)) c='json-bool'; else if (/null/.test(m)) c='json-null'; return `<span class="${c}">${m}</span>`; }
  );
}

document.getElementById('docContent')?.addEventListener('input', function() {
  document.getElementById('charCount').textContent = this.value.length + ' caracteres';
});

// Init — auto-detectar URL de API
document.getElementById('apiUrl').value = getDefaultApiUrl();
checkHealth();
setInterval(checkHealth, 30000);
