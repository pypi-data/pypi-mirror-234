import argsparse
import supervision as sv
from ultraanalytics import YOLO
from tqdm import tqdm


class Odin:
    """
    Odin is a class that uses the ultralytics library to perform object detection and tracking.

    Args:

        source_weights_path (str): Path to the weights file for the model.
        source_video_path (str): Path to the video file to be processed.
        target_video_path (str): Path to the video file to be written.
        confidence_threshold (float): Confidence threshold for the model.
        iou_threshold (float): IOU threshold for the model.

    Examples:
        >>> from odin import Odin
        >>> odin = Odin(
        ...     source_weights_path="yolov8n.pt",
        ...     source_video_path="https://youtu.be/LNwODJXcvt4",
        ...     target_video_path="output.mp4",
        ...     confidence_threshold=0.3,
        ...     iou_threshold=0.7,
        ... )
        >>> odin.run()




    """

    def __init__(
        self,
        source_weights_path: str = None,
        source_video_path: str = None,
        target_video_path: str = None,
        confidence_threshold: float = 0.3,
        iou_threshold: float = 0.7,
    ):
        super(Odin, self).__init__()

        self.source_weights_path = source_weights_path
        self.source_video_path = source_weights_path
        self.target_video_path = target_video_path
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold

    def run(self):
        """
        Runs the object detection and tracking pipeline.
        """
        model = YOLO(self.source_weights_path)

        tracker = sv.ByteTrack()
        box_annotator = sv.BoxAnnotator()
        frame_generator = sv.get_video_frames_generator(
            source_path=self.source_video_path
        )
        video_info = sv.VideoInfo.from_video_path(video_path=self.source_video_path)

        with sv.VideoSink(
            target_path=self.target_video_path, video_info=video_info
        ) as sink:
            for frame in tqdm(frame_generator, total=video_info.total_frames):
                results = model(
                    frame,
                    verbose=True,
                    conf=self.confidence_threshold,
                    iou=self.iou_threshold,
                )[0]
                detections = sv.Detections.from_ultranalytics(results)
                detections = tracker.update_with_detections(detections)

                labels = [
                    f"#{tracker_id} {model.model.names[class_id]}"
                    for _, _, _, class_id, tracker_id in detections
                ]

                annotated_frame = box_annotator.annotate(
                    scene=frame.copy(), detections=detections, labels=labels
                )

                result = sink.write_frame(frame=annotated_frame)
                return result
