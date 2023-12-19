from django.shortcuts import render, HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseRedirect
from django.urls import reverse
# views.py
import cv2
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from moviepy.editor import VideoFileClip, AudioFileClip
import requests
import json
import tempfile
import os
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .forms import VideoProcessingForm
from django.templatetags.static import static


from django.shortcuts import render, HttpResponse
from .forms import VideoProcessingForm

processed_video_url = settings.MEDIA_URL + 'processed_video.mp4'

def process_video(request):
    if request.method == 'POST':
        form = VideoProcessingForm(request.POST, request.FILES)
        if form.is_valid():
            tweet_link = form.cleaned_data['tweet_link']
            video_file = request.FILES['video_file']  # Access the uploaded video file

            try:
                # Fetch the tweet image using the user-provided tweet link
                image_url = fetch_tweet_image(tweet_link)

                if image_url:
                    # Download and save the image as screenshot.png
                    save_tweet_image(image_url)

                    # Process the video with the overlay
                    final_processed_video_path = process_video_with_overlay(image_url, video_file)

                    if final_processed_video_path:
                        # Extract the filename from the processed video path
                        final_processed_video_filename = os.path.basename(final_processed_video_path)

                        # Assuming you serve static files using Django's 'static' view
                        # Adjust 'app_name' and 'proc'processed_video.mp4'essed_videos' to match your project structure
                        return render(request, 'processed_video.html')

                    else:
                        return HttpResponse("Video processing failed. Please try again later.")
                else:
                    return HttpResponse("Failed to fetch the tweet image.")
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
    else:
        form = VideoProcessingForm()

    return render(request, 'process_video.html', {'form': form})

def fetch_tweet_image(tweet_url):
    # Define the API URL
    url = "https://tweetpik.com/api/v2/images"

    # Define your API key
    api_key = "d1d0d488-5d3f-4345-a312-c6b51c80400e"

    # Create a JSON payload with the user-provided tweet URL and custom options
    payload = {
        "url": tweet_url,
        "textPrimaryColor": "#FFFFFF",
        "backgroundColor": "#000000",
        "dimension": "tiktok"
    }

    # Define the headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }

    # Send the POST request to the API
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Check if the request was successful
    if response.status_code == 201:
        # Parse the JSON response to get the image URL
        response_data = json.loads(response.text)
        image_url = response_data.get("url")
        return image_url
    else:
        print("Error fetching tweet image:", response.status_code)
        return None

def save_tweet_image(image_url):
    # Download the image
    image_response = requests.get(image_url)

    # Check if the image download was successful
    if image_response.status_code == 200:
        # Save the image as screenshot.png
        with open("screenshot.png", "wb") as image_file:
            image_file.write(image_response.content)
        print("Screenshot saved as screenshot.png")
    else:
        print("Error downloading the image:", image_response.status_code)

