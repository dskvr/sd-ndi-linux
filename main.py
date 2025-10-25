#!/usr/bin/env python3
"""
StreamDiffusion NDI Real-time Video Processor
Captures NDI video stream, applies AI transformation, outputs to NDI
"""

import sys
import os
import time
import argparse
from datetime import datetime
import numpy as np
import torch
import cv2
from PIL import Image

# Add StreamDiffusion to path
sys.path.append("D:/dev/StreamDiffusion/streamdiffusion_repo")

try:
    import NDIlib as NDI
except ImportError:
    print("ERROR: ndi-python not installed")
    print("Install with: pip install ndi-python")
    sys.exit(1)

from utils.wrapper import StreamDiffusionWrapper

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


def find_ndi_source_by_name(sources, search_name):
    """Find NDI source by name (text search, returns first match)"""
    if not sources:
        return None

    search_name_lower = search_name.lower()

    # Try exact match first
    for source in sources:
        if search_name_lower in source.ndi_name.lower():
            print(f"\nAuto-selected NDI source: {source.ndi_name}")
            return source

    print(f"\nERROR: No NDI source matching '{search_name}' found")
    return None


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


def setup_streamdiffusion(device="cuda", dtype=torch.float16, acceleration="xformers"):
    """Initialize StreamDiffusion pipeline"""
    print("\nInitializing StreamDiffusion...")
    print(f"  Model: {MODEL_ID}")
    print(f"  Device: {device}")
    print(f"  Resolution: {WIDTH}x{HEIGHT}")
    print(f"  Prompt: {DEFAULT_PROMPT}")
    print(f"  Acceleration: {acceleration}")

    stream = StreamDiffusionWrapper(
        model_id_or_path=MODEL_ID,
        use_tiny_vae=True,
        device=device,
        dtype=dtype,
        t_index_list=T_INDEX_LIST,
        frame_buffer_size=FRAME_BUFFER_SIZE,
        width=WIDTH,
        height=HEIGHT,
        use_lcm_lora=True,
        output_type="pil",
        warmup=10,
        vae_id=None,
        acceleration=acceleration,
        mode="img2img",
        use_denoising_batch=True,
        cfg_type="self",
        use_safety_checker=False,
    )

    stream.prepare(
        prompt=DEFAULT_PROMPT,
        negative_prompt=DEFAULT_NEGATIVE_PROMPT,
        num_inference_steps=50,
        guidance_scale=1.2,
    )

    print("StreamDiffusion initialized successfully!")
    return stream


def ndi_frame_to_pil(video_frame, store_resolution=None):
    """Convert NDI video frame to PIL Image"""
    # NDI frames are typically in UYVY or RGBA format
    # Convert to RGB PIL Image
    data = np.frombuffer(video_frame.data, dtype=np.uint8)

    # Store original resolution if dict provided
    if store_resolution is not None and 'width' not in store_resolution:
        store_resolution['width'] = video_frame.xres
        store_resolution['height'] = video_frame.yres

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

    # Return numpy array directly (NDI expects numpy array, not bytes)
    return img_rgba


def main():
    parser = argparse.ArgumentParser(description="StreamDiffusion NDI Real-time Processor")
    parser.add_argument("--timeout", type=int, default=5, help="NDI source search timeout (seconds)")
    parser.add_argument("--acceleration", choices=["xformers", "tensorrt"], default="xformers",
                       help="Acceleration mode")
    parser.add_argument("--device", default="cuda", help="Device to use (cuda/cpu)")
    parser.add_argument("--ndi-source", type=str, default=None,
                       help="NDI source name to auto-select (text search, matches first)")
    args = parser.parse_args()

    # List and select NDI source
    sources, ndi_find = list_ndi_sources(timeout=args.timeout)
    if not sources:
        print("No NDI sources available. Exiting.")
        return 1

    # Auto-select source by name if provided, otherwise prompt user
    if args.ndi_source:
        selected_source = find_ndi_source_by_name(sources, args.ndi_source)
    else:
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

    # Create NDI sender with custom name
    print(f"Creating NDI sender: {OUTPUT_NDI_NAME}")
    send_settings = NDI.SendCreate()
    send_settings.p_ndi_name = OUTPUT_NDI_NAME
    ndi_send = NDI.send_create(send_settings)
    if ndi_send is None:
        print("ERROR: Failed to create NDI sender")
        NDI.recv_destroy(ndi_recv)
        NDI.find_destroy(ndi_find)
        return 1

    # Setup StreamDiffusion
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    dtype = torch.float16 if device.type == "cuda" else torch.float32
    stream = setup_streamdiffusion(device=device, dtype=dtype, acceleration=args.acceleration)

    frame_count = 0
    start_time = time.time()
    last_stats_time = start_time
    bytes_received_total = 0
    bytes_sent_total = 0
    bytes_received_last = 0
    bytes_sent_last = 0
    input_resolution = {}
    session_info_printed = False

    try:
        while True:
            # Receive NDI frame
            t, v, a, m = NDI.recv_capture_v2(ndi_recv, 1000)  # 1000ms timeout

            if t == NDI.FRAME_TYPE_VIDEO:
                # Track received bytes
                frame_bytes_received = len(v.data) if hasattr(v, 'data') else 0
                bytes_received_total += frame_bytes_received

                # Convert NDI frame to PIL Image (capture resolution on first frame)
                pil_input = ndi_frame_to_pil(v, input_resolution)

                # Print session info once we have the first frame
                if not session_info_printed and input_resolution:
                    print("\n" + "="*80)
                    print("STREAMING STARTED".center(80))
                    print("="*80)
                    print(f"  Input Source:       {selected_source.ndi_name}")
                    print(f"  Input Resolution:   {input_resolution['width']}x{input_resolution['height']}")
                    print(f"  Output Source:      {OUTPUT_NDI_NAME}")
                    print(f"  Output Resolution:  {WIDTH}x{HEIGHT}")
                    print(f"  Model:              {MODEL_ID}")
                    print(f"  Device:             {device}")
                    print(f"  Acceleration:       {args.acceleration}")
                    print(f"  Prompt:             {DEFAULT_PROMPT}")
                    if DEFAULT_NEGATIVE_PROMPT:
                        print(f"  Negative Prompt:    {DEFAULT_NEGATIVE_PROMPT}")
                    print("="*80)
                    print("\nPress Ctrl+C to stop\n")
                    session_info_printed = True

                # Process through StreamDiffusion
                # The wrapper returns PIL images directly (output_type="pil")
                pil_output = stream(image=pil_input, prompt=DEFAULT_PROMPT)

                # Convert back to NDI frame
                ndi_frame_data = pil_to_ndi_frame(pil_output)

                # Create NDI video frame
                video_frame = NDI.VideoFrameV2()
                video_frame.xres = WIDTH
                video_frame.yres = HEIGHT
                video_frame.FourCC = NDI.FOURCC_VIDEO_TYPE_RGBA
                video_frame.frame_rate_N = 30000
                video_frame.frame_rate_D = 1001
                video_frame.data = ndi_frame_data
                video_frame.line_stride_in_bytes = WIDTH * 4

                # Track sent bytes
                frame_bytes_sent = WIDTH * HEIGHT * 4  # RGBA
                bytes_sent_total += frame_bytes_sent

                # Send NDI frame
                NDI.send_send_video_v2(ndi_send, video_frame)

                # Free the NDI frame
                NDI.recv_free_video_v2(ndi_recv, v)

                frame_count += 1

                # Print stats every frame (updates same line)
                current_time = time.time()
                elapsed = current_time - start_time
                stats_interval = current_time - last_stats_time

                if stats_interval >= 1.0:  # Update stats display every second
                    fps = frame_count / elapsed

                    # Calculate per-second rates
                    bytes_recv_per_sec = (bytes_received_total - bytes_received_last) / stats_interval
                    bytes_sent_per_sec = (bytes_sent_total - bytes_sent_last) / stats_interval

                    # Update last values
                    bytes_received_last = bytes_received_total
                    bytes_sent_last = bytes_sent_total
                    last_stats_time = current_time

                    # Format bytes for display
                    def format_bytes(b):
                        if b >= 1_000_000_000:
                            return f"{b/1_000_000_000:.2f} GB"
                        elif b >= 1_000_000:
                            return f"{b/1_000_000:.2f} MB"
                        elif b >= 1_000:
                            return f"{b/1_000:.2f} KB"
                        else:
                            return f"{b} B"

                    now = datetime.now()
                    date_str = now.strftime("%Y-%m-%d")
                    time_str = now.strftime("%H:%M:%S")

                    # Print stats on same line (carriage return)
                    print(f"\r{date_str} {time_str} | FPS: {fps:.2f} | "
                          f"RX: {format_bytes(bytes_received_total)} ({format_bytes(bytes_recv_per_sec)}/s) | "
                          f"TX: {format_bytes(bytes_sent_total)} ({format_bytes(bytes_sent_per_sec)}/s) | "
                          f"Frames: {frame_count}", end='', flush=True)

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
