const SESSION_ID = "s_" + Math.random().toString(36).substring(2, 10);
const langExt = {
  Python: "main.py", JavaScript: "index.js", TypeScript: "index.ts",
  Java: "Main.java", "C++": "main.cpp", Go: "main.go",
  Rust: "main.rs", SQL: "query.sql", Other: "code.txt"
};

const codeEl = document.getElementById("code");
const lnEl = document.getElementById("ln");

function updateFilename() {
  const lang = document.getElementById("language").value;
  document.getElementById("fname").textContent = langExt[lang] || "code.txt";
}

codeEl.addEventListener("input", () => {
  const lines = codeEl.value.split("\n").length;
  lnEl.textContent = Array.from({length: lines}, (_, i) => i + 1).join("\n");
  document.getElementById("cc").textContent = codeEl.value.length;
});

codeEl.addEventListener("scroll", () => { lnEl.scrollTop = codeEl.scrollTop; });

async function runReview() {
  const code = codeEl.value.trim();
  const language = document.getElementById("language").value;
  const btn = document.getElementById("run-btn");
  const errEl = document.getElementById("err");
  const resultEl = document.getElementById("result");

  errEl.classList.add("hidden");
  resultEl.classList.add("hidden");

  if (code.length < 10) { showErr("Need at least 10 characters."); return; }
  if (code.length > 10000) { showErr("Exceeds 10,000 character limit."); return; }

  btn.disabled = true;
  btn.textContent = "Analysing...";

  try {
    const res = await fetch("/api/review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, language, session_id: SESSION_ID })
    });
    const data = await res.json();
    if (!res.ok) { showErr(data.detail || "Review failed."); return; }
    renderResult(data, language);
  } catch {
    showErr("Network error.");
  } finally {
    btn.disabled = false;
    btn.innerHTML = "&#9654; Run Review";
  }
}

function renderResult(data, language) {
  const el = document.getElementById("result");
  el.classList.remove("hidden");
  el.scrollIntoView({ behavior: "smooth", block: "nearest" });

  const badge = document.getElementById("quality-badge");
  badge.textContent = data.overall_quality;
  badge.className = "badge";
  if (data.overall_quality === "Good") badge.classList.add("good");
  else if (data.overall_quality === "Needs Improvement") badge.classList.add("improve");
  else badge.classList.add("poor");

  document.getElementById("summary").textContent = data.summary;
  document.getElementById("rmeta").textContent =
    `${language} · ${data.issues.length} issues · ${data.suggestions.length} suggestions · ${new Date().toLocaleTimeString()}`;
  document.getElementById("ic").textContent = data.issues.length;
  document.getElementById("sc").textContent = data.suggestions.length;

  const issuesEl = document.getElementById("issues");
  issuesEl.innerHTML = '<div class="items">' + (data.issues.length === 0
    ? '<p class="empty">No issues found.</p>'
    : data.issues.map(i => `
      <div class="issue-card">
        <div class="itop">
          <span class="cat cat-${(i.category||'default').toLowerCase()}">${i.category||'Issue'}</span>
          <span class="iline">line ${i.line||'?'}</span>
        </div>
        <div class="idesc">${esc(i.description)}</div>
      </div>`).join('')) + '</div>';

  const suggEl = document.getElementById("suggestions");
  suggEl.innerHTML = '<div class="items">' + (data.suggestions.length === 0
    ? '<p class="empty">No suggestions.</p>'
    : data.suggestions.map(s => `
      <div class="sugg-card">
        <div class="stitle">${esc(s.title)}</div>
        <div class="sdesc">${esc(s.description)}</div>
        ${s.example && s.example !== 'N/A' ? `<div class="sexample">${esc(s.example)}</div>` : ''}
      </div>`).join('')) + '</div>';
}

function clearAll() {
  codeEl.value = "";
  lnEl.textContent = "1";
  document.getElementById("cc").textContent = "0";
  document.getElementById("result").classList.add("hidden");
  document.getElementById("err").classList.add("hidden");
}

function showErr(msg) {
  const el = document.getElementById("err");
  el.textContent = msg;
  el.classList.remove("hidden");
}

function esc(s) {
  if (!s) return "";
  return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}
