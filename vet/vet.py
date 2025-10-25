import streamlit as st
import google.generativeai as genai
from api_key import api_key

# Configure Google Generative AI
genai.configure(api_key=api_key)

# Generation configuration for generative model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

system_prompts = [
    """
You are an experienced veterinary expert specializing in image analysis, working with a renowned animal health institution. Your expertise is essential in identifying anomalies, diseases, or health issues in animals based on diagnostic images.

Your duties include:  
1. **Thorough Examination:** Carefully analyze each diagnostic image, focusing on identifying any abnormalities, injuries, or signs of disease in the animal.  
2. **Observation Report:** Record all findings systematically, detailing any irregularities or health concerns observed in the images.  
3. **Next Steps and Advice:** Recommend follow-up actions, such as additional tests, evaluations, or procedures based on your observations.  
4. **Treatment Recommendations:** Where appropriate, suggest potential treatment options or interventions to address identified issues.  

**Key Considerations:**  
1. **Image Relevance:** Ensure your response focuses only on images related to animal health.  
2. **Image Quality:** If the image lacks clarity or is insufficient for a definitive evaluation, note that certain details are "Indeterminate due to image quality."  
3. **Disclaimer:** Always include the disclaimer: "Consult with a veterinarian before making any further decisions."  
4. **Structured Response:** Present your analysis under the following headings:  
   - Detailed Analysis  
   - Analysis Report  
   - Recommendations  
   - Treatments  

Your insights are invaluable in guiding informed decisions for animal care. Please proceed with precision and adhere to this structured approach.  
"""
]

# Initialize the generative model
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Streamlit UI setup
st.set_page_config(page_title="Medical Assistant", page_icon="🩺")


# Add custom CSS
st.markdown(
    """
    <style>
        /* General Body Styling */
        body {
            background-color: #f7f8fa;
        }
        

        /* Title Styling */
        .st-title {
            color: #4a4e69;
            text-shadow: 1px 1px 2px #8d99ae;
            font-weight: bold;
        }

        /* Sidebar Styling */
        .stSidebar {
            background-color: rgba(128, 128, 128,) !important;
            color: white !important;
        }

        /* Chat History Box */
        .chat-history {
            padding: 15px;
            background-color: #ffffff;
            border-radius: 10px;
            color: black;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
        }

        /* Input Styling */
        .stTextInput input {
            background-color: #f1f1f1;
            color: black;
            border: 1px solid #dcdcdc;
            border-radius: 5px;
        }

        /* Buttons */
        .stButton button {
            background-color: #4a4e69;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #22223b;
        }

         /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin-bottom: 2rem;
    }

    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header h2 {
        color: #e0e0e0;
        font-size: 1.5rem;
        font-weight: 400;
    }
    
    /* Container styling */
    .css-1y4p8pa {
        padding: 2rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Header
st.markdown("""
    <div class="main-header">
        <h1>HealthLens</h1>
        <h2>An AI-Powered Medical Diagnosis </h2>
    </div>
""", unsafe_allow_html=True)

# File uploader for image analysis
file_uploaded = st.file_uploader('Upload the image for Analysis',
                                 type=['png', 'jpg', 'jpeg'])

if file_uploaded:
    st.image(file_uploaded, width=200, caption='Uploaded Image')

submit = st.button("Generate Analysis")

if submit and file_uploaded:
    image_data = file_uploaded.getvalue()

    image_parts = [
        {
            "mime_type": "image/jpg",
            "data": image_data
        }
    ]

    prompt_parts = [
        image_parts[0],
        system_prompts[0],
    ]

    response = model.generate_content(prompt_parts)
    if response:
        st.title('Detailed analysis based on the uploaded image')
        st.write(response.text)

# Adding a Chatbot with Chat History and "Enter" Submission
st.sidebar.title("Chatbot Assistant 💬")
st.sidebar.write("Ask any medical-related questions about animal care and health.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Create a form for text input and handle Enter key submission
with st.sidebar.form(key="chat_form", clear_on_submit=True):
    user_query = st.text_input("Type your question here:", key="chat_input")
    submit_query = st.form_submit_button("Ask")

# Process the query when the form is submitted
if submit_query and user_query:
    chatbot_prompt = f"""
    You are an expert veterinarian assistant. Please answer the following user query accurately and professionally:
    User Query: {user_query}
    """
    chat_response = model.generate_content([chatbot_prompt])
    
    # If a response is generated, add to chat history
    if chat_response:
        st.session_state.chat_history.append({"user": user_query, "bot": chat_response.text})
    else:
        st.session_state.chat_history.append({"user": user_query, "bot": "Sorry, I couldn't process your query. Please try again."})

# Display chat history
if st.session_state.chat_history:
    st.sidebar.write("### Chat History:")
    for chat in st.session_state.chat_history:
        st.sidebar.markdown(f"<div class='chat-history'><strong>You:</strong> {chat['user']}<br><strong>Bot:</strong> {chat['bot']}</div>", unsafe_allow_html=True)

# Footer information
st.sidebar.markdown("---")
st.sidebar.markdown("**Note:** The chatbot is for informational purposes only. Always consult a professional veterinarian for specific concerns.")

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 1rem; 
                background: rgba(255, 255, 255, 0.1); border-radius: 10px;">
        <p style="color: #e0e0e0; font-size: 0.9rem;">
            Made with ❤️ for healthcare  
        </p>
    </div>
""", unsafe_allow_html=True)