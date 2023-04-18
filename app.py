from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/start_assistant')
def start_assistant():
    subprocess.Popen(['python', 'voice_assistant.py'])
    return 'Voice assistant has started!'

if __name__ == '__main__':
    app.run()