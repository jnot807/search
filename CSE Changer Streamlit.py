import streamlit as st
import requests
import pandas as pd
import base64

API_KEY = "AIzaSyBuskvy0h2pfBTyMsqmsb659duKYq2sCP8"  # Use your own API key

st.title("Google Custom Search Engine")
st.write("**Number of search results** (Remember: Google CSE has a limit of 1000 results per day)")

# Ask user for CSE ID
cse_id = st.text_input("Enter your CSE ID", "")
query = st.text_input("Enter your search query", "")
num_results = st.number_input("Number of results", min_value=1, max_value=100, value=10)

def get_table_download_link(df):
    """Generates a link to download the search results as an HTML file."""
    html_table = df.to_html(index=False, escape=False)
    b64 = base64.b64encode(html_table.encode()).decode()
    href = f'<a href="data:file/html;base64,{b64}" download="search_results.html">Download Search Results (HTML)</a>'
    return href

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
                    results.append({"Title": item["title"], "Link": item["link"]})
            else:
                st.error("No results found or API limit reached.")
                break

        # Convert results to DataFrame and provide a download link
        if results:
            df = pd.DataFrame(results)
            st.write("### Search Results:")
            st.dataframe(df)
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)
