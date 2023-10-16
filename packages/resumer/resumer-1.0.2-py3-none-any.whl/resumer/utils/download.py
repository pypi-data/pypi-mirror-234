import os
import requests

awesome_cv_url = "https://raw.githubusercontent.com/posquit0/Awesome-CV/master/awesome-cv.cls"

current_directory = os.path.dirname(os.path.abspath(__file__))

root_directory = os.path.dirname(current_directory)

preset_directory = os.path.join(root_directory, "preset")

def download_asset():
    if os.path.exists(os.path.join(preset_directory, "awesome-cv.cls")):
        return
    r = requests.get(awesome_cv_url)
    with open(os.path.join(preset_directory, "awesome-cv.cls"), "wb") as f:
        f.write(r.content)

