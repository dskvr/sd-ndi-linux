#!/usr/bin/env python3
"""
StreamDiffusion NDI Real-time Video Processor
Captures NDI video stream, applies AI transformation, outputs to NDI
"""

import sys
import os
import time
import argparse
import numpy as np
import torch
import cv2
from PIL import Image

# Add StreamDiffusion to path if installed locally
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "streamdiffusion_repo"))

try:
    import NDI
except ImportError:
    print("ERROR: ndi-python not installed")
    print("Install with: pip install ndi-python")
    sys.exit(1)

from streamdiffusion import StreamDiffusion
from streamdiffusion.image_utils import postprocess_image

# Configuration
DEFAULT_PROMPT = "cyberpunk, neon lights, dark background, glowing, futuristic"
DEFAULT_NEGATIVE_PROMPT = "black and white, blurry, low resolution, pixelated, pixel art, low quality, low fidelity"
MODEL_ID = "stabilityai/sd-turbo"
OUTPUT_NDI_NAME = "streamdiffusion-ndi-render"

# StreamDiffusion parameters
WIDTH = 512
HEIGHT = 512
T_INDEX_LIST = [35, 45]  # Denoising timesteps
FRAME_BUFFER_SIZE = 1


def list_ndi_sources(timeout=5):
    """List available NDI sources"""
    print(f"Searching for NDI sources (timeout: {timeout}s)...")

    if not NDI.initialize():
        print("ERROR: Failed to initialize NDI")
        return []

    ndi_find = NDI.find_create_v2()
    if ndi_find is None:
        print("ERROR: Failed to create NDI finder")
        return []

    # Wait for sources
    time.sleep(timeout)

    sources = NDI.find_get_current_sources(ndi_find)

    if not sources:
        print("No NDI sources found")
        NDI.find_destroy(ndi_find)
        return []

    print(f"\nFound {len(sources)} NDI source(s):")
    for idx, source in enumerate(sources):
        print(f"  [{idx}] {source.ndi_name}")

    return sources, ndi_find


def select_ndi_source(sources):
    """Let user select an NDI source"""
    if not sources:
        return None

    if len(sources) == 1:
        print(f"\nAuto-selecting only available source: {sources[0].ndi_name}")
        return sources[0]

    while True:
        try:
            choice = input(f"\nSelect NDI source [0-{len(sources)-1}]: ")
            idx = int(choice)
            if 0 <= idx < len(sources):
                return sources[idx]
            else:
                print(f"Invalid choice. Please enter 0-{len(sources)-1}")
        except ValueError:
            print("Invalid input. Please enter a number")
        except KeyboardInterrupt:
            print("\nCancelled by user")
            return None


def setup_streamdiffusion(device="cuda", dtype=torch.float16):
    """Initialize StreamDiffusion pipeline"""
    print("\nInitializing StreamDiffusion...")
    print(f"  Model: {MODEL_ID}")
    print(f"  Device: {device}")
    print(f"  Resolution: {WIDTH}x{HEIGHT}")
    print(f"  Prompt: {DEFAULT_PROMPT}")

    # This is a simplified version - you'll need to adapt based on StreamDiffusion API
    # For now, this is a placeholder structure
    stream = StreamDiffusion(
        model_id_or_path=MODEL_ID,
        t_index_list=T_INDEX_LIST,
        frame_buffer_size=FRAME_BUFFER_SIZE,
        width=WIDTH,
        height=HEIGHT,
        warmup=10,
        acceleration="xformers",  # or "tensorrt" for better performance
        mode="img2img",
        use_denoising_batch=True,
        cfg_type="self",
        device=device,
        dtype=dtype,
    )

    stream.prepare(
        prompt=DEFAULT_PROMPT,
        negative_prompt=DEFAULT_NEGATIVE_PROMPT,
        num_inference_steps=50,
        guidance_scale=1.2,
    )

    print("StreamDiffusion initialized successfully!")
    return stream


def ndi_frame_to_pil(video_frame):
    """Convert NDI video frame to PIL Image"""
    # NDI frames are typically in UYVY or RGBA format
    # Convert to RGB PIL Image
    data = np.frombuffer(video_frame.data, dtype=np.uint8)

    # Reshape based on NDI frame format
    if video_frame.FourCC == NDI.FOURCC_VIDEO_TYPE_UYVY:
        # UYVY to RGB conversion
        img_yuv = data.reshape((video_frame.yres, video_frame.xres, 2))
        img_rgb = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB_UYVY)
    elif video_frame.FourCC == NDI.FOURCC_VIDEO_TYPE_RGBA:
        img_rgba = data.reshape((video_frame.yres, video_frame.xres, 4))
        img_rgb = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2RGB)
    else:
        # Default: assume BGRA
        img = data.reshape((video_frame.yres, video_frame.xres, 4))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

    # Resize to model resolution
    img_rgb = cv2.resize(img_rgb, (WIDTH, HEIGHT))

    # Convert to PIL Image
    return Image.fromarray(img_rgb)


