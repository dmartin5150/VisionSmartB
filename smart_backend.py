# Import required packages

from flask import Flask, flash, request, redirect, render_template, send_from_directory,abort
from flask_cors import CORS
import pandas as pd
import json
import numpy as np

app = Flask(__name__)
CORS(app)
app.secret_key = "seamless care" # for encrypting the session
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



patientInfo = [
  {'patientName':'Seamless Apple', 'FIN':'1111111'}
]

documentInfo = [
  {'FIN':'1111111','docName': 'falls','status': 'complete'},
  {'FIN': '1111111','docName':'Isolation Precautions', 'status': 'incomplete'}
]

patient_df = pd.DataFrame(patientInfo)
document_df = pd.DataFrame(documentInfo)

print(patient_df)
print(document_df)


def get_data(request, string):
    data_requested = request[string]
    return data_requested


def get_doc_data(doc_data):
    doc_info = [{'docName': row.docName, 'status': row.status}
                          for index, row in doc_data.iterrows()] 
    return doc_info


@app.route('/patientName',methods=['POST'])
def get_patient_name_async():
    FIN = get_data(request.json, "FIN")
    patientName = patient_df[patient_df['FIN'] == FIN]
    curName = ''
    if (patientName.shape[0] != 0):
        curName = patientName['patientName']
    return json.dumps(curName), 200

@app.route('/patientData',methods=['POST'])
def get_patient_data_async():
    FIN = get_data(request.json, "FIN")
    docInfo = document_df[document_df['FIN'] == FIN]
    docInfo = [{'name':'', 'status':''}]
    if (docInfo.shape[0] != 0):
        docInfo = get_doc_data(docInfo)
    return json.dumps(docInfo), 200



app.run(host='0.0.0.0', port=5002)