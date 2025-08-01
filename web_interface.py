#!/usr/bin/env python3
"""
Web Interface for Scopus CSV to RDF Converter
Flask-based web application
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import os
import json
from pathlib import Path
from werkzeug.utils import secure_filename
import tempfile
from scopus_converter import ConversorRDFScopus

class EnhancedConversorRDFScopus(ConversorRDFScopus):
    """Versión extendida del convertidor que soporta delimitadores personalizados"""
    
    def __init__(self, ruta_config="config.json"):
        super().__init__(ruta_config)
        self.custom_multi_delimiters = {}
    
    def set_multi_value_delimiters(self, delimiters_dict):
        """Configura delimitadores personalizados por columna"""
        self.custom_multi_delimiters = delimiters_dict
    
    def set_base_uri(self, base_uri):
        """Configura la URL base personalizada para las entidades RDF"""
        self.base_uri = base_uri
    
    def procesar_multivalor(self, texto, tipo_entidad, columna_origen):
        """Versión mejorada que usa delimitadores personalizados por columna"""
        if not texto or str(texto).strip() in self._valores_nulos:
            return []
        
        # Usar delimitador personalizado si está configurado para esta columna
        delimiter = self.custom_multi_delimiters.get(columna_origen, ';')
        
        # Procesar con el delimitador apropiado
        elementos = [e.strip() for e in str(texto).split(delimiter) 
                    if e.strip() and e.strip() not in self._valores_nulos]
        
        uris = []
        for elemento in elementos:
            uri = self._procesar_elemento_individual(elemento, tipo_entidad, columna_origen)
            if uri:
                uris.append(uri)
        
        return uris

app = Flask(__name__)
app.secret_key = 'scopus_converter_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Configuración
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'csv', 'txt'}

# Crear directorios
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Subir archivo CSV"""
    # Verificar si es una recarga de archivo existente
    reload_filepath = request.form.get('reload_file')
    if reload_filepath and os.path.exists(reload_filepath):
        # Recargar archivo existente para reconfiguración
        filename = os.path.basename(reload_filepath)
        filepath = reload_filepath
    else:
        # Subida normal de archivo
        if 'file' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('index'))
        
        if not (file and allowed_file(file.filename)):
            flash('Tipo de archivo no válido. Solo se permiten CSV y TXT.', 'error')
            return redirect(url_for('index'))
            
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
    
    # Detectar delimitadores automáticamente
    detected_delimiters = detect_csv_delimiters(filepath)
    
    # Leer una muestra para obtener columnas
    try:
        import pandas as pd
        sample_df = pd.read_csv(filepath, delimiter=detected_delimiters['recommended'], nrows=20, encoding='utf-8-sig')
        sample_columns = sample_df.columns.tolist()
        sample_data = sample_df.to_dict('records')
    except:
        sample_columns = []
        sample_data = []
    
    # Cargar base_uri desde config.json
    try:
        import json
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            default_base_uri = config.get('ontology', {}).get('base_uri', 'https://onto.utpl.edu.ec/scopus/resource/')
    except:
        default_base_uri = 'https://onto.utpl.edu.ec/scopus/resource/'
    
    file_info = {
        'filename': filename,
        'filepath': filepath,
        'file_size': os.path.getsize(filepath),
        'detected_delimiters': detected_delimiters,
        'sample_columns': sample_columns,
        'sample_data': sample_data,
        'default_base_uri': default_base_uri
    }
    
    return render_template('configure_delimiter.html', file_info=file_info)

