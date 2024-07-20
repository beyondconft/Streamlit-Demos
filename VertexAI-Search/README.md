# GoogleCloud: Search a Datastore in Vertex AI and Summarize Content using Gemini with Streamlit Streamlit
Single-page application to search a Agent Builder Datastore and summarize the data using Gemini with Streamlit.  

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
         PROJECT_ID = "<gcp-project-id>"
         LOCATION = "global"
         DATASTORE_NAME = "<datastore_name>"
         DATASTORE_ID = "<datastore_id>"
         SEARCH_APP_LOCATION = "global"
         SEARCH_ENGINE_ID = "search_engine_id"
         LOCATION_GEMINI_MODEL = "<gcp_region>"
   ```
   
| **Environment Variable** | **Description** |
| --- | --- |
| PROJECT_ID | Google Cloud Project ID |
| LOCATION | global |
| DATASTORE_NAME | Google Cloud Agent Builder Datastore Name |
| DATASTORE_ID | Google Cloud Agent Builder Datastore ID |
| SEARCH_APP_LOCATION | global |
| SEARCH_ENGINE_ID | Google Cloud Agent Builder Search Engine ID |
| LOCATION_GEMINI_MODEL | Google Cloud Region |


## Run Application
`streamlit run query-and-summarization.py`