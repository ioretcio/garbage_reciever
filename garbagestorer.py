from flask import Flask, request, Response, send_file,  make_response
import os
import requests
import json

app = Flask(__name__)
app.config["DEBUG"] = False
url = "http://194.35.13.94:5000/getmail"
rootdir = "/srv/ftp/mediastorage"

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
    
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5674)
