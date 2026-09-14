from pathlib import Path

import cv2


class Camera:

    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.capture = None

    def open(self) -> None:
        self.capture = cv2.VideoCapture(self.camera_index)
        if not self.capture.isOpened():
            raise RuntimeError("Could not open the camera.")

    def capture_image(self, output_path: str = "captured_image.jpg") -> str:
        if self.capture is None:
            self.open()

        success, frame = self.capture.read()
        if not success:
            raise RuntimeError("Could not capture an image from the camera.")

        output = Path(output_path)
        if not cv2.imwrite(str(output), frame):
            raise RuntimeError(f"Could not save image to {output}.")

        return str(output)

    def close(self) -> None:
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        cv2.destroyAllWindows()
