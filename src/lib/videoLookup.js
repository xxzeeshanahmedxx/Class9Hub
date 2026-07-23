import { subjects, getData } from './data';
import { videoSlug } from './slugify';

export function buildVideoIndex() {
  const index = [];
  for (const s of subjects) {
    const data = getData(s.id);
    const chapters = data.chapters || [];
    for (const ch of chapters) {
      const chNum = ch.number || ch.chapterNumber || '';
      // Chapters with direct videos
      if (ch.videos) {
        for (const v of ch.videos) {
          const slug = videoSlug(s.id, chNum, v.title);
          index.push({
            slug,
            videoId: v.videoId,
            title: v.title,
            subtitle: v.subtitle || '',
            duration: v.duration || '',
            subjectId: s.id,
            subjectTitle: s.title,
            accent: s.accent,
            chapterId: ch.id,
            chapterNumber: chNum,
            chapterTitle: ch.title || '',
            sectionId: null,
            sectionTitle: null,
            url: `/watch/${slug}/`,
          });
        }
      }
      // Chapters with sections (exercises)
      if (ch.sections) {
        for (const sec of ch.sections) {
          for (const v of sec.videos || []) {
            const slug = videoSlug(s.id, chNum, v.title);
            index.push({
              slug,
              videoId: v.videoId,
              title: v.title,
              subtitle: v.subtitle || '',
              duration: v.duration || '',
              subjectId: s.id,
              subjectTitle: s.title,
              accent: s.accent,
              chapterId: ch.id,
              chapterNumber: chNum,
              chapterTitle: ch.title || '',
              sectionId: sec.id,
              sectionTitle: sec.title || '',
              url: `/watch/${slug}/`,
            });
          }
        }
      }
    }
  }
  return index;
}

export function findVideoBySlug(slug) {
  const index = buildVideoIndex();
  return index.find(v => v.slug === slug) || null;
}
