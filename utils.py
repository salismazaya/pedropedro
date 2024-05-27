from PIL import Image, ImageDraw, ImageFont

def create_instagram_notification(profile_pic_path, username, output_path):
    # Load the profile picture
    profile_pic = Image.open(profile_pic_path).convert("RGBA")
    
    # Create a mask for a rounded profile picture
    size = (100, 100)  # Fixed size for the profile picture
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    
    # Resize and apply the rounded mask to the profile picture
    profile_pic = profile_pic.resize(size, Image.ANTIALIAS)
    profile_pic.putalpha(mask)
    
    # Create a white circle background for the profile picture
    background = Image.new('RGBA', size, (255, 255, 255, 255))
    background.paste(profile_pic, (0, 0), profile_pic)
    
    # Create the notification base image with a white background
    notification_width = 500
    notification_height = 100
    notification_image = Image.new('RGBA', (notification_width, notification_height), (255, 255, 255, 255))
    
    # Paste the profile picture onto the notification image
    profile_pic_size = 60
    profile_pic_position = (10, (notification_height - profile_pic_size) // 2)
    background = background.resize((profile_pic_size, profile_pic_size), Image.ANTIALIAS)
    notification_image.paste(background, profile_pic_position, background)
    
    # Add the username and text
    draw = ImageDraw.Draw(notification_image)
    font = ImageFont.load_default()  # You can replace this with a TTF font file for better matching
    username_position = (profile_pic_position[0] + profile_pic_size + 10, profile_pic_position[1])
    text_position = (username_position[0], username_position[1] + 20)
    
    draw.text(username_position, username, font=font, fill=(0, 0, 0))
    draw.text(text_position, "started following you. 19m", font=font, fill=(128, 128, 128))
    
    # Add the follow button
    button_width = 80
    button_height = 30
    button_position = (notification_width - button_width - 10, (notification_height - button_height) // 2)
    draw.rectangle([button_position, (button_position[0] + button_width, button_position[1] + button_height)], fill=(0, 153, 255))
    
    # Add the text on the follow button
    button_text = "Follow"
    button_text_position = (button_position[0] + (button_width - font.getsize(button_text)[0]) // 2,
                            button_position[1] + (button_height - font.getsize(button_text)[1]) // 2)
    draw.text(button_text_position, button_text, font=font, fill = (255, 255, 255))
    
    # Save the final image
    notification_image.save(output_path)

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

# Fungsi untuk menempel gambar ke video
def overlay_image_on_video(video_path, image_path, output_path, position=("center", 200)):
    # Buka video dan gambar
    video_clip = VideoFileClip(video_path)
    image_clip = ImageClip(image_path).set_duration(video_clip.duration)
    
    # Sesuaikan ukuran gambar agar lebih kecil jika diperlukan
    image_clip = image_clip.resize(width = 800)  # Resize image height to 1/3 of video height

    # Set posisi gambar
    image_clip = image_clip.set_position(position)
    
    # Membuat video gabungan
    final_clip = CompositeVideoClip([video_clip, image_clip])

    # Simpan video yang sudah digabungkan
    final_clip.write_videofile(output_path, codec="libx264", fps=video_clip.fps)
