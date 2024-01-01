import csv
import re
from googleapiclient.discovery import build


class YouTubeCommentsReader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def get_video_comments(self, video_id, max_comments=1000):
        request = self.youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText"
        )

        response = request.execute()

        comments = []
        next_page_token = None

        while len(comments) < max_comments:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100,  # Adjust maxResults as needed (max is 100)
                pageToken=next_page_token
            )

            response = request.execute()

            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)

            next_page_token = response.get("nextPageToken")

            if not next_page_token or len(comments) >= max_comments:
                break  # No more pages

        return comments[:max_comments]


class CommentCSVWriter:

    def __init__(self, csv_file_name="comments.csv"):
        self.csv_file_name = csv_file_name

    def write_to_csv(self, data):
        with open(self.csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            for comment in data:
                csv_writer.writerow([comment])


class Video_url:

    def __init__(self, url):
        self.url = url

    def extract_video_id(self):
        """
            Extracts the video ID from a YouTube URL using regular expressions.
        """
        video_id = re.search(r'(?<=v=)[^&#]+', self.url)
        video_id = video_id or re.search(r'(?<=be/)[^&#]+', self.url)

        return video_id.group(0) if video_id else None
