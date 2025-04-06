import streamlit as st
import requests
from PIL import Image
import pandas as pd

def call_insects_api(image_file):
    api_endpoint = "http://127.0.0.1:8085/insects-predict"
    response = requests.post(api_endpoint, files={"image":image_file})
    response.raise_for_status()
    if response.status_code==200:
        return response
    
def set_custom_style():
    # Add custom CSS to make the app look more like a garden website
    st.markdown("""
    <style>
        .main {
            background-color: #f5f7f0;
        }
        h1, h2, h3 {
            color: #2e6930;
            font-family: 'Georgia', serif;
        }
        .stButton>button {
            background-color: #4c8c4a;
            color: white;
            border-radius: 5px;
            font-weight: bold;
            border: none;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #3a6b39;
        }
        .upload-header {
            background-color: #e8f3e8;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #4c8c4a;
            margin-bottom: 20px;
        }
        .result-container {
            background-color: #e8f3e8;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .info-box {
            background-color: #f0f5e9;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #c3d9c4;
            margin: 10px 0;
        }
        .footer {
            margin-top: 50px;
            text-align: center;
            color: #666;
            border-top: 1px solid #ddd;
            padding-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

def render_insects_form():
    st.markdown("<div class='upload-header'>", unsafe_allow_html=True)
    st.header("🐞 Insect Identification Tool")
    st.markdown("Upload a photo of an insect from your garden to identify it and learn more about it.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Upload your image")
        image_file = st.file_uploader("Select a clear photo of the insect", type=["jpg", "jpeg", "png"])
        
        if image_file is not None:
            st.image(
                image_file, 
                width=300,
                caption="Uploaded Image", 
                use_container_width=True
            )
            is_clicked = st.button("Identify Insect 🔍")
        else:
            st.markdown("<div class='info-box'>📸 Tips for good photos: Make sure the insect is clearly visible and in focus. Good lighting helps!</div>", unsafe_allow_html=True)
    
    with col2:
        if image_file is not None and 'is_clicked' in locals() and is_clicked:
            with st.spinner("Analyzing your image..."):
                try:
                    response = call_insects_api(image_file)
                    results = response.json()
                    
                    st.markdown("<div class='result-container'>", unsafe_allow_html=True)
                    st.markdown("### 🔎 Identification Results")
                    
                    # Format and display results in a more attractive way
                    if isinstance(results, dict) and 'predictions' in results:
                        predictions_df = pd.DataFrame(results['predictions'])
                        
                        # Extract top prediction
                        top_prediction = predictions_df.iloc[0]
                        st.markdown(f"#### Identified as: **{top_prediction['class']}**")
                        st.markdown(f"Confidence: **{top_prediction['confidence']:.1%}**")
                        
                        # Show all predictions in a table
                        st.markdown("##### Other possibilities:")
                        st.dataframe(
                            predictions_df.rename(
                                columns={"class": "Species", "confidence": "Confidence"}
                            ).assign(Confidence=lambda df: df['Confidence'].map("{:.1%}".format))
                        )
                        
                        # Display insect information (this would come from the API in a real implementation)
                        st.markdown("#### About this insect:")
                        st.markdown(f"*Information about {top_prediction['class']} would appear here.*")
                        
                    else:
                        st.write(results)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.balloons()
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
        else:
            st.markdown("### About Insect Identification")
            st.markdown("""
            <div class='info-box'>
            Our AI-powered tool can help you identify common garden insects, including:
            
            * Beneficial pollinators like bees and butterflies
            * Potential pests that might damage your plants
            * Harmless garden visitors
            
            After identification, you'll learn if the insect is beneficial or harmful to your garden ecosystem.
            </div>
            """, unsafe_allow_html=True)

def app():
    st.set_page_config(
        page_title="Garden Insect Identifier",
        page_icon="🦋",
        layout="wide",
        initial_sidebar_state="auto",
    )
    
    set_custom_style()

    # Main header with garden theme
    st.title("🌿 Garden Insect Identifier 🦋")
    
    # Intro text
    st.markdown("""
    Welcome to the Garden Insect Identifier! This tool helps gardeners identify insects in their gardens 
    and determine whether they're beneficial pollinators, harmless visitors, or potential pests.
    """)
    
    # Horizontal separator for visual appeal
    st.markdown("<hr style='border: 1px solid #c3d9c4; margin: 30px 0px;'>", unsafe_allow_html=True)
    
    # Main content
    render_insects_form()
    
    # Footer
    st.markdown("""
    <div class='footer'>
        <p>Garden Insect Identifier | Helping gardeners create balanced ecosystems</p>
        <p>Upload images of garden insects to get instant AI-powered identification</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()