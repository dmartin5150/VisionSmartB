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
  {'patientName':'Seamless Apple', 'FIN':'1111111', 'MRN':'0000000'},
  {'patientName':'Seamless Larry', 'FIN':'2222222', 'MRN':'2222222'}
]

documentInfo = [
  {'MRN':'0000000','FIN':'1111111','docType': 'falls','docStatus': 'Complete'},
  {'MRN':'0000000','FIN':'1111111','docType':'Isolation Precautions', 'docStatus': 'Not Complete'},
  {'MRN':'2222222','FIN':'2222222','docType': 'falls','docStatus': 'Complete'},
  {'MRN':'2222222','FIN':'2222222','docType':'Isolation Precautions', 'docStatus': 'Not Complete'}
]

patient_df = pd.DataFrame(patientInfo)
document_df = pd.DataFrame(documentInfo)

print(patient_df)
# print(document_df)


def get_data(request, string):
    data_requested = request[string]
    return data_requested


def get_doc_data(doc_data):
    doc_info = [{'docName': row.docName, 'status': row.status}
                          for index, row in doc_data.iterrows()] 
    return doc_info

def update_docs(FIN, docType, docValue):
    row_index = document_df.loc[(document_df['FIN'] == FIN) & (document_df['docType'] == docType)].index[0]
    document_df.loc[row_index,docType] = docValue

def getDemo(curFin):
    curdemo = patient_df.loc[patient_df['FIN'] == curFin]
    print('curdemo', curdemo )
    patientName = curdemo.iloc[0]['patientName']
    FIN = curdemo.iloc[0]['FIN']
    MRN = curdemo.iloc[0]['MRN']
    print('FIN', FIN)
    return {'patientName':patientName, 'FIN':FIN,'MRN':MRN}

def getDocStats(curFin):
    curDocs = document_df[document_df['FIN'] == curFin]
    curDocStatus={}
    curDocList =[]
    if (curDocs.shape[0] != 0):
        curDocsTypes = curDocs['docType'].drop_duplicates().to_list()
        for curDocType in curDocsTypes:
            # print('curDocType',curDocType)
            curDoc = curDocs.loc[curDocs['docType'] == curDocType]
            rowIndex=curDoc.index[0]
            docType = curDoc.iloc[0]['docType']
            docStatus = curDoc.iloc[0]['docStatus']
            curDocStatus ={'docType':docType, 'docStatus':docStatus}
            print('curdocstatus', curDocStatus)
            curDocList.append(curDocStatus)
    return curDocList




def get_all_data():
    curFINS = patient_df['FIN'].drop_duplicates().to_list()
    patDemo = {}
    patList = []
    if (len(curFINS) > 0):
        for curFin in curFINS:
            patDemo = getDemo(curFin)
            # print('patDemo',patDemo)
            patStatus= getDocStats(curFin)
            patList.append({'patDemo':patDemo,'patStatus':patStatus})
            # patList.append({'patDemo':patDemo})
        return patList
    else: 
        return [{'patDemo':{'patientName':'', 'FIN':'', 'MRN':''},'patStatus':[]}]
    


@app.route('/patientName',methods=['POST'])
def get_patient_name_async():
    FIN = get_data(request.json, "FIN")
    patientName = patient_df[patient_df['FIN'] == FIN]
    curName = ''
    if (patientName.shape[0] != 0):
        curName = patientName[0,'patientName']
    return json.dumps(curName), 200

@app.route('/patientData',methods=['POST'])
def get_patient_data_async():
    FIN = get_data(request.json, "FIN")
    docInfo = document_df[document_df['FIN'] == FIN]
    docInfo = [{'name':'', 'status':''}]
    if (docInfo.shape[0] != 0):
        docInfo = get_doc_data(docInfo)
    return json.dumps(docInfo), 200

@app.route('/updateDocs',methods=['POST'])
def update_docs_async():
    FIN = get_data(request.json, "FIN")
    docType = get_data(request.json, "docType")
    docValue = get_data(request.json, 'docValue')
    update_docs(FIN, 'status',docValue)
    return json.dumps('doc updated'), 200

@app.route('/allPatientInfo', methods=['POST'])
def get_all_data_async():
    return json.dumps(get_all_data()),200



app.run(host='0.0.0.0', port=5002)