const PDFDocument = require('pdfkit');
const fs = require('fs');

const mdFile = process.argv[2];
const outputFile = process.argv[3];

if (!mdFile || !outputFile) {
  console.error('Usage: node generate-pdf.js <input.md> <output.pdf>');
  process.exit(1);
}

const content = fs.readFileSync(mdFile, 'utf8');
const doc = new PDFDocument({
  size: 'A4',
  margins: { top: 25, bottom: 25, left: 25, right: 25 }
});

const stream = fs.createWriteStream(outputFile);
doc.pipe(stream);

const lines = content.split('\n');
let inTable = false;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];

  if (line.startsWith('```')) continue;
  if (line.startsWith('|') && line.endsWith('|')) {
    if (!inTable && i > 0 && lines[i-1].trim() === '') continue;
    if (line.includes('---') && line.includes('|')) continue;
    const cells = line.split('|').filter(c => c.trim()).map(c => c.trim());
    doc.fontSize(10).font('Helvetica');
    doc.text(cells.join('  |  '), { indent: 10 });
    doc.moveDown(0.15);
    inTable = true;
    continue;
  }
  inTable = false;

  if (line.trim() === '') { doc.moveDown(0.3); continue; }

  if (line.startsWith('# ')) {
    doc.fontSize(20).font('Helvetica-Bold');
    doc.text(line.slice(2), { underline: true });
    doc.moveDown(0.5);
  } else if (line.startsWith('## ')) {
    doc.fontSize(15).font('Helvetica-Bold');
    doc.text(line.slice(3));
    doc.moveDown(0.3);
  } else if (line.startsWith('---')) {
    doc.moveDown(0.3);
    doc.fontSize(10).text('─'.repeat(70));
    doc.moveDown(0.3);
  } else if (line.startsWith('- ')) {
    doc.fontSize(11).font('Helvetica');
    const text = line.slice(2);
    const boldMatch = text.match(/^\*\*(.+?)\*\*(.*)/);
    if (boldMatch) {
      doc.text('• ', { continued: true });
      doc.font('Helvetica-Bold').text(boldMatch[1] + ' ', { continued: true });
      doc.font('Helvetica').text(boldMatch[2]);
    } else {
      doc.text('• ' + text);
    }
    doc.moveDown(0.1);
  } else if (/^\d+[\.\)] /.test(line)) {
    doc.fontSize(11).font('Helvetica');
    const boldMatch = line.match(/^\d+[\.\)] (.+)$/);
    if (boldMatch) {
      const text = boldMatch[1];
      const qMatch = text.match(/^\*\*(.+?)\*\*(.*)/);
      if (qMatch) {
        doc.font('Helvetica-Bold').text(qMatch[1] + ' ', { continued: true });
        doc.font('Helvetica').text(qMatch[2]);
      } else {
        doc.text(line);
      }
    } else {
      doc.text(line);
    }
    doc.moveDown(0.1);
  } else if (line.startsWith('**Answer:')) {
    doc.fontSize(11).font('Helvetica');
    doc.text(line.replace(/\*\*/g, ''));
    doc.moveDown(0.1);
  } else if (line.startsWith('**Ans:**')) {
    doc.fontSize(11).font('Helvetica');
    doc.text(line.replace(/\*\*/g, ''));
    doc.moveDown(0.1);
  } else if (line.startsWith('**')) {
    doc.fontSize(11).font('Helvetica-Bold');
    doc.text(line.replace(/\*\*/g, ''));
    doc.moveDown(0.1);
  } else {
    doc.fontSize(11).font('Helvetica');
    doc.text(line);
    doc.moveDown(0.1);
  }

  if (doc.y > doc.page.height - 40) doc.addPage();
}

doc.end();
stream.on('finish', () => console.log('PDF:', outputFile));
