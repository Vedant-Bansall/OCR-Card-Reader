from aqt import mw
from aqt.utils import showCritical, showInfo
from aqt.qt import QDialog, QVBoxLayout, QComboBox, QLabel, QPushButton, QHBoxLayout, Qt
from PyQt6.QtMultimedia import QCamera, QMediaCaptureSession, QImageCapture, QMediaDevices
from PyQt6.QtMultimediaWidgets import QVideoWidget

from sys import exit

camera_devices = QMediaDevices.videoInputs()

if len(camera_devices) == 0:
    showCritical("No cameras found")

else:
    available_cameras = []
    for camera in camera_devices:
        available_cameras.append(camera.description())

    # Device Select
    if len(available_cameras) != 1:
        def selected_camera():
            selected_device = camera_select.currentText()
            camera_select_dialog.close()
            capture_image()

        camera_select_dialog = QDialog(mw)
        camera_select_dialog.setModal(True)
        camera_select_dialog.setFixedSize(450, 200)
        camera_select_dialog.setWindowTitle("Deck Select")

        camera_select_label = QLabel("Select the camera you\n want to add this card to")
        camera_select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        camera_select_label.setStyleSheet("font-family: 'Courier New', Courier, monospace; font-size: 24px")

        camera_select = QComboBox()
        camera_select.setFixedSize(300, 30)
        camera_select.addItems(available_cameras)

        camera_select_confirm = QPushButton("Confirm")
        camera_select_confirm.setFixedSize(110, 30)
        camera_select_confirm.clicked.connect(selected_camera)

        camera_select_row = QHBoxLayout()
        camera_select_row.addWidget(camera_select)
        camera_select_row.addWidget(camera_select_confirm)

        camera_select_box = QVBoxLayout()
        camera_select_box.addWidget(camera_select_label)
        camera_select_box.addLayout(camera_select_row)
        camera_select_dialog.setLayout(camera_select_box)
        camera_select_dialog.exec()

        # Capture Image
        def capture_image():
            photo_dialog = QDialog(mw)
            photo_dialog.setWindowTitle("Take Photo")

            video = QVideoWidget()
            video.setMinimumSize(640, 480)

            photo_box_layout = QVBoxLayout()

            photo_box_layout.addWidget(video)
            photo_dialog.setLayout(photo_box_layout)