from googleapiclient.discovery import build


class YouTubeCommentsReader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def get_video_comments(self, video_id):
        request = self.youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText"
        )

        response = request.execute()

        comments = []
        next_page_token = None

        while True:
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

            if not next_page_token:
                break  # No more pages

        return comments
