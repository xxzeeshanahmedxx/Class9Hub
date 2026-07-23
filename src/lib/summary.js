export function mdToHtml(md) {
  if (!md) return '';
  let html = '';
  const lines = md.split('\n');
  let inList = false;

  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];

    // Skip template variable lines like {info['...']}
    if (line.includes("{info['") || line.trim() === '---' || line.trim() === '* * *') continue;

    // Headings
    if (line.startsWith('## ')) {
      if (inList) { html += '</ul>'; inList = false; }
      html += `<h2 class="text-[17px] sm:text-[18px] font-bold mt-6 mb-3" style="color: var(--text-primary);">${escapeHtml(line.replace('## ', ''))}</h2>`;
      continue;
    }
    if (line.startsWith('# ')) {
      if (inList) { html += '</ul>'; inList = false; }
      html += `<h2 class="text-[20px] sm:text-[22px] font-extrabold mt-6 mb-3" style="color: var(--text-primary);">${escapeHtml(line.replace('# ', ''))}</h2>`;
      continue;
    }

    // Horizontal rule
    if (line.match(/^[-*_]{3,}$/)) {
      if (inList) { html += '</ul>'; inList = false; }
      html += '<hr class="my-6" style="border-color: var(--border);" />';
      continue;
    }

    // Bullet list items
    if (line.match(/^[-*]\s/)) {
      if (!inList) { html += '<ul class="space-y-2 my-3">'; inList = true; }
      html += `<li class="text-[14px] sm:text-[15px] leading-relaxed flex items-start gap-2" style="color: var(--text-secondary);"><span class="mt-1.5 w-1.5 h-1.5 rounded-full flex-shrink-0" style="background: var(--accent); opacity: 0.5;"></span><span>${formatInline(line.replace(/^[-*]\s/, ''))}</span></li>`;
      continue;
    }

    // Numbered list items
    if (line.match(/^\d+[.)]\s/)) {
      if (!inList) { html += '<ol class="space-y-2 my-3 list-decimal list-inside">'; inList = true; }
      html += `<li class="text-[14px] sm:text-[15px] leading-relaxed" style="color: var(--text-secondary);">${formatInline(line.replace(/^\d+[.)]\s/, ''))}</li>`;
      continue;
    }

    // Empty line
    if (line.trim() === '') {
      if (inList) { html += '</ul>'; inList = false; }
      continue;
    }

    // Regular paragraph
    if (inList) { html += '</ul>'; inList = false; }
    html += `<p class="text-[14px] sm:text-[15px] leading-relaxed mb-3" style="color: var(--text-secondary);">${formatInline(line)}</p>`;
  }

  if (inList) html += '</ul>';
  return html;
}

function escapeHtml(text) {
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function formatInline(text) {
  text = escapeHtml(text);
  // Bold
  text = text.replace(/\*\*(.+?)\*\*/g, '<strong class="font-semibold" style="color: var(--text-primary);">$1</strong>');
  // Italic
  text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
  // Inline code
  text = text.replace(/`(.+?)`/g, '<code class="font-mono text-[13px] px-1 py-0.5 rounded" style="background: var(--accent)10; color: var(--accent);">$1</code>');
  return text;
}
