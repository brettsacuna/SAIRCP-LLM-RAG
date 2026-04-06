// =============================================
// SAIRCP Frontend — app.js
// =============================================

const API = () => document.getElementById('apiUrl').value.replace(/\/+$/, '');
let analysisHistory = [];
let selectedFile = null;

// --- Navigation ---
function switchView(name) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const view = document.getElementById('view-' + name);
  const btn = document.querySelector(`[data-view="${name}"]`);
  if (view) view.classList.add('active');
  if (btn) btn.classList.add('active');
}

// --- Loading overlay ---
function showLoading(text, sub) {
  const ol = document.getElementById('loadingOverlay');
  document.getElementById('loadingText').textContent = text || 'Procesando...';
  document.getElementById('loadingSub').textContent = sub || '';
  ol.classList.add('active');
}
function hideLoading() {
  document.getElementById('loadingOverlay').classList.remove('active');
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

// --- Health check ---
async function checkHealth() {
  const dot = document.querySelector('.status-dot');
  const label = dot.nextElementSibling;
  try {
    const data = await apiCall('/health');
    dot.className = 'status-dot online';
    label.textContent = `v${data.version} — online`;
    return data;
  } catch {
    dot.className = 'status-dot offline';
    label.textContent = 'Sin conexión';
    return null;
  }
}

async function fetchHealth() {
  const container = document.getElementById('healthResult');
  container.style.display = 'block';
  try {
    const data = await apiCall('/health');
    const comps = Object.entries(data.components || {});
    container.innerHTML = `
      <div class="result-card">
        <div class="result-card-header">
          <span style="font-weight:600">Estado del sistema</span>
          <span class="risk-badge risk-badge--low">${data.status.toUpperCase()}</span>
        </div>
        <div class="result-card-body">
          <div class="result-meta">
            <div class="result-meta-item">Versión: <span>${data.version}</span></div>
            <div class="result-meta-item">Timestamp: <span>${new Date(data.timestamp).toLocaleString()}</span></div>
          </div>
          <div class="health-grid" style="margin-top:16px">
            ${comps.map(([k, v]) => `
              <div class="health-item">
                <div class="health-dot ${v === 'ok' ? 'ok' : 'error'}"></div>
                <span class="health-label">${k}</span>
                <span class="health-value">${v}</span>
              </div>`).join('')}
          </div>
        </div>
      </div>
      <div style="margin-top:14px">
        <button class="toggle-raw" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'block':'none'">{ } JSON</button>
        <div class="json-view" style="display:none;margin-top:8px">${syntaxHighlight(data)}</div>
      </div>`;
  } catch (e) {
    container.innerHTML = `<div class="error-msg">Error al conectar con la API: ${e.message || JSON.stringify(e.data)}</div>`;
  }
}

// --- Analyze document (text) ---
async function handleAnalyze(e) {
  e.preventDefault();
  const content = document.getElementById('docContent').value;
  const docType = document.getElementById('docType').value;
  const processId = document.getElementById('processId').value || undefined;
  const entityName = document.getElementById('entityName').value || undefined;

  showLoading('Analizando documento...', 'Agentes: Analizador → Comparador → Investigador → Evaluador → Generador');

  try {
    const data = await apiCall('/analyze', {
      method: 'POST',
      body: JSON.stringify({
        content, document_type: docType, process_id: processId, entity_name: entityName,
      }),
    });
    hideLoading();
    addToHistory(data);
    renderAnalysisResult('analyzeResult', data);
  } catch (err) {
    hideLoading();
    const container = document.getElementById('analyzeResult');
    container.style.display = 'block';
    container.innerHTML = `<div class="error-msg">Error: ${formatError(err)}</div>`;
  }
  return false;
}

// --- Upload file ---
function handleDrop(e) {
  e.preventDefault();
  document.getElementById('dropZone').classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file) setFile(file);
}
function handleFileSelect(input) {
  if (input.files[0]) setFile(input.files[0]);
}
function setFile(file) {
  selectedFile = file;
  document.getElementById('fileInfo').style.display = 'flex';
  document.getElementById('fileName').textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
  document.getElementById('uploadBtn').disabled = false;
}
function clearFile() {
  selectedFile = null;
  document.getElementById('fileInfo').style.display = 'none';
  document.getElementById('fileInput').value = '';
  document.getElementById('uploadBtn').disabled = true;
}

