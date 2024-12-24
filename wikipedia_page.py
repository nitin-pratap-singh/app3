import streamlit as st
import google.generativeai as genai
import os

# Configuration
st.set_page_config(page_title="Wikipedia Page Generator", page_icon="📚")

# Set up Gemini API (ensure you have set the GOOGLE_API_KEY environment variable)
try:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
except Exception as e:
    st.error(f"Error configuring API: {e}")
    st.stop()

# Create the Gemini model
model = genai.GenerativeModel('gemini-pro')

def generate_wikipedia_page(topic):
    """
    Generate a Wikipedia-style page for the given topic
    """
    # Prompt engineering to create a Wikipedia-like article
    prompt = f"""Write a comprehensive, encyclopedic article about {topic} in the style of Wikipedia.
    The article should include:
    1. An introductory overview
    2. Detailed history and background
    3. Key characteristics or attributes
    4. Significance or impact
    5. Relevant subsections as appropriate
    6. Neutral, academic tone
    7. Properly formatted with clear sections
    
    Topic: {topic}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

def main():
    """
    Main Streamlit application
    """
    st.title("📚 Wikipedia-style Page Generator")
    
    # Sidebar for instructions
    st.sidebar.header("How to Use")
    st.sidebar.info(
        "Enter a topic to generate a comprehensive, Wikipedia-style article. "
        "The AI will create an informative and neutral description."
    )
    
    # Topic input
    topic = st.text_input("Enter a topic for your Wikipedia-style page:", 
                          placeholder="e.g., Artificial Intelligence, Quantum Computing")
    
    # Generate button
    if st.button("Generate Page"):
        if topic:
            # Show loading spinner
            with st.spinner("Generating Wikipedia-style page..."):
                article = generate_wikipedia_page(topic)
            
            # Display the generated article
            if article:
                st.markdown("## Generated Article")
                st.markdown(article)
                
                # Download option
                st.download_button(
                    label="Download Article",
                    data=article,
                    file_name=f"{topic.replace(' ', '_')}_wiki.md",
                    mime="text/markdown"
                )
            else:
                st.error("Failed to generate the article. Please try again.")
        else:
            st.warning("Please enter a topic first!")

# Run the app
if __name__ == "__main__":
    main()
    