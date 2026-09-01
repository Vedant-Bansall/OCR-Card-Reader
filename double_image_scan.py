#Imports
#Qt
from PyQt6.QtCore import QTimer
from aqt.qt import QThread, qconnect, pyqtSignal, QDialog, QLabel, QVBoxLayout, QTextEdit, QFrame, Qt, QPushButton, QComboBox, QHBoxLayout
from aqt.utils import showCritical
from aqt import mw

#Get ImagePaths
from pathlib import Path

def start_scan():
    global background
    config = mw.addonManager.getConfig(__name__)

    #Claude's code (get it?, GET IT?, HAHAHAHHA I'M SO FUNNY HAHAHAHAH (im sorry))
    if config["provider"] == "Claude":
        import anthropic
        import base64
        import mimetypes

        class Background(QThread):
            scan_finished = pyqtSignal(str, str)
            error_signal = pyqtSignal(str)

            def __init__(self, api_key: str):
                super().__init__()
                self.api_key = api_key

            def run(self):
                # Get API Key
                api_key = config["claude_api_key"]

                # Create client
                client = anthropic.Anthropic(api_key=api_key)

                # Front and Back Variables Creation
                current_dir = Path(__file__).parent.absolute()
                image_path = f"{current_dir}/ImagePaths.txt"

                with open(image_path, "r") as Paths:
                    front = Paths.readline().strip()
                    back = Paths.readline().strip()

                # Front Base64-Encoded Image
                mime_type, _ = mimetypes.guess_type(front)
                front_media_type = mime_type
                with open(front, "rb") as image_file:
                    front_image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")

                # Back Base64-Encoded Image
                mime_type, _ = mimetypes.guess_type(back)
                back_media_type = mime_type
                with open(back, "rb") as image_file:
                    back_image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")

                # Create Front
                try:
                    front_interaction = client.messages.create(
                        model="claude-sonnet-5",
                        max_tokens=2048,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": front_media_type,
                                            "data": front_image_data,
                                        },
                                    },
                                    {"type": "text", "text": "Type out what the image says and only the text (Nothing like: 'here is what the image says' and then the text. Do not structure it with new lines, rather as a paragraph."},
                                ],
                            }
                        ],
                    )


                    # Create Back
                    back_interaction = client.messages.create(
                        model="claude-sonnet-5",
                        max_tokens=2048,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": back_media_type,
                                            "data": back_image_data,
                                        },
                                    },
                                    {"type": "text", "text": "Type out what the image says and only the text (Nothing like: 'here is what the image says' and then the text. Do not structure it with new lines, rather as a paragraph."},
                                ],
                            }
                        ],
                    )

                    self.scan_finished.emit(front_interaction.content[0].text, back_interaction.content[0].text)

                except Exception as e:
                    self.error_signal.emit(str(e))

        api_key = config["claude_api_key"]

    elif config["provider"] == "Gemini":
        from google import genai

        class Background(QThread):
            scan_finished = pyqtSignal(str, str)
            error_signal = pyqtSignal(str)

            def __init__(self, api_key: str):
                super().__init__()
                self.api_key = api_key

            def run(self):
                # Get API Key
                config = mw.addonManager.getConfig(__name__)
                api_key = config["gemini_api_key"]

                # Create client
                client = genai.Client(api_key=api_key)

                # Front and Back Variables Creation
                current_dir = Path(__file__).parent.absolute()
                image_path = f"{current_dir}/ImagePaths.txt"

                with open(image_path, "r") as Paths:
                    front = Paths.readline().strip()
                    back = Paths.readline().strip()

                #front and back uploaded
                front_uploaded = client.files.upload(file=front)
                back_uploaded = client.files.upload(file=back)

                # Create Front
                try:
                    front_interaction = client.interactions.create(
                        model="gemini-3.6-flash",
                        input=[
                            {"type": "text",
                             "text": "Type out what the image says and only the text (Example of what not to do: 'here is what the image says' and then the text. Do not structure it with new lines, rather as a paragraph."},
                            {
                                "type": "image",
                                "uri": front_uploaded.uri,
                                "mime_type": front_uploaded.mime_type
                            }
                        ]
                    )

                    # Create Back
                    back_interaction = client.interactions.create(
                        model="gemini-3.6-flash",
                        input=[
                            {"type": "text",
                             "text": "Type out what the image says and only the text (Nothing like: 'here is what the image says' and then the text. Do not structure it with new lines, rather as a paragraph."},
                            {
                                "type": "image",
                                "uri": back_uploaded.uri,
                                "mime_type": back_uploaded.mime_type
                            }
                        ]
                    )

                    self.scan_finished.emit(front_interaction.output_text, back_interaction.output_text)

                except Exception as e:
                    self.error_signal.emit(str(e))

        api_key = config["gemini_api_key"]

    elif config["provider"] == "ChatGPT":
        from openai import OpenAI
        import base64
        import mimetypes

        class Background(QThread):
            scan_finished = pyqtSignal(str, str)
            error_signal = pyqtSignal(str)

            def __init__(self, api_key: str):
                super().__init__()
                self.api_key = api_key

            def run(self):
                # Get API Key
                config = mw.addonManager.getConfig(__name__)
                api_key = config["OpenAI_api_key"]

                # Create client
                client = OpenAI(api_key=api_key)

                # Front and Back Variables Creation
                current_dir = Path(__file__).parent.absolute()
                image_path = f"{current_dir}/ImagePaths.txt"

                with open(image_path, "r") as Paths:
                    front = Paths.readline().strip()
                    back = Paths.readline().strip()

                with open(front, "rb") as image_file:
                    front_image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")
                mime_type, _ = mimetypes.guess_type(front)
                front_media_type = mime_type

                with open(back, "rb") as image_file:
                    back_image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")
                mime_type, _ = mimetypes.guess_type(back)
                back_media_type = mime_type

                # Create Front
                try:
                    #create front
                    front_interaction = client.responses.create(
                        model="gpt-5.4-mini",
                        input=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "input_text", "text": "Type out what the image says and only the text (Nothing like: 'here is what the image says' and then the text. Do not structure it with new lines, rather as a paragraph."},
                                    {
                                        "type": "input_image",
                                        "image_url": f"data:{front_media_type};base64,{front_image_data}"
                                    },
                                ],
                            }
                        ],
                    )

                    #create back
                    back_interaction = client.responses.create(
                        model="gpt-5.4-mini",
                        input=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "input_text",
                                     "text": "Type out what the image says and only the text (Nothing like: 'here is what the image says' and then the text. Do not structure it with new lines, rather as a paragraph."},
                                    {
                                        "type": "input_image",
                                        "image_url": f"data:{back_media_type};base64,{back_image_data}"
                                    },
                                ],
                            }
                        ],
                    )

                    self.scan_finished.emit(front_interaction.output_text, back_interaction.output_text)

                except Exception as e:
                    self.error_signal.emit(str(e))

        api_key = config["OpenAI_api_key"]

    background = Background(api_key)
    qconnect(background.scan_finished, scan_handler)
    qconnect(background.error_signal, show_error)

    dot_count = 0

    def loading_animation():
        nonlocal dot_count
        loading_label.setText(f"Scanning{'.' * (dot_count % 3 + 1)}")
        dot_count += 1

    global loading_dialog
    loading_dialog = QDialog(mw)
    loading_dialog.setModal(True)
    loading_dialog.setWindowTitle("Scanning...")

    global timer
    timer = QTimer()
    timer.timeout.connect(loading_animation)
    timer.setInterval(333)
    timer.start()

    loading_label = QLabel()
    loading_label.setStyleSheet("font-size: 32px; padding: 2rem;")

    loading_box = QVBoxLayout()
    loading_box.addWidget(loading_label)

    loading_dialog.setLayout(loading_box)
    loading_dialog.show()

    background.start()

