# main.py

from utils import reddit_utils, text_utils, video_utils

def main():
    redditObj = reddit_utils.reddit_obj()
    subred = redditObj.subreddit("amitheasshole")
    top = subred.top(time_filter="day", limit=2)
    # background = video_utils.create_background("background/bg2.jpg")

    for i in top:
        titl = i.title
        desc = i.selftext
        break

    # text_utils.process_text(desc)
    video_utils.create_video(titl, desc, 'background/small_video_clip.mp4')

if __name__ == "__main__":
    main()
