import os
import subprocess
import glob
import re

# Source directory
SRC_DIR = "Images"
# Destination directory
DEST_DIR = os.path.join(SRC_DIR, "compressed")

# Make sure destination exists
os.makedirs(DEST_DIR, exist_ok=True)

# Find all image and video files in Images directory (excluding compressed folder itself)
all_files = glob.glob(os.path.join(SRC_DIR, "*"))

image_extensions = {".heic", ".jpg", ".jpeg", ".png"}
video_extensions = {".mp4", ".mov"}

processed_basenames = set()

def get_unique_base(filename):
    # Normalize duplicate names like "IMG_0538(1).HEIC" or "IMG_0538.HEIC" to "IMG_0538"
    base = os.path.basename(filename)
    name, ext = os.path.splitext(base)
    # Remove things like (1) or (2) or (1)(1)
    clean_name = re.sub(r'\(\d+\)', '', name).strip()
    return clean_name, ext.lower()

images_to_process = []
videos_to_process = []

for f in all_files:
    if os.path.isdir(f):
        continue
    clean_name, ext = get_unique_base(f)
    if ext in image_extensions:
        if clean_name not in processed_basenames:
            processed_basenames.add(clean_name)
            images_to_process.append((f, clean_name))
    elif ext in video_extensions:
        if clean_name not in processed_basenames:
            processed_basenames.add(clean_name)
            size_mb = os.path.getsize(f) / (1024 * 1024)
            videos_to_process.append((f, clean_name, size_mb))

print(f"Found {len(images_to_process)} unique images and {len(videos_to_process)} unique videos to process.")

# Process images: HEIC/JPG/JPEG/PNG -> WebP
# We will scale images to max width of 1920 for performance, keeping aspect ratio, and compress with q=75
for img_path, clean_name in images_to_process:
    out_name = f"{clean_name}.webp"
    out_path = os.path.join(DEST_DIR, out_name)
    
    if os.path.exists(out_path):
        print(f"Skipping image {out_name}, already exists.")
        continue
        
    print(f"Compressing {os.path.basename(img_path)} -> {out_name}...")
    # FFmpeg command: scale to max 1920 wide, maintain aspect, output webp with quality 75
    # Use -vf "scale=min(1920\\,iw):-2" to scale down but never scale up
    cmd = [
        "ffmpeg", "-y", "-i", img_path,
        "-vf", "scale=min(1920\\,iw):-2",
        "-vcodec", "libwebp", "-q:v", "75",
        out_path
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
        print(f"Successfully processed {out_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {img_path}: {e.stderr.decode('utf-8', errors='ignore')}")

# Process videos: MP4/MOV -> WebM
# We will only convert smaller videos to save time, or convert a couple of key ones.
# The user wants drone footage for hero and before/after.
# We'll convert 3-4 key videos: a drone video for hero and 2 job videos.
videos_to_process.sort(key=lambda x: x[2]) # sort by size (smallest first)

for vid_path, clean_name, size_mb in videos_to_process:
    out_name = f"{clean_name}.webm"
    out_path = os.path.join(DEST_DIR, out_name)
    
    if os.path.exists(out_path):
        print(f"Skipping video {out_name}, already exists.")
        continue
        
    # We only process if size is < 15MB OR if it contains 'dji_fly' and size < 40MB
    if size_mb > 15.0 and not (clean_name.startswith("dji_fly") and size_mb < 40.0):
        print(f"Skipping large video {clean_name} ({size_mb:.1f} MB)")
        continue
        
    print(f"Compressing video {os.path.basename(vid_path)} ({size_mb:.1f} MB) -> {out_name}...")
    # Convert to webm with libvpx-vp9, scale to 720p (1280x720) for web performance, low bitrate (crf 33)
    cmd = [
        "ffmpeg", "-y", "-i", vid_path,
        "-vf", "scale=1280:-2",
        "-vcodec", "libvpx-vp9", "-crf", "33", "-b:v", "0",
        "-an", # remove audio for hero bg
        out_path
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True, timeout=120)
        print(f"Successfully processed video {out_name}")
    except subprocess.TimeoutExpired:
        print(f"Timeout processing video {vid_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing video {vid_path}: {e.stderr.decode('utf-8', errors='ignore')}")
