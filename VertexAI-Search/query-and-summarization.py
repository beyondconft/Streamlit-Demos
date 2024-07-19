import streamlit as st
import sys
import os
from dotenv import load_dotenv, dotenv_values
import vertexai
from typing import List
import re
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1alpha as discoveryengine
import vertexai.preview.generative_models as generative_models
from vertexai.generative_models import (
    GenerativeModel,
    GenerationConfig,
    HarmCategory,
    HarmBlockThreshold,
)

def generate(PROMPT_GEMINI: str) -> str:
    """
    Given the prompt
    output the summarized response to user's original query
    """
    
    model = GenerativeModel("gemini-1.0-pro")  # specify the Gemini model version
    #model = GenerativeModel("gemini-1.5-pro-001")  # specify the Gemini model version
    #model = GenerativeModel("gemini-1.5-pro-001",)
    #model = GenerativeModel("gemini-1.5-flash-001",)
    
    responses = model.generate_content(
        PROMPT_GEMINI,
        generation_config=generation_config,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        stream=False,
    )
    
    st.write(responses.text)

# load variables from .env file
load_dotenv()

my_project_id = os.environ["PROJECT_ID"]
my_search_app_location = os.environ["SEARCH_APP_LOCATION"]
my_search_engine_id = os.environ["SEARCH_ENGINE_ID"]
my_location_gemini_model = os.environ["LOCATION_GEMINI_MODEL"]
my_datastore_name = os.environ["DATASTORE_NAME"]
my_datastore_id = os.environ["DATASTORE_ID"]

left_co, cent_co,last_co = st.columns(3)

with cent_co:
    st.image('build-with-gemini.png')

st.title('Search a Datastore Using Google Gemini')

vertexai.init(project=my_project_id, location=my_location_gemini_model)

with st.form("my_form"):
    search_query = st.text_input("LLM Prompt", label_visibility="hidden")
    submit = st.form_submit_button('Ask Question')
    
if submit:
    # Create a client using a regional endpoint
    client = discoveryengine.SearchServiceClient(
        client_options=(
            ClientOptions(
                api_endpoint=f"{my_search_app_location}-discoveryengine.googleapis.com"
            )
            if my_search_app_location != "global"
            else None
        )
    )

    # The full resource name of the search app serving config
    serving_config = f"projects/{my_project_id}/locations/{my_search_app_location}/collections/default_collection/engines/{my_search_engine_id}/servingConfigs/default_config"

    response = client.search(
        discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=search_query,
            page_size=10,
        )
    )
    
    retrieved_data: List[str] = []

    for result in response.results:
        data = result.document.derived_struct_data
        if not data:
            continue

        snippets: List[str] = [
            re.sub("<[^>]*>", "", snippet_item.get("snippet", ""))
            for snippet_item in data.get("snippets", [])
            if snippet_item.get("snippet")
        ]

        extractive_answers: List[str] = [
            re.sub("<[^>]*>", "", snippet_item.get("content", ""))
            for snippet_item in data.get("extractive_answers", [])
            if snippet_item.get("content")
        ]

        if snippets:
            title = data.get("title", "Unknown Title")
            retrieved_data.append(
                f"--- Snippets from Document {title} ---\n{''.join(snippets)}\n"
            )
        elif extractive_answers:
            title = data.get("link", "Unknown")
            retrieved_data.append(
                f"--- Snippets from Document {title} ---\n{''.join(extractive_answers)}\n"
            )
            
    generation_config = GenerationConfig(
    temperature=0,
    top_p=1.0,
    max_output_tokens=8192,
    )
    
    # Prompt for Gemini Pro model
    PROMPT_GEMINI = f"""Provide an answer to the question based on the information in the Document snippets provided with citations.
    Question: {search_query}
    {''.join(retrieved_data)}
    """
    
    print(f"PROMPT:\n{PROMPT_GEMINI}")

    print("Gemini Response:\n")
    generate(PROMPT_GEMINI)
    