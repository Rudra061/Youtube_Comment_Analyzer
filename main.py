import os
from dotenv import load_dotenv, find_dotenv
from comment import YouTubeCommentsReader, CommentCSVWriter, Video_url
from textblob import TextBlob
import matplotlib.pyplot as plt


def analyze_sentiment(comment):
    analysis = TextBlob(comment)
    polarity = analysis.sentiment.polarity
    # Classify the polarity of the comment
    if polarity > 0.1:
        return 'Positive'
    elif -0.1 <= polarity <= 0.1:
        return 'Neutral'
    else:
        return 'Negative'


if __name__ == "__main__":
    # Reading the API_KEY
    load_dotenv(find_dotenv())
    api_key = os.getenv("YOUTUBE_API_KEY")

    # Enter the YouTube video link
    input_url = Video_url(str(input("Enter Video Url : ")))

    video_id = input_url.extract_video_id()
    print(video_id)

    # Create an instance of YouTubeCommentsReader
    youtube_comments_reader = YouTubeCommentsReader(api_key)

    # Get the comments for the specified video
    video_comments = youtube_comments_reader.get_video_comments(video_id)
    print(len(video_comments))

    # writing the comments into a csv file
    csv_writer = CommentCSVWriter()
    csv_writer.write_to_csv(video_comments)

    print("Comments fetched, starting analysis")

    sentiment_counts = {'Positive': 0, 'Neutral': 0, 'Negative': 0}

    # Analyze the sentiment for each comment
    for comment in video_comments:
        sentiment = analyze_sentiment(comment)
        sentiment_counts[sentiment] += 1
        # print(f"Comment: {comment} \nSentiment: {sentiment}\n")

    # Draw a pie chart
    labels = sentiment_counts.keys()
    sizes = sentiment_counts.values()

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'lightblue', 'lightcoral'])
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

    plt.title('Sentiment Distribution')
    plt.show()
