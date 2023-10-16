from .frame_selection import export_sharpest_frames

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Export the sharpest frames from a video')
    parser.add_argument('input_path', help='Input video path')
    parser.add_argument('output_directory', help='Output directory path for exported images')
    parser.add_argument('--frame_prefix', default='frame_', help='Prefix for exported images')
    parser.add_argument('--format', default='jpg', help='Format of the output(Defaults to jpg)')
    parser.add_argument('--downscale', type=int, default=1, help='Downscale image size by factor. (Defaults to 1)')
    parser.add_argument('--interval', type=int, default=12, help='Number of frames per interval. For each interval, the sharpest frame will be exported. (Defaults to 12)')

    args = parser.parse_args()
    
    export_sharpest_frames(args.input_path, args.output_directory, args.frame_prefix, args.format, args.downscale, args.interval)

main()
# if __name__ == "__main__":
#     main()