#Libraries from aqt
from aqt import mw
from aqt.utils import showInfo #This is not needed once the take photo feature is made
from aqt.qt import *
from aqt.qt import QDialog, QDialogButtonBox, QAction, QLabel, QVBoxLayout, QFrame, QLineEdit

#Path Library for real cd
from pathlib import Path

#Option Select GUI
def option_select() -> None:
    label = QLabel("Select file select type")
    button_box = QDialogButtonBox()
    box_layout = QVBoxLayout()
    file_option = QDialog(mw)
    line = QFrame()
    file_option.setModal(True)
    file_option.setWindowTitle("OCR Card Reader")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("font: 20px Fredo; font-weight: bold; padding-top: 20px; padding-bottom: 15px;")
    box_layout.addWidget(label)
    line.setFrameShape(QFrame.Shape.HLine)
    box_layout.addWidget(line)
    file_select_btn = button_box.addButton("Select file", QDialogButtonBox.ButtonRole.AcceptRole)
    take_photo_btn = button_box.addButton("Take Photo", QDialogButtonBox.ButtonRole.ActionRole)
    cancel_btn = button_box.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)
    button_box.setStyleSheet("display: flex; width: 65px; height: 20px; margin-right: 10px; margin-left: 10px; border: 2px solid darkgrey; margin-top: 15px; margin-bottom: 7.5px; justify-content: spaced-evenly; padding-left: 25px; padding-right: 25px;")
    box_layout.addWidget(button_box)
    #box_layout.setContentsMargins(20, 20, 20, 20)
    file_option.setLayout(box_layout)

    def on_click(btn) -> None:
        if btn == file_select_btn:
            open_files = select_files()
            current_dir = Path(__file__).parent.absolute()
            image_path = f"{current_dir}/ImagePaths.txt"
            with open(image_path, "w") as Paths:
                for image in open_files:
                    Paths.write(image + "\n")

            #add API key to config.json function
            def add_api_config():
                #debug - showInfo(f"Attempting to save: '{api_line_edit.text()}'")
                config = mw.addonManager.getConfig(__name__)
                config["api_key"] = api_line_edit.text()
                mw.addonManager.writeConfig(__name__, config)
                #more debugging - saved = mw.addonManager.getConfig(__name__)
                #also this - showInfo(str(saved))

            #Close File Option
            file_option.close()

            #API Key Input
            api_label = QLabel("Please enter a Google Gemini API Key. Click enter to continue once inputted.")
            api_label.setStyleSheet("font: 20px Fredo; font-weight: bold; padding-top: 20px; padding-bottom: 15px;")
            tutorial_label = QLabel(f'To see a tutorial on how to create one, <a href="https://youtu.be/Cl4XKgz6EJQ?si=4MlxM4faNWoTgugH">Click here</a>')
            tutorial_label.setOpenExternalLinks(True)
            api_box_layout = QVBoxLayout()
            api_line_edit = QLineEdit()
            api_line_edit.setPlaceholderText("Enter API Key")
            api_key = api_line_edit.returnPressed.connect(lambda: add_api_config())
            api_dialog = QDialog(mw)
            api_dialog.setModal(True)
            api_dialog.setWindowTitle("API Key")
            api_box_layout.addWidget(api_label)
            api_box_layout.addWidget(api_line_edit)
            api_box_layout.addWidget(tutorial_label)
            api_dialog.setLayout(api_box_layout)
            api_dialog.exec()

        elif btn == take_photo_btn:
            take_image()
        elif btn == cancel_btn:
            cancel()

    # File select functions:
    def select_files():
        open_files, _ = QFileDialog.getOpenFileNames(mw, "Select files", '', "Image Files (*.jpeg *.jpg *.jpe *.png *.avif)")
        return open_files

    def take_image():
        showInfo("This feature is still being developed! Sorry, please take an image on your phone, upload the files and select the files. Once the image taking feature is implemented in the future then you can use it.")

    def cancel():
        file_option.close()

    qconnect(button_box.clicked, on_click)
    file_option.exec()

action = QAction("OCR Card Reader", mw)
qconnect(action.triggered, option_select)
mw.form.menuTools.addAction(action)