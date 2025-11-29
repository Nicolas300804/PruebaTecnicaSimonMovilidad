# Procesador de Datos de Taxis NYC

Este script procesa archivos de datos de taxis de NYC y genera dos reportesCSV:

1. **ultima_ubicacion.csv**: Última ubicación conocida por vehículo
2. **viajes_por_hora.csv**: Reporte de viajes por hora del día

## 🛠️ Herramientas y Dependencias

### Herramientas Elegidas

- **Python:** Lenguaje principal
- **Pandas**: Manipulación y análisis de datos (DataFrame operations)

### Dependencias

Las dependencias usadas para ejecutar el programa son pandas y pyarrow, se instalan con el siguiente comando

```bash
pip install pandas pyarrow
```

> **Nota**: `pyarrow` es necesaria para leer archivos Parquet con pandas.

## 📝 Instrucciones de Instalación

1. **Clonar o descargar** este proyecto en el directorio deseado
2. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

   O instalar manualmente:

   ```bash
   pip install pandas pyarrow
   ```

## 🚀 Cómo Ejecutar

### Comando de Ejecución

```bash
python Prueba.py
```

La **ejecución automática** del comando iniciará el *script* que completará el **proceso de obtención** de los archivos **CSV** requeridos.

## ⚠️ Notas

- El script maneja automáticamente archivos con o sin columnas de latitud/longitud
- Si no existen coordenadas, los valores aparecerán como vacíos
- Todas las horas del día (0-23) se incluyen en el reporte por hora, incluso si no hay viajes

## Video Demo

### **https://youtu.be/4HRTbBrmJjE**
