import pandas as pd
import os

# CONFIGURACIÓN: Pon aquí el nombre exacto de tu archivo Excel
archivo_excel = 'DESPACHO INCIDENCIAS 2025.xlsx'

meses_map = {
    'CRUDO ENERO': 'Enero', 'CRUDO FEBRERO': 'Febrero', 'CRUDO MARZO': 'Marzo',
    'CRUDO ABRIL': 'Abril', 'CRUDO MAYO': 'Mayo', 'CRUDO JUNIO': 'Junio',
    'CRUDO JULIO': 'Julio', 'CRUDO AGOSTO': 'Agosto', 'CRUDO SEPTIEMBRE': 'Septiembre',
    'CRUDO OCTUBRE': 'Octubre', 'CRUDO NOVIEMBRE': 'Noviembre', 'CRUDO DICIEMBRE': 'Diciembre'
}

todos_los_datos = []

if not os.path.exists(archivo_excel):
    print(f"Error: No encuentro el archivo '{archivo_excel}' en esta carpeta.")
else:
    print(f"Abriendo {archivo_excel}...")
    # Cargamos el Excel completo (solo los nombres de las hojas primero)
    xl = pd.ExcelFile(archivo_excel)
    
    for hoja in xl.sheet_names:
        nombre_hoja = hoja.strip().upper()
        # Buscamos si la hoja está en nuestro mapa de meses
        mes_clave = next((k for k in meses_map.keys() if k in nombre_hoja), None)
        
        if mes_clave:
            print(f"-> Procesando hoja: {hoja}...")
            df = pd.read_excel(xl, sheet_name=hoja)
            df['Mes'] = meses_map[mes_clave]
            
            # Filtro de Prevención
            if 'Agencia' in df.columns:
                df_prev = df[df['Agencia'].str.contains('AP GCBA|PREVENCION', na=False, case=False)].copy()
                todos_los_datos.append(df_prev)
            else:
                print(f"   Advertencia: No se encontró columna 'Agencia' en hoja {hoja}")

    if todos_los_datos:
        df_final = pd.concat(todos_los_datos, ignore_index=True)
        
        # Clasificación de Seguridad vs Servicio
        security_kw = ['ROBO', 'HURTO', 'ACCIDENTE', 'INCENDIO', 'PELEA', 'ARMA', 'HERIDO', 'DANIOS', 'CONTRAVENCIONES']
        df_final['Categoria'] = df_final['Tipo y Subtipo'].apply(
            lambda x: 'Seguridad/Emergencia' if any(kw in str(x).upper() for kw in security_kw) else 'Servicio/Orden'
        )
        
        df_final.to_csv('consolidado_prevencion.csv', index=False)
        print(f"\n¡EXITO! Archivo 'consolidado_prevencion.csv' creado con {len(df_final)} registros.")
    else:
        print("\nERROR: No se encontró ninguna hoja que coincida con 'CRUDO MES'.")