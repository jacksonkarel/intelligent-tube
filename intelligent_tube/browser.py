import streamlit as st

st.title("Simple Web Browser")

# Input field for the URL
url = st.text_input("Enter a URL", "https://www.google.com")

# Button to navigate to the URL
if st.button("Go"):
    try:
        # Display the webpage in an iframe
        st.components.v1.iframe(url, height=600, scrolling=True)
    except Exception as e:
        st.error(f"An error occurred: {e}")
