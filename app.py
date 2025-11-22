from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# ✅ Use the latest Gemini model (supports vision input too)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")  # or "gemini-1.5-pro"

# ✅ Function to get response from Gemini
def get_gemini_response(prompt_text, image_parts, question):
    response = model.generate_content([prompt_text, image_parts[0], question])
    return response.text

# ✅ Extract image details
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# ✅ Streamlit UI setup
st.set_page_config(page_title="Multilingual Invoice Extractor")
st.header("🧾 Multilingual Invoice Extractor")

question = st.text_input("Ask something about the invoice:", key="input")
uploaded_file = st.file_uploader("Upload an image of the invoice...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice", use_column_width=True)

submit = st.button("Analyze Invoice")

prompt_text = """
You are an expert in analyzing invoices.
Look at the uploaded image and answer questions accurately
based on the content of the invoice (any language).
"""

if submit:
    if uploaded_file is None:
        st.error("Please upload an image first.")
    else:
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(prompt_text, image_data, question)
        st.subheader("The Response is:")
        st.write(response)
