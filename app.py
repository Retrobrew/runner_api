from flask import Flask, request
import sys
import subprocess
import os
import json
from flask import jsonify


app = Flask(__name__)

@app.route('/compile')
def compile():
    id = request.args.get('id')
    compiler = request.args.get('compiler')
    print(id)
    print(compiler)

    #task = subprocess.run([sys.executable, '-c', 'test.sh'], capture_output=True, text=True)
    #print(task)
    memory = subprocess.Popen(['./compiler.sh', id, compiler], stdout=subprocess.PIPE, encoding='utf-8', universal_newlines=True)
    #memory = subprocess.Popen(['echo hi\nhi'], stdout=subprocess.PIPE, encoding='utf-8', universal_newlines=True)

    print(memory)
    out, error = memory.communicate()
    print(out)
    out = out.replace('\n', '<br>')
    return out

@app.route('/execute')
def execute():
    id = request.args.get('id')
    print(id)

    #task = subprocess.run([sys.executable, '-c', 'test.sh'], capture_output=True, text=True)
    #print(task)
    memory = subprocess.Popen(['./executer.sh', id], stdout=subprocess.PIPE, encoding='utf-8', universal_newlines=True)
    #memory = subprocess.Popen(['echo hi\nhi'], stdout=subprocess.PIPE, encoding='utf-8', universal_newlines=True)

    print(memory)
    out, error = memory.communicate()
    print(out)
    out = out.replace('\n', '')
    return out

@app.route('/viewer')
def getFile():
    id = request.args.get('id')
    path = request.args.get('path')
    file = '/mnt/project_storage/sources/'+id+path
    f = open(file, "r")

    result = {
        "name" : path,
        "content": f.read()
    }

    print(f.read())
    return json.dumps(result)

def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir\
(path)]
    else:
        d['type'] = "file"
    return d



@app.route('/explorer')
def getDirectory():
    id = request.args.get('id')

    return jsonify(path_to_dict('/mnt/project_storage/sources/'+id+'/')), 200

@app.route('/create')
def createProject():
    id = request.args.get('id')
    template = request.args.get('template')
    memory = subprocess.Popen(['./create.sh', id, template], stdout=subprocess.PIPE, encoding='utf-8', universal_newlines=True)

    return jsonify(path_to_dict('/mnt/project_storage/sources/'+id+'/')), 200

if __name__ == '__main__':
    from waitress import serve
    from flask_cors import CORS

    CORS(app, resources={r"*": {"origins": "*"}})
    serve(app, host="0.0.0.0", port=8080)
