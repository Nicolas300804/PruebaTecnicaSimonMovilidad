import pandas as pd
import os

def procesar_datos_taxis(archivo_parquet, directorio_salida=None):
        
    print(f"Leyendo archivo: {archivo_parquet}")
    
    # Leer el archivo Parquet
    df = pd.read_parquet(archivo_parquet)
    
    print(f"Total de registros leídos: {len(df)}") #Obtiene el nmero de fila con el len
    print(f"Columnas disponibles: {df.columns.tolist()}")
    
    # Verificar columnas necesarias
    columnas_necesarias = ['tpep_pickup_datetime', 'PULocationID']
    columnas_faltantes = [col for col in columnas_necesarias if col not in df.columns]
    
    if columnas_faltantes:
        print(f"ADVERTENCIA: Faltan columnas: {columnas_faltantes}")
    
    # Los archivos modernos de NYC Taxi no tienen pickup_latitude/longitude
    # Usaremos las columnas disponibles o valores nulos si no existen
    
    # Asegurar que tpep_pickup_datetime es datetime
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    
    # Definir directorio de salida
    if directorio_salida is None:
        directorio_salida = os.path.dirname(archivo_parquet)
    
    # CSV 1: Ultima Ubicacion Conocida
  
    print("\nGenerando ultima_ubicacion.csv...")
    
    # Ordenar por vehicle_id y timestamp
    df_sorted = df.sort_values(['PULocationID', 'tpep_pickup_datetime'])
    
    # Obtener el último registro por vehículo
    df_ultima_ubicacion = df_sorted.groupby('PULocationID').last().reset_index()
    
    # Preparar el DataFrame de salida
    salida_ubicacion = pd.DataFrame({
        'vehicle_id': df_ultima_ubicacion['PULocationID'],
        'ultimo_timestamp': df_ultima_ubicacion['tpep_pickup_datetime'],
        'ultima_latitud': df_ultima_ubicacion.get('pickup_latitude', None),
        'ultima_longitud': df_ultima_ubicacion.get('pickup_longitude', None)
    })
    
    # Guardar archivo CSV
    archivo_ubicacion = os.path.join(directorio_salida, 'ultima_ubicacion.csv')
    salida_ubicacion.to_csv(archivo_ubicacion, index=False)
    print(f"✓ Archivo guardado: {archivo_ubicacion}")
    print(f"  Total de vehículos únicos: {len(salida_ubicacion)}")
    
   

    # CSV 2: Reporte de viaje por hora
    print("\nGenerando viajes_por_hora.csv...")
    
    # Extraer la hora del día
    df['hora_del_dia'] = df['tpep_pickup_datetime'].dt.hour
    
    # Agrupar por hora y contar viajes
    viajes_por_hora = df.groupby('hora_del_dia').size().reset_index(name='total_viajes')
    
    # Asegurar que todas las horas (0-23) estén presentes
    # Esto garantiza que incluso si no hay viajes en alguna hora, aparezca con 0
    todas_horas = pd.DataFrame({'hora_del_dia': range(24)})
    
    # Combinamos el DataFrame de todas las horas con los datos agrupados
    # Usamos merge con how='left' para mantener todas las horas aunque no tengan viajes
    viajes_por_hora = todas_horas.merge(viajes_por_hora, on='hora_del_dia', how='left')
    
    # Rellenamos los valores nulos con 0 (horas sin viajes) y convertimos a entero
    viajes_por_hora['total_viajes'] = viajes_por_hora['total_viajes'].fillna(0).astype(int)
    
    # Guardar archivo CSV
    archivo_horas = os.path.join(directorio_salida, 'viajes_por_hora.csv')
    viajes_por_hora.to_csv(archivo_horas, index=False)
    print(f"✓ Archivo guardado: {archivo_horas}")
    # Calculamos e imprimimos el total de viajes procesados
    # Si existe una columna 'total_viajes', usamos su suma (para datos agrupados)
    # Si no existe, usamos el total de registros del DataFrame como conteo
    print(f"  Total de viajes procesados: {df['total_viajes'].sum() if 'total_viajes' in df.columns else len(df)}")

    
    # Mostrar muestra de datos
    print("\n Muestra de ultima_ubicacion.csv (primeras 5 filas):")
    print(salida_ubicacion.head())
    
    print("\n Muestra de viajes_por_hora.csv:")
    print(viajes_por_hora)
    
    return salida_ubicacion, viajes_por_hora


if __name__ == "__main__":
    # Usar el directorio actual donde está el script
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # Buscar archivo parquet en el directorio actual
    archivo_parquet = None
    for archivo in os.listdir(directorio_actual):
        if archivo.endswith('.parquet') and 'yellow_tripdata' in archivo:
            archivo_parquet = os.path.join(directorio_actual, archivo)
            break
    
    if archivo_parquet is None:
        print(f"ERROR: No se encontró ningún archivo yellow_tripdata*.parquet en {directorio_actual}")
        print("\nPor favor, coloca el archivo parquet en este directorio.")
    else:
        print(f"Usando archivo: {archivo_parquet}")
        # Procesar los datos
        procesar_datos_taxis(archivo_parquet)
