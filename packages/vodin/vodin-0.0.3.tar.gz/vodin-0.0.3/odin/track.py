import cv2
import threading
from ultralytics import YOLO


class Tracker:
    def __init__(self, model_path):
        """
        # Load an official or custom model
        model = YOLO('yolov8n.pt')  # Load an official Detect model
        model = YOLO('yolov8n-seg.pt')  # Load an official Segment model
        model = YOLO('yolov8n-pose.pt')  # Load an official Pose model
        model = YOLO('path/to/best.pt')  # Load a custom trained model
        """
        self.model = YOLO(model_path)

    def track(self, source, conf=0.3, iou=0.5, show=True, tracker="botsort.yaml"):
        """
        Ultralytics YOLO supports the following tracking algorithms. They can be enabled by passing the relevant YAML configuration file such as tracker=tracker_type.yaml:

        BoT-SORT - Use botsort.yaml to enable this tracker.
        ByteTrack - Use bytetrack.yaml to enable this tracker.
        The default tracker is BoT-SORT.
        """
        return self.model.track(
            source=source, conf=conf, iou=iou, show=show, tracker=tracker
        )

    def run_tracker_in_thread(self, filename, file_index):
        video = cv2.VideoCapture(filename)
        while True:
            ret, frame = video.read()
            if not ret:
                break
            results = self.model.track(frame, persist=True)
            res_plotted = results[0].plot()
            cv2.imshow(f"Tracking_Stream_{file_index}", res_plotted)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
        video.release()

    def multi_thread_tracking(self, video_files):
        threads = []
        for i, video_file in enumerate(video_files):
            thread = threading.Thread(
                target=self.run_tracker_in_thread, args=(video_file, i + 1), daemon=True
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        cv2.destroyAllWindows()


# Initialize the tracker with a model
tracker = Tracker("yolov8n.pt")

# Perform tracking with the model
results = tracker.track(source="https://youtu.be/LNwODJXcvt4", show=True)

# Run tracking on multiple video streams simultaneously
# video_files = ["path/to/video1.mp4", "path/to/video2.mp4"]
# tracker.multi_thread_tracking(video_files)
