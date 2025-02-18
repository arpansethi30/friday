import cv2
import numpy as np
import logging
from typing import List, Tuple, Dict, Any

class VisionSystem:
    def __init__(self):
        self.logger = logging.getLogger('FRIDAY.Vision')
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            if self.face_cascade.empty():
                raise ValueError("Failed to load face cascade classifier")
        except Exception as e:
            self.logger.error(f"Error initializing vision system: {e}")
            self.face_cascade = None

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Basic image analysis without deep learning"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            height, width = img.shape[:2]
            analysis = {
                "size": {"width": width, "height": height},
                "faces": self.detect_faces(img),
                "color_stats": self._analyze_colors(img)
            }
            return analysis
        except Exception as e:
            self.logger.error(f"Error analyzing image: {e}")
            return {"error": str(e)}

    def detect_faces(self, frame: np.ndarray) -> List[Dict[str, int]]:
        """Detect faces in image and return their locations"""
        if self.face_cascade is None:
            return []
        
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            return [
                {"x": int(x), "y": int(y), "width": int(w), "height": int(h)}
                for (x, y, w, h) in faces
            ]
        except Exception as e:
            self.logger.error(f"Face detection error: {e}")
            return []

    def _analyze_colors(self, img: np.ndarray) -> Dict[str, Any]:
        """Analyze color distribution in image"""
        try:
            # Convert to HSV for better color analysis
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Calculate average color values
            avg_color = np.mean(hsv, axis=(0, 1))
            
            # Calculate color histogram
            hist = cv2.calcHist([hsv], [0], None, [180], [0, 180])
            dominant_hue = np.argmax(hist)
            
            return {
                "average_hue": float(avg_color[0]),
                "average_saturation": float(avg_color[1]),
                "average_value": float(avg_color[2]),
                "dominant_hue": int(dominant_hue)
            }
        except Exception as e:
            self.logger.error(f"Color analysis error: {e}")
            return {}
