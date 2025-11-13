/* Fanmei site – Lightweight Q&A chat widget (frontend-only)
 * Drop-in: add <script defer src="{{ url_for('static', filename='js/fmw-chat.js') }}"></script> before </body>
 * No global CSS changed. All styles are scoped to .fmw-*
 */
(() => {
  const URLS = {
    about:   '/about',
    contact: '/about#contact',
    ai:      '/projects/ai',
    azure:   '/projects/ai#azure-architecture', // 若你的 Azure 动画页有单独路由，改这里
  };
  const ACCENT = '#0f5d66';     // 主题色（深青）
  const AUTO_COLLAPSE_MS = 8000;// 回答后若无操作，自动收起的毫秒数
  const WIDTH = 360;            // 面板宽度（px），可改为 320~420
  // ========================================================================

  // ====== 注入局部 CSS（只作用于 .fmw-*，不会影响全站） ======================
  const css = `
  .fmw-wrap{position:fixed;right:18px;bottom:18px;z-index:9999;font:14px/1.45 system-ui,Segoe UI,Roboto,Helvetica,Arial;}
  .fmw-fab{
    width:64px;height:64px;border-radius:50%;border:none;cursor:pointer;
    display:flex;align-items:center;justify-content:center;
    color:#fff;background:${ACCENT};
    box-shadow:0 14px 34px rgba(0,0,0,.22);
    animation:fmw-pulse 2.6s infinite;
  }
  .fmw-fab svg{width:28px;height:28px;fill:#fff}
  .fmw-fab::after{
    content:"Chat";position:absolute;right:74px;bottom:18px;
    background:#fff;color:${ACCENT};font-weight:800;
    padding:.35rem .6rem;border-radius:999px;box-shadow:0 8px 18px rgba(0,0,0,.14);
    opacity:0;transform:translateY(8px);pointer-events:none;
    transition:.25s;
  }
  .fmw-fab.nudge::after{opacity:1;transform:none;}
  @keyframes fmw-pulse{0%{box-shadow:0 0 0 0 rgba(15,93,102,.45)}70%{box-shadow:0 0 0 18px rgba(15,93,102,0)}100%{box-shadow:0 0 0 0 rgba(15,93,102,0)}}

  .fmw-panel{
    position:fixed;right:18px;bottom:94px;width:min(${WIDTH}px, calc(100vw - 28px));
    background:#fff;border-radius:16px;box-shadow:0 22px 48px rgba(0,0,0,.22);
    opacity:0;transform:translateY(12px) scale(.98);pointer-events:none;
    transition:transform .22s ease, opacity .22s ease;
  }
  .fmw-open .fmw-panel{opacity:1;transform:none;pointer-events:auto;}

  .fmw-head{
    display:flex;align-items:center;justify-content:space-between;gap:.6rem;
    padding:.65rem .85rem;border-radius:16px 16px 0 0;
    background:linear-gradient(180deg,#e9f3f1,#e4f0ef);
    border-bottom:1px solid rgba(0,0,0,.06);
  }
  .fmw-title{margin:0;font-weight:800;color:${ACCENT};font-size:1rem}
  .fmw-close{
    appearance:none;border:none;border-radius:10px;cursor:pointer;
    padding:.35rem .55rem;background:#fff;color:${ACCENT};font-weight:800;
    box-shadow:0 1px 0 rgba(0,0,0,.05), inset 0 0 0 1px rgba(0,0,0,.06);
  }

  /* 关键信息：固定高度 + 可滚动容器 */
  .fmw-msgs{
    max-height:360px;min-height:220px;overflow:auto;
    padding:.75rem;background:#fafcfc;
  }

  .fmw-suggest{display:flex;gap:.5rem;flex-wrap:wrap;padding:0 .75rem .5rem;background:#fafcfc}
  .fmw-chip{
    appearance:none;border:none;cursor:pointer;background:#fff;
    border-radius:999px;padding:.35rem .6rem;font-weight:700;color:${ACCENT};
    box-shadow:0 1px 0 rgba(0,0,0,.06), inset 0 0 0 1px rgba(0,0,0,.06);
  }

  .fmw-bubble{max-width:82%;margin:.35rem 0;padding:.55rem .7rem;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,.06)}
  .fmw-bot{background:#fff;color:#24474d;border:1px solid rgba(0,0,0,.06)}
  .fmw-me {background:${ACCENT};color:#fff;margin-left:auto}

  .fmw-input{
    display:flex;gap:.5rem;align-items:center;padding:.65rem .75rem;border-top:1px solid rgba(0,0,0,.06);
    background:linear-gradient(180deg,#fdfefe,#f6fbfa);border-radius:0 0 16px 16px;
  }
  .fmw-input input{
    flex:1 1 auto;padding:.55rem .65rem;border-radius:10px;border:1px solid #dbe6e6;outline:none;
  }
  .fmw-send{
    appearance:none;border:none;border-radius:10px;cursor:pointer;
    padding:.55rem .8rem;background:linear-gradient(180deg,#FFF6DE,#FBE9BB);
    color:${ACCENT};font-weight:800;box-shadow:0 2px 0 rgba(0,0,0,.06), inset 0 0 0 1px rgba(0,0,0,.06)
  }

  /* 覆盖链接颜色（只在聊天面板内生效）—— 解决“黄色不可读” */
  .fmw-panel a{color:${ACCENT} !important;text-decoration:underline;text-underline-offset:2px}
  .fmw-panel a:visited{color:#0c4a53 !important}
  `;
  const style = document.createElement('style');
  style.id = 'fmw-chat-style';
  style.textContent = css;
  document.head.appendChild(style);

  // ====== 挂载 DOM =========================================================
  const wrap = document.createElement('div');
  wrap.className = 'fmw-wrap';
  wrap.innerHTML = `
    <div class="fmw-panel" role="dialog" aria-label="Ask about this site">
      <div class="fmw-head">
        <h3 class="fmw-title">Ask about this site</h3>
        <button class="fmw-close" type="button" aria-label="Close">✕</button>
      </div>

      <div class="fmw-msgs" id="fmw-msgs" aria-live="polite"></div>

      <div class="fmw-suggest" id="fmw-suggest">
        <button class="fmw-chip">Show me AI projects</button>
        <button class="fmw-chip">Where is the Azure Architecture demo?</button>
        <button class="fmw-chip">Who is Fanmei Wang?</button>
      </div>

      <div class="fmw-input">
        <input id="fmw-q" type="text" placeholder="Ask about About / Education / Teaching / Projects …" autocomplete="off">
        <button class="fmw-send" id="fmw-send" type="button">Send</button>
      </div>
    </div>

    <button class="fmw-fab nudge" id="fmw-fab" aria-label="Open chat" title="Ask Fanmei">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M4 4h16v12H7l-3 3V4z"></path>
      </svg>
    </button>
  `;
  document.body.appendChild(wrap);

  // ====== 行为逻辑 =========================================================
  const panel   = wrap.querySelector('.fmw-panel');
  const fab     = wrap.querySelector('#fmw-fab');
  const closeBt = wrap.querySelector('.fmw-close');
  const msgsEl  = wrap.querySelector('#fmw-msgs');
  const qInput  = wrap.querySelector('#fmw-q');
  const sendBt  = wrap.querySelector('#fmw-send');
  const chips   = wrap.querySelectorAll('.fmw-chip');

  let collapseTimer = null;
  function scrollToBottom(){ msgsEl.scrollTop = msgsEl.scrollHeight; }
  function open(){ wrap.classList.add('fmw-open'); fab.classList.remove('nudge'); clearTimeout(collapseTimer); setTimeout(scrollToBottom, 0); }
  function close(){ wrap.classList.remove('fmw-open'); clearTimeout(collapseTimer); }
  fab.addEventListener('click', open);
  closeBt.addEventListener('click', close);
  panel.addEventListener('mouseenter', ()=>clearTimeout(collapseTimer));
  panel.addEventListener('mouseleave', ()=> maybeScheduleClose());

  function addBubble(html, who='bot'){
    const b = document.createElement('div');
    b.className = `fmw-bubble ${who==='me'?'fmw-me':'fmw-bot'}`;
    b.innerHTML = html;
    msgsEl.appendChild(b);
    scrollToBottom();
  }

  function sanitize(x){ return (x||'').toString().trim(); }

  function answerFor(qRaw){
    const q = sanitize(qRaw).toLowerCase();

    // 简单意图匹配（可按需扩展）
    if (/ai\s*projects?/.test(q) || /show.*ai/.test(q)) {
      return `All AI demos are here: <a href="${URLS.ai}" target="_self" rel="noopener">AI Projects</a>.`;
    }
    if (/azure.*(architecture|demo|animated)/.test(q) || /lakehouse|databricks/.test(q)) {
      return `Open the step‑by‑step animated Azure Architecture demo: <a href="${URLS.azure}" target="_self" rel="noopener">Open</a>.`;
    }
    if (/who\s+is\s+fanmei|who\s+are\s+you|fanmei\s+wang/.test(q)) {
      return `I'm Fanmei Wang. See <a href="${URLS.about}" target="_self" rel="noopener">About</a> for a short profile.`;
    }
    if (/contact|reach|email|talk/.test(q)) {
      return `Please <a href="${URLS.contact}" target="_self" rel="noopener">contact me here</a>.`;
    }

    // 兜底：告知可回答范围 + 提示按钮
    return `I can answer questions <em>about this site</em>: About, Education, Teaching, Projects (incl. Azure Architecture), and how to contact Fanmei. Try the quick buttons above.`;
  }

  function maybeScheduleClose(){
    clearTimeout(collapseTimer);
    collapseTimer = setTimeout(()=>{ if (!qInput.matches(':focus')) close(); }, AUTO_COLLAPSE_MS);
  }

  function send(){
    const q = sanitize(qInput.value);
    if(!q) return;
    addBubble(q, 'me');
    qInput.value = '';
    const a = answerFor(q);
    // 延时一点点像“思考中”
    setTimeout(()=>{ addBubble(a, 'bot'); maybeScheduleClose(); }, 200);
  }

  chips.forEach(c => c.addEventListener('click', () => {
    qInput.value = c.textContent || '';
    send();
  }));
  sendBt.addEventListener('click', send);
  qInput.addEventListener('keydown', (e)=>{ if(e.key === 'Enter') send(); });

  // 初次轻微提醒
  setTimeout(()=> fab.classList.add('nudge'), 900);

  // 可选：首条欢迎语
  addBubble(`Hi! I can answer questions <strong>only</strong> about Fanmei's profile, education, teaching, projects (incl. Azure Architecture), publications, and how to contact her.`);
})();

