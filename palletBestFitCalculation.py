import tempfile
import os
import pandas as pd
from googleapiclient.http import MediaFileUpload

def generate_and_upload_excel(df, folder_id, drive_service):
    result_filename = "Pallet Best Fit Result.xlsx"

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        tmp.flush()
        tmp.seek(0)

        # Upload the file to the same Google Drive folder
        file_metadata = {
            'name': result_filename,
            'parents': [folder_id],
            'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }

        media_body = MediaFileUpload(tmp.name, mimetype=file_metadata['mimeType'])

        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media_body,
            fields='id'
        ).execute()

    # Cleanup temp file
    os.unlink(tmp.name)

    return {
        'outputFileId': uploaded_file['id'],
        'outputFileName': result_filename
    }
