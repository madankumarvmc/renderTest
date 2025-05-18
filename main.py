from flask import Flask, request, jsonify
# import pandas as pd
import io
import os
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload

app = Flask(__name__)

@app.route('/')
def index():
    # return '✅ Flask is running. Use POST /run to trigger your script.'
    return jsonify({"status": "received", "fileId": "file_id"})


# Setup service account credentials
# SERVICE_ACCOUNT_FILE = 'service_account.json'
# SCOPES = ['https://www.googleapis.com/auth/drive']

# creds = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# drive_service = build('drive', 'v3', credentials=creds)

@app.route('/run', methods=['POST'])
def run():
    # data = request.get_json()
    # file_id = data.get('fileId')

    # if not file_id:
    #     return jsonify({'error': 'Missing fileId'}), 400

    # try:
    #     request_file = drive_service.files().get_media(fileId=file_id)
    #     fh = io.BytesIO()
    #     downloader = MediaIoBaseDownload(fh, request_file)
    #     done = False
    #     while done is False:
    #         status, done = downloader.next_chunk()

    #     fh.seek(0)
    #     df = pd.read_excel(fh)
    #     print("Excel File Content:")
    #     print(df.head())

    #     return jsonify({'status': 'success', 'rows': len(df)})

    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

    data = request.get_json()
    file_id = data.get("fileId")
    
    if not file_id:
        return jsonify({"error": "No fileId provided"}), 400  # Return error if fileId is missing
    
    # Here, you can implement your actual script logic (e.g., reading the file, etc.)
    return jsonify({"status": "received", "fileId": "aa raha hai bhai"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5001)))
