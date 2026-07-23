#!/usr/bin/env python3
"""Fetch YouTube transcripts for all subject videos."""
import json, os, time, sys
from youtube_transcript_api import YouTubeTranscriptApi

DATA_DIR = '/home/user/class9hub/src/data'
OUT_DIR = '/home/user/class9hub/transcripts'
SUBJECTS = ['physics', 'chemistry', 'biology', 'computer']

os.makedirs(OUT_DIR, exist_ok=True)

def get_video_ids(subject_id):
    """Extract all video IDs from subject JSON."""
    with open(f'{DATA_DIR}/{subject_id}.json') as f:
        data = json.load(f)
    
    videos = []
    for ch in data['chapters']:
        if 'sections' in ch:
            for sec in ch['sections']:
                for v in sec.get('videos', []):
                    videos.append({
                        'videoId': v['videoId'],
                        'title': v.get('title', ''),
                        'subtitle': v.get('subtitle', ''),
                        'duration': v.get('duration', ''),
                        'chapter': ch.get('title', ''),
                        'chapterId': ch.get('id', ''),
                        'section': sec.get('title', ''),
                        'sectionId': sec.get('id', ''),
                    })
        elif 'videos' in ch:
            for v in ch['videos']:
                videos.append({
                    'videoId': v['videoId'],
                    'title': v.get('title', ''),
                    'subtitle': v.get('subtitle', ''),
                    'duration': v.get('duration', ''),
                    'chapter': ch.get('title', ''),
                    'chapterId': ch.get('id', ''),
                    'section': '',
                    'sectionId': '',
                })
    return videos

def fetch_transcript(video_id):
    """Fetch transcript for a single video."""
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id, languages=['hi', 'hi-Latn', 'ur', 'en'])
    text = ' '.join([t.text for t in transcript.snippets])
    return text

def main():
    total_success = 0
    total_fail = 0
    all_results = {}
    
    for subject in SUBJECTS:
        print(f'\n{"="*60}')
        print(f'Processing: {subject.upper()}')
        print(f'{"="*60}')
        
        videos = get_video_ids(subject)
        subject_dir = os.path.join(OUT_DIR, subject)
        os.makedirs(subject_dir, exist_ok=True)
        
        success = 0
        fail = 0
        
        for i, vid in enumerate(videos):
            vid_id = vid['videoId']
            out_file = os.path.join(subject_dir, f'{vid_id}.txt')
            
            # Skip if already fetched
            if os.path.exists(out_file) and os.path.getsize(out_file) > 100:
                success += 1
                print(f'  [{i+1}/{len(videos)}] {vid_id} - CACHED')
                continue
            
            try:
                text = fetch_transcript(vid_id)
                
                # Save transcript with metadata header
                with open(out_file, 'w') as f:
                    f.write(f'Video ID: {vid_id}\n')
                    f.write(f'Title: {vid["title"]}\n')
                    f.write(f'Subtitle: {vid["subtitle"]}\n')
                    f.write(f'Chapter: {vid["chapter"]}\n')
                    f.write(f'Section: {vid["section"]}\n')
                    f.write(f'Duration: {vid["duration"]}\n')
                    f.write(f'Subject: {subject}\n')
                    f.write(f'---\n')
                    f.write(text)
                
                success += 1
                print(f'  [{i+1}/{len(videos)}] {vid_id} - OK ({len(text)} chars)')
                
                # Small delay to avoid rate limiting
                time.sleep(0.3)
                
            except Exception as e:
                fail += 1
                err_type = type(e).__name__
                print(f'  [{i+1}/{len(videos)}] {vid_id} - FAILED ({err_type})')
                
                # Save error marker
                with open(out_file, 'w') as f:
                    f.write(f'Video ID: {vid_id}\n')
                    f.write(f'Title: {vid["title"]}\n')
                    f.write(f'Subject: {subject}\n')
                    f.write(f'---\n')
                    f.write(f'ERROR: {err_type}\n')
                
                time.sleep(0.5)
        
        total_success += success
        total_fail += fail
        print(f'\n{subject}: {success} OK, {fail} failed out of {len(videos)}')
        
        # Save manifest
        manifest = {
            'subject': subject,
            'total': len(videos),
            'success': success,
            'fail': fail,
            'videos': videos,
        }
        with open(os.path.join(subject_dir, '_manifest.json'), 'w') as f:
            json.dump(manifest, f, indent=2)
    
    print(f'\n{"="*60}')
    print(f'TOTAL: {total_success} OK, {total_fail} failed out of {total_success + total_fail}')
    print(f'{"="*60}')

if __name__ == '__main__':
    main()