def process_video_with_overlay(image_url, video_file):
    try:
        # Download the tweet image
        response = requests.get(image_url)

        if response.status_code != 200:
            print("Error downloading the tweet image:", response.status_code)
            return None

        # Save the image as a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as image_file:
            image_file.write(response.content)
            tweet_image_path = image_file.name

        # Load the tweet image
        tweet_image = cv2.imread(tweet_image_path, cv2.IMREAD_UNCHANGED)

        if tweet_image is None:
            print(f"Error: Could not load the image from {tweet_image_path}")
            return None

        # Ensure the overlay image has an alpha channel
        if tweet_image.shape[2] == 3:  # If the image has no alpha channel
            # Add an alpha channel with full opacity (255)
            tweet_image = cv2.cvtColor(tweet_image, cv2.COLOR_RGB2RGBA)

        # Resize the overlay image to make it smaller
        desired_overlay_width = int(tweet_image.shape[1] * 0.9)  # Adjust the scaling factor as needed
        desired_overlay_height = int(tweet_image.shape[0] * 0.9)  # Adjust the scaling factor as needed
        tweet_image = cv2.resize(tweet_image, (desired_overlay_width, desired_overlay_height))

        # Calculate the cropping amount from the top (6% of the image height)
        crop_percentage = 6
        crop_height = int(tweet_image.shape[0] * (crop_percentage / 100))

        # Crop the top portion of the overlay image
        tweet_image = tweet_image[crop_height:, :]

        # Get the dimensions of the cropped overlay image
        overlay_height, overlay_width, _ = tweet_image.shape

        # Make specific black pixels in the overlay image transparent
        black_color = (0, 0, 0, 255)  # RGBA value for black
        black_pixels = np.all(tweet_image[:, :, :3] == black_color[:3], axis=2)
        tweet_image[black_pixels, 3] = 0  # Set the alpha channel to 0 for black pixels

        # Brightness factor (less than 1 reduces brightness, greater than 1 increases brightness)
        brightness_factor = 1.2  # Adjust this value as needed

        # Contrast factor (less than 1 reduces contrast, greater than 1 increases contrast)
        contrast_factor = 0.5  # Adjust this value as needed

        # Partial desaturation factor (less than 1 reduces saturation, greater than 1 increases saturation)
        desaturation_factor = 0.5  # Adjust this value as needed

        # Open the video file
        if hasattr(video_file, 'temporary_file_path'):
            # The video is stored on disk
            video_path = video_file.temporary_file_path()
        else:
            # The video is stored in memory
            video_memory = video_file.read()
            temp_video_path = None

            # Create a temporary video file and save the uploaded video to it
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
                temp_video_path = temp_video_file.name
                temp_video_file.write(video_memory)
            video_path = temp_video_path

        # Get the dimensions of the video frames
        video_clip = VideoFileClip(video_path)
        frame_width, frame_height = video_clip.size

        # Define a temporary directory to store intermediate video files
        temp_dir = tempfile.mkdtemp()

        # Define the path for the processed video
        processed_video_filename = 'processed_video.mp4'
        processed_video_path = os.path.join(settings.MEDIA_ROOT, processed_video_filename)
        
        # Define a VideoWriter with audio support
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(processed_video_path, fourcc, 30, (frame_width, frame_height), isColor=True)
        
        for frame in video_clip.iter_frames(fps=video_clip.fps, dtype='uint8'):
            # Apply grayscale effect with partial desaturation
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            frame_gray = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2BGR)
            frame_desaturated = cv2.addWeighted(frame, desaturation_factor, frame_gray, 1 - desaturation_factor, 0)

            # Adjust the brightness and contrast of the entire frame, including the overlayed region
            frame_adjusted = cv2.convertScaleAbs(frame_desaturated, alpha=brightness_factor, beta=0)
            frame_adjusted = cv2.convertScaleAbs(frame_adjusted, alpha=contrast_factor, beta=0)

            # Calculate the position for overlaying the picture
            x_position = (frame_width - overlay_width) // 2
            y_position = (frame_height - overlay_height) // 2

            # Create a mask for the picture's alpha channel with the same dimensions as ROI
            mask = np.zeros((overlay_height, overlay_width), dtype=np.float32)
            mask[:overlay_height, :overlay_width] = tweet_image[:, :, 3] / 255.0

            # Extract the regions of interest
            roi_frame = frame_adjusted[y_position:y_position+overlay_height, x_position:x_position+overlay_width]
            roi_overlay = tweet_image[:, :, :3]


            # Multiply the picture and frame using the alpha channel mask
            for c in range(0, 3):
                roi_frame[:, :, c] = roi_frame[:, :, c] * (1 - mask) + roi_overlay[:, :, c] * mask

            # Update the frame with the modified ROI
            frame_adjusted[y_position:y_position+overlay_height, x_position:x_position+overlay_width] = roi_frame

            # Write the frame to the output video
            out.write(frame_adjusted)

        # Release the VideoWriter
        out.release()
        # Extract audio from the original video
        audio = video_clip.audio

        # Combine the processed video with the audio
        final_video = VideoFileClip(processed_video_path)
        final_video = final_video.set_audio(audio)

        # Write the final video to the output file
        final_output_path = 'media/final_output.mp4'
        final_video.write_videofile(final_output_path, codec='libx264', audio_codec='aac')

        # Print the path to the final output video
        print("Final output video saved at:", final_output_path)

        return final_output_path

    except Exception as e:
        # Handle any exceptions or errors gracefully
        print(f"Video processing error: {str(e)}")
        return None
    
def playback_processed_video(request):
    # Define the path to the processed video
    processed_video_path = os.path.join(settings.MEDIA_ROOT, 'processed_video.mp4')
    processed_video_url = settings.MEDIA_URL + 'processed_video.mp4'


    if os.path.exists(processed_video_path):
        # Serve the video using the X-Sendfile header (requires appropriate server configuration)
        response = HttpResponse(content_type='video/mp4')
        response['Content-Type'] = 'video/mp4'
        response['Accept-Ranges'] = 'bytes'
        response['X-Sendfile'] = processed_video_url


        # Print the processed_video_url for debugging
        print("processed_video_url:", response.get('X-Sendfile'))

        return response
    else:
        return HttpResponse("Processed video not found.")