async function handleUpload(e) {
  e.preventDefault();
  if (!selectedFile) return;

  showLoading('Procesando archivo...', `Extrayendo texto de ${selectedFile.name}`);

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const url = API() + '/api/v1/analyze/upload';
    const res = await fetch(url, { method: 'POST', body: formData });
    const data = await res.json();
    hideLoading();
    if (!res.ok) throw { status: res.status, data };
    addToHistory(data);
    renderAnalysisResult('uploadResult', data);
  } catch (err) {
    hideLoading();
    const container = document.getElementById('uploadResult');
    container.style.display = 'block';
    container.innerHTML = `<div class="error-msg">Error: ${formatError(err)}</div>`;
  }
  return false;
}

// --- Query RAG ---
async function handleQuery(e) {
  e.preventDefault();
  const query = document.getElementById('queryInput').value;
  const topK = parseInt(document.getElementById('topK').value) || 5;

  showLoading('Consultando base de conocimiento...', 'Buscando documentos relevantes');

  try {
    const data = await apiCall('/query', {
      method: 'POST',
      body: JSON.stringify({ query, top_k: topK }),
    });
    hideLoading();
    const container = document.getElementById('queryResult');
    container.style.display = 'block';
    container.innerHTML = `
      <div class="query-answer">${escapeHtml(data.response)}</div>
      <div class="query-sources">
        <strong>Fuentes:</strong> ${data.sources.length ? data.sources.map(s => `<span class="tag">${s.id} (dist: ${s.distance?.toFixed(3) || 'N/A'})</span>`).join(' ') : 'Sin fuentes encontradas'}
      </div>
      <div class="result-meta" style="margin-top:10px">
        <div class="result-meta-item">Tokens: <span>${data.tokens_used}</span></div>
        <div class="result-meta-item">Latencia: <span>${data.latency_ms.toFixed(0)}ms</span></div>
      </div>
      <div style="margin-top:14px">
        <button class="toggle-raw" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'block':'none'">{ } JSON</button>
        <div class="json-view" style="display:none;margin-top:8px">${syntaxHighlight(data)}</div>
      </div>`;
  } catch (err) {
    hideLoading();
    const container = document.getElementById('queryResult');
    container.style.display = 'block';
    container.innerHTML = `<div class="error-msg">Error: ${formatError(err)}</div>`;
  }
  return false;
}

// --- Ingest ---
async function handleIngest(e) {
  e.preventDefault();
  const raw = document.getElementById('ingestDocs').value;

  let docs;
  try {
    docs = JSON.parse(raw);
    if (!Array.isArray(docs)) docs = [docs];
  } catch {
    const container = document.getElementById('ingestResult');
    container.style.display = 'block';
    container.innerHTML = `<div class="error-msg">Error: JSON no válido. Verifique el formato.</div>`;
    return false;
  }

  showLoading('Ingresando documentos...', `${docs.length} documento(s)`);

  try {
    const data = await apiCall('/ingest', {
      method: 'POST',
      body: JSON.stringify({ documents: docs }),
    });
    hideLoading();
    const container = document.getElementById('ingestResult');
    container.style.display = 'block';
    container.innerHTML = `
      <div class="result-card">
        <div class="result-card-header">
          <span style="font-weight:600">Ingesta completada</span>
          <span class="risk-badge risk-badge--low">${data.status.toUpperCase()}</span>
        </div>
        <div class="result-card-body">
          <div class="result-meta">
            <div class="result-meta-item">Chunks indexados: <span>${data.indexed_docs}</span></div>
            <div class="result-meta-item">Errores: <span>${data.errors.length}</span></div>
          </div>
          ${data.errors.length ? `<div class="error-msg" style="margin-top:12px">${data.errors.join('<br>')}</div>` : ''}
        </div>
      </div>`;
  } catch (err) {
    hideLoading();
    const container = document.getElementById('ingestResult');
    container.style.display = 'block';
    container.innerHTML = `<div class="error-msg">Error: ${formatError(err)}</div>`;
  }
  return false;
}

