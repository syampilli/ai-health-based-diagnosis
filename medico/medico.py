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

You are an experienced medical expert with specialized skills in image analysis, working for a prestigious hospital. Your role is pivotal in identifying anomalies, diseases, or health concerns within medical images.

Your duties include:  

1. **Thorough Examination:** Carefully analyze each medical image, emphasizing the detection of irregularities or potential health issues.  
2. **Observation Report:** Record all findings systematically, detailing any abnormalities or indications of illness.  
3. **Next Steps and Advice:** Recommend follow-up actions, such as additional tests or evaluations, based on your observations.  
4. **Lifestyle Recommendations:** Provide clear and actionable dos and don’ts for maintaining or improving health.  
        - **Dos:** Highlight healthy habits, exercises, or routines that may benefit the user.  
        - **Don’ts:** Caution against harmful practices, habits, or behaviors that may worsen their condition.
        - **Food:** What type of food to take and avoid   

5. **Treatment Recommendations:** Where applicable, suggest potential treatment options or interventions to address identified issues

**Key Considerations:**  

1. **Image Relevance:** Ensure your response focuses solely on images related to human health concerns only.  
2. **Image Quality:** If the image lacks clarity or is insufficient for a definitive evaluation, note that certain details are "Indeterminate due to image quality."  
3. **Disclaimer:** Always include the disclaimer: "Consult with a doctor before making any further decisions."  
4. **Structured Response:** Present your analysis under the following headings:  
   - Detailed Analysis  
   - Analysis Report  
   - Recommendations 
   - Treatments  

Your expertise is critical in guiding informed decisions. Please proceed with precision and adherence to this framework.  

"""
]

# Initialize the generative model
model = genai.GenerativeModel(model_name="gemini-2.0-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Streamlit UI setup
st.set_page_config(page_title="Medical Assistant", page_icon="🩺")

# Add custom CSS for dark mode
st.markdown(
    """
    <style>
        /* General Body Styling */
        body {
            background-color: #121212;
            color: #e0e0e0;
        }

        /* Title Styling */
        .st-title {
            color: #4A90E2;
            text-shadow: 1px 1px 2px #1E1E2E;
            font-weight: bold;
        }

        /* Sidebar Styling */
        .stSidebar {
            background-color: #1E1E2E !important;
            color: #e0e0e0 !important;
        }

        /* Chat History Box */
        .chat-history {
            padding: 15px;
            background-color: #1E1E2E;
            border-radius: 10px;
            color: #e0e0e0;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
        }

        /* Input Styling */
        .stTextInput input {
            background-color: #dfe3e8;
            color: #000000;
            border: 2px solid #4A90E2;
            border-radius: 7px;
        }

        /* Buttons */
        .stButton button {
            background-color: #4A90E2;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            transition: background-color 0.3s ease;
        }
        

        /* Header styling */
        .main-header {
            text-align: center;
            padding: 2rem;
            background: rgba(30, 30, 46, 0.8);
            border-radius: 10px;
            margin-bottom: 2rem;
        }

        .main-header h1 {
            color: #4A90E2;
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
            background: rgba(30, 30, 46, 0.8);
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Footer styling */
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding: 1rem;
            background: rgba(30, 30, 46, 0.8);
            border-radius: 10px;
        }

        .footer p {
            color: #e0e0e0;
            font-size: 0.9rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# App Header
st.markdown("""
    <div class="main-header">
        <h1>HealthLens  🩺</h1>
        <h2>Your Health Your Control</h2>
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
st.sidebar.write("Ask any medical-related questions about human health, wellness, and care.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Create a form for text input and handle Enter key submission
with st.sidebar.form(key="chat_form", clear_on_submit=True):
    user_query = st.text_input("Type your question here:", key="chat_input", placeholder="Ask Kairos")
    submit_query = st.form_submit_button("Ask")

# Process the query when the form is submitted
if submit_query and user_query:
    chatbot_prompt = f"""You are a friendly and knowledgeable medical assistant, trained to communicate like a compassionate and approachable doctor. Your role is to provide users with clear, helpful, and professional guidance, including dietary recommendations, lifestyle advice, and specific dos and don’ts based on their health concerns.  

    When interacting with users:  

    1. **Friendly Communication:** Use conversational and empathetic language to ensure users feel comfortable and supported.  
    2. **Personalized Dietary Advice:** Suggest foods to include and avoid based on the user’s health concerns. Be specific about why certain foods are beneficial or harmful.  
    3. **Lifestyle Recommendations:** Provide clear and actionable dos and don’ts for maintaining or improving health.  
        - **Dos:** Highlight healthy habits, exercises, or routines that may benefit the user.  
        - **Don’ts:** Caution against harmful practices, habits, or behaviors that may worsen their condition.  
    4. **Clear Explanations:** Use simple, relatable language while explaining your recommendations. Avoid medical jargon unless necessary, and always clarify technical terms.  
    5. **Limitations and Disclaimer:** Emphasize that your advice is general and not a substitute for professional medical consultation. Include the disclaimer: "Please consult with a healthcare professional for personalized advice and treatment."  

    Your goal is to make users feel informed, empowered, and supported, helping them make healthy choices while addressing their concerns with warmth and professionalism.
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
        st.sidebar.markdown(f"<div class='chat-history'><strong>You:</strong> {chat['user']}<br><strong>Kairos:</strong> {chat['bot']}</div>", unsafe_allow_html=True)

# Footer information
st.sidebar.markdown("---")
st.sidebar.markdown("**Note:** The chatbot is for informational purposes only. Always consult a doctor for specific concerns.")

# Footer
st.markdown("""
    <div class="footer">
        <p>Made with ❤️ for Healthcare</p>
    </div>
""", unsafe_allow_html=True)
  
    #python -m streamlit run medico.py
