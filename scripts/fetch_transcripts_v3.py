#!/usr/bin/env python3
"""Fetch all remaining transcripts — conservative 8s delays, auto-retry on block."""
import json, os, time, sys
from youtube_transcript_api import YouTubeTranscriptApi

DATA_DIR = '/home/user/class9hub/src/data'
OUT_DIR = '/home/user/class9hub/transcripts'
# Smaller subjects first to maximize coverage before any block
SUBJECTS = ['computer', 'chemistry', 'biology', 'physics']
DELAY = 8
BLOCK_WAIT = 180  # 3 min if blocked (usually lifts in 10-15 min)

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

def is_cached(out_file):
    if not os.path.exists(out_file):
        return False
    with open(out_file) as f:
        content = f.read()
    return 'ERROR:' not in content and len(content) > 200

def main():
    total_new = 0
    total_cached = 0
    total_fail = 0
    start_time = time.time()
    
    for subject in SUBJECTS:
        print(f'\n{"="*60}', flush=True)
        print(f'{subject.upper()} — starting', flush=True)
        print(f'{"="*60}', flush=True)
        
        videos = get_video_ids(subject)
        subject_dir = os.path.join(OUT_DIR, subject)
        os.makedirs(subject_dir, exist_ok=True)
        
        new = cached = fails = 0
        consecutive_blocks = 0
        
        for i, vid in enumerate(videos):
            vid_id = vid['videoId']
            out_file = os.path.join(subject_dir, f'{vid_id}.txt')
            
            if is_cached(out_file):
                cached += 1
                continue
            
            # If we hit 3 blocks in a row, stop this subject
            if consecutive_blocks >= 3:
                print(f'  3 consecutive blocks — skipping remaining {len(videos)-i} videos', flush=True)
                fails += len(videos) - i
                break
            
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
                
                new += 1
                total_new += 1
                consecutive_blocks = 0
                elapsed = int(time.time() - start_time)
                print(f'  [{i+1}/{len(videos)}] {vid_id} OK ({len(text)} chars) | total new: {total_new} | {elapsed//60}m elapsed', flush=True)
                time.sleep(DELAY)
                
            except Exception as e:
                err = type(e).__name__
                
                with open(out_file, 'w') as f:
                    f.write(f'Video ID: {vid_id}\n')
                    f.write(f'Title: {vid["title"]}\n')
                    f.write(f'Subject: {subject}\n')
                    f.write(f'---\n')
                    f.write(f'ERROR: {err}\n')
                
                if err == 'IpBlocked':
                    consecutive_blocks += 1
                    fails += 1
                    total_fail += 1
                    print(f'  [{i+1}/{len(videos)}] {vid_id} BLOCKED — waiting {BLOCK_WAIT}s (strike {consecutive_blocks}/3)', flush=True)
                    time.sleep(BLOCK_WAIT)
                elif err == 'NoTranscriptFound':
                    fails += 1
                    total_fail += 1
                    print(f'  [{i+1}/{len(videos)}] {vid_id} NO TRANSCRIPT', flush=True)
                    time.sleep(2)
                else:
                    fails += 1
                    total_fail += 1
                    print(f'  [{i+1}/{len(videos)}] {vid_id} ERROR: {err}', flush=True)
                    time.sleep(DELAY)
        
        total_cached += cached
        print(f'\n{subject}: +{new} new, {cached} cached, {fails} failed', flush=True)
    
    elapsed = int(time.time() - start_time)
    print(f'\n{"="*60}', flush=True)
    print(f'DONE in {elapsed//60}m: {total_new} new + {total_cached} cached + {total_fail} failed = {total_new+total_cached+total_fail} total', flush=True)
    print(f'{"="*60}', flush=True)

if __name__ == '__main__':
    main()
