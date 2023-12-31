import os
from dotenv import load_dotenv, find_dotenv
import csv
from comment import YouTubeCommentsReader

if __name__ == "__main__":
    # Reading the API_KEY
    load_dotenv(find_dotenv())
    api_key = os.getenv("YOUTUBE_API_KEY")
    print(api_key)
    # Replace 'YOUR_VIDEO_ID' with the actual video ID you want to retrieve comments for

    video_id = "YmwskGLycHo"

    # Create an instance of YouTubeCommentsReader
    youtube_comments_reader = YouTubeCommentsReader(api_key)

    # Get and print the comments for the specified video
    video_comments = youtube_comments_reader.get_video_comments(video_id)

    csv_file_name = "comments.csv"

    # Write the data to the CSV file
    with open(csv_file_name, mode='w', newline='',  encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write each row of the data list to the CSV file
        for comment in video_comments:
            csv_writer.writerow([comment])

    print(f"Data has been written to {csv_file_name}.")
