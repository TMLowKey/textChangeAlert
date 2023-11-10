import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
from PIL import ImageGrab
import numpy as np
import cv2
import time
import winsound
import pytesseract
import threading


# Define global variables to store x1, y1, x2, y2
x1_global = None
y1_global = None
x2_global = None
y2_global = None

coordinates_set_event = threading.Event()

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capture the screen...')
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        global x1_global, y1_global, x2_global, y2_global

        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        x1_global = x1
        y1_global = y1
        x2_global = x2
        y2_global = y2

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save('capture.png')
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        cv2.imshow('Captured Image', img)
        #cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Signal that coordinates are set
        coordinates_set_event.set()

    def imageProcessing(self):
        # Wait for the coordinates to be set
        coordinates_set_event.wait()

        print("Coordinates are set, starting image processing...")

        starttime = time.monotonic()
        while True:
            bbox = (x1_global, y1_global, x2_global, y2_global)
            screenshot = ImageGrab.grab(bbox)
            screenshot.save("screenshot.png")

            time.sleep(2 - ((time.monotonic() - starttime) % 2))

            screenshot2 = ImageGrab.grab(bbox)

            # Extract text from images using Tesseract with specific configurations
            text1 = pytesseract.image_to_string(screenshot, config="--oem 3 -l eng")
            text2 = pytesseract.image_to_string(screenshot2, config="--oem 3 -l eng")

            print(text1)
            print(text2)

            if text1 == text2:
                print("Screenshots are identical.")
            elif (("Local [11]") in text1 and ("Local [14]") in text2) or (("Local [14]") in text1 and ("Local [11]") in text2):
                print("error")
            else:
                print("Screenshots are different.")
                print("Playing the file 'alertSound.wav'")
                winsound.PlaySound("alertSound.wav", winsound.SND_ALIAS)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()

    # Start the imageProcessing function in a separate thread
    processing_thread = threading.Thread(target=window.imageProcessing)
    processing_thread.start()

    app.aboutToQuit.connect(app.deleteLater)

    sys.exit(app.exec_())
