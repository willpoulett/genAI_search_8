import streamlit as st
from dotenv import load_dotenv
import requests
import urllib.request 
import json 
import os 
import ssl  

# Load environment variables
load_dotenv()

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Initialize session state
if "initialise" not in st.session_state:
    st.session_state["initialise"] = True
    st.session_state["summary"] = None
    st.session_state["simple_summary"] = None
    st.session_state["feedback"] = False

# Define page configurations
st.set_page_config(
    page_title="NHS Websites Search App",
    layout="wide",
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Search", "Developer Evaluation Page"])

if page == "Search":
    # Page 1: NHS Websites Search
    st.title("NHS Websites Search")

    col1, col2 = st.columns([2, 1])

    def get_summary(query, simple=False):

            ENDPOINT = os.getenv("ENDPOINT_URL")
            API_KEY = os.getenv("ENDPOINT_KEY")
            
            data = {"query":"tell me about website policy"}

            body = str.encode(json.dumps(data))

            # Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
            if not API_KEY:
                raise Exception("A key should be provided to invoke the endpoint")

            headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ API_KEY)}

            req = urllib.request.Request(ENDPOINT, body, headers)

            try:
                response = urllib.request.urlopen(req)

                result = response.read()
                print(result)
                return result
            except urllib.error.HTTPError as error:
                print("The request failed with status code: " + str(error.code))

                # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
                print(error.info())
                print(error.read().decode("utf8", 'ignore'))


    def open_feedback():
        with col2:
            st.subheader("Please give Feedback:")
            subcol1, subcol2 = st.columns([1, 1])
            with subcol1:
                if st.button(":thumbsup:"):
                    st.write("YES!")
            with subcol2:
                if st.button(":thumbsdown:"):
                    st.write("No :(")
        return None

    with col1:
        # Search Bar
        query = st.text_input("Enter your search query:", "")

        subcol1, subcol2, subcol3 = st.columns([2, 1, 1])

        with subcol2:
            if st.button("Simplify"):
                print()

        with subcol3:
            if st.button("Feedback") or st.session_state["feedback"]:
                st.session_state["feedback"] = True
                open_feedback()

        if query:
            # Get summary text based on the search query
            summary = get_summary(query)

            st.markdown(f"""
            ### Summary
                        
            {summary}

            Here is a [link](https://www.england.nhs.uk/)
            """)

elif page == "Test Page":
    # Page 2: Test Page
    st.title("Test!")
    st.write("This is a test page.")


