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

def get_styled_table(df):
    """Generates a styled HTML table similar to the uploaded format."""
    html_table = df.to_html(index=False, escape=False)
    styled_html = f'''
    <html>
    <head>
        <title>Search Results</title>
        <style>
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid black; padding: 10px; text-align: left; }}
            th {{ background-color: #f2f2f2; font-weight: bold; }}
            td a {{ color: blue; text-decoration: none; }}
            td a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>Search Results for: "{query}"</h1>
        {html_table}
    </body>
    </html>
    '''
    return styled_html

def get_table_download_link(df):
    """Generates a downloadable HTML file link for the search results."""
    styled_html = get_styled_table(df)
    b64 = base64.b64encode(styled_html.encode()).decode()
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
                    results.append({"Title": item["title"], "Link": f'<a href="{item["link"]}" target="_blank">{item["link"]}</a>'})
            else:
                st.error("No results found or API limit reached.")
                break

        # Convert results to DataFrame and provide a download link
        if results:
            df = pd.DataFrame(results)
            st.write("### Search Results:")
            st.write(get_styled_table(df), unsafe_allow_html=True)
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)
