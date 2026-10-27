LANDING_HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ReproLens 复现镜</title>
<style>
:root{--ink:#152033;--muted:#64748b;--line:#dbe4f0;--blue:#2457d6;--paper:#fff;--bg:#f4f7fc;--green:#0f8a5f;--red:#b42336}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:radial-gradient(circle at 10% 0%,rgba(36,87,214,.14),transparent 34%),radial-gradient(circle at 90% 12%,rgba(14,165,233,.12),transparent 30%),var(--bg);font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif}
main{max-width:1160px;margin:0 auto;padding:42px 22px 70px}.hidden{display:none!important}.top{display:flex;justify-content:space-between;align-items:center;gap:14px;margin-bottom:32px}.brand{font-size:20px;font-weight:900}.brand span{color:var(--blue)}.stable{display:inline-flex;align-items:center;gap:7px;padding:7px 11px;border-radius:999px;background:#e7f7ef;color:#0f7a52;font-size:12px;font-weight:800}
.hero{display:grid;grid-template-columns:1.2fr .8fr;gap:36px;align-items:center}.eyebrow{color:var(--blue);font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:12px}h1{font-size:56px;line-height:1.08;margin:12px 0 20px}h1 span{color:var(--blue)}.lead{font-size:17px;line-height:1.8;color:#40516c;max-width:680px}.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}.chip{padding:7px 11px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.72);font-size:12px;font-weight:700;color:#40516c}
.panel{background:rgba(255,255,255,.92);border:1px solid rgba(219,228,240,.85);border-radius:22px;padding:24px;box-shadow:0 18px 55px rgba(35,55,95,.12)}.panel strong{font-size:18px}.search{display:flex;gap:8px;margin-top:14px}.search input{min-width:0;flex:1;border:1px solid var(--line);border-radius:11px;padding:13px 14px;font-size:14px;outline:none}.search input:focus{border-color:#9fb7e8;box-shadow:0 0 0 3px rgba(36,87,214,.1)}.search button{border:0;border-radius:11px;padding:0 18px;background:linear-gradient(135deg,#2457d6,#0ea5e9);color:#fff;font-size:14px;font-weight:800;cursor:pointer}.search button:disabled{opacity:.6;cursor:wait}.samples{display:flex;flex-wrap:wrap;gap:7px;margin-top:11px}.sample{border:1px solid var(--line);background:#fff;color:#526175;border-radius:999px;padding:7px 10px;font-size:12px;cursor:pointer}.hint{margin-top:12px;color:var(--muted);font-size:12px;line-height:1.65}.status{display:none;margin-top:14px;padding:11px 13px;border-radius:11px;background:#eef3fb;color:#31507a;font-size:13px;line-height:1.6}.status.show{display:block}.status.error{background:#fff0f2;color:#9e1f31}.status.loading{background:#eef3fb}.spinner{display:inline-block;width:13px;height:13px;border:2px solid #b8c9ee;border-top-color:#2457d6;border-radius:50%;animation:spin .8s linear infinite;vertical-align:-2px;margin-right:7px}@keyframes spin{to{transform:rotate(360deg)}}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:38px}.step{background:rgba(255,255,255,.76);border:1px solid var(--line);border-radius:16px;padding:18px}.step b{display:block;margin-bottom:8px}.step p{margin:0;color:var(--muted);font-size:13px;line-height:1.65}
.result-head{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;margin-bottom:18px}.result-title{font-size:28px;margin:0}.score-line{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:8px;color:var(--muted);font-size:13px}.score-big{font-size:44px;line-height:1;color:var(--blue);font-weight:900}.ready{display:inline-block;padding:6px 10px;border-radius:999px;background:#eef3fb;color:#31507a;font-size:12px;font-weight:800}.back{border:1px solid var(--line);background:#fff;color:var(--blue);border-radius:10px;padding:10px 13px;font-weight:800;cursor:pointer}.tabs{display:flex;flex-wrap:wrap;gap:7px;padding:8px;background:#fff;border:1px solid #e3eaf4;border-radius:14px;box-shadow:0 5px 18px rgba(23,32,51,.06);position:sticky;top:10px;z-index:10}.tab{border:0;border-radius:9px;padding:10px 13px;background:transparent;color:#526175;font-weight:800;cursor:pointer}.tab.active{background:#eef3fb;color:var(--blue)}.pane{margin-top:14px}.frame-wrap{background:#fff;border:1px solid #e3eaf4;border-radius:14px;overflow:hidden;box-shadow:0 6px 22px rgba(23,32,51,.06)}iframe{display:block;width:100%;height:calc(100vh - 220px);min-height:620px;border:0;background:white}.score-pre{margin:0;background:#172033;color:#eaf0fa;border-radius:14px;padding:18px;min-height:500px;overflow:auto;font-size:12px;line-height:1.6}.meta-card{background:#fff;border-radius:14px;padding:16px;box-shadow:0 5px 18px rgba(23,32,51,.06);color:#526175;font-size:13px;line-height:1.8;margin-bottom:12px}
.modal{position:fixed;inset:0;background:rgba(15,23,42,.62);display:grid;place-items:center;padding:22px;z-index:50}.modal.hidden{display:none}.modal-card{width:min(900px,100%);max-height:86vh;display:flex;flex-direction:column;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.25)}.modal-head{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;border-bottom:1px solid var(--line)}.modal-head strong{word-break:break-all}.modal-actions{display:flex;gap:8px}.modal-actions button,.modal-actions a{border:0;border-radius:8px;background:#eef3fb;color:var(--blue);padding:8px 11px;font-weight:800;text-decoration:none;cursor:pointer}.modal-card pre{margin:0;padding:17px;overflow:auto;background:#172033;color:#eaf0fa;line-height:1.55;font-size:12px;flex:1}
.note{margin-top:20px;color:var(--muted);font-size:12px;line-height:1.7}@media(max-width:850px){.hero{grid-template-columns:1fr}h1{font-size:44px}.steps{grid-template-columns:1fr}}@media(max-width:560px){main{padding:28px 14px 50px}h1{font-size:36px}.search{flex-direction:column}.search button{padding:12px}.tabs{position:static}iframe{height:75vh;min-height:520px}}
</style>
</head>
<body><main>
<div class="top"><div class="brand">Repro<span>Lens</span> · 复现镜</div><span class="stable">● 稳定公网动态版</span></div>
<section id="landing">
  <div class="hero">
    <div>
      <div class="eyebrow">Evidence-constrained repository audit</div>
      <h1>给开源 AI 项目做一次<br><span>复现体检</span></h1>
      <p class="lead">粘贴 GitHub 仓库或 GitHub Pages 地址，ReproLens 会固定到具体 commit，检查环境、数据、模型、实验、文档和 AI 特有风险，并把 README 声明与仓库证据一一对应。</p>
      <div class="chips"><span class="chip">六维 25 项检查</span><span class="chip">证据可追溯</span><span class="chip">声明验证</span><span class="chip">AutoFix 复测</span><span class="chip">不执行第三方代码</span></div>
    </div>
    <div class="panel">
      <strong>分析公开仓库</strong>
      <div class="search"><input id="repo" placeholder="https://github.com/owner/repo" autocomplete="off"><button id="run">开始体检</button></div>
      <div class="samples"><button class="sample" data-url="https://github.com/huggingface/smolagents">huggingface/smolagents</button><button class="sample" data-url="https://github.com/WeChatCV/Wan-Alpha">WeChatCV/Wan-Alpha</button><button class="sample" data-url="https://donghaotian123.github.io/Wan-Alpha/">Wan-Alpha Pages</button></div>
      <div class="hint">支持 GitHub 仓库和 GitHub Pages 地址；固定到 commit；不会执行第三方仓库代码。大型仓库可能需要 1～3 分钟。</div>
      <div id="status" class="status"></div>
    </div>
  </div>
  <section class="steps"><div class="step"><b>1. 先找证据</b><p>每条 PASS / PARTIAL 都有 Evidence ID，可以回到文件、行号和原文。</p></div><div class="step"><b>2. 再验声明</b><p>检查 README 说的模型、运行方式、数据和评测是否有真实依据。</p></div><div class="step"><b>3. 最后整改</b><p>生成最小修复提案并复测，只保留能够提高评分的修改。</p></div></section>
  <p class="note">分析结果是复现就绪度快照，不代表项目一定能够成功复现；证据仍应人工复核。</p>
</section>
<section id="result" class="hidden">
  <div class="result-head"><div><h2 id="result-title" class="result-title">分析结果</h2><div class="score-line"><span id="result-score" class="score-big">0</span><span>/ 100</span><span id="result-ready" class="ready">-</span><span id="result-commit"></span></div></div><button id="back" class="back">重新分析</button></div>
  <div class="tabs"><button class="tab active" data-tab="report">完整报告</button><button class="tab" data-tab="claims">声明矩阵</button><button class="tab" data-tab="autofix">AutoFix 验证</button><button class="tab" data-tab="score">评分 JSON</button></div>
  <div id="report-pane" class="pane"><div class="frame-wrap"><iframe id="report-frame" title="完整报告"></iframe></div></div>
  <div id="claims-pane" class="pane hidden"><div class="frame-wrap"><iframe id="claims-frame" title="声明矩阵"></iframe></div></div>
  <div id="autofix-pane" class="pane hidden"><div class="frame-wrap"><iframe id="autofix-frame" title="AutoFix 验证"></iframe></div></div>
  <div id="score-pane" class="pane hidden"><div class="meta-card">评分 JSON 可被 CI、Webhook 或其他外部系统直接读取。</div><pre id="score-pre" class="score-pre"></pre></div>
</section>
</main>
<div id="file-modal" class="modal hidden"><div class="modal-card"><div class="modal-head"><strong id="file-title">文件</strong><div class="modal-actions"><button id="download-file">下载</button><button id="close-file">关闭</button></div></div><pre id="file-content"></pre></div></div>
<script>
const STORAGE_KEY='reprolens:last-result:v2';
const repo=document.getElementById('repo'),run=document.getElementById('run'),status=document.getElementById('status');
const landing=document.getElementById('landing'),result=document.getElementById('result'),back=document.getElementById('back');
const reportFrame=document.getElementById('report-frame'),claimsFrame=document.getElementById('claims-frame'),autofixFrame=document.getElementById('autofix-frame');
const scorePre=document.getElementById('score-pre');
let state={data:null,activeFile:null,timer:null};
function setStatus(message,type='loading'){status.className='status show '+type;status.innerHTML=type==='loading'?'<span class="spinner"></span>'+message:message;}
function clearStatus(){status.className='status';status.textContent='';}
function formatElapsed(ms){return Math.floor(ms/1000)+' 秒';}
async function analyze(){
  const value=repo.value.trim();if(!value){setStatus('请先输入 GitHub 仓库或 GitHub Pages 地址。','error');return;}
  run.disabled=true;run.textContent='分析中…';const started=Date.now();clearStatus();
  setStatus('正在获取仓库并执行静态审计，大型仓库可能需要几分钟。已等待 0 秒');
  state.timer=setInterval(()=>setStatus('正在获取仓库并执行静态审计，大型仓库可能需要几分钟。已等待 '+formatElapsed(Date.now()-started)),1000);
  try{
    const response=await fetch('/api/audit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:value}),cache:'no-store'});
    let data;try{data=await response.json();}catch(error){throw new Error('服务器返回了无法解析的响应（HTTP '+response.status+'）。');}
    if(!response.ok)throw new Error(data.detail||data.error||'分析失败');
    state.data=data;localStorage.setItem(STORAGE_KEY,JSON.stringify(data));renderResult(data);
  }catch(error){setStatus(error.message||'分析失败，请稍后重试。','error');}
  finally{run.disabled=false;run.textContent='开始体检';clearInterval(state.timer);}
}
function renderResult(data){
  landing.classList.add('hidden');result.classList.remove('hidden');
  document.getElementById('result-title').textContent=data.summary.source_url;
  document.getElementById('result-score').textContent=Number(data.summary.score).toFixed(1);
  document.getElementById('result-ready').textContent=data.summary.readiness;
  document.getElementById('result-commit').textContent='commit '+String(data.summary.source_commit||'').slice(0,12);
  reportFrame.srcdoc=data.report_html;claimsFrame.srcdoc=data.claims_html;autofixFrame.srcdoc=data.autofix_html;scorePre.textContent=data.score_json;
  wireFrame(reportFrame,'report');wireFrame(claimsFrame,'claims');wireFrame(autofixFrame,'autofix');showTab('report');window.scrollTo(0,0);
}
function wireFrame(frame,mode){
  frame.onload=()=>{try{
    const doc=frame.contentDocument;
    doc.addEventListener('click',(event)=>{
      const link=event.target.closest('a');if(!link)return;const href=link.getAttribute('href')||'';
      if((mode==='claims'&&href.startsWith('report.html#'))||href==='report.html'){
        event.preventDefault();showTab('report');const hash=href.includes('#')?href.split('#')[1]:'';if(hash)setTimeout(()=>{reportFrame.contentWindow.location.hash=hash;},120);return;
      }
      if(mode==='autofix'&&href.startsWith('autofix/')){event.preventDefault();openFile(href);}
    });
  }catch(error){console.warn('cannot attach frame handlers',error);}};
}
function showTab(name){
  document.querySelectorAll('.tab').forEach(button=>button.classList.toggle('active',button.dataset.tab===name));
  for(const key of ['report','claims','autofix','score'])document.getElementById(key+'-pane').classList.toggle('hidden',key!==name);
}
function openFile(path){
  const content=state.data&&state.data.autofix_files?state.data.autofix_files[path]:null;
  if(content==null){setStatus('没有找到该生成文件。','error');return;}
  state.activeFile={path,content};document.getElementById('file-title').textContent=path;document.getElementById('file-content').textContent=content;document.getElementById('file-modal').classList.remove('hidden');
}
function closeFile(){document.getElementById('file-modal').classList.add('hidden');state.activeFile=null;}
function downloadFile(){if(!state.activeFile)return;const blob=new Blob([state.activeFile.content],{type:'text/plain;charset=utf-8'});const url=URL.createObjectURL(blob);const link=document.createElement('a');link.href=url;link.download=state.activeFile.path.split('/').pop();link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
document.querySelectorAll('.sample').forEach(button=>button.addEventListener('click',()=>{repo.value=button.dataset.url;repo.focus();}));
document.querySelectorAll('.tab').forEach(button=>button.addEventListener('click',()=>showTab(button.dataset.tab)));
run.addEventListener('click',analyze);repo.addEventListener('keydown',event=>{if(event.key==='Enter')analyze();});
back.addEventListener('click',()=>{result.classList.add('hidden');landing.classList.remove('hidden');clearStatus();window.scrollTo(0,0);});
document.getElementById('close-file').addEventListener('click',closeFile);document.getElementById('download-file').addEventListener('click',downloadFile);document.getElementById('file-modal').addEventListener('click',event=>{if(event.target.id==='file-modal')closeFile();});
try{const saved=localStorage.getItem(STORAGE_KEY);if(saved){state.data=JSON.parse(saved);repo.value=state.data.summary.source_url||'';renderResult(state.data);}}catch(error){console.warn(error);}
</script>
</body></html>'''
