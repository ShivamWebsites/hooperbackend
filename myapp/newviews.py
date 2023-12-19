# # views.py
# import os
# import tempfile
# import requests
# import json
# from django.conf import settings
# from django.http import HttpResponse
# from django.shortcuts import render
# from django.core.files.storage import FileSystemStorage
# # import ffmpeg

# from .forms import VideoProcessingForm

# def process_video(request):
#     if request.method == 'POST':
#         form = VideoProcessingForm(request.POST, request.FILES)
#         if form.is_valid():
#             tweet_link = form.cleaned_data['tweet_link']
#             video_file = request.FILES['video_file']

#             try:
#                 image_url = fetch_tweet_image(tweet_link)

#                 if image_url:
#                     save_tweet_image(image_url)
#                     final_processed_video_path = process_video_with_overlay(image_url, video_file)

#                     if final_processed_video_path:
#                         return render(request, 'processed_video.html', {'video_url': final_processed_video_path})
#                     else:
#                         return HttpResponse("Video processing failed. Please try again later.")
#                 else:
#                     return HttpResponse("Failed to fetch the tweet image.")
#             except Exception as e:
#                 return HttpResponse(f"An error occurred: {str(e)}")
#     else:
#         form = VideoProcessingForm()

#     return render(request, 'process_video.html', {'form': form})

# def fetch_tweet_image(tweet_url):
#     # Define the API URL
#     url = "https://tweetpik.com/api/v2/images"

#     # Define your API key
#     api_key = "d1d0d488-5d3f-4345-a312-c6b51c80400e"

#     # Create a JSON payload with the user-provided tweet URL and custom options
#     payload = {
#         "url": tweet_url,
#         "textPrimaryColor": "#FFFFFF",
#         "backgroundColor": "#000000",
#         "dimension": "tiktok"
#     }

#     # Define the headers
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": api_key
#     }

#     # Send the POST request to the API
#     response = requests.post(url, data=json.dumps(payload), headers=headers)

#     # Check if the request was successful
#     if response.status_code == 201:
#         # Parse the JSON response to get the image URL
#         response_data = json.loads(response.text)
#         image_url = response_data.get("url")
#         return image_url
#     else:
#         print("Error fetching tweet image:", response.status_code)
#         return None

# def save_tweet_image(image_url):
#     # Download the image
#     image_response = requests.get(image_url)

#     # Check if the image download was successful
#     if image_response.status_code == 200:
#         # Save the image as screenshot.png
#         with open("screenshot.png", "wb") as image_file:
#             image_file.write(image_response.content)
#         print("Screenshot saved as screenshot.png")
#     else:
#         print("Error downloading the image:", image_response.status_code)

# def process_video_with_overlay(image_url, video_file):
#     try:
#         # Download the tweet image
#         response = requests.get(image_url)

#         if response.status_code != 200:
#             print("Error downloading the tweet image:", response.status_code)
#             return None

#         # Save the image as a temporary file
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as image_file:
#             image_file.write(response.content)
#             tweet_image_path = image_file.name

#         # Define the output video path
#         output_video_path = os.path.join(settings.MEDIA_ROOT, 'final_output.mp4')

#         # Use ffmpeg-python for video processing
#         input_video_path = video_file.temporary_file_path() if hasattr(video_file, 'temporary_file_path') else None

#         (
#             ffmpeg
#             .input(input_video_path, vf='scale=640:480')  # Resize video if needed
#             .output(output_video_path, vf='movie=' + tweet_image_path + ' [watermark]; [in][watermark] overlay=W-w-10:H-h-10 [out]')
#             .run(overwrite_output=True)
#         )

#         return output_video_path
#     except Exception as e:
#         print(f"Video processing error: {str(e)}")
#         return None

# def playback_processed_video(request):
#     processed_video_path = os.path.join(settings.MEDIA_ROOT, 'final_output.mp4')

#     if os.path.exists(processed_video_path):
#         with open(processed_video_path, 'rb') as video_file:
#             response = HttpResponse(video_file.read(), content_type='video/mp4')
#         return response
#     else:
#         return HttpResponse("Processed video not found.")
