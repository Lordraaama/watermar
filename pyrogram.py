from pyrogram import Client, filters
from pyrogram.types import InputFile
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

app = Client("video_watermark_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("start"))
def start(_, message):
    message.reply_text("Welcome to the Video Watermark Bot!\nSend me a video file to add a watermark.")


@app.on_message(filters.video)
def watermark_video(_, message):
    try:
        video_path = message.video.file_id
        video_file = app.download_media(video_path)
        watermark_text = "Your Watermark Here"
        
        # Add watermark to the video
        output_video_path = add_watermark(video_file, watermark_text)

        # Send the watermarked video
        message.reply_video(video=InputFile(output_video_path))

    except Exception as e:
        print(f"Error: {e}")
        message.reply_text("An error occurred while processing the video.")


def add_watermark(video_path, watermark_text):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Create a TextClip with the watermark text
    watermark_clip = TextClip(watermark_text, fontsize=40, color='white', bg_color='black', size=(video_clip.size[0], 50))

    # Set the position of the watermark
    watermark_clip = watermark_clip.set_position(('center', 10)).set_duration(video_clip.duration)

    # Composite the video with the watermark
    watermarked_clip = CompositeVideoClip([video_clip, watermark_clip])

    # Define the output path for the watermarked video
    output_path = "watermarked_video.mp4"

    # Write the watermarked video to the output path
    watermarked_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)

    return output_path


if __name__ == "__main__":
    app.run()
