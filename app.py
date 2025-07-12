import streamlit as st
import pandas as pd
import easyocr
import numpy as np
from PIL import Image
import re

st.set_page_config(page_title="Extractor Lotto a SQLite", layout="centered")
st.title("📸 Extraer datos de Lotto desde imagen")
st.write("Sube una imagen con resultados y genera CSV + SQL automáticamente.")

# Campo para que el usuario elija la fecha base
fecha_base = st.date_input("Selecciona la fecha para estos resultados")

uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen subida", use_column_width=True)

    with st.spinner("Extrayendo texto con EasyOCR..."):
        reader = easyocr.Reader(['es'], gpu=False)
        image_np = np.array(image)
        result = reader.readtext(image_np)

    texto_extraido = "\n".join([item[1] for item in result])
    st.text_area("Texto detectado:", texto_extraido, height=250)

    # Expresión regular para capturar: hora, número, animal
    patron = re.compile(r"(\d{1,2}:\d{2})\s+(\d{1,2})\s+([A-ZÁÉÍÓÚÑ]+)")

    data = []
    for match in patron.findall(texto_extraido):
        hora, numero, animal = match
        data.append({
            "fecha": fecha_base.strftime("%Y-%m-%d"),
            "hora": hora.zfill(5),
            "numero": int(numero),
            "animal": animal.upper()
        })

    if data:
        df = pd.DataFrame(data)
        st.success("✅ Datos estructurados correctamente:")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        sql = "\n".join([
            f"INSERT INTO Resultados (fecha, hora, numero, animal) VALUES ('{r['fecha']}', '{r['hora']}', {r['numero']}, '{r['animal']}');"
            for _, r in df.iterrows()
        ]).encode("utf-8")

        st.download_button("📄 Descargar CSV", csv, "resultados.csv", "text/csv")
        st.download_button("🗃 Descargar SQL", sql, "resultados.sql", "text/sql")
    else:
        st.warning("⚠️ No se pudo extraer ningún dato estructurado. Asegúrate de que el texto tenga el formato correcto, por ejemplo: 09:00 13 MONO")
        