// --- Render analysis result ---
function renderAnalysisResult(containerId, data) {
  const container = document.getElementById(containerId);
  container.style.display = 'block';

  const riskClass = data.risk_level === 'BAJO' ? 'low' : data.risk_level === 'MEDIO' ? 'med' : 'high';
  const riskColor = riskClass === 'low' ? '#34d399' : riskClass === 'med' ? '#fbbf24' : '#f87171';
  const pct = Math.min(data.total_score, 100);
  const circumference = 2 * Math.PI * 34;
  const offset = circumference - (pct / 100) * circumference;

  container.innerHTML = `
    <div class="result-card">
      <div class="result-card-header">
        <div style="display:flex;align-items:center;gap:16px">
          <div class="score-ring">
            <svg viewBox="0 0 80 80">
              <circle cx="40" cy="40" r="34" fill="none" stroke="${riskColor}20" stroke-width="5"/>
              <circle cx="40" cy="40" r="34" fill="none" stroke="${riskColor}" stroke-width="5"
                stroke-dasharray="${circumference}" stroke-dashoffset="${offset}" stroke-linecap="round"/>
            </svg>
            <div class="score-ring-value" style="color:${riskColor}">${data.total_score}</div>
          </div>
          <div>
            <div style="font-weight:600;font-size:16px">Resultado del análisis</div>
            <div style="font-size:12px;color:var(--text-2);margin-top:2px">${data.analysis_id}</div>
          </div>
        </div>
        <span class="risk-badge risk-badge--${riskClass}">${data.risk_level}</span>
      </div>
      <div class="result-card-body">
        <div class="result-meta">
          <div class="result-meta-item">Tipo: <span>${data.document_type}</span></div>
          <div class="result-meta-item">Modelo: <span>${data.model_used}</span></div>
          <div class="result-meta-item">Tiempo: <span>${(data.processing_time_ms / 1000).toFixed(1)}s</span></div>
          <div class="result-meta-item">Trace: <span style="font-family:var(--mono);font-size:11px">${data.trace_id?.substring(0, 12)}...</span></div>
        </div>

        ${data.summary ? `
        <div class="result-section">
          <h3>Resumen ejecutivo</h3>
          <div class="summary-text">${escapeHtml(data.summary)}</div>
        </div>` : ''}

        ${data.alerts?.length ? `
        <div class="result-section">
          <h3>Alertas <span class="section-count">${data.alerts.length}</span></h3>
          ${data.alerts.map(a => renderAlert(a)).join('')}
        </div>` : ''}

        ${data.requirements_found?.length ? `
        <div class="result-section">
          <h3>Requisitos encontrados <span class="section-count">${data.requirements_found.length}</span></h3>
          <div class="tag-list">${data.requirements_found.map(r => `<span class="tag">${escapeHtml(r)}</span>`).join('')}</div>
        </div>` : ''}

        ${data.potential_restrictions?.length ? `
        <div class="result-section">
          <h3>Restricciones potenciales <span class="section-count">${data.potential_restrictions.length}</span></h3>
          <div class="tag-list">${data.potential_restrictions.map(r => `<span class="tag" style="border-color:rgba(248,113,113,.3);color:var(--risk-high)">${escapeHtml(r)}</span>`).join('')}</div>
        </div>` : ''}

        ${data.providers_found?.length ? `
        <div class="result-section">
          <h3>Proveedores identificados <span class="section-count">${data.providers_found.length}</span></h3>
          ${data.providers_found.map(p => `
            <div class="provider-row">
              <span class="provider-name">${escapeHtml(p.name || 'N/A')}</span>
              <span class="provider-ruc">${p.ruc || ''}</span>
              <span class="provider-source">${p.source || ''}</span>
            </div>`).join('')}
        </div>` : ''}

        ${data.comparable_processes?.length ? `
        <div class="result-section">
          <h3>Procesos comparables <span class="section-count">${data.comparable_processes.length}</span></h3>
          <div class="tag-list">${data.comparable_processes.map(p => `<span class="tag">${escapeHtml(p.id || p.description || JSON.stringify(p))}</span>`).join('')}</div>
        </div>` : ''}
      </div>
    </div>
    <div style="margin-top:14px">
      <button class="toggle-raw" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'block':'none'">{ } JSON completo</button>
      <div class="json-view" style="display:none;margin-top:8px">${syntaxHighlight(data)}</div>
    </div>`;
}

