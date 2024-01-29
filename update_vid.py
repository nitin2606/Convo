import requests
import os
import question
import json


def download_video(url, local_filename):
    response = requests.get(url, stream=True)
    with open(local_filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

def sync_video(video_urls):

    print("Video Sync in Progress....")
    print()

    for key in video_urls:

        video_url = video_urls[key]
        video_title = str(key)+".mp4"
        local_path = os.path.join("static", video_title)

        download_video(video_url, local_path)

    

    temp_dict = question.video_urls
  

    for key in video_urls:

        temp_dict[key] = "static/"+str(key)+".mp4"
    
    with open('video_urls.json', 'w') as file:
        json.dump(temp_dict, file)
    
 
    print('Video Sync Completed.')
    print()







