import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason, Tool
import vertexai.preview.generative_models as generative_models
import streamlit as st
from io import StringIO
import os
from dotenv import load_dotenv, dotenv_values



def generate():
    
    # load variables from .env file
    load_dotenv()

    my_project = os.environ["PROJECT"]
    my_location = os.environ["LOCATION"]
    gcs_uri = os.environ["GCS_URI"]

    vertexai.init(project=my_project, location=my_location)
    
    document1 = Part.from_uri(
            mime_type="application/pdf",
            uri=gcs_uri
            )

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
    
    model = GenerativeModel(
        "gemini-1.5-flash-001",
    )
    
    response = model.generate_content(
        [document1, prompt],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )

    print(response.text)
    return response.text


####



    
left_co, cent_co,last_co = st.columns(3)

with cent_co:
    st.image('build-with-gemini.png')

st.title('Search a PDF Using Google Gemini')

with st.form("my_form"):
    prompt = st.text_input("LLM Prompt", label_visibility="hidden")
    submit = st.form_submit_button('Ask Question')
        
if submit:
    response = generate()
    st.write(response)

