from dataclasses import dataclass
from numpy import ndarray
import cv2
from enum import Enum

@dataclass
class Keypoint2D:
    x: int
    y: int
    score: float
    name: str


@dataclass
class KPFrame:
    keypoints: list[Keypoint2D]

@dataclass
class Annotation:
    x: int
    y: int
    radius: int
    color: (int, int, int)

@dataclass
class Label:
    x: int
    y: int
    name: str

@dataclass
class BBox:
    x: int
    y: int
    width: int
    height: int
    color: (int, int, int)
    label: str
    confidence: float

@dataclass
class Classification:
    predictions: list[dict[str, float]]

class Canvas:
    FONT = cv2.FONT_HERSHEY_PLAIN
    FONT_SIZE = 1
    THICKNESS = 2
    LABEL_WIDTH = 50

    image : ndarray = None
    def __init__(self, image : ndarray = None):
        self.image = image
    
    def add_annotations(self, annotations : list[Annotation]):
        self.annotations = annotations
        for dot in annotations:
            cv2.circle(self.image, (dot.x, dot.y), 0, dot.color, int(dot.radius * 50))

    def add_bboxes(self, bboxes: list[BBox]):
        self.bboxes = bboxes
        for bbox in bboxes:
            cv2.rectangle(img=self.image,
                pt1=(int(bbox.x - (bbox.width // 2)), int(bbox.y - (bbox.height // 2))),
                pt2=(int(bbox.x + (bbox.width // 2)), int(bbox.y + (bbox.height // 2))),
                color=bbox.color, thickness=self.THICKNESS)
            cv2.putText(self.image, bbox.label,
                        (int(bbox.x - (bbox.width // 2)), int(bbox.y - (bbox.height // 2) - 2 * self.THICKNESS)),
                        self.FONT, self.FONT_SIZE, bbox.color, 1, lineType = cv2.LINE_AA)
            
    def add_labels(self, labels: list[Label]):
        self.labels = labels
        for label in labels:
            cv2.circle(img=self.image, center=(label.x, label.y), radius=0, color=(255, 255, 255), thickness=self.LABEL_WIDTH)
            text_size = cv2.getTextSize(label.name, self.FONT, self.FONT_SIZE, self.THICKNESS)[0]
            text_origin = (label.x - text_size[0] // 2, label.y + text_size[1] // 2)
            cv2.putText(self.image, label.name, text_origin, self.FONT, self.FONT_SIZE, (0, 0, 0), 1, lineType = cv2.LINE_AA)

    def set_image(self, image):
        self.annotations = None
        self.bboxes = None
        self.labels = None
        self.image = image.copy()

    def show(self, time : int):
        cv2.imshow("Image", self.image)
        return cv2.waitKey(time) & 0xFF == 27 # exit with esc
    
    def close(self):
        cv2.destroyAllWindows()