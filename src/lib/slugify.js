export function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-+|-+$/g, '')
    .trim();
}

export function videoSlug(subjectId, chapterNumber, title) {
  const ch = `ch${chapterNumber}`;
  const name = slugify(title).slice(0, 60).replace(/-+$/g, '');
  return `${subjectId}-${ch}-${name}`;
}
