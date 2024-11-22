import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Initialize session state for navigation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Function to fetch and parse the webpage
def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    except Exception as e:
        st.error(f"Error fetching the page: {e}")
        return None

# Main application function
def main():
    st.title("Text-Based Browser in Streamlit")

    # Get the current URL from session state or default to an empty string
    if st.session_state.history:
        current_url = st.session_state.history[-1]
    else:
        current_url = ''

    # URL input field
    url_input = st.text_input("Enter URL", value=current_url)

    # 'Go' button to navigate to the entered URL
    if st.button("Go"):
        if url_input:
            st.session_state.history.append(url_input)

    # 'Back' button to navigate to the previous page
    if len(st.session_state.history) > 1:
        if st.button("Back"):
            st.session_state.history.pop()
            url_input = st.session_state.history[-1]
            st.rerun()

    # If there's a URL to fetch
    if st.session_state.history:
        current_url = st.session_state.history[-1]
        soup = fetch_page(current_url)
        if soup:
            # Extract and display the text content of the page
            text = soup.get_text()
            st.text_area("Page Content", text, height=300)

            # Extract all hyperlinks
            st.subheader("Links on this page:")
            links = []
            for link in soup.find_all('a'):
                href = link.get('href')
                link_text = link.get_text()
                if href:
                    # Resolve relative URLs
                    href = urllib.parse.urljoin(current_url, href)
                    links.append((link_text.strip() or href, href))

            # Display the links as buttons
            for link_text, href in links:
                if st.button(link_text):
                    st.session_state.history.append(href)
                    st.rerun()

if __name__ == "__main__":
    main()