@app.route('/analyze', methods=['POST'])
def analyze_file():
    """Analizar archivo con delimitador seleccionado"""
    filepath = request.form.get('filepath')
    delimiter = request.form.get('delimiter', ',')
    default_multi_delimiter = request.form.get('default_multi_delimiter', ';')
    base_uri = request.form.get('base_uri', '').strip()
    
    # Validar y formatear base_uri
    if base_uri:
        if not base_uri.startswith(('http://', 'https://')):
            base_uri = 'https://' + base_uri
        if not base_uri.endswith('/'):
            base_uri += '/'
    else:
        base_uri = 'https://onto.utpl.edu.ec/scopus/resource/'
    
    # Obtener delimitadores configurados manualmente por columna
    configured_multi_delimiters = {}
    for key, value in request.form.items():
        if key.startswith('multi_delimiter_') and value.strip():
            column_name = key.replace('multi_delimiter_', '')
            configured_multi_delimiters[column_name] = value
    
    if not filepath or not os.path.exists(filepath):
        flash('Archivo no encontrado', 'error')
        return redirect(url_for('index'))
    
    try:
        import pandas as pd
        
        # Leer CSV con delimitador seleccionado
        df = pd.read_csv(filepath, delimiter=delimiter, nrows=20, encoding='utf-8-sig')
        
        # Contar filas totales
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            total_rows = sum(1 for line in f) - 1  # Restar header
        
        # Usar delimitadores configurados manualmente o detectar automáticamente
        if configured_multi_delimiters:
            multi_value_delimiters = configured_multi_delimiters
        else:
            multi_value_delimiters = detect_multi_value_delimiters(df, default_multi_delimiter)
        
        file_info = {
            'filename': os.path.basename(filepath),
            'filepath': filepath,
            'headers': df.columns.tolist(),
            'row_count': total_rows,
            'file_size': os.path.getsize(filepath),
            'headers_count': len(df.columns),
            'delimiter': delimiter,
            'default_multi_delimiter': default_multi_delimiter,
            'multi_value_delimiters': multi_value_delimiters,
            'sample_data': df.head(20).to_dict('records'),
            'configured_manually': bool(configured_multi_delimiters),
            'base_uri': base_uri
        }
        
        return render_template('convert.html', file_info=file_info)
        
    except Exception as e:
        flash(f'Error al analizar el archivo: {str(e)}', 'error')
        return redirect(url_for('index'))

def detect_csv_delimiters(filepath):
    """Detecta automáticamente posibles delimitadores CSV"""
    delimiters = [',', ';', '\t', '|', ' ']
    delimiter_scores = {}
    
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            sample = f.read(2048)  # Leer muestra
            
        for delimiter in delimiters:
            try:
                import csv
                reader = csv.reader(sample.splitlines(), delimiter=delimiter)
                rows = list(reader)
                if len(rows) > 1:
                    col_counts = [len(row) for row in rows[:5]]
                    if len(set(col_counts)) == 1 and col_counts[0] > 1:
                        delimiter_scores[delimiter] = col_counts[0]
            except:
                continue
                
        # Devolver delimitadores ordenados por score
        sorted_delimiters = sorted(delimiter_scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'recommended': sorted_delimiters[0][0] if sorted_delimiters else ',',
            'options': [
                (',', 'Coma (,)', delimiter_scores.get(',', 0)),
                (';', 'Punto y coma (;)', delimiter_scores.get(';', 0)),
                ('\t', 'Tabulación', delimiter_scores.get('\t', 0)),
                ('|', 'Barra vertical (|)', delimiter_scores.get('|', 0)),
                (' ', 'Espacio', delimiter_scores.get(' ', 0))
            ]
        }
    except Exception:
        return {
            'recommended': ',',
            'options': [(',', 'Coma (,)', 0), (';', 'Punto y coma (;)', 0), ('\t', 'Tabulación', 0), ('|', 'Barra vertical (|)', 0), (' ', 'Espacio', 0)]
        }

def detect_multi_value_delimiters(df, preferred_delimiter=';'):
    """Detecta automáticamente delimitadores de múltiples valores por columna"""
    auto_delimiters = {}
    
    # Priorizar el delimitador preferido, luego otros comunes
    common_delimiters = [preferred_delimiter]
    if preferred_delimiter != ';':
        common_delimiters.append(';')
    
    # Agregar otros delimitadores
    other_delimiters = [',', '|', ' and ', ' & ', ' - ', ' / ', ' | ']
    for delim in other_delimiters:
        if delim != preferred_delimiter:
            common_delimiters.append(delim)
    
    for column in df.columns:
        column_data = df[column].dropna().astype(str)
        
        # Analizar solo las primeras filas para eficiencia
        sample_data = column_data.head(10)
        
        delimiter_scores = {}
        
        for delimiter in common_delimiters:
            score = 0
            total_cells = 0
            
            for value in sample_data:
                if pd.isna(value) or value == 'nan':
                    continue
                    
                total_cells += 1
                
                # Contar cuántas veces aparece el delimitador
                if delimiter in str(value):
                    # Verificar que después del delimitador hay contenido válido
                    parts = str(value).split(delimiter)
                    if len(parts) > 1:
                        # Verificar que las partes no estén vacías
                        valid_parts = [part.strip() for part in parts if part.strip()]
                        if len(valid_parts) > 1:
                            score += len(valid_parts) - 1
            
            # Calcular puntuación promedio
            if total_cells > 0:
                delimiter_scores[delimiter] = score / total_cells
        
        # Seleccionar el mejor delimitador si supera el umbral
        if delimiter_scores:
            best_delimiter = max(delimiter_scores.items(), key=lambda x: x[1])
            
            # Solo considerar si aparece en al menos 30% de las celdas con cierta frecuencia
            if best_delimiter[1] > 0.3:
                auto_delimiters[column] = best_delimiter[0]
    
    return auto_delimiters

