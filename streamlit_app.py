import streamlit as st
import requests
import os


# Configure the page
st.set_page_config(
    page_title="Document Assistant Manual 01", page_icon="📄", layout="wide"
)

# Add a title and description
st.title("📄 Document Assistant Manual 01")

# Get API URL from environment variable or default
# API_URL = os.getenv("API_URL")  # Replace with your actual Hugging Face Space if needed
API_URL = "https://gufranrana-rag-api-manual-01.hf.space"


def query_rag_system(query: str):
    """Send query to the RAG endpoint and return results"""
    try:
        response = requests.get(
            f"{API_URL}/ask",
            params={"question": query},  # Use GET with query parameters
            timeout=60,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The API might be starting up, please try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error connecting to the API: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None


# Create the main query interface
st.markdown("Enter your query to get AI-generated responses based on the documents.")

# Use columns for layout
col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_area(
        "Enter your query:",
        height=100,
        placeholder="Ask me anything about the document...",
    )

with col2:
    st.write("")  # Add some spacing
    st.write("")  # Add some spacing
    submit_button = st.button("Submit Query", type="primary")

# Add example queries
with st.expander("💡 Example Queries"):
    st.markdown("""
    - What is the length (L) in millimeters for the female/female thread configuration in the REG-0101 model?
    - What is the length (GT) in millimeters for the Female/male thread G ¾ in the REG-0101 model?
    - What should be considered when isolating pressure systems to ensure safety?
    - What is the reference density for wet solids in the Alfa Laval separator bowl?
    - What should be stored or discharged in accordance with current rules and directives during valve maintenance?
    """)

# Handle form submission
if submit_button and query.strip():
    with st.spinner("🤔 Processing your query..."):
        result = query_rag_system(query)
        if result:
            st.subheader("Response")
            response_text = result.get("response", "No response received")
            st.markdown(response_text)
elif submit_button and not query.strip():
    st.warning("⚠️ Please enter a query before submitting.")