function renderAlert(alert) {
  const riskClass = alert.severity === 'BAJO' ? 'low' : alert.severity === 'MEDIO' ? 'med' : 'high';
  return `
    <div class="alert-card">
      <div class="alert-card-header">
        <span class="alert-title">${escapeHtml(alert.description)}</span>
        <span class="risk-badge risk-badge--${riskClass}" style="font-size:10px;padding:3px 10px">${alert.severity}</span>
      </div>
      ${alert.document_fragment ? `<div class="alert-fragment">"${escapeHtml(alert.document_fragment)}"</div>` : ''}
      ${alert.indicators?.length ? `
        <div style="margin-top:8px">${alert.indicators.map(i => `
          <span class="indicator-pill">${escapeHtml(i.indicator)} <span class="indicator-weight">${i.weight}pts</span></span>
        `).join('')}</div>` : ''}
      ${alert.recommendation ? `<div class="alert-recommendation">${escapeHtml(alert.recommendation)}</div>` : ''}
    </div>`;
}

// --- History ---
function addToHistory(result) {
  analysisHistory.unshift(result);
  updateDashboard();
}

function updateDashboard() {
  const total = analysisHistory.length;
  const low = analysisHistory.filter(r => r.risk_level === 'BAJO').length;
  const med = analysisHistory.filter(r => r.risk_level === 'MEDIO').length;
  const high = analysisHistory.filter(r => r.risk_level === 'ALTO').length;

  document.getElementById('statAnalysis').textContent = total;
  document.getElementById('statLow').textContent = low;
  document.getElementById('statMed').textContent = med;
  document.getElementById('statHigh').textContent = high;

  const list = document.getElementById('recentResults');
  if (!total) return;

  list.innerHTML = analysisHistory.slice(0, 10).map(r => {
    const riskClass = r.risk_level === 'BAJO' ? 'low' : r.risk_level === 'MEDIO' ? 'med' : 'high';
    const riskColor = riskClass === 'low' ? 'var(--risk-low)' : riskClass === 'med' ? 'var(--risk-med)' : 'var(--risk-high)';
    return `
      <div class="result-list-item" onclick="showHistoryDetail('${r.analysis_id}')">
        <div class="rli-score" style="color:${riskColor}">${r.total_score}</div>
        <div class="rli-info">
          <div class="rli-title">${r.analysis_id} — ${r.document_type}</div>
          <div class="rli-meta">${r.alerts?.length || 0} alertas · ${r.risk_level}</div>
        </div>
        <div class="rli-time">${new Date(r.timestamp).toLocaleTimeString()}</div>
        <span class="risk-badge risk-badge--${riskClass}" style="font-size:10px;padding:3px 10px">${r.risk_level}</span>
      </div>`;
  }).join('');
}

function showHistoryDetail(id) {
  const result = analysisHistory.find(r => r.analysis_id === id);
  if (!result) return;
  switchView('analyze');
  renderAnalysisResult('analyzeResult', result);
}

// --- Utilities ---
function escapeHtml(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function formatError(err) {
  if (err?.data?.detail) {
    if (Array.isArray(err.data.detail)) {
      return err.data.detail.map(d => `${d.loc?.join('.')} — ${d.msg}`).join('; ');
    }
    return err.data.detail;
  }
  return err?.message || JSON.stringify(err);
}

function syntaxHighlight(obj) {
  const json = JSON.stringify(obj, null, 2);
  return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+\.?\d*([eE][+-]?\d+)?)/g,
    (match) => {
      let cls = 'json-number';
      if (/^"/.test(match)) {
        cls = /:$/.test(match) ? 'json-key' : 'json-string';
      } else if (/true|false/.test(match)) {
        cls = 'json-bool';
      } else if (/null/.test(match)) {
        cls = 'json-null';
      }
      return `<span class="${cls}">${match}</span>`;
    }
  );
}

// --- Char counter ---
document.getElementById('docContent')?.addEventListener('input', function () {
  document.getElementById('charCount').textContent = this.value.length + ' caracteres';
});

// --- Init ---
checkHealth();
setInterval(checkHealth, 30000);