@app.route('/convert', methods=['POST'])
def convert_file():
    """Convertir CSV a RDF"""
    filepath = request.form.get('filepath')
    delimiter = request.form.get('delimiter', ',')
    max_rows = request.form.get('max_rows')
    base_uri = request.form.get('base_uri', '').strip()
    
    # Validar y formatear base_uri
    if base_uri:
        if not base_uri.startswith(('http://', 'https://')):
            base_uri = 'https://' + base_uri
        if not base_uri.endswith('/'):
            base_uri += '/'
    else:
        base_uri = 'https://onto.utpl.edu.ec/scopus/resource/'
    
    # Obtener delimitadores de múltiples valores configurados
    multi_value_delimiters = {}
    for key, value in request.form.items():
        if key.startswith('multi_delimiter_') and value.strip():
            column_name = key.replace('multi_delimiter_', '')
            multi_value_delimiters[column_name] = value
    
    if not filepath or not os.path.exists(filepath):
        flash('Archivo no encontrado', 'error')
        return redirect(url_for('index'))
    
    try:
        import pandas as pd
        
        # Leer CSV con delimitador configurado
        if max_rows and max_rows.strip():
            df = pd.read_csv(filepath, delimiter=delimiter, nrows=int(max_rows), encoding='utf-8-sig')
        else:
            df = pd.read_csv(filepath, delimiter=delimiter, encoding='utf-8-sig')
        
        # Crear archivo temporal con configuración aplicada
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8')
        df.to_csv(temp_file.name, index=False, sep=delimiter)
        temp_file.close()
        
        # Crear convertidor con configuración de delimitadores personalizados
        converter = EnhancedConversorRDFScopus('config.json')
        
        # Configurar base_uri personalizada
        converter.set_base_uri(base_uri)
        
        # Configurar delimitadores de múltiples valores si están configurados
        if multi_value_delimiters:
            converter.set_multi_value_delimiters(multi_value_delimiters)
        
        # Procesar archivo
        converter.procesar_csv(temp_file.name)
        
        # Generar RDF
        rdf_content = converter.generar_ttl()
        
        # Limpiar archivo temporal
        os.unlink(temp_file.name)
        
        # Guardar archivo de salida
        filename = Path(filepath).stem
        output_filename = f"{filename}_ontology.ttl"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rdf_content)
        
        # Estadísticas
        num_entities = len(converter.entities)
        num_triples = rdf_content.count(' .\n')
        file_size = len(rdf_content.encode('utf-8'))
        
        stats = {
            'entities': num_entities,
            'triples': num_triples,
            'file_size': file_size,
            'output_file': output_filename,
            'output_path': output_path,
            'processed_rows': len(df),
            'multi_value_delimiters': multi_value_delimiters
        }
        
        # Preview del RDF (primeras 50 líneas)
        rdf_lines = rdf_content.split('\n')
        rdf_preview = '\n'.join(rdf_lines[:50])
        if len(rdf_lines) > 50:
            rdf_preview += '\n\n... (archivo completo disponible para descarga)'
        
        return render_template('result.html', stats=stats, rdf_preview=rdf_preview)
        
    except Exception as e:
        flash(f'Error al convertir archivo: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    """Descargar archivo RDF generado"""
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            flash('Archivo no encontrado', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error al descargar archivo: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/config')
def view_config():
    """Ver configuración actual"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        return render_template('config.html', config=config)
    except Exception as e:
        flash(f'Error al cargar configuración: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    print("=== INTERFAZ WEB SCOPUS CSV -> RDF ===")
    print("Iniciando servidor web...")
    print("Accede a: http://localhost:5000")
    print("Presiona Ctrl+C para detener")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)