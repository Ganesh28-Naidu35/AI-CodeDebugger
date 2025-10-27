import streamlit as st
import google.generativeai as genai
import time
from streamlit.components.v1 import html

# 🖥️ Set page config FIRST (must be the first Streamlit command)
st.set_page_config(
    page_title="AI Code Debugger Pro", 
    layout="wide",
    page_icon="🛠️"
)

# 🔐 Configure Gemini API key
genai.configure("your api key")  # Replace with your actual API key

# 📌 Set the correct model
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# 🎉 Confetti effect
def show_confetti():
    confetti_js = """
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
    const count = 200;
    const defaults = {
        origin: { y: 0.7 },
        spread: 90,
        ticks: 100
    };

    function fire(particleRatio, opts) {
        confetti({
            ...defaults,
            ...opts,
            particleCount: Math.floor(count * particleRatio)
        });
    }

    fire(0.25, { spread: 26, startVelocity: 55 });
    fire(0.2, { spread: 60 });
    fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8 });
    fire(0.1, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2 });
    fire(0.1, { spread: 120, startVelocity: 45 });
    </script>
    """
    html(confetti_js, height=0, width=0)

# 🎨 Apply dark theme CSS
def apply_dark_theme():
    dark_theme = """
    <style>
    /* Add any additional dark theme CSS here if needed */
    </style>
    """
    st.markdown(dark_theme, unsafe_allow_html=True)

# 🔍 Analyze code using Gemini
def analyze_code(code, language):
    prompt = f"""
You are a concise programming assistant.

Given the following {language} code, identify any errors, provide the corrected version, and briefly explain the changes.

Format your response in exactly 3 sections:
Errors:
Corrected code:
Explanation:

Limit your entire response to 6 lines or fewer.
CODE:
{code}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini error: {str(e)}"

# Main app function
def main():
    # Apply dark theme
    apply_dark_theme()
    
    # Header with title
    st.title("✨ AI Code Debugger Pro")
    st.caption("Upload your code and get instant debugging assistance")
    
    # Divider
    st.markdown("---")
    
    # Main content
    with st.container():
        # Two-column layout
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.subheader("📥 Input Code", divider="rainbow")
            
            # Language selection
            with st.expander("⚙️ Settings", expanded=True):
                language = st.selectbox(
                    "Select the programming language:",
                    ["Python", "Java", "C", "C++", "JavaScript"],
                    index=0
                )
                
                # File uploader
                uploaded_file = st.file_uploader(
                    "Upload a code file",
                    type=["py", "java", "c", "cpp", "js", "txt"]
                )
            
            # Manual code input option
            with st.expander("✍️ Or type code manually", expanded=False):
                manual_code = st.text_area(
                    "Enter your code here:",
                    height=200,
                    placeholder="Paste your code here...",
                    label_visibility="collapsed"
                )
            
            # Determine code source
            code = ""
            if uploaded_file:
                code = uploaded_file.read().decode("utf-8")
            elif manual_code:
                code = manual_code
            
            # Display code if available
            if code:
                st.subheader("📜 Your Code", divider="rainbow")
                st.code(code, language=language.lower())
                
                # Analyze button
                if st.button(
                    "🔍 Analyze Code",
                    use_container_width=True,
                    type="primary"
                ):
                    with st.spinner("🔮 Analyzing your code..."):
                        # Add a progress bar animation
                        progress_bar = st.progress(0)
                        for percent_complete in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(percent_complete + 1)
                        
                        # Get analysis results
                        result = analyze_code(code, language)
                        
                        # Display results in the right column
                        with col2:
                            st.subheader("📊 Analysis Results", divider="rainbow")
                            
                            # Show confetti instead of balloons
                            show_confetti()
                            
                            # Display results in tabs
                            tab1, tab2, tab3 = st.tabs(["🧐 Errors", "✨ Corrected Code", "📝 Explanation"])
                            
                            with tab1:
                                if "Errors:" in result:
                                    error_part = result.split("Errors:")[1].split("Corrected code:")[0]
                                    st.error(error_part.strip())
                                else:
                                    st.warning("No errors detected!")
                            
                            with tab2:
                                if "Corrected code:" in result:
                                    corrected_part = result.split("Corrected code:")[1].split("Explanation:")[0]
                                    st.code(corrected_part.strip(), language=language.lower())
                                else:
                                    st.info("No corrections suggested")
                            
                            with tab3:
                                if "Explanation:" in result:
                                    explanation_part = result.split("Explanation:")[1]
                                    st.success(explanation_part.strip())
                                else:
                                    st.info("No explanation provided")
        
        # Right column placeholder
        with col2:
            if not code:
                st.subheader("📊 Analysis Results", divider="rainbow")
                st.info("👈 Upload or type your code and click 'Analyze Code' to get started")

if __name__ == "__main__":
    main()