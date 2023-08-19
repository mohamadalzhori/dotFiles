# event_widget.py

import subprocess
import time
from libqtile.widget import TextBox
import threading

class NextEventWidget(TextBox):
    def __init__(self, update_interval=10, *args, **kwargs):
        self.update_interval = update_interval
        super().__init__(*args, **kwargs)
        self.update_thread = threading.Thread(target=self.update_thread_function, daemon=True)
        self.update_thread.start()

    def update_thread_function(self):
        while True:
            api_output = self.run_api_script()
            if api_output is not None:
                self.text = api_output
            time.sleep(self.update_interval)

    def run_api_script(self):
        script_path = "/home/zhori/.local/bin/scripts/gcal.py"
        result = subprocess.run(["python3", script_path], capture_output=True, text=True)
        if result.returncode == 0:
            api_output = result.stdout.strip()
            return api_output
        else:
            self.log_message(result.stderr)
            return None

    def log_message(self, message):
        print("Error:", message)  # You can customize this to log or display the error

def create_next_event_widget():
    return NextEventWidget(text="")

