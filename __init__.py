#Libraries from aqt
from aqt import mw
from aqt.utils import showInfo, showCritical  # This is not needed once the take photo feature is made
from aqt.qt import *
from aqt.qt import QDialog, QDialogButtonBox, QAction, QLabel, QVBoxLayout, QFrame, QLineEdit

#Path Library for real cd
import sys
from pathlib import Path

from . import double_image_scan

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
    file_select_btn = button_box.addButton("Select 2 files", QDialogButtonBox.ButtonRole.AcceptRole)
    take_photo_btn = button_box.addButton("Take Photo", QDialogButtonBox.ButtonRole.ActionRole)
    cancel_btn = button_box.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)
    button_box.setStyleSheet("display: flex; width: 65px; height: 20px; margin-right: 10px; margin-left: 10px; border: 2px solid darkgrey; margin-top: 15px; margin-bottom: 7.5px; justify-content: spaced-evenly; padding-left: 25px; padding-right: 25px;")
    box_layout.addWidget(button_box)
    file_option.setLayout(box_layout)

    def on_click(btn) -> None:
        if btn == file_select_btn:
            open_files = select_files()
            current_dir = Path(__file__).parent.absolute()
            image_path = f"{current_dir}/ImagePaths.txt"
            with open(image_path, "w") as Paths:
                for image in open_files:
                    Paths.write(image + "\n")

            if len(open_files) > 0:
                if len(open_files) == 2:
                    #choose provider
                    config = mw.addonManager.getConfig(__name__)

                    #updates provider
                    def provider_on_click(prov_btn):
                        if prov_btn == claude:
                            config["provider"] = "Claude"
                            mw.addonManager.writeConfig(__name__, config)
                            sys.path.insert(0, str(Path(__file__).parent / "libs" / "claude"))
                            provider_dialog.close()
                        elif prov_btn == gemini:
                            config["provider"] = "Gemini"
                            mw.addonManager.writeConfig(__name__, config)
                            sys.path.insert(0, str(Path(__file__).parent / "libs" / "google-genai"))
                            provider_dialog.close()
                        elif prov_btn == chatGPT:
                            config["provider"] = "ChatGPT"
                            mw.addonManager.writeConfig(__name__, config)
                            sys.path.insert(0, str(Path(__file__).parent / "libs" / "openai"))
                            provider_dialog.close()

                    provider_label = QLabel("Select AI provider")
                    provider_button_box = QDialogButtonBox()
                    provider_box_layout = QVBoxLayout()
                    provider_dialog = QDialog(mw)
                    provider_line = QFrame()
                    provider_dialog.setModal(True)
                    provider_dialog.setWindowTitle("Select AI provider")
                    provider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    provider_label.setStyleSheet("font: 20px Fredo; font-weight: bold; padding-top: 20px; padding-bottom: 15px;")
                    provider_box_layout.addWidget(provider_label)
                    provider_line.setFrameShape(QFrame.Shape.HLine)
                    provider_box_layout.addWidget(provider_line)
                    claude = provider_button_box.addButton("Claude", QDialogButtonBox.ButtonRole.AcceptRole)
                    gemini = provider_button_box.addButton("Gemini", QDialogButtonBox.ButtonRole.ActionRole)
                    chatGPT = provider_button_box.addButton("ChatGPT", QDialogButtonBox.ButtonRole.HelpRole)
                    provider_button_box.setStyleSheet("display: flex; width: 65px; height: 20px; margin-right: 10px; margin-left: 10px; border: 2px solid darkgrey; margin-top: 15px; margin-bottom: 7.5px; justify-content: spaced-evenly; padding-left: 25px; padding-right: 25px;")
                    provider_box_layout.addWidget(provider_button_box)
                    provider_dialog.setLayout(provider_box_layout)
                    qconnect(provider_button_box.clicked, provider_on_click)
                    provider_dialog.exec()

                    #add API key to config.json function
                    def add_api_config():
                        also_config = mw.addonManager.getConfig(__name__)
                        if also_config["provider"] == "Claude":
                            prov_len = len(also_config["provider"])
                            if len(api_line_edit.text()) == 0 and prov_len != 0:
                                api_dialog.close()

                            else:
                                config_3 = mw.addonManager.getConfig(__name__)
                                config_3["api_key"] = api_line_edit.text()
                                mw.addonManager.writeConfig(__name__, config_3)
                                api_dialog.close()

                            double_image_scan.start_scan()

                        elif also_config["provider"] == "Gemini":
                            prov_len = len(also_config["provider"])
                            if len(api_line_edit.text()) == 0 and prov_len != 0:
                                api_dialog.close()

                            else:
                                config_3 = mw.addonManager.getConfig(__name__)
                                config_3["api_key"] = api_line_edit.text()
                                mw.addonManager.writeConfig(__name__, config_3)
                                api_dialog.close()

                            double_image_scan.start_scan()


                        elif also_config["provider"] == "ChatGPT":
                            prov_len = len(also_config["provider"])
                            if len(api_line_edit.text()) == 0 and prov_len != 0:
                                api_dialog.close()

                            else:
                                config_3 = mw.addonManager.getConfig(__name__)
                                config_3["api_key"] = api_line_edit.text()
                                mw.addonManager.writeConfig(__name__, config_3)
                                api_dialog.close()

                            double_image_scan.start_scan()

                    #Close File Option
                    file_option.close()

                    #API Key Input
                    api_label = QLabel("Please enter an API key (for the respective provider you chose). Click enter to continue once inputted.")
                    api_label.setStyleSheet("font: 20px Fredo; font-weight: bold; padding-top: 20px; padding-bottom: 15px;")
                    tutorial_label = QLabel(f'To see a tutorial on how to create a claude api key, <a href="https://youtu.be/vgncj7MJbVU?si=uZRm9WaEkbO4xn2X">Click here</a>; To see a tutorial on how to create a gemini api key, <a href="https://youtu.be/Cl4XKgz6EJQ?si=4MlxM4faNWoTgugH">Click here</a>; To see a tutorial on how to create a ChatGPT api key, <a href="https://youtu.be/SzPE_AE0eEo?si=e1edO44gxAK1uV_p">Click here</a>')
                    tutorial_label.setOpenExternalLinks(True)
                    info_label = QLabel("NOTE: if you have already previously entered an API key from a provider you have used this script on before (e.g you have previously inserted a gemini key), click enter with nothing in the input bar but you must have used that provider the most recent time you have ran this addon.")
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
                    api_box_layout.addWidget(info_label)
                    api_dialog.setLayout(api_box_layout)
                    api_dialog.exec()
                else:
                    file_option.close()
                    showCritical("Please insert 2 files (Front and Back respectively)!")
            else:
                file_option.close()

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
action.setShortcut("Ctrl+Shift+R")
qconnect(action.triggered, option_select)
mw.form.menuTools.addAction(action)