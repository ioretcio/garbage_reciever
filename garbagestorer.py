from flask import Flask, request, Response, send_file,  make_response
import os
import requests
import json
import logging
app = Flask(__name__)
app.config["DEBUG"] = False
url = "http://194.35.13.94:5000/getmail"
rootdir = "/srv/ftp/mediastorage"
log_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'service.log')
print(log_file_path)

if not os.path.exists(log_file_path):
    open(log_file_path, 'w').close()



logging.basicConfig(filename=log_file_path, filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)


def printLog(text):
    logging.info(text)

printLog("Starting service")



@app.route('/sendMedia', methods=['POST'])
def upload_file():
    print("TYR")
    
    if 'file' not in request.files:
        return Response(json.dumps({"status": "No file"}), status=400)
    file = request.files['file']
    if file.filename == '':
        return Response(json.dumps({"status": "No filename"}), status=400)
    
    headers = request.headers
    token = headers.get('token')
    headers = {'token': token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        email = response_json.get('email')
        if not os.path.exists(os.path.join(rootdir, email)):
            os.mkdir(os.path.join(rootdir, email))
        if not os.path.exists(os.path.join(rootdir, email,file.filename )):
            file.save(os.path.join(rootdir, email, file.filename))
            return Response("ok", status=200) 
        return Response("file already exist", status=409) 
    
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5674)
