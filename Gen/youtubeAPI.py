from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Youtube API 키 설정
API_KEY = ''


def youtube_url(search_query):
    # YouTube Data API 클라이언트 빌드
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    try:
        # YouTube에서 비디오 검색
        search_response = youtube.search().list(
            q=search_query,
            part='id',
            type='video'
        ).execute()

        # 첫 번째 비디오 ID 가져오기
        video_id = search_response['items'][0]['id']['videoId']

        # 비디오 링크 생성
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        return video_url

    except HttpError as e:
        print('YouTube API 호출 오류 발생:', e)

    except IndexError:
        video_id = ''