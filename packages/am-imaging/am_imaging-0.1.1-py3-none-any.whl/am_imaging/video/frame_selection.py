import os
import cv2
import numpy as np

def get_sharpest_frame_in_block(block):
    max_sharpness = -1
    sharpest_frame = None
    max_index = -1
    
    for i, frame in enumerate(block):
        sharpness = cv2.Laplacian(frame, cv2.CV_64F).var()
        if sharpness > max_sharpness:
            max_sharpness = sharpness
            sharpest_frame = frame
            max_index = i
            
    return sharpest_frame, max_index, max_sharpness


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
            sharpest_frame, block_idx, sharpness = get_sharpest_frame_in_block(block)
            print(f'Selecting frame {frame_idx + block_idx} (offset: {block_idx}) with sharpness {sharpness}')
            yield sharpest_frame
        except:
            pass
    cap.release()  

def export_sharpest_frames(input_path, output_directory, frame_prefix='frame_', format='jpg', downscale=1, interval=12):
    sharpest_frames = get_sharpest_frames(input_path, interval)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for idx, sharpest_frame in enumerate(sharpest_frames):
        sharpest_frame = sharpest_frame
        if downscale != 1:
            dim = np.take(sharpest_frame.shape, [1,0]) // downscale
            sharpest_frame = cv2.resize(sharpest_frame, dim, cv2.INTER_AREA)
        output_path = os.path.join(output_directory, f'{frame_prefix}{idx}.{format}')
        cv2.imwrite(output_path, sharpest_frame)





