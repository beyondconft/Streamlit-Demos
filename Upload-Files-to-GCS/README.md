# GoogleCloud: Upload Files to Google Cloud Storage using Streamlit
Single-page application to upload files to Google Cloud Storage using Streamlit.  

## Pre-requisites
1. Activate virtual python environment
```
python3 -m venv venv
source venv/bin/activate
```
2. [Install Streamlit in Python Virtual Environment](https://docs.streamlit.io/library/get-started/installation) \
   ``` pip install streamlit ```
3. [Install Google Cloud Vertex AI Python SDK](https://cloud.google.com/vertex-ai/docs/start/install-sdk) \
   ``` pip install google-cloud-aiplatform ```
4. [Authenticate to Google Cloud](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login) \
   ``` gcloud auth application-default login ```
5. Create .env file and set the following Environment Variables 
   ```
         export BUCKET_NAME = <google-cloud-storage-bucket-name>
   ```
   
| **Environment Variable** | **Description** |
| --- | --- |
| BUCKET_NAME | Google Cloud Storage Bucket Name | 

## Run Application
`streamlit run UploadFiles2GCS.py`