import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason, Tool
import vertexai.preview.generative_models as generative_models
import streamlit as st
from io import StringIO
import os
from dotenv import load_dotenv, dotenv_values
from google.cloud import discoveryengine_v1alpha as discoveryengine
from google.api_core.client_options import ClientOptions
from typing import List


def create_engine(
    project_id: str, location: str, data_store_name: str, data_store_id: str
):
    # Create a client
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )
    client = discoveryengine.EngineServiceClient(client_options=client_options)

    # Initialize request argument(s)
    config = discoveryengine.Engine.SearchEngineConfig(
        search_tier="SEARCH_TIER_ENTERPRISE", search_add_ons=["SEARCH_ADD_ON_LLM"]
    )

    engine = discoveryengine.Engine(
        display_name=data_store_name,
        solution_type="SOLUTION_TYPE_SEARCH",
        industry_vertical="GENERIC",
        data_store_ids=[data_store_id],
        search_engine_config=config,
    )

    request = discoveryengine.CreateEngineRequest(
        parent=discoveryengine.DataStoreServiceClient.collection_path(
            project_id, location, "default_collection"
        ),
        engine=engine,
        engine_id=engine.display_name,
    )

    # Make the request
    operation = client.create_engine(request=request)
    response = operation.result(timeout=90)
    

def search_sample(
    project_id: str,
    location: str,
    data_store_id: str,
    search_query: str,
) -> List[discoveryengine.SearchResponse]:
    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.SearchServiceClient(client_options=client_options)

    # The full resource name of the search engine serving config
    # e.g. projects/{project_id}/locations/{location}/dataStores/{data_store_id}/servingConfigs/{serving_config_id}
    serving_config = client.serving_config_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        serving_config="default_config",
    )

    # Optional: Configuration options for search
    # Refer to the `ContentSearchSpec` reference for all supported fields:
    # https://cloud.google.com/python/docs/reference/discoveryengine/latest/google.cloud.discoveryengine_v1.types.SearchRequest.ContentSearchSpec
    content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
        # For information about snippets, refer to:
        # https://cloud.google.com/generative-ai-app-builder/docs/snippets
        snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
            return_snippet=True
        ),
        # For information about search summaries, refer to:
        # https://cloud.google.com/generative-ai-app-builder/docs/get-search-summaries
        summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
            summary_result_count=5,
            include_citations=True,
            ignore_adversarial_query=True,
            ignore_non_summary_seeking_query=True,
        ),
    )

    # Refer to the `SearchRequest` reference for all supported fields:
    # https://cloud.google.com/python/docs/reference/discoveryengine/latest/google.cloud.discoveryengine_v1.types.SearchRequest
    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        page_size=10,
        content_search_spec=content_search_spec,
        query_expansion_spec=discoveryengine.SearchRequest.QueryExpansionSpec(
            condition=discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
        ),
        spell_correction_spec=discoveryengine.SearchRequest.SpellCorrectionSpec(
            mode=discoveryengine.SearchRequest.SpellCorrectionSpec.Mode.AUTO
        ),
    )

    response = client.search(request)
    return response

###

left_co, cent_co,last_co = st.columns(3)

with cent_co:
    st.image('build-with-gemini.png')

st.title('Search a Datastore Using Google Gemini')

# load variables from .env file
load_dotenv()

my_project_id = os.environ["PROJECT_ID"]
my_location = os.environ["LOCATION"]
my_datastore_name = os.environ["DATASTORE_NAME"]
my_datastore_id = os.environ["DATASTORE_ID"]

# create_engine(my_project_id, my_location, my_datastore_name, my_datastore_id)

with st.form("my_form"):
    query = st.text_input("LLM Prompt", label_visibility="hidden")
    submit = st.form_submit_button('Ask Question')
    
if submit:
    response = search_sample(my_project_id, my_location, my_datastore_id, query)
    st.write(response.summary.summary_text)
