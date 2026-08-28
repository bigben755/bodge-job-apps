from pathlib import Path

path = Path('admin.html')
s = path.read_text()

css_anchor = "    @media(max-width:900px){.app{grid-template-columns:1fr;padding:12px}.list{max-height:420px}.detail-empty{min-height:250px}.meta-grid{grid-template-columns:1fr}.topbar-inner{padding:10px 13px}.site-link{display:none}}"
css = """    .modal-backdrop{position:fixed;inset:0;z-index:60;background:rgba(0,0,0,.72);display:grid;place-items:center;padding:20px;backdrop-filter:blur(8px)}
    .compose-card{width:min(760px,100%);max-height:92vh;overflow:auto;border:1px solid var(--line);border-radius:24px;background:#151519;box-shadow:var(--shadow)}
    .compose-head{padding:22px 24px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;gap:18px;align-items:flex-start}.compose-head h2{margin:2px 0 6px;font-size:1.7rem}.compose-body{padding:22px 24px}.compose-body .field{margin:0 0 16px}.compose-body textarea{min-height:220px;resize:vertical}.attach-box{border:1px dashed rgba(159,77,255,.45);border-radius:15px;padding:15px;background:rgba(159,77,255,.04)}.attach-box input{margin-top:8px;max-width:100%}.attachment-list{display:grid;gap:7px;margin-top:10px}.attachment-item{display:flex;justify-content:space-between;gap:12px;color:var(--muted);font-size:.8rem}.compose-actions{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;margin-top:20px}.compose-actions-right{display:flex;gap:9px}.compose-note{font-size:.78rem;color:var(--muted);margin:8px 0 0}.icon-btn{border:1px solid var(--line);border-radius:11px;background:transparent;color:var(--ink);padding:8px 11px;font-weight:800}.icon-btn:hover{background:rgba(255,255,255,.06)}
"""
if '.modal-backdrop{' not in s:
    if css_anchor not in s:
        raise SystemExit('CSS anchor not found')
    s = s.replace(css_anchor, css + css_anchor)

top_anchor = '        <a class="site-link" href="./">View website</a>'
compose_button = '        <button class="ghost hidden" id="compose-btn" type="button">Compose email</button>\n'
if 'id="compose-btn"' not in s:
    if top_anchor not in s:
        raise SystemExit('Topbar anchor not found')
    s = s.replace(top_anchor, compose_button + top_anchor)

modal = '''
    <div class="modal-backdrop hidden" id="compose-modal" role="dialog" aria-modal="true" aria-labelledby="compose-title">
      <section class="compose-card">
        <div class="compose-head">
          <div><p class="eyebrow">New message</p><h2 id="compose-title">Compose email</h2><p class="muted">Send from <strong>hello@bodge-job.com</strong></p></div>
          <button class="icon-btn" id="compose-close" type="button" aria-label="Close compose window">Close</button>
        </div>
        <form class="compose-body" id="compose-form">
          <div class="field"><label for="compose-to">To</label><input id="compose-to" name="to" type="text" autocomplete="off" placeholder="name@example.com" required><p class="compose-note">Separate multiple addresses with commas, semicolons or new lines.</p></div>
          <div class="field"><label for="compose-subject">Subject</label><input id="compose-subject" name="subject" type="text" maxlength="200" required></div>
          <div class="field"><label for="compose-body">Message</label><textarea id="compose-body" name="body" maxlength="50000" required placeholder="Write your email..."></textarea></div>
          <div class="attach-box">
            <strong>Attachments</strong>
            <p class="compose-note">Up to 10 files, 20 MB total.</p>
            <input id="compose-files" type="file" multiple>
            <div class="attachment-list" id="attachment-list"></div>
          </div>
          <div class="compose-actions">
            <div class="status" id="compose-status" role="status" aria-live="polite"></div>
            <div class="compose-actions-right"><button class="ghost" id="compose-cancel" type="button">Cancel</button><button class="primary" id="compose-send" type="submit">Send email</button></div>
          </div>
        </form>
      </section>
    </div>
'''
main_anchor = '  </main>\n\n  <script>'
if 'id="compose-modal"' not in s:
    if main_anchor not in s:
        raise SystemExit('Main anchor not found')
    s = s.replace(main_anchor, '  </main>' + modal + '\n  <script>')

old_clear = "function clearSession(){ token=''; localStorage.removeItem(TOKEN_KEY); loginView.classList.remove('hidden'); adminView.classList.add('hidden'); $('refresh-btn').classList.add('hidden'); $('logout-btn').classList.add('hidden'); }"
new_clear = "function clearSession(){ token=''; localStorage.removeItem(TOKEN_KEY); loginView.classList.remove('hidden'); adminView.classList.add('hidden'); $('compose-btn').classList.add('hidden'); $('refresh-btn').classList.add('hidden'); $('logout-btn').classList.add('hidden'); closeCompose(); }"
if old_clear in s:
    s = s.replace(old_clear, new_clear)

old_show = "function showAdmin(){ loginView.classList.add('hidden'); adminView.classList.remove('hidden'); $('refresh-btn').classList.remove('hidden'); $('logout-btn').classList.remove('hidden'); }"
new_show = "function showAdmin(){ loginView.classList.add('hidden'); adminView.classList.remove('hidden'); $('compose-btn').classList.remove('hidden'); $('refresh-btn').classList.remove('hidden'); $('logout-btn').classList.remove('hidden'); }"
if old_show in s:
    s = s.replace(old_show, new_show)

listener_anchor = "    $('request-code').addEventListener('click',requestCode);"
compose_js = r'''    function openCompose(){
      $('compose-modal').classList.remove('hidden'); document.body.style.overflow='hidden'; setStatus($('compose-status'),''); setTimeout(()=>$('compose-to').focus(),0);
    }
    function closeCompose(){
      const modal=$('compose-modal'); if(modal) modal.classList.add('hidden'); document.body.style.overflow='';
    }
    function fmtBytes(bytes){
      if(bytes<1024)return bytes+' B'; if(bytes<1024*1024)return (bytes/1024).toFixed(1)+' KB'; return (bytes/(1024*1024)).toFixed(1)+' MB';
    }
    function renderAttachments(){
      const files=[...$('compose-files').files]; const list=$('attachment-list'); list.replaceChildren();
      if(!files.length)return;
      files.forEach(file=>{ const row=document.createElement('div'); row.className='attachment-item'; const name=document.createElement('span'); name.textContent=file.name; const size=document.createElement('span'); size.textContent=fmtBytes(file.size); row.append(name,size); list.append(row); });
      const total=files.reduce((n,f)=>n+f.size,0); const totalRow=document.createElement('div'); totalRow.className='attachment-item'; const a=document.createElement('strong'); a.textContent=files.length+' file'+(files.length===1?'':'s'); const b=document.createElement('strong'); b.textContent=fmtBytes(total)+' total'; totalRow.append(a,b); list.append(totalRow);
      setStatus($('compose-status'), total>20*1024*1024?'Attachments exceed the 20 MB limit.':'', total>20*1024*1024?'error':'');
    }
    async function sendCompose(event){
      event.preventDefault(); const btn=$('compose-send'); const files=[...$('compose-files').files]; const total=files.reduce((n,f)=>n+f.size,0);
      if(files.length>10){setStatus($('compose-status'),'You can attach up to 10 files.','error');return;}
      if(total>20*1024*1024){setStatus($('compose-status'),'Attachments must be 20 MB or less in total.','error');return;}
      const form=new FormData(); form.append('to',$('compose-to').value.trim()); form.append('subject',$('compose-subject').value.trim()); form.append('body',$('compose-body').value.trim()); form.append('request_id',crypto.randomUUID()); files.forEach(file=>form.append('attachments',file,file.name));
      btn.disabled=true; setStatus($('compose-status'),'Sending…');
      try{
        const res=await fetch(API+'?action=compose',{method:'POST',headers:{Authorization:'Bearer '+token},body:form}); const data=await res.json().catch(()=>({}));
        if(res.status===401){clearSession();throw new Error('Your admin session has expired. Please log in again.');}
        if(!res.ok)throw new Error(data.error||'Email could not be sent.');
        setStatus($('compose-status'),'Email accepted for delivery.','ok'); $('compose-form').reset(); renderAttachments();
        setTimeout(closeCompose,900);
      }catch(e){setStatus($('compose-status'),e.message,'error');}
      finally{btn.disabled=false;}
    }

'''
if 'async function sendCompose(event)' not in s:
    if listener_anchor not in s:
        raise SystemExit('Listener anchor not found')
    s = s.replace(listener_anchor, compose_js + listener_anchor)

listener_line = "    $('request-code').addEventListener('click',requestCode); $('resend-code').addEventListener('click',requestCode); $('verify-code').addEventListener('click',verifyCode); $('login-code').addEventListener('keydown',e=>{if(e.key==='Enter')verifyCode();}); $('refresh-btn').addEventListener('click',loadInbox); $('logout-btn').addEventListener('click',logout); $('send-reply').addEventListener('click',sendReply); $('archive-btn').addEventListener('click',archiveSelected);"
extra = "\n    $('compose-btn').addEventListener('click',openCompose); $('compose-close').addEventListener('click',closeCompose); $('compose-cancel').addEventListener('click',closeCompose); $('compose-files').addEventListener('change',renderAttachments); $('compose-form').addEventListener('submit',sendCompose); $('compose-modal').addEventListener('click',e=>{if(e.target===$('compose-modal'))closeCompose();}); document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('compose-modal').classList.contains('hidden'))closeCompose();});"
if "$('compose-btn').addEventListener" not in s:
    if listener_line not in s:
        raise SystemExit('Event listener line not found')
    s = s.replace(listener_line, listener_line + extra)

path.write_text(s)