def pil_to_ndi_frame(pil_image, frame_format=NDI.FOURCC_VIDEO_TYPE_RGBA):
    """Convert PIL Image to NDI frame data"""
    # Convert PIL to numpy array
    img_rgb = np.array(pil_image)

    # Convert to RGBA for NDI
    img_rgba = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2RGBA)

    return img_rgba.tobytes()


def main():
    parser = argparse.ArgumentParser(description="StreamDiffusion NDI Real-time Processor")
    parser.add_argument("--timeout", type=int, default=5, help="NDI source search timeout (seconds)")
    parser.add_argument("--acceleration", choices=["xformers", "tensorrt"], default="xformers",
                       help="Acceleration mode")
    parser.add_argument("--device", default="cuda", help="Device to use (cuda/cpu)")
    args = parser.parse_args()

    # List and select NDI source
    sources, ndi_find = list_ndi_sources(timeout=args.timeout)
    if not sources:
        print("No NDI sources available. Exiting.")
        return 1

    selected_source = select_ndi_source(sources)
    if selected_source is None:
        print("No source selected. Exiting.")
        NDI.find_destroy(ndi_find)
        return 1

    print(f"\nSelected source: {selected_source.ndi_name}")

    # Create NDI receiver
    print("\nCreating NDI receiver...")
    ndi_recv = NDI.recv_create_v3()
    if ndi_recv is None:
        print("ERROR: Failed to create NDI receiver")
        NDI.find_destroy(ndi_find)
        return 1

    NDI.recv_connect(ndi_recv, selected_source)
    NDI.recv_set_tally(ndi_recv, NDI.recv_tally_t(True, False))  # Set program tally

    # Create NDI sender
    print(f"Creating NDI sender: {OUTPUT_NDI_NAME}")
    ndi_send = NDI.send_create()
    if ndi_send is None:
        print("ERROR: Failed to create NDI sender")
        NDI.recv_destroy(ndi_recv)
        NDI.find_destroy(ndi_find)
        return 1

    # Setup StreamDiffusion
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    dtype = torch.float16 if device.type == "cuda" else torch.float32
    stream = setup_streamdiffusion(device=device, dtype=dtype)

    print("\n" + "="*60)
    print("STREAMING STARTED")
    print("="*60)
    print(f"Input:  {selected_source.ndi_name}")
    print(f"Output: {OUTPUT_NDI_NAME}")
    print(f"Prompt: {DEFAULT_PROMPT}")
    print("\nPress Ctrl+C to stop")
    print("="*60 + "\n")

    frame_count = 0
    start_time = time.time()

    try:
        while True:
            # Receive NDI frame
            t, v, a, m = NDI.recv_capture_v2(ndi_recv, 1000)  # 1000ms timeout

            if t == NDI.FRAME_TYPE_VIDEO:
                # Convert NDI frame to PIL Image
                pil_input = ndi_frame_to_pil(v)

                # Process through StreamDiffusion
                # Note: You'll need to adapt this based on StreamDiffusion's actual API
                output_tensor = stream(image=pil_input, prompt=DEFAULT_PROMPT)
                pil_output = postprocess_image(output_tensor)[0]

                # Convert back to NDI frame
                ndi_frame_data = pil_to_ndi_frame(pil_output)

                # Create NDI video frame
                video_frame = NDI.video_frame_v2_t()
                video_frame.xres = WIDTH
                video_frame.yres = HEIGHT
                video_frame.FourCC = NDI.FOURCC_VIDEO_TYPE_RGBA
                video_frame.frame_rate_N = 30000
                video_frame.frame_rate_D = 1001
                video_frame.data = ndi_frame_data
                video_frame.line_stride_in_bytes = WIDTH * 4

                # Send NDI frame
                NDI.send_send_video_v2(ndi_send, video_frame)

                # Free the NDI frame
                NDI.recv_free_video_v2(ndi_recv, v)

                frame_count += 1

                # Print stats every 30 frames
                if frame_count % 30 == 0:
                    elapsed = time.time() - start_time
                    fps = frame_count / elapsed
                    print(f"Processed {frame_count} frames | {fps:.2f} FPS")

            elif t == NDI.FRAME_TYPE_AUDIO:
                # Free audio frame (we're not processing audio)
                NDI.recv_free_audio_v2(ndi_recv, a)

    except KeyboardInterrupt:
        print("\n\nStopping...")

    finally:
        # Cleanup
        print("Cleaning up...")
        NDI.recv_destroy(ndi_recv)
        NDI.send_destroy(ndi_send)
        NDI.find_destroy(ndi_find)
        NDI.destroy()

        elapsed = time.time() - start_time
        if frame_count > 0:
            avg_fps = frame_count / elapsed
            print(f"\nProcessed {frame_count} frames in {elapsed:.1f}s ({avg_fps:.2f} FPS average)")

        print("Done!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
