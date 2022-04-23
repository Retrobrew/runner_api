from flask import Flask, request
import sys
import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
    id = request.args.get('id')
    task = subprocess.run([sys.executable, '-c', 'print(' + str(id) + ')'], capture_output=True, text=True)
    print(task)
    memory = subprocess.Popen(['./test.sh'], stdout=subprocess.PIPE)
    print(memory)
    out, error = memory.communicate()
    return out


if __name__ == '__main__':
    app.run()
