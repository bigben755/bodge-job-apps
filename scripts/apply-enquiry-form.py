from pathlib import Path

page = Path('index.html')
html = page.read_text(encoding='utf-8')

old_contact = '''    <section class="contact-section" id="contact">
      <div class="wrap contact-inner">
        <img src="assets/bodge-job-logo.png" alt="" width="120" height="120">
        <div>
          <p class="eyebrow">Get in touch</p>
          <h2>Found something we bodged?</h2>
          <p>
            Bug report, feedback, app idea or just a hello — we’d be happy to hear from you.
          </p>
          <a class="button" href="mailto:support@bodgejobapps.com">Contact Bodge Job Apps</a>
        </div>
      </div>
    </section>'''

new_contact = '''    <section class="contact-section" id="contact">
      <div class="wrap contact-inner contact-form-layout">
        <div class="contact-intro">
          <img src="assets/bodge-job-logo.png" alt="" width="120" height="120">
          <div>
            <p class="eyebrow">Get in touch</p>
            <h2>Found something we bodged?</h2>
            <p>Bug report, feedback, app idea or just a hello — send it straight to the workbench.</p>
            <p class="contact-fallback">Prefer email? <a href="mailto:hello@bodge-job.com">hello@bodge-job.com</a></p>
          </div>
        </div>

        <form class="enquiry-form" id="enquiry-form">
          <div class="form-grid">
            <label>
              <span>Your name</span>
              <input type="text" name="name" autocomplete="name" maxlength="120" required>
            </label>
            <label>
              <span>Email address</span>
              <input type="email" name="email" autocomplete="email" maxlength="254" required>
            </label>
          </div>
          <label>
            <span>What’s this about?</span>
            <select name="topic" required>
              <option value="Bug report">Bug report</option>
              <option value="Feedback">Feedback</option>
              <option value="App idea">App idea</option>
              <option value="Business enquiry">Business enquiry</option>
              <option value="General enquiry">General enquiry</option>
            </select>
          </label>
          <label>
            <span>Message</span>
            <textarea name="message" rows="6" maxlength="5000" placeholder="Tell us what happened, what you’re thinking, or what you’d like to know…" required></textarea>
          </label>
          <label class="hp-field" aria-hidden="true">
            <span>Website</span>
            <input type="text" name="website" tabindex="-1" autocomplete="off">
          </label>
          <div class="enquiry-actions">
            <button class="button" id="enquiry-submit" type="submit">Send message</button>
            <p class="form-status" id="enquiry-status" role="status" aria-live="polite"></p>
          </div>
          <p class="form-note">Your details are used only to read and respond to your enquiry.</p>
        </form>
      </div>
    </section>'''

if old_contact not in html:
    raise SystemExit('Expected contact section was not found.')
html = html.replace(old_contact, new_contact, 1)

old_legal = '''          <a href="findsy/privacy-policy/">Findsy Privacy Policy</a>
          <a href="just-three-words/privacy-policy/">Just Three Words Privacy Policy</a>'''
new_legal = '''          <a href="findsy/privacy-policy/">Findsy Privacy Policy</a>
          <a href="just-three-words/privacy-policy/">Just Three Words Privacy Policy</a>
          <a href="admin.html">Admin</a>'''
if old_legal not in html:
    raise SystemExit('Expected footer legal links were not found.')
html = html.replace(old_legal, new_legal, 1)

css = '''
    .contact-form-layout {
      display:grid;
      grid-template-columns:minmax(0,.78fr) minmax(420px,1.22fr);
      gap:clamp(30px,6vw,76px);
      align-items:start;
    }
    .contact-intro { display:grid; gap:22px; align-items:start; }
    .contact-intro > img { border-radius:50%; }
    .contact-fallback { margin-top:18px; color:var(--muted); font-size:.92rem; }
    .contact-fallback a { color:var(--lime); }
    .enquiry-form {
      display:grid;
      gap:17px;
      padding:clamp(24px,4vw,38px);
      border:1px solid var(--line);
      border-radius:28px;
      background:linear-gradient(145deg,rgba(255,255,255,.055),rgba(255,255,255,.018));
      box-shadow:0 22px 65px rgba(0,0,0,.18);
    }
    .form-grid { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
    .enquiry-form label { display:grid; gap:7px; }
    .enquiry-form label > span { font-size:.78rem; font-weight:900; letter-spacing:.02em; }
    .enquiry-form input,
    .enquiry-form select,
    .enquiry-form textarea {
      width:100%;
      border:1px solid rgba(255,255,255,.13);
      border-radius:14px;
      background:rgba(8,8,11,.74);
      color:var(--text);
      padding:13px 14px;
      outline:none;
      font:inherit;
      transition:border-color .18s ease, box-shadow .18s ease;
    }
    .enquiry-form select { min-height:49px; }
    .enquiry-form textarea { resize:vertical; min-height:145px; }
    .enquiry-form input:focus,
    .enquiry-form select:focus,
    .enquiry-form textarea:focus { border-color:var(--purple); box-shadow:0 0 0 4px rgba(159,77,255,.12); }
    .enquiry-actions { display:flex; align-items:center; gap:16px; flex-wrap:wrap; }
    .form-status { margin:0; min-height:22px; color:var(--muted); font-size:.88rem; font-weight:700; }
    .form-status.ok { color:var(--lime); }
    .form-status.error { color:#ff9191; }
    .form-note { margin:0; color:var(--muted); font-size:.76rem; }
    .hp-field { position:absolute !important; left:-10000px !important; width:1px !important; height:1px !important; overflow:hidden !important; }
    @media (max-width:860px) {
      .contact-form-layout { grid-template-columns:1fr; }
      .contact-intro { grid-template-columns:auto 1fr; }
    }
    @media (max-width:620px) {
      .form-grid { grid-template-columns:1fr; }
      .contact-intro { grid-template-columns:1fr; }
      .contact-intro > img { width:86px; height:86px; }
    }
'''
html = html.replace('  </style>', css + '\n  </style>', 1)

script = '''
  <script>
    (() => {
      const form = document.getElementById('enquiry-form');
      if (!form) return;
      const endpoint = 'https://aovgfefhybcptxdauyqy.supabase.co/functions/v1/submit-enquiry';
      const status = document.getElementById('enquiry-status');
      const button = document.getElementById('enquiry-submit');

      function setStatus(message, kind = '') {
        status.textContent = message;
        status.className = 'form-status' + (kind ? ' ' + kind : '');
      }

      form.addEventListener('submit', async (event) => {
        event.preventDefault();
        button.disabled = true;
        button.textContent = 'Sending…';
        setStatus('Sending your message…');

        const data = Object.fromEntries(new FormData(form).entries());
        try {
          const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
          });
          const result = await response.json().catch(() => ({}));
          if (!response.ok) throw new Error(result.error || 'Your message could not be sent.');
          form.reset();
          setStatus(result.message || 'Thanks — your message has landed safely.', 'ok');
        } catch (error) {
          setStatus((error && error.message) || 'Something went wrong. Please try again.', 'error');
        } finally {
          button.disabled = false;
          button.textContent = 'Send message';
        }
      });
    })();
  </script>
'''
html = html.replace('</body>', script + '\n</body>', 1)

page.write_text(html, encoding='utf-8')
print('Bodge Job enquiry form and Admin footer link applied.')
