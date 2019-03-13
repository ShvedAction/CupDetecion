import cv2

class Video:
    """
    To read and write video
    """

    
    def __init__(self, path):
        self._path = path
        self._isReadHead = False
    
    def read_head(self):
        self._video_capture = cv2.VideoCapture(self._path)
        self._fps = self._video_capture.get(cv2.CAP_PROP_FPS)
        self._width = int(self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self._video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._isReadHead = True
        return self._fps, self._width, self._height

    def read(self):
        if not self._isReadHead:
            self.read_head()
        
        while self._video_capture.isOpened():
            ret, bgr_image = self._video_capture.read()
            if not ret:
                print("error: failed to capture image from video: " + self._path)
                break
            else:
                yield bgr_image

        self._video_capture.release()

    def write(self, frames, fps, width, height):
        """
        frames should be iterator of bgr
        """
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(self._path, fourcc, fps, (width, height))

        for frame in frames:
            writer.write(frame)

        writer.release()


#semi-automatic tests

def _how_it_use(input_path, output_path):
    """
    input_path is path to video wich will be readed
    output_path is path for changed video
    """
    source_video = Video(input_path)
    out_video = Video(output_path)

    fps, width, height = source_video.read_head()

    def _draw_rect(bgr):
        """Draw rectangle"""
        cv2.rectangle(bgr, (10,10), (100,100), (0,0,255), 4)
        return bgr

    frames = (_draw_rect(bgr) for bgr in source_video.read())

    out_video.write(frames, fps, width, height)

def main():
    import argparse
    argParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argParser.add_argument("--input", type=str, help="taget video", required=True)
    argParser.add_argument("--output", type=str, default="out.mp4", help="path to save the result video")
    args = argParser.parse_args()

    _how_it_use(args.input, args.output)

if __name__ == "__main__":
    main()