import sys
sys.path.insert(0, 'video_handling')

from video import Video
from cup_detection import SimpleHSVDetector, draw_detections

#This parametrs should be tune in the ocv_threshhold ipython notebook (see the file)
TARGET_COLOR = (125, 70, 70)
WEIGHT_COLOR = (20, 40, .40)
THRESHHOLD = 0.99
OVERLAP_THRESHHOLD = 0.7
WINDOW_SIZE = 250
CLIP_LIMIT = 5.0
TILE_GRID_SIZE=(6,6)

def higlight_cup(input_path, output_path):
    detector = SimpleHSVDetector(color=TARGET_COLOR, weight_color=WEIGHT_COLOR, threshhold=THRESHHOLD,
                    overlap_threshhold=OVERLAP_THRESHHOLD, window_size=WINDOW_SIZE, clipLimit=CLIP_LIMIT,
                    tileGridSize=TILE_GRID_SIZE)
    
    source_video = Video(input_path)
    out_video = Video(output_path)
    
    fps, width, height = source_video.read_head()

    def handle_each_frame(bgr):
        detections = detector.detect(bgr)
        draw_detections(bgr, detections)
        return bgr
    
    frames = (handle_each_frame(bgr) for bgr in source_video.read())

    out_video.write(frames, fps, width, height)



def main():
    import argparse
    argParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argParser.add_argument("--input", type=str, help="taget video", required=True)
    argParser.add_argument("--output", type=str, default="out.mp4", help="path to save the result video")
    args = argParser.parse_args()

    higlight_cup(args.input, args.output)

if __name__ == "__main__":
    main()