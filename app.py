import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import io

st.set_page_config(page_title="Extractor Lotto a SQLite", layout="centered")
st.title("📸 Extraer datos de Lotto desde imagen")
st.write("Sube una captura con resultados y genera CSV + SQL automáticamente.")

uploaded_file = st.file_uploader("Sube una imagen", type=["png","jpg","jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen subida", use_column_width=True)

    with st.spinner("Extrayendo texto con OCR..."):
        text = pytesseract.image_to_string(image, config="--oem 3 --psm 6")

    st.text_area("Texto detectado:", text, height=200)
    st.warning("Revisa el texto. Próximamente se estructurará automáticamente.")

    if st.button("📥 Descargar CSV y SQL"):
        # Aquí se debería parsear `text`, por ahora ejemplo estático:
        data = [
            {"fecha":"2020-12-28","hora":"09:00","numero":13,"animal":"MONO"},
            {"fecha":"2020-12-28","hora":"10:00","numero":11,"animal":"GATO"}
        ]
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False).encode("utf-8")
        sql = "\n".join(
            f"INSERT INTO Resultados (fecha,hora,numero,animal) VALUES ('{r['fecha']}','{r['hora']}',{r['numero']},'{r['animal']}');"
            for r in data
        ).encode("utf-8")
        st.download_button("📄 Descargar CSV", csv, "resultados.csv", "text/csv")
        st.download_button("🗃 Descargar SQL", sql, "resultados.sql", "text/sql")
      
