import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Depurador RRHH", page_icon="🛠️", layout="wide")

st.title("🛠️ Depurador de Base de Datos - Vigencia RRHH")
st.markdown("""
Sube tu archivo **CSV** exportado del sistema. La aplicación se encargará de estandarizar RUTs, 
limpiar nombres/cargos, separar el sueldo base de los bonos y formatear las fechas de vencimiento.
""")

# --- CARGA DEL ARCHIVO ---
archivo_subido = st.file_uploader("Arrastra tu archivo CSV aquí", type=["csv"])

if archivo_subido is not None:
    try:
        # Leer el archivo con separador de punto y coma
        df = pd.read_csv(archivo_subido, sep=';', encoding='utf-8')
        
        st.subheader("Vista previa: Datos Originales")
        st.dataframe(df.head(3))

        # --- BOTÓN DE EJECUCIÓN ---
        if st.button("🚀 Depurar Base de Datos"):
            with st.spinner('Analizando y limpiando datos...'):
                
                # 1. Limpieza de texto (Mayúsculas y quitar espacios extra)
                columnas_texto = ['RUT', 'NOMBRE', 'CARGO', 'UN']
                for col in columnas_texto:
                    if col in df.columns:
                        df[col] = df[col].astype(str).str.strip().str.upper()

                # 2. Separar Sueldo Pactado
                if 'SUELDO PACTADO' in df.columns:
                    # Dividir en el primer signo "+"
                    df[['SUELDO_BASE', 'BONOS_CONDICIONES']] = df['SUELDO PACTADO'].astype(str).str.split(r'\+', n=1, expand=True)
                    df['BONOS_CONDICIONES'] = df['BONOS_CONDICIONES'].fillna('SIN BONO')

                # 3. Fechas y Estados
                if 'FECHA APROX TERMINO ITEM' in df.columns:
                    # Clasificar estado del contrato
                    df['ESTADO_CONTRATO'] = np.where(
                        df['FECHA APROX TERMINO ITEM'].astype(str).str.contains('INDEFINIDO', case=False, na=False), 
                        'INDEFINIDO', 
                        'PLAZO FIJO/OBRA'
                    )
                    # Forzar formato fecha (lo que sea texto como "INDEFINIDO" quedará vacío/NaT)
                    df['FECHA_VENCIMIENTO_REAL'] = pd.to_datetime(df['FECHA APROX TERMINO ITEM'], errors='coerce', format='%d-%m-%Y')

                # 4. Reordenar y filtrar columnas finales
                columnas_deseadas = [
                    'RUT', 'NOMBRE', 'CARGO', 'UN', 'FECHA INGRESO', 
                    'SUELDO_BASE', 'BONOS_CONDICIONES', 
                    'ESTADO_CONTRATO', 'RENOVACIÓN 2', 'FECHA_VENCIMIENTO_REAL'
                ]
                
                # Solo mantenemos las columnas que realmente existan para evitar errores
                columnas_finales = [col for col in columnas_deseadas if col in df.columns]
                df_limpio = df[columnas_finales]

            # --- RESULTADOS ---
            st.success("¡Limpieza completada con éxito!")
            
            st.subheader("Vista previa: Datos Depurados")
            st.dataframe(df_limpio.head(5))

            # --- DESCARGA DEL ARCHIVO LIMPIO ---
            csv_limpio = df_limpio.to_csv(sep=';', index=False, encoding='utf-8-sig').encode('utf-8')
            
            st.download_button(
                label="⬇️ Descargar Base Depurada (CSV)",
                data=csv_limpio,
                file_name="Vigencia_RRHH_Depurada.csv",
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"Hubo un error procesando el archivo. Asegúrate de que sea el CSV correcto. Detalle técnico: {e}")
