from flask import Flask, request, jsonify
from os.path import exists
import sys
import subprocess
import os
import json


app = Flask(__name__)
DIR = '/mnt/project_storage/sources/'

@app.route('/compile')
def compile():
    id = request.args.get('id')
    compiler = request.args.get('compiler')
    version = request.args.get('version')
    print(id)
    print(compiler)

    if not version :
        version = "latest"

    #task = subprocess.run([sys.executable, '-c', 'test.sh'], capture_output=True, text=True)
    #print(task)
    memory = subprocess.Popen(['./compiler.sh', id, compiler, version], stdout=subprocess.PIPE, encoding='utf-8', universal_newlines=True)
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
    version = request.args.get('version') 

    if not version:
        version = "latest"

    file = DIR + id + "/" + version + path

    if not exists(file):
        return "File not found", 400

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

    return jsonify(path_to_dict(DIR + id + '/')), 200

@app.route('/create')
def createProject():
    id = request.args.get('id')
    project = DIR + id

    if exists(project):
        return "Project with this id already exists", 400

    template = request.args.get('template')
    memory = subprocess.Popen(['./create.sh', id, template], stdout=subprocess.PIPE, encoding='utf-8', universal_newlines=True)

    return jsonify(path_to_dict(DIR + id + '/')), 200

@app.route('/new-file', methods=['POST'])
def newFile():
    project = request.form.get('project')
    filename = request.form.get('filename')
    file_extension = request.form.get('extension')
    file = DIR + project + '/latest' + filename + file_extension

    if exists(file):
        return "File with this name already exists", 400

    open(file, 'a').close()

    return "Created", 200

@app.route('/write', methods=['POST'])
def writeFile():
    project = request.form.get('project')
    path = request.form.get('file')
    content = request.form.get('content')

    file = DIR + project + path + "/latest"

    if not exists(file):
        return "Unknown file", 404

    f = open(file, "w")
    f.write(content)
    f.close()

    return "Saved", 200

@app.route('/delete')
def deleteFile():
    project = request.args.get('id')
    path = request.args.get('path')

    file = DIR + project + path + "/latest"

    if not exists(file):
        return "Unknown file", 404

    os.remove(file)

    return "Deleted", 200

@app.route('/archive', methods=['GET'])
def archive():
    id = request.args.get('id')
    version = request.args.get('version')

    memory = subprocess.Popen(['./archive.sh', id, version], stdout=subprocess.PIPE, encoding='utf-8', universal_newlines=True)

    print(memory)
    out, error = memory.communicate()
    print(out)
    out = out.replace('\n', '<br>')
    return out

if __name__ == '__main__':
    from waitress import serve
    from flask_cors import CORS

    CORS(app, resources={r"*": {"origins": "*"}})
    serve(app, host="0.0.0.0", port=8080)
