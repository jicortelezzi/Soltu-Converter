import pandas as pd
import streamlit as st

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Assembly.csv", sep=",")
# Convertir columnas clave a string y quitar espacios
    cols = ['soltu_id', 'pgsc_id', 'sin punto', 'dmg_sequence', 'dmt_sequence', 'evalue']
    for col in cols:
        df[col] = df[col].astype(str).str.strip()
    return df
df = load_data()

# Title and description
st.title("🧬 Potato Gene ID Converter :potato:")
st.write("Enter a gene ID to retrieve the corresponding Soltu or PGSC identifier, along with the associated e-value (if available).")
with st.expander("❓ How to use this tool (click to expand)"):
    st.markdown(
        """
        - Select the type of ID you want to convert (Soltu or PGSC).
        - Enter a complete ID (e.g., `Soltu.DM.01G044060.1` or `PGSC0003DMT400004232`).
        """,
        unsafe_allow_html=True
    )
# Initialize session state
if "last_query_type" not in st.session_state:
    st.session_state.last_query_type = "Convert Soltu"
if "input_value" not in st.session_state:
    st.session_state.input_value = ""

# Selection: query type
query_type = st.radio("Select type of conversion:", ["Convert Soltu ID", "Convert PGSC ID"])

# Clear input when query type changes
if query_type != st.session_state.last_query_type:
    st.session_state.input_value = ""
    st.session_state.last_query_type = query_type

# Input
# Determinar placeholder dinámico
if query_type == "Convert Soltu ID":
    placeholder_text = "e.g., Soltu.DM.09G009070.1"
else:
    placeholder_text = "e.g., PGSC0003DMC400015119"
user_input = st.text_input("Enter gene ID:", value=st.session_state.input_value, key="input_value", placeholder=placeholder_text)
# Process input
if user_input:
    if query_type == "Convert Soltu ID":
        match = df[df['soltu_id'] == user_input]

        # If not found, try matching in 'sin punto' column
        if match.empty:
            match = df[df['sin punto'] == user_input]
            if not match.empty:
                row = match.iloc[0]
                st.success(f"**Matched by truncated Soltu ID**\n\n**PGSC ID:** `{row['pgsc_id']}`\n\n**E-value:** `{row['evalue']}`")
            else:
                st.error("Soltu ID not found.")
        else:
            row = match.iloc[0]
            st.success(f"**PGSC ID:** `{row['pgsc_id']}`\n\n**E-value:** `{row['evalue']}`")

    else:  # PGSC ID to Soltu
        match = df[
            (df['pgsc_id'] == user_input) |
            (df['dmg_sequence'] == user_input) |
            (df['dmt_sequence'] == user_input)
        ]
        if not match.empty:
            row = match.iloc[0]
            st.success(f"**Soltu ID:** `{row['soltu_id']}`\n\n**E-value:** `{row['evalue']}`")

        else:
            st.error("PGSC ID not found.")

# Footer
st.markdown("---")

st.markdown(
    """
    <div style='text-align: center;'>
        <img src="https://www.fbmc.fcen.uba.ar/wp-content/uploads/2020/02/logo-ingebi.jpg" style="max-width: 100px; width: 100%; height: auto;">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='text-align: center; font-size: 0.9em; color: #555;'>
        <a href="https://ingebi-conicet.gov.ar/es_ingenieria-genetica-de-plantas/" target="_blank"
           style="color: #1f77b4; text-decoration: none; font-weight: bold;">
            Genetic Engineering in Plants Laboratory (INGEBI-CONICET) 🇦🇷
        </a><br>
        Gene data obtained from 
        <a href="https://spuddb.uga.edu/index.shtml" target="_blank"
           style="color: #1f77b4; text-decoration: none; font-weight: bold;">
           SPUD DB
        </a>.<br>
        <span style="font-style: italic;">Developed by Juan Ignacio Cortelezzi</span><br>
        <span style="font-style: italic;">PGSC protein and cdna data from Ivan Federico Gitman Berco</span><br><br>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    ---
    <div style='font-size: 0.85em; color: #666; text-align: justify;'>
    <strong>Disclaimer:</strong><br>
    The information provided by this tool is based on BLAST alignments and sequence similarity. While efforts have been made to ensure accuracy, users are strongly advised to validate gene identities and annotations through independent sources. We do not take responsibility for any decisions or interpretations made based on this data. Use of the information is at your own risk. This tool is intended for research and educational purposes only.
    </div>
    """,
    unsafe_allow_html=True
)