def scan_handler(front_text: str, back_text: str) -> None:
    def open_back_editor():#
        front_text_edited = front_editor.toPlainText()
        config = mw.addonManager.getConfig(__name__)
        config["card_front"] = front_text_edited
        mw.addonManager.writeConfig(__name__, config)
        front_dialog.close()
        back_dialog.exec()

    def close_back_editor():
        back_text_edited = back_editor.toPlainText()
        config = mw.addonManager.getConfig(__name__)
        config["card_back"] = back_text_edited
        mw.addonManager.writeConfig(__name__, config)
        back_dialog.close()
        deck_select()

    loading_dialog.close()

    #Back Text Editor
    back_dialog = QDialog(mw)
    back_dialog.setModal(True)
    back_dialog.setFixedSize(800, 650)
    back_dialog.setWindowTitle("Edit Card Back")

    back_box = QVBoxLayout()

    back_label = QLabel("Edit Card Back")
    back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    back_label.setStyleSheet("font-size: 50px")

    back_line = QFrame()
    back_line.setFrameShape(QFrame.Shape.HLine)

    back_editor = QTextEdit()
    back_editor.setFixedSize(780, 450)
    back_editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
    back_editor.setPlainText(back_text)

    back_confirm_button = QPushButton("Confirm")
    back_confirm_button.setStyleSheet("font-size: 20px; font-weight: bold; background-color: blue; color: white; border: 1px solid white; border-radius: 5px;")
    back_confirm_button.setFixedSize(150, 75)
    back_confirm_button.clicked.connect(close_back_editor)

    back_lower_line = QFrame()
    back_lower_line.setFrameShape(QFrame.Shape.HLine)

    #Adding everything
    back_box.addWidget(back_label)
    back_box.addWidget(back_line)
    back_box.addWidget(back_editor)
    back_box.addWidget(back_lower_line)
    back_box.addWidget(back_confirm_button)

    back_dialog.setLayout(back_box)

    #Front Text Editor
    front_dialog = QDialog(mw)
    front_dialog.setModal(True)
    front_dialog.setFixedSize(800, 650)
    front_dialog.setWindowTitle("Edit Card Front")

    front_box = QVBoxLayout()

    front_label = QLabel("Edit Card Front")
    front_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    front_label.setStyleSheet("font-size: 50px")

    front_line = QFrame()
    front_line.setFrameShape(QFrame.Shape.HLine)

    front_editor = QTextEdit()
    front_editor.setFixedSize(780, 450)
    front_editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
    front_editor.setPlainText(front_text)

    front_confirm_button = QPushButton("Confirm")
    front_confirm_button.setStyleSheet("font-size: 20px; font-weight: bold; background-color: blue; color: white; border: 1px solid white; border-radius: 5px;")
    front_confirm_button.setFixedSize(150, 75)
    front_confirm_button.clicked.connect(open_back_editor)

    front_lower_line = QFrame()
    front_lower_line.setFrameShape(QFrame.Shape.HLine)

    #Adding everything
    front_box.addWidget(front_label)
    front_box.addWidget(front_line)
    front_box.addWidget(front_editor)
    front_box.addWidget(front_lower_line)
    front_box.addWidget(front_confirm_button)

    front_dialog.setLayout(front_box)
    front_dialog.exec()

