(() => {
  const $ = (id) => document.getElementById(id);
  const text = $('research-text');
  const humanInput = $('humanize-input');
  const notice = $('notice');
  const levels = {
    1: 'تصحيح لغوي خفيف: علامات الترقيم والأخطاء الواضحة.',
    2: 'تحسين محدود: وضوح أفضل وانتقالات أنعم.',
    3: 'إعادة تنظيم معتدلة: ترابط وصياغة أكاديمية.',
    4: 'إعادة صياغة واسعة: بنية وأساليب أكثر نضجًا.',
    5: 'تحرير عميق: تغيير أكبر في الأسلوب مع ثبات الحقائق والمراجع.'
  };
  let selectedLevel = 3;
  const showNotice = (message, error = false) => { notice.textContent = message; notice.className = `notice ${error ? 'error' : ''}`; };
  const words = value => value.trim() ? value.trim().split(/\s+/).length : 0;
  $('word-count').textContent = '0 كلمة';
  text.addEventListener('input', () => { $('word-count').textContent = `${words(text.value)} كلمة`; });
  $('clear-text').addEventListener('click', () => { text.value = ''; $('word-count').textContent = '0 كلمة'; });
  document.querySelectorAll('.tab').forEach(tab => tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(item => item.classList.toggle('active', item === tab));
    const upload = tab.dataset.tab === 'upload'; $('paste-box').classList.toggle('hidden', upload); $('upload-box').classList.toggle('hidden', !upload);
  }));
  $('upload-box').addEventListener('click', event => { if (event.target !== $('file-input')) $('file-input').click(); });
  $('file-input').addEventListener('change', async event => {
    const file = event.target.files[0]; if (!file) return; $('file-name').textContent = file.name;
    if (/\.(txt|md|html?)$/i.test(file.name)) { text.value = await file.text(); $('word-count').textContent = `${words(text.value)} كلمة`; document.querySelector('[data-tab="paste"]').click(); }
    else showNotice('تم اختيار الملف. تحليل PDF وDOCX يحتاج ربط محرك الخادم لاستخراج النص.', true);
  });
  $('scan-btn').addEventListener('click', () => {
    const content = text.value.trim(); if (content.length < 40) return showNotice('أدخل 40 حرفًا على الأقل لإجراء قراءة أولية.', true);
    const sentenceCount = Math.max(1, content.split(/[.!؟؛\n]+/).filter(Boolean).length); const tokens = content.toLowerCase().split(/\s+/).filter(Boolean);
    const unique = new Set(tokens).size; const repetition = Math.round((1 - unique / Math.max(tokens.length, 1)) * 100);
    const ai = Math.min(92, Math.max(4, Math.round(12 + (sentenceCount > 2 && Math.abs(tokens.length / sentenceCount - 18) < 5 ? 14 : 3) + Math.min(10, repetition))));
    const similarity = Math.min(98, Math.max(0, Math.round(repetition * .65)));
    $('ai-score').innerHTML = `${ai}<em>%</em>`; $('similarity-score').innerHTML = `${similarity}<em>%</em>`; $('ai-bar').style.width = `${ai}%`; $('similarity-bar').style.width = `${similarity}%`; $('scan-status').textContent = 'اكتمل الفحص الأولي'; showNotice('اكتمل الفحص الأولي. استخدم المؤشرات للمراجعة البشرية ولا تعتبرها حكمًا نهائيًا.');
  });
  document.querySelectorAll('[data-level]').forEach(button => button.addEventListener('click', () => { selectedLevel = Number(button.dataset.level); document.querySelectorAll('[data-level]').forEach(item => item.classList.toggle('selected', item === button)); $('level-value').textContent = selectedLevel; $('level-description').textContent = levels[selectedLevel]; }));
  $('humanize-btn').addEventListener('click', () => {
    const value = humanInput.value.trim(); if (value.length < 40) return showNotice('أدخل 40 حرفًا على الأقل لتحسين النص.', true);
    let output = value.replace(/\s+/g, ' ').trim();
    if (selectedLevel >= 2) output = output.replace(/،/g, '، ' ).replace(/\s+/g, ' ');
    if (selectedLevel >= 3) output = output.replace(/\bمن خلال\b/g, 'عبر').replace(/\bبهدف\b/g, 'من أجل');
    if (selectedLevel >= 4) output = output.replace(/\bوفي هذا السياق\b/g, 'وفي هذا الإطار').replace(/\bيهدف البحث إلى\b/g, 'يسعى هذا البحث إلى');
    if (selectedLevel >= 5) output = output.replace(/\bبشكل كبير\b/g, 'على نحو ملحوظ').replace(/\bكما أن\b/g, 'إضافة إلى ذلك، فإن');
    $('result-text').textContent = output; $('humanize-result').classList.remove('hidden'); showNotice('تم تحسين الصياغة محليًا. راجع النص وأفصح عن استخدام أدوات المساعدة حسب سياسة مؤسستك.');
  });
  $('copy-result').addEventListener('click', async () => { await navigator.clipboard?.writeText($('result-text').textContent); $('copy-result').textContent = 'تم النسخ'; setTimeout(() => $('copy-result').textContent = 'نسخ النص', 1500); });
})();
