import streamlit as st
import requests

API_KEY = "AIzaSyBuskvy0h2pfBTyMsqmsb659duKYq2sCP8"  # Use your own API key

st.title("Google Custom Search Engine")

# Ask user for CSE ID
cse_id = st.text_input("Enter your CSE ID", "")
query = st.text_input("Enter your search query", "")
num_results = st.number_input("Number of results", min_value=1, max_value=100, value=10)

if st.button("Search"):
    if not cse_id or not query:
        st.warning("Please enter both CSE ID and query.")
    else:
        results = []
        for start_index in range(1, num_results + 1, 10):
            url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={cse_id}&start={start_index}"
            response = requests.get(url)
            data = response.json()

            if "items" in data:
                for item in data["items"]:
                    results.append((item["title"], item["link"]))
            else:
                st.error("No results found or API limit reached.")
                break

        # Display results
        for title, link in results:
            st.markdown(f"### [{title}]({link})")
