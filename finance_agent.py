from textwrap import dedent
from phi.assistant import Assistant
from phi.tools.serpapi_tools import SerpApiTools
import streamlit as st
from phi.llm.openai import OpenAIChat
import speech_recognition as sr

# Function to capture speech and convert to text
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        try:
            audio = r.listen(source, timeout=5)
            st.info("Processing speech...")
            text = r.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            st.error("No speech detected. Please try again.")
            return None
        except sr.RequestError:
            st.error("Could not process speech. Please try again.")
            return None
        except sr.UnknownValueError:
            st.error("Could not understand audio. Please try again.")
            return None

# Initialize session state
if 'financial_goals' not in st.session_state:
    st.session_state.financial_goals = ""
if 'current_situation' not in st.session_state:
    st.session_state.current_situation = ""

# Set up the Streamlit app
st.title("AI Personal Finance Planner 💰")
st.caption("Manage your finances with AI Personal Finance Manager by creating personalized budgets, investment plans, and savings strategies using GPT-4o")

# Get OpenAI API key from user
openai_api_key = st.text_input("Enter OpenAI API Key to access GPT-4o", type="password")

# Get SerpAPI key from the user
serp_api_key = st.text_input("Enter Serp API Key for Search functionality", type="password")

if openai_api_key and serp_api_key:
    researcher = Assistant(
        name="Researcher",
        role="Searches for financial advice, investment opportunities, and savings strategies based on user preferences",
        llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
        description=dedent(
            """\
        You are a world-class financial researcher. Given a user's financial goals and current financial situation,
        generate a list of search terms for finding relevant financial advice, investment opportunities, and savings strategies.
        Then search the web for each term, analyze the results, and return the 10 most relevant results.
        """
        ),
        instructions=[
            "Given a user's financial goals and current financial situation, first generate a list of 3 search terms related to those goals.",
            "For each search term, `search_google` and analyze the results.",
            "From the results of all searches, return the 10 most relevant results to the user's preferences.",
            "Remember: the quality of the results is important.",
        ],
        tools=[SerpApiTools(api_key=serp_api_key)],
        add_datetime_to_instructions=True,
    )
    planner = Assistant(
        name="Planner",
        role="Generates a personalized financial plan based on user preferences and research results",
        llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
        description=dedent(
            """\
        You are a senior financial planner. Given a user's financial goals, current financial situation, and a list of research results,
        your goal is to generate a personalized financial plan that meets the user's needs and preferences.
        """
        ),
        instructions=[
            "Given a user's financial goals, current financial situation, and a list of research results, generate a personalized financial plan that includes suggested budgets, investment plans, and savings strategies.",
            "Ensure the plan is well-structured, informative, and engaging.",
            "Ensure you provide a nuanced and balanced plan, quoting facts where possible.",
            "Remember: the quality of the plan is important.",
            "Focus on clarity, coherence, and overall quality.",
            "Never make up facts or plagiarize. Always provide proper attribution.",
        ],
        add_datetime_to_instructions=True,
        add_chat_history_to_prompt=True,
        num_history_messages=3,
    )

    # Create columns for text input and speech button for financial goals
    col1, col2 = st.columns([4, 1])
    with col1:
        financial_goals = st.text_input(
            "What are your financial goals?",
            value=st.session_state.financial_goals
        )
    with col2:
        if st.button("🎤 Record Goals", key="goals_button"):
            spoken_text = speech_to_text()
            if spoken_text:
                st.session_state.financial_goals = spoken_text
                st.rerun()

    # Create columns for text area and speech button for current situation
    col3, col4 = st.columns([4, 1])
    with col3:
        current_situation = st.text_area(
            "Describe your current financial situation",
            value=st.session_state.current_situation
        )
    with col4:
        if st.button("🎤 Record Situation", key="situation_button"):
            spoken_text = speech_to_text()
            if spoken_text:
                st.session_state.current_situation = spoken_text
                st.rerun()

    if st.button("Generate Financial Plan"):
        with st.spinner("Processing..."):
            # Get the response from the assistant
            response = planner.run(f"Financial goals: {financial_goals}, Current situation: {current_situation}", stream=False)
            st.write(response)