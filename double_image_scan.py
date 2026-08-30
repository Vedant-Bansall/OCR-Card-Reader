#Imports
#Imports for testing
from aqt.qt import QAction, QThread, qconnect, pyqtSignal

#print("path")
from pathlib import Path
#print("path")
from google import genai
#print("genai")
from aqt import mw

#Creating and configuring Background Thread
class Background(QThread):
    scan_finished = pyqtSignal(str, str)

    def run(self):
        # Get API Key
        config = mw.addonManager.getConfig(__name__)
        api_key = config["api_key"]

        # print("client created")
        # Create client
        client = genai.Client(api_key=api_key)

        # print("variables created")
        # Front and Back Variables Creation
        current_dir = Path(__file__).parent.absolute()
        image_path = f"{current_dir}/ImagePaths.txt"

        with open(image_path, "r") as Paths:
            front = Paths.readline().strip()
            back = Paths.readline().strip()

        # print("front and back uploaded")
        front_uploaded = client.files.upload(file=front)
        back_uploaded = client.files.upload(file=back)

        # Create Front
        front_interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=[
                {"type": "text",
                 "text": "Type out what the image says and only the text (Nothing like: 'here is what the image says' and then the text"},
                {
                    "type": "image",
                    "uri": front_uploaded.uri,
                    "mime_type": front_uploaded.mime_type
                }
            ]
        )

        # print("front interaction created")
        # Create Back
        back_interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=[
                {"type": "text",
                 "text": "Type out what the image says and only the text (Nothing like: 'here is what the image says' and then the text"},
                {
                    "type": "image",
                    "uri": back_uploaded.uri,
                    "mime_type": back_uploaded.mime_type
                }
            ]
        )

        self.scan_finished.emit(front_interaction.output_text, back_interaction.output_text)

background = Background()
background.start()

action = QAction("Image Scan Test", mw)
qconnect(action.triggered, background.run)
mw.form.menuTools.addAction(action)