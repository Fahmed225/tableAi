from flask import Flask, send_from_directory, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from api.HelloApiHandler import HelloApiHandler
from langchain.chat_models import ChatOpenAI
import os
import ssl
import certifi
import openai
from langchain.document_loaders import PyPDFLoader


# this is to fix the SSL error on MacOS
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(certifi.where(), '/Users/ahmedf1/Downloads/sni.cloudflaressl.com.cer')


os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(certifi.where(),'/Users/ahmedf1/Downloads/sni.cloudflaressl.com.cer')
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): 
  ssl._create_default_https_context = ssl._create_unverified_context


app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app) #comment this on deployment
api = Api(app)


openai.verify_ssl_certs = False




@app.route('/data')
def send_data():
    return jsonify({'message': 'Hello World'})

allowed_file = lambda filename: '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf', 'json']

# create a route for accepting POST request from the client side that takes file of type pdf or json 
# and process it and return the result to the client side
@app.route('/upload', methods=['POST'])
def upload():
    # get the file from the request
    file = request.files['file']
   # check if file is blob 
    if file and allowed_file(file.filename):
        # define the uploads directory
        upload_dir = 'uploads'
        # ensure the directory exists
        os.makedirs(upload_dir, exist_ok=True)
        # save the file to the uploads folder
        file.save(os.path.join('uploads', file.filename))
        # check if the file is pdf
        if file.filename.rsplit('.', 1)[1].lower() == 'pdf':
            # call the function to process the pdf file from the uploads folder
            return process_pdf(os.path.join('uploads', file.filename))
            
        # check if the file is json
        # elif file.filename.rsplit('.', 1)[1].lower() == 'json':
        #     # call the function to process the json file
        #     return process_json(file)
       
    else:
        # return error message if the file is not allowed
        return jsonify({'error': 'File type not allowed'})
    
def process_pdf(file):
    # create a PyPDFLoader object
    loader = PyPDFLoader(file)
    pages = loader.load_and_split()
    pages_dict = [{"page_content": page.page_content, "metadata": page.metadata} for page in pages]
    return jsonify({'pages': pages_dict})
