from textwrap import dedent
from phi.assistant import Assistant
from phi.tools.serpapi_tools import SerpApiTools
import streamlit as st
from phi.llm.openai import OpenAIChat

# Set up the Streamlit app
st.title("AI Personal Finance Planner 💰")
st.caption("Manage your finances with AI Personal Finance Manager by creating personalized budgets, investment plans, and savings strategies using GPT-4o")

# Custom CSS for platform buttons
st.markdown("""
    <style>
    .platform-button {
        display: inline-block;
        padding: 15px;
        margin: 10px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: bold;
        width: 220px;
        transition: transform 0.2s;
        position: relative;
    }
    .platform-button:hover {
        transform: scale(1.05);
    }
    .platform-logo {
        width: 40px;
        height: 40px;
        margin-right: 10px;
        vertical-align: middle;
    }
    .zerodha { background-color: #387ED1; }
    .upstox { background-color: #FF6B6B; }
    .groww { background-color: #00D09C; }
    .angel { background-color: #FF8C00; }
    .coindcx { background-color: #2C3E50; }
    .coinswitch { background-color: #6C5CE7; }
    .binance { background-color: #F3B63A; }
    .request-box {
        border: 2px dashed #ccc;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

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

    # Input fields for the user's financial goals and current financial situation
    financial_goals = st.text_input("What are your financial goals?")
    current_situation = st.text_area("Describe your current financial situation")

    if st.button("Generate Financial Plan"):
        with st.spinner("Processing..."):
            # Get the response from the assistant
            response = planner.run(f"Financial goals: {financial_goals}, Current situation: {current_situation}", stream=False)
            st.write(response)
            
            # Display investment platform options after the response
            st.markdown("### 🤖 Let Our AI Execute Your Investment Strategy")
            st.markdown("Select your preferred platform and let our AI handle your investments:")
            
            # Trading Platforms Section
            st.subheader("📊 Stock Trading Platforms")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                    <a href="https://kite.zerodha.com" target="_blank">
                        <div class="platform-button zerodha">
                            <img src="https://images.sftcdn.net/images/t_app-icon-m/p/febac357-40e7-4197-becf-9a738dfc8343/3716141484/full-width-zerodha-kite-trading-platform-logo" class="platform-logo" alt="Zerodha">
                            Kite by Zerodha
                        </div>
                    </a>
                    <a href="https://upstox.com" target="_blank">
                        <div class="platform-button upstox">
                            <img src="https://yt3.googleusercontent.com/dd4s5znNFk_II32JYer0dhjhqRi_rFwPcYEzLtwA9id1u4WZK2MjNt5PTyKVChxdJ8BvW4WJ=s900-c-k-c0x00ffffff-no-rj" class="platform-logo" alt="Upstox">
                            Upstox
                        </div>
                    </a>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                    <a href="https://groww.in" target="_blank">
                        <div class="platform-button groww">
                            <img src="https://yt3.googleusercontent.com/KyIoz7-0-PKrCKPkjFHv2Wv50dhuFN6ohsr9oO_8AfIXdwenMQJH8Rau1oOlMgUfI-jWq0PK3xE=s900-c-k-c0x00ffffff-no-rj" class="platform-logo" alt="Groww">
                            Groww
                        </div>
                    </a>
                    <a href="https://angelone.in" target="_blank">
                        <div class="platform-button angel">
                            <img src="https://play-lh.googleusercontent.com/T5ibZuIwAGX5gnIjh7Il0wpcUtDPYL6MekYwTLvvgYUOZAaKS-_RotixDcDw0K6QDQ" class="platform-logo" alt="Angel One">
                            Angel One
                        </div>
                    </a>
                """, unsafe_allow_html=True)

            # Request box for trading platforms
            st.markdown("""
                <div class="request-box">
                    <h4>Request Your Trading Platform</h4>
                </div>
            """, unsafe_allow_html=True)
            trading_platform_request = st.text_input("Enter your preferred trading platform name", key="trading_platform")

            # Cryptocurrency Platforms Section
            st.subheader("💎 Cryptocurrency Platforms")
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("""
                    <a href="https://coindcx.com" target="_blank">
                        <div class="platform-button coindcx">
                            <img src="https://zengo.com/wp-content/uploads/CoinDCX.png" class="platform-logo" alt="CoinDCX">
                            CoinDCX
                        </div>
                    </a>
                    <a href="https://coinswitch.co" target="_blank">
                        <div class="platform-button coinswitch">
                            <img src="https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/11/a5/8a/11a58af7-6e7c-c5ec-5a99-4fb3d07a0def/AppIcon-0-0-1x_U007emarketing-0-7-0-85-220.png/1200x600wa.png" class="platform-logo" alt="CoinSwitch">
                            CoinSwitch
                        </div>
                    </a>
                """, unsafe_allow_html=True)
                
            with col4:
                st.markdown("""
                    <a href="https://binance.com" target="_blank">
                        <div class="platform-button binance">
                            <img src="https://public.bnbstatic.com/20190405/eb2349c3-b2f8-4a93-a286-8f86a62ea9d8.png" class="platform-logo" alt="Binance">
                            Binance
                        </div>
                    </a>
                """, unsafe_allow_html=True)

            # Request box for crypto platforms
            st.markdown("""
                <div class="request-box">
                    <h4>Request Your Crypto Platform</h4>
                </div>
            """, unsafe_allow_html=True)
            crypto_platform_request = st.text_input("Enter your preferred cryptocurrency platform name", key="crypto_platform")
            
            st.markdown("---")
            st.caption("Note: These are simulated options for demonstration purposes. Our AI will execute trades on your behalf only after proper verification and authorization.")