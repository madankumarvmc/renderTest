from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import io
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from palletBestFitCalculation import pallet_capacity
from saveFileToDrive import generate_and_upload_excel


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    # return '✅ Flask is running. Use POST /run to trigger your script.'
    return jsonify({"status": "received", "fileId": "file_id"})


# Setup service account credentials
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    folder_id = data.get('folderId')
    file_name = data.get('fileName')

    if not folder_id or not file_name:
        return jsonify({'error': 'Missing folderId or fileName'}), 400

    try:
        # Search for the file in the specified folder by name (test change)
        query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
        response = drive_service.files().list(q=query, fields="files(id, name)").execute()
        files = response.get('files', [])

        if not files:
            return jsonify({'error': f"File '{file_name}' not found in folder."}), 404

        file_id = files[0]['id']

        # Download the file
        request_file = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request_file)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        fh.seek(0)
        
        # Get the Pallet best fit result
        try:
            pallet_capacity_df = pallet_capacity(fh)
        except Exception as e:
            return jsonify({'error': f'Sheet reading failed: {str(e)}'}), 500

        # Save the excel file to the Drive
        result = generate_and_upload_excel(pallet_capacity_df, folder_id, drive_service)

        return jsonify({
            'status': 'success',
            'rows': len(pallet_capacity_df),
            **result  # merges outputFileId and outputFileName
})

    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # data = request.get_json()
    # file_id = data.get("fileId")
    
    # if not file_id:
    #     return jsonify({"error": "No fileId provided"}), 400  # Return error if fileId is missing
    
    # # Here, you can implement your actual script logic (e.g., reading the file, etc.)
    # return jsonify({"status": "received", "fileId": file_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5001)))
