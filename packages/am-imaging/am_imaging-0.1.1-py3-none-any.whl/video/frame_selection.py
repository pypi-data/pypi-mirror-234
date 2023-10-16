import os
import cv2
import numpy as np

def get_sharpest_frame_in_block(block):
    max_sharpness = -1
    sharpest_frame = None
    
    for frame in block:
        sharpness = cv2.Laplacian(frame, cv2.CV_64F).var()
        if sharpness > max_sharpness:
            max_sharpness = sharpness
            sharpest_frame = frame
            
    return sharpest_frame


def get_sharpest_frames(video_path, interval_frames):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for frame_idx in range(0, total_frames, interval_frames):
        block = []
        for _ in range(interval_frames):
            ret, frame = cap.read()
            if not ret:
                break
            block.append(frame)
        try:
            sharpest_frame = get_sharpest_frame_in_block(block)
        #   print(f'The sharpest frame at the block {frame_idx//interval_frames} got sharpness measure {sharpest_frame[0]}')
            yield sharpest_frame
        except:
            pass
    cap.release()  

def export_sharpest_frames(input_path, output_directory, frame_prefix, format='jpg', downscale=1, interval=12):
    sharpest_frames = get_sharpest_frames(input_path, interval)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for idx, sharpest_frame_info in enumerate(sharpest_frames):
        sharpest_frame = sharpest_frame_info[1]
        if downscale != 1:
            sharpest_frame = cv2.resize(sharpest_frame, (sharpest_frame.shape[1] // downscale, sharpest_frame.shape[0] // downscale))
        output_path = os.path.join(output_directory, f'{frame_prefix}_{idx}.{format}')
        cv2.imwrite(output_path, sharpest_frame)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Export the sharpest frames from a video')
    parser.add_argument('input_path', required=True, help='Input video path')
    parser.add_argument('output_directory', required=True, help='Output directory path for exported images')
    parser.add_argument('--frame_prefix', default='frame_', help='Prefix for exported images')
    parser.add_argument('--format', default='jpg', help='Format of the output(Defaults to jpg)')
    parser.add_argument('--downscale', type=int, default=1, help='Downscale image size by factor. (Defaults to 1)')
    parser.add_argument('--interval', type=int, default=12, help='Number of frames per interval. For each interval, the sharpest frame will be exported. (Defaults to 12)')

    args = parser.parse_args()
    
    export_sharpest_frames(args.input_path, args.output_directory, args.frame_prefix, args.format, args.downscale, args.interval)

if __name__ == "__main__":
    main()


