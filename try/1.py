import csv
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# YouTube API 키
API_KEY = os.getenv('YOUTUBE_API_KEY')

# YouTube API 클라이언트 생성
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_playlist_videos(plyylink):
    video_link = []

    # plyylist에서 ID추출
    plyy_id = plyylink.split('list=')[1].split('&')[0]

    # playlistItems 메서드를 호출해 재생목록에 있는 비디오 ID 추출
    playlist_items = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=plyy_id,
        maxResults=50  # 재생목록의 최대 비디오 개수 (기본 50, 최대 50)
    ).execute()
    
    # videoid를 통해 video 링크 생성
    for item in playlist_items['items']:
        video_id = item['contentDetails']['videoId']
        video_link.append(f'https://www.youtube.com/watch?v={video_id}')
    
    return video_link

def song(plyy_link,csv_file,result_csv_file):
    song_info = []
    song_vids = get_playlist_videos(plyy_link)
    count = 0
    with open(csv_file, 'r', encoding='utf-8', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            song_info.append({
                'song_uuid': row[0],
                'song_cmt':row[1],
                'song_vid':str(song_vids[count]),
                'song_index':count,
                'plyy_id':row[2],
                'src_id':row[3]
            })
            count += 1
            
    # 파일이 존재하지 않는 경우 헤더 추가
    if not os.path.isfile(result_csv_file):
        with open(result_csv_file, 'w', encoding='utf-8', newline='') as file:
            fwriter = csv.writer(file)
            header = ['song_uuid',
                'song_cmt',
                'song_vid',
                'song_index',
                'plyy_id',
                'src_id']
            fwriter.writerow(header)

    with open(result_csv_file, 'a', encoding='utf-8', newline='') as file:
        fwriter = csv.writer(file)
        for song in song_info:
            fwriter.writerow([song['song_uuid'],song['song_cmt'],song['song_vid'],song['song_index'],song['plyy_id'],song['src_id']])

    return song_info



# 예시 사용법

playlist_link = ['https://youtube.com/playlist?list=PLi5p5mTdWhrg1KSjpUUapLBP32quyvP3k&feature=shared',
                'https://youtube.com/playlist?list=PLi5p5mTdWhrhGf-bgu3fYJrM2r1lWCU76&feature=shared'
                ]
file_names = ['mh_song.csv','sm-SONG.csv']
song_info = []
for i in range(len(playlist_link)) :
    song(playlist_link[i],file_names[i],'song.csv')

# print(song_info)
# 재생목록에서 비디오 정보 가져오기
# vidlink = get_playlist_videos(playlist_link)
