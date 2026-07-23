#!/usr/bin/env python3
"""Fetch YouTube transcripts — conservative mode with 5s delays."""
import json, os, time
from youtube_transcript_api import YouTubeTranscriptApi

DATA_DIR = '/home/user/class9hub/src/data'
OUT_DIR = '/home/user/class9hub/transcripts'
SUBJECTS = ['physics', 'chemistry', 'biology', 'computer']

os.makedirs(OUT_DIR, exist_ok=True)

def get_video_ids(subject_id):
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

def main():
    total_ok = 0
    total_fail = 0
    total_skip = 0
    
    for subject in SUBJECTS:
        print(f'\n{"="*60}')
        print(f'Processing: {subject.upper()}')
        print(f'{"="*60}')
        
        videos = get_video_ids(subject)
        subject_dir = os.path.join(OUT_DIR, subject)
        os.makedirs(subject_dir, exist_ok=True)
        
        ok = 0
        fail = 0
        skip = 0
        
        for i, vid in enumerate(videos):
            vid_id = vid['videoId']
            out_file = os.path.join(subject_dir, f'{vid_id}.txt')
            
            # Skip if already fetched successfully
            if os.path.exists(out_file):
                with open(out_file) as f:
                    content = f.read()
                if 'ERROR:' not in content and len(content) > 200:
                    skip += 1
                    continue
            
            try:
                ytt_api = YouTubeTranscriptApi()
                transcript = ytt_api.fetch(vid_id, languages=['hi', 'hi-Latn', 'ur', 'en'])
                text = ' '.join([t.text for t in transcript.snippets])
                
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
                
                ok += 1
                print(f'  [{i+1}/{len(videos)}] {vid_id} OK ({len(text)} chars)')
                time.sleep(5)  # 5 second delay
                
            except Exception as e:
                err = type(e).__name__
                fail += 1
                print(f'  [{i+1}/{len(videos)}] {vid_id} FAIL ({err})')
                
                with open(out_file, 'w') as f:
                    f.write(f'Video ID: {vid_id}\n')
                    f.write(f'Title: {vid["title"]}\n')
                    f.write(f'Subject: {subject}\n')
                    f.write(f'---\n')
                    f.write(f'ERROR: {err}\n')
                
                # If blocked, wait longer
                if err == 'IpBlocked':
                    print('  IP blocked — waiting 60s...')
                    time.sleep(60)
                else:
                    time.sleep(5)
        
        total_ok += ok
        total_fail += fail
        total_skip += skip
        print(f'\n{subject}: {ok} new, {skip} cached, {fail} failed')
    
    print(f'\n{"="*60}')
    print(f'TOTAL: {total_ok} new, {total_skip} cached, {total_fail} failed')
    print(f'{"="*60}')

if __name__ == '__main__':
    main()