def show_error(error: str) -> None:
    showCritical(str(error))
    loading_dialog.close()

def deck_select():
    def confirm_deck():
        selected_deck = deck_select.currentText()
        config = mw.addonManager.getConfig(__name__)
        config["selected_deck"] = selected_deck
        mw.addonManager.writeConfig(__name__, config)
        deck_dialog.close()
        card_creation()

    all_decks = mw.col.decks.all_names()

    #Deck select
    deck_dialog = QDialog(mw)
    deck_dialog.setModal(True)
    deck_dialog.setFixedSize(450, 200)
    deck_dialog.setWindowTitle("Deck Select")

    deck_label = QLabel("Select the deck you\n want to add this card to")
    deck_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    deck_label.setStyleSheet("font-family: 'Courier New', Courier, monospace; font-size: 24px")

    deck_select = QComboBox()
    deck_select.setFixedSize(300, 30)
    deck_select.addItems(all_decks)

    deck_confirm = QPushButton("Confirm")
    deck_confirm.setFixedSize(110, 30)
    deck_confirm.clicked.connect(confirm_deck)

    deck_row = QHBoxLayout()
    deck_row.addWidget(deck_select)
    deck_row.addWidget(deck_confirm)

    deck_box = QVBoxLayout()
    deck_box.addWidget(deck_label)
    deck_box.addLayout(deck_row)
    deck_dialog.setLayout(deck_box)
    deck_dialog.exec()

def card_creation():
    config = mw.addonManager.getConfig(__name__)
    question = config["card_front"]
    answer = config["card_back"]

    #Create card
    deck = mw.col.decks.by_name(config["selected_deck"])
    note_type = mw.col.models.by_name("Basic")
    flashcard = mw.col.new_note(note_type)
    flashcard["Front"] = question
    flashcard["Back"] = answer
    mw.col.add_note(flashcard, deck["id"])

# Testing
# action = QAction("Image Scan Test", mw)
# qconnect(action.triggered, start_scan)
# mw.form.menuTools.addAction(action)