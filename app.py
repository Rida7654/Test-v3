
import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
import io
import re

# Fonctions d'extraction automatique
def extract_date(text):
    match = re.search(r"(0[1-9]|[12][0-9]|3[01])[\/\-](0[1-9]|1[0-2])[\/\-](\d{2,4})", text)
    return match.group() if match else "Non trouvé"

def extract_number(text):
    match = re.search(r"N°\s*\d+/\d{2}", text)
    return match.group() if match else "Non trouvé"

def extract_supplier(text):
    lines = text.split('\n')
    for line in lines:
        if "SARL" in line or "GROUP" in line or "SOCIETE" in line.upper():
            return line.strip()
    return "Non trouvé"

def extract_amount(text):
    match = re.search(r"(\d{1,3}(?:[\s,]\d{3})*(?:[.,]\d{2})?)\s*(DH|MAD|€)?", text)
    return match.group() if match else "Non trouvé"

# Interface Streamlit
st.title("EXCLF - Extraction de Factures vers Excel")

uploaded_files = st.file_uploader("Importer vos factures (PDF ou images)", accept_multiple_files=True)

data = []

if uploaded_files:
    for file in uploaded_files:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)

        date = extract_date(text)
        numero = extract_number(text)
        fournisseur = extract_supplier(text)
        montant = extract_amount(text)

        data.append({
            "Date": date,
            "Numéro": numero,
            "Fournisseur": fournisseur,
            "Montant HT": montant
        })

    df = pd.DataFrame(data)
    st.write(df)

    output = io.BytesIO()
    df.to_excel(output, index=False)
    st.download_button("Télécharger le fichier Excel", data=output.getvalue(), file_name="factures.xlsx")
