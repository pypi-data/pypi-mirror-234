import numpy as np
from mexican_sign_language_toolkit.neighbors import Bruteforce
from mexican_sign_language_toolkit.pose_landmarker import PoseLandmarker
from mexican_sign_language_toolkit.lexer import tokenize
import mediapipe as mp
import cv2
import time
import requests
import os
import glob
import traceback
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def download_file(url, local_filename):
    """
    Download a file from the given URL and save it to the specified local filename.
    :param url: The URL of the file to download
    :param local_filename: The local file name to save the downloaded file
    """
    with requests.get(url, stream=True) as response:
        # Check if the request was successful (status code 200)
        response.raise_for_status()
        # Write the content of the request to a local file
        with open(local_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                

def create_space():
    images = [*glob.glob('**/*.png', recursive=True),*glob.glob('**/*.jpg', recursive=True),*glob.glob('**/*.jpeg', recursive=True)]
    pose_landmarker = PoseLandmarker()
    regex,db = pose_landmarker.create_database_from_images(images)
    np.save('language_space.npy', db)
    np.save('regex.npy', regex)


def install(*paths):
    default_http_requests = [
        "https://github.com/sanchezcarlosjr/mexican_sign_language_toolkit/raw/main/checkpoints/regex.npy",
        "https://github.com/sanchezcarlosjr/mexican_sign_language_toolkit/raw/main/checkpoints/language_space.npy",
        "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task",
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
    ]
    default_names = [
        "regex.npy",
        "language_space.npy",
        "pose_landmarker.task",
        "hand_landmarker.task"
    ]
    for index, path in enumerate(paths):
        if not os.path.exists(path):
            download_file(default_http_requests[index], default_names[index])

class Pipeline:
    """
    Base pipeline class for processing and predicting landmarks.
    """
    def __init__(self, space_path='language_space.npy', regex_path='regex.npy', pose_landmarker="pose_landmarker.task", hand_landmarker="hand_landmarker.task"):
        install(regex_path, space_path, pose_landmarker, hand_landmarker)
        self.pose_landmarker_path = pose_landmarker
        self.hand_landmarker_path = hand_landmarker
        space = np.load(space_path, allow_pickle=True)
        regex = str(np.load(regex_path, allow_pickle=True))
        self.brute_force = Bruteforce(space)
        self.match = tokenize(regex)

    def predict(self, *input):
        """
        Predict with landmarks and handle exceptions gracefully.
        """
        try:
            landmarks = self.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=input[0]), *input[1:])
            if landmarks is None:
                return ""
            signal = self.brute_force.classify(landmarks)
            result = self.match(signal)
            return result[0] if result else ""
        except Exception as e:
            just_the_string = traceback.format_exc()
            logger.debug(just_the_string)
            return ""


class ImagePipeline(Pipeline):
    def start_landmarker(self):
        self.pose_landmarker = PoseLandmarker(mp.tasks.vision.RunningMode.IMAGE, self.pose_landmarker_path, self.hand_landmarker_path)
    def detect(self, mp_image):
        return self.pose_landmarker.detect_for_image(mp_image) 


class VideoPipeline(Pipeline):
    def start_landmarker(self):
        self.pose_landmarker = PoseLandmarker(mp.tasks.vision.RunningMode.VIDEO, self.pose_landmarker_path, self.hand_landmarker_path)
    """
    Pipeline for processing and predicting landmarks from videos.
    """
    def predict(self, input):
        cap = cv2.VideoCapture(input)
        fps = cap.get(cv2.CAP_PROP_FPS)
        predictions = []
        frame_index = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_timestamp_ms = 1000 * frame_index / fps
            prediction = super().predict(rgb_frame, int(frame_timestamp_ms))
            if prediction != "":
               predictions.append(prediction) 
            frame_index += 1

        cap.release()
        return " ".join(predictions)

    def detect(self, mp_image, frame_timestamp_ms):
        return self.pose_landmarker.detect_for_video(mp_image, frame_timestamp_ms)
            
        
def pipeline(pipe = None):
    if pipe == None:
        pipe = ImagePipeline()
    pipe.start_landmarker()
    return pipe.predict
