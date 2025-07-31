#!/usr/bin/env python3
"""
Convertidor optimizado Scopus CSV → RDF/Turtle
Versión corregida con datatypes y lógica consistente
"""

import csv
import json
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import os

class ConversorRDFScopus:
    def __init__(self, ruta_config="config.json"):
        self.config = json.loads(Path(ruta_config).read_text(encoding='utf-8'))
        self.base_uri = self.config['ontology']['base_uri']
        
        # Valores nulos desde config
        self._valores_nulos = set(self.config['null_values'])
        
        # Mapeos desde config
        self.mapeos = self.config['mappings']
        self.datatypes = self.config.get('datatypes', {})
        self.tipo_entidad_a_rdf = self.config['entity_type_mappings']
        self.propiedades_por_tipo = self.config['entity_properties']
        self.mapeo_tipos_documento = self.config['document_type_mappings']
        
        # Almacenamiento
        self.entities = {}
        self.processed = set()
        
    def limpiar_cadena(self, texto):
        """Limpia y escapa strings para TTL"""
        if not texto or str(texto).strip() in self._valores_nulos:
            return None
        
        texto = str(texto).strip()
        # Escapado básico para TTL
        texto = texto.replace('\\', '\\\\')
        texto = texto.replace('"', '\\"')
        texto = texto.replace('\n', '\\n')
        texto = texto.replace('\r', '\\r')
        texto = texto.replace('\t', '\\t')
        return texto
    
    def crear_uri(self, prefijo, identificador):
        """Genera URI única con validación mejorada"""
        if not identificador or str(identificador).strip() in self._valores_nulos:
            return None
        
        id_str = str(identificador).strip()
        
        # Limpiar caracteres problemáticos
        caracteres_seguros = ""
        for char in id_str:
            if char.isalnum() or char in '-_.':
                caracteres_seguros += char
            else:
                caracteres_seguros += '_'
        
        # Evitar URIs muy largas
        if len(caracteres_seguros) > 50:
            hash_suffix = hashlib.md5(id_str.encode()).hexdigest()[:8]
            caracteres_seguros = caracteres_seguros[:40] + '_' + hash_suffix
        
        # Validar que no esté vacío después de limpieza
        if not caracteres_seguros or caracteres_seguros == '_':
            return None
        
        return f"<{self.base_uri}{prefijo}_{caracteres_seguros}>"
    
    def obtener_datatype(self, columna, valor):
        """Obtiene el datatype apropiado para una columna"""
        # Primero verificar en datatypes config
        if columna in self.datatypes:
            return self.datatypes[columna]
        
        # Verificar en mapeos si tiene datatype específico
        mapeo = self.mapeos.get(columna, {})
        if isinstance(mapeo, dict) and 'datatype' in mapeo:
            return mapeo['datatype']
        
        # Inferir datatype básico del valor
        if isinstance(valor, int) or (isinstance(valor, str) and valor.isdigit()):
            return "xsd:integer"
        elif isinstance(valor, float):
            return "xsd:decimal"
        elif isinstance(valor, str) and valor.lower() in ['true', 'false']:
            return "xsd:boolean"
        
        return "xsd:string"
    
    def procesar_csv(self, archivo_csv):
        """Procesa archivo CSV completo"""
        print(f"Procesando: {archivo_csv}")
        
        with open(archivo_csv, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for i, fila in enumerate(reader, 1):
                if i % 500 == 0:
                    print(f"   {i} filas procesadas...")
                
                self.procesar_fila(fila)
        
        print(f"Completado: {len(self.entities)} entidades generadas")

    def agregar_entidad(self, uri, tipo_rdf, propiedades):
        """Añade entidad si no existe y la URI es válida"""
        if not uri or uri == "None" or "<None>" in uri:
            return
        
        if uri not in self.processed:
            self.entities[uri] = (tipo_rdf, propiedades)
            self.processed.add(uri)
    
    def procesar_multivalor(self, texto, tipo_entidad, columna_origen):
        """Procesa campos multivaluados con validación mejorada"""
        if not texto or str(texto).strip() in self._valores_nulos:
            return []
        
        # Usar ; como separador por defecto
        elementos = [e.strip() for e in str(texto).split(';') 
                    if e.strip() and e.strip() not in self._valores_nulos]
        
        uris = []
        for elemento in elementos:
            uri = self._procesar_elemento_individual(elemento, tipo_entidad, columna_origen)
            if uri:
                uris.append(uri)
        
        return uris
    
    def _procesar_elemento_individual(self, elemento, tipo_entidad, columna_origen):
        """Procesa un elemento individual de campo multivaluado"""
        # Extraer nombre e ID si están en formato "Nombre (ID)"
        nombre = elemento
        id_elemento = None
        
        if '(' in elemento and ')' in elemento:
            partes = elemento.split('(')
            nombre = partes[0].strip()
            id_parte = partes[-1].replace(')', '').strip()
            
            # Solo usar como ID si parece un identificador válido
            if id_parte and len(id_parte) > 2:
                id_elemento = id_parte
        
        # Crear URI usando ID si está disponible, sino usar nombre
        identificador = id_elemento if id_elemento else nombre
        uri = self.crear_uri(tipo_entidad, identificador)
        
        if uri:
            # Crear propiedades según tipo de entidad
            propiedades = []
            
            if tipo_entidad == 'Person':
                propiedades.append(('foaf:name', nombre))
                if id_elemento:
                    propiedades.append(('scopus:authorId', id_elemento))
            elif tipo_entidad == 'Organization':
                propiedades.append(('foaf:name', nombre))
            elif tipo_entidad == 'Concept':
                propiedades.append(('skos:prefLabel', nombre))
            elif tipo_entidad == 'Journal':
                propiedades.append(('dc:title', nombre))
            else:
                # Tipo genérico
                propiedades.append(('rdfs:label', nombre))
            
            # Registrar entidad
            tipo_rdf = self.tipo_entidad_a_rdf.get(tipo_entidad, 'schema:Thing')
            self.agregar_entidad(uri, tipo_rdf, propiedades)
        
        return uri
    
    def procesar_fila(self, fila):
        """Procesa una fila del CSV"""
        # Validación de campos requeridos
        campos_requeridos = self.config.get('validation', {}).get('required_fields', ['Title'])
        for campo in campos_requeridos:
            if not fila.get(campo) or str(fila[campo]).strip() in self._valores_nulos:
                return  # Saltar fila si faltan campos críticos
        
        # Crear URI del documento principal
        id_doc = self._obtener_identificador_documento(fila)
        uri_doc = self.crear_uri('pub', id_doc)
        if not uri_doc:
            uri_doc = self.crear_uri('pub', f"doc_{len(self.entities)}")
        
        # Determinar tipo de documento
        tipo_doc = fila.get('Document Type', 'Article')
        tipo_rdf = self.mapeo_tipos_documento.get(tipo_doc, 'schema:CreativeWork')
        
        # Procesar todas las propiedades
        propiedades = []
        
        for columna_csv, mapeo in self.mapeos.items():
            if columna_csv in fila and fila[columna_csv]:
                valor = fila[columna_csv]
                
                if isinstance(mapeo, str):
                    # Mapeo simple (literal)
                    self._procesar_literal_simple(propiedades, mapeo, valor, columna_csv)
                
                elif isinstance(mapeo, dict):
                    if 'type' in mapeo:
                        # Mapeo a objeto/entidad
                        self._procesar_objeto(propiedades, mapeo, valor, columna_csv)
                    else:
                        # Mapeo literal con datatype
                        self._procesar_literal_tipado(propiedades, mapeo, valor, columna_csv)
        
        # Registrar documento principal
        self.agregar_entidad(uri_doc, tipo_rdf, propiedades)
    
    def _obtener_identificador_documento(self, fila):
        """Obtiene el mejor identificador disponible para el documento"""
        # Prioridad: DOI > EID > Art. No. > índice
        for campo_id in ['DOI', 'EID', 'Art. No.']:
            if fila.get(campo_id) and str(fila[campo_id]).strip() not in self._valores_nulos:
                return str(fila[campo_id]).strip()
        return f"doc_{len(self.entities)}"
    
    def _procesar_literal_simple(self, propiedades, propiedad, valor, columna):
        """Procesa propiedad literal simple"""
        datatype = self.obtener_datatype(columna, valor)
        propiedades.append((propiedad, valor, datatype))
    
    def _procesar_literal_tipado(self, propiedades, mapeo, valor, columna):
        """Procesa propiedad literal con datatype específico"""
        propiedad = mapeo['property']
        datatype = mapeo.get('datatype', self.obtener_datatype(columna, valor))
        propiedades.append((propiedad, valor, datatype))
    
    def _procesar_objeto(self, propiedades, mapeo, valor, columna):
        """Procesa propiedad que referencia objetos"""
        tipo_entidad = mapeo['type']
        propiedad = mapeo['property']
        
        # Procesar como multivalor (puede ser uno o varios elementos)
        uris_relacionadas = self.procesar_multivalor(valor, tipo_entidad, columna)
        
        for uri in uris_relacionadas:
            propiedades.append((propiedad, uri, None))  # None indica que es URI, no literal
    
    def generar_ttl(self):
        """Genera contenido TTL completo"""
        from io import StringIO
        
        buffer = StringIO()
        
        # Escribir prefijos
        self._escribir_prefijos(buffer)
        
        # Escribir instancias
        self._escribir_instancias(buffer)
        
        return buffer.getvalue()
    
    def _escribir_prefijos(self, buffer):
        """Escribe prefijos del vocabulario"""
        buffer.write("# === PREFIJOS ===\n")
        for prefijo, uri in self.config['prefixes'].items():
            buffer.write(f"@prefix {prefijo}: <{uri}> .\n")
        buffer.write("\n")
    
    def _escribir_instancias(self, buffer):
        """Escribe todas las instancias RDF"""
        buffer.write("# === INSTANCIAS RDF ===\n\n")
        
        for uri, (tipo_rdf, propiedades) in self.entities.items():
            if not uri or "<None>" in uri:
                continue
            
            # Escribir tipo
            buffer.write(f"{uri} rdf:type {tipo_rdf} .\n")
            
            # Escribir propiedades
            for prop in propiedades:
                if len(prop) == 3:
                    propiedad, valor, datatype = prop
                    
                    if datatype is None:
                        # Es una URI (objeto)
                        buffer.write(f"{uri} {propiedad} {valor} .\n")
                    else:
                        # Es un literal
                        valor_limpio = self.limpiar_cadena(valor)
                        if valor_limpio:
                            buffer.write(f'{uri} {propiedad} "{valor_limpio}"^^{datatype} .\n')
                else:
                    # Compatibilidad con formato anterior
                    propiedad, valor = prop
                    valor_limpio = self.limpiar_cadena(valor)
                    if valor_limpio:
                        buffer.write(f'{uri} {propiedad} "{valor_limpio}"^^xsd:string .\n')
            
            buffer.write("\n")
    
    def guardar_archivos(self):
        """Guarda archivo TTL"""
        contenido = self.generar_ttl()
        
        archivo_principal = self.config['output']['main']
        
        with open(archivo_principal, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        # Calcular estadísticas
        num_tripletas = contenido.count(' .\n')
        num_entidades = len(self.entities)
        
        print(f"Guardado: {archivo_principal}")
        print(f"Entidades: {num_entidades:,}")
        print(f"Tripletas: {num_tripletas:,}")
        
        # Mostrar estadísticas por tipo
        self._mostrar_estadisticas_tipos()
    
    def _mostrar_estadisticas_tipos(self):
        """Muestra estadísticas por tipo de entidad"""
        tipos_count = {}
        for uri, (tipo_rdf, props) in self.entities.items():
            tipos_count[tipo_rdf] = tipos_count.get(tipo_rdf, 0) + 1
        
        print("\nEntidades por tipo:")
        for tipo, count in sorted(tipos_count.items(), key=lambda x: x[1], reverse=True):
            print(f"   {tipo}: {count:,}")
    
    def crear_interfaz_grafica(self):
        """Crea una interfaz gráfica completa y amigable"""
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("Convertidor Scopus CSV → RDF/Turtle")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Centrar ventana
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
        
        # Variables para archivos
        self.archivo_csv_var = tk.StringVar(value="Ningún archivo seleccionado")
        self.archivo_salida_var = tk.StringVar(value="ontologia_scopus.ttl")
        
        self._crear_widgets()
        self._configurar_estilos()
        
    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Convertidor Scopus CSV -> RDF/Turtle", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Descripción
        desc_label = ttk.Label(main_frame, 
                              text="Convierte archivos CSV de Scopus a formato RDF/Turtle\n"
                                   "para crear ontologías semánticas.",
                              font=('Arial', 10),
                              foreground='gray')
        desc_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Separador
        separator1 = ttk.Separator(main_frame, orient='horizontal')
        separator1.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Sección 1: Archivo CSV de entrada
        input_label = ttk.Label(main_frame, text="📄 Archivo CSV de Scopus:", 
                               font=('Arial', 12, 'bold'))
        input_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        # Frame para archivo de entrada
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        
        self.archivo_entry = ttk.Entry(input_frame, textvariable=self.archivo_csv_var, 
                                      state='readonly', font=('Arial', 9))
        self.archivo_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.boton_buscar = ttk.Button(input_frame, text="📂 Buscar...", 
                                      command=self.seleccionar_archivo_csv_gui)
        self.boton_buscar.grid(row=0, column=1)
        
        # Separador
        separator2 = ttk.Separator(main_frame, orient='horizontal')
        separator2.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 20))
        
        # Sección 2: Archivo de salida
        output_label = ttk.Label(main_frame, text="💾 Archivo RDF de salida:", 
                                font=('Arial', 12, 'bold'))
        output_label.grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        
        # Frame para archivo de salida
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        output_frame.columnconfigure(0, weight=1)
        
        self.salida_entry = ttk.Entry(output_frame, textvariable=self.archivo_salida_var, 
                                     font=('Arial', 9))
        self.salida_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.boton_guardar = ttk.Button(output_frame, text="📁 Guardar como...", 
                                       command=self.seleccionar_archivo_salida)
        self.boton_guardar.grid(row=0, column=1)
        
        # Separador
        separator3 = ttk.Separator(main_frame, orient='horizontal')
        separator3.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 20))
        
        # Área de progreso y estado
        self.estado_label = ttk.Label(main_frame, text="Listo para convertir", 
                                     font=('Arial', 10), foreground='green')
        self.estado_label.grid(row=9, column=0, columnspan=3, pady=(0, 10))
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Botones principales
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=11, column=0, columnspan=3, pady=(10, 0))
        
        self.boton_convertir = ttk.Button(button_frame, text="🚀 Convertir a RDF", 
                                         command=self.ejecutar_conversion_gui,
                                         style='Accent.TButton')
        self.boton_convertir.grid(row=0, column=0, padx=(0, 10))
        
        self.boton_salir = ttk.Button(button_frame, text="Salir", 
                                     command=self.root.quit)
        self.boton_salir.grid(row=0, column=1)
        
        # Área de información
        info_frame = ttk.LabelFrame(main_frame, text="Informacion", padding="10")
        info_frame.grid(row=12, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
        info_frame.columnconfigure(0, weight=1)
        
        info_text = ("• Selecciona un archivo CSV exportado desde Scopus\n"
                    "• El archivo RDF se guardará en formato Turtle (.ttl)\n"
                    "• La conversión puede tardar unos minutos según el tamaño\n"
                    "• Se mostrarán estadísticas al finalizar la conversión")
        
        info_label = ttk.Label(info_frame, text=info_text, font=('Arial', 9), 
                              foreground='gray', justify=tk.LEFT)
        info_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
    def _configurar_estilos(self):
        """Configura estilos personalizados"""
        style = ttk.Style()
        
        # Estilo para botón principal
        style.configure('Accent.TButton', font=('Arial', 11, 'bold'))
        
    def seleccionar_archivo_csv_gui(self):
        """Selecciona archivo CSV con interfaz mejorada"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV de Scopus",
            filetypes=[
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ],
            initialdir=os.getcwd()
        )
        
        if archivo:
            self.archivo_csv_var.set(archivo)
            self.estado_label.config(text="Archivo CSV seleccionado", foreground='green')
            
            # Sugerir nombre de salida basado en el archivo de entrada
            nombre_base = Path(archivo).stem
            nombre_salida = f"{nombre_base}_rdf.ttl"
            directorio = Path(archivo).parent
            ruta_completa = directorio / nombre_salida
            self.archivo_salida_var.set(str(ruta_completa))
        
    def seleccionar_archivo_salida(self):
        """Selecciona ubicación para guardar archivo RDF"""
        archivo = filedialog.asksaveasfilename(
            title="Guardar archivo RDF como...",
            defaultextension=".ttl",
            filetypes=[
                ("Archivos Turtle", "*.ttl"),
                ("Archivos RDF", "*.rdf"),
                ("Todos los archivos", "*.*")
            ],
            initialdir=os.path.dirname(self.archivo_salida_var.get()) if self.archivo_salida_var.get() else os.getcwd(),
            initialfile=os.path.basename(self.archivo_salida_var.get()) if self.archivo_salida_var.get() else "ontologia_scopus.ttl"
        )
        
        if archivo:
            self.archivo_salida_var.set(archivo)
            self.estado_label.config(text="Ubicacion de salida configurada", foreground='green')
    
    def ejecutar_conversion_gui(self):
        """Ejecuta la conversión con interfaz gráfica mejorada"""
        # Validar archivo de entrada
        archivo_csv = self.archivo_csv_var.get()
        if archivo_csv == "Ningún archivo seleccionado" or not archivo_csv:
            messagebox.showerror("Error", "Por favor selecciona un archivo CSV de entrada")
            return
        
        if not Path(archivo_csv).exists():
            messagebox.showerror("Error", f"El archivo seleccionado no existe:\n{archivo_csv}")
            return
        
        # Validar archivo de salida
        archivo_salida = self.archivo_salida_var.get()
        if not archivo_salida:
            messagebox.showerror("Error", "Por favor especifica la ubicación del archivo de salida")
            return
        
        # Crear directorio de salida si no existe
        try:
            Path(archivo_salida).parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"No se puede crear el directorio de salida:\n{str(e)}")
            return
        
        # Actualizar configuración de salida
        self.config['output']['main'] = archivo_salida
        
        # Ejecutar conversión
        self.boton_convertir.config(state='disabled')
        self.boton_buscar.config(state='disabled')
        self.boton_guardar.config(state='disabled')
        self.progress.start(10)
        self.estado_label.config(text="🔄 Procesando archivo CSV...", foreground='blue')
        
        # Forzar actualización de interfaz
        self.root.update()
        
        try:
            # Procesar archivo
            self.procesar_csv(archivo_csv)
            
            self.estado_label.config(text="💾 Guardando archivo RDF...", foreground='blue')
            self.root.update()
            
            # Guardar archivo
            self.guardar_archivos()
            
            # Mostrar resultado exitoso
            self.progress.stop()
            self.estado_label.config(text="Conversion completada exitosamente", foreground='green')
            
            # Mostrar estadísticas
            estadisticas = self._generar_estadisticas()
            messagebox.showinfo(
                "🎉 Conversión Completada",
                f"El archivo CSV se ha convertido exitosamente a RDF.\n\n"
                f"📊 ESTADÍSTICAS:\n"
                f"• Archivo de entrada: {Path(archivo_csv).name}\n"
                f"• Archivo de salida: {Path(archivo_salida).name}\n"
                f"• Entidades generadas: {len(self.entities):,}\n"
                f"• Tamaño del archivo: {self._obtener_tamano_archivo(archivo_salida)}\n\n"
                f"{estadisticas}\n\n"
                f"📁 Ubicación: {archivo_salida}"
            )
            
        except Exception as e:
            self.progress.stop()
            error_msg = f"Error durante la conversión:\n{str(e)}"
            self.estado_label.config(text="Error en la conversion", foreground='red')
            messagebox.showerror("Error de Conversión", error_msg)
        
        finally:
            # Rehabilitar botones
            self.boton_convertir.config(state='normal')
            self.boton_buscar.config(state='normal')
            self.boton_guardar.config(state='normal')
            self.progress.stop()
    
    def _generar_estadisticas(self):
        """Genera estadísticas detalladas de la conversión"""
        tipos_count = {}
        for uri, (tipo_rdf, props) in self.entities.items():
            tipos_count[tipo_rdf] = tipos_count.get(tipo_rdf, 0) + 1
        
        stats = "🔍 TIPOS DE ENTIDADES:\n"
        for tipo, count in sorted(tipos_count.items(), key=lambda x: x[1], reverse=True)[:5]:
            nombre_corto = tipo.split(':')[-1] if ':' in tipo else tipo
            stats += f"• {nombre_corto}: {count:,}\n"
        
        return stats
    
    def _obtener_tamano_archivo(self, ruta_archivo):
        """Obtiene el tamaño del archivo en formato legible"""
        try:
            size_bytes = Path(ruta_archivo).stat().st_size
            if size_bytes < 1024:
                return f"{size_bytes} bytes"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            else:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
        except:
            return "Desconocido"
    
    def iniciar_interfaz_grafica(self):
        """Inicia la interfaz gráfica completa"""
        print("Iniciando interfaz grafica amigable...")
        self.crear_interfaz_grafica()
        self.root.mainloop()

    def seleccionar_archivo_csv(self):
        """Abre diálogo para seleccionar archivo CSV"""
        print("Seleccionando archivo CSV...")
        
        # Configurar ventana raíz de Tkinter (oculta)
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        root.attributes('-topmost', True)  # Traer diálogo al frente
        
        # Mostrar diálogo de selección de archivo
        archivo_seleccionado = filedialog.askopenfilename(
            title="Seleccionar archivo CSV de Scopus",
            filetypes=[
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ],
            initialdir=".",
        )
        
        root.destroy()  # Limpiar ventana
        
        if not archivo_seleccionado:
            print("No se selecciono ningun archivo")
            return None
        
        if not archivo_seleccionado.lower().endswith('.csv'):
            messagebox.showwarning("Advertencia", "El archivo seleccionado no es un CSV")
            return None
        
        print(f"Archivo seleccionado: {archivo_seleccionado}")
        return archivo_seleccionado
    
    def ejecutar_con_interfaz(self):
        """Ejecuta conversión con interfaz gráfica para seleccionar archivo"""
        print("CONVERTIDOR CSV -> RDF (Version con Interfaz)")
        print("=" * 50)
        
        # Seleccionar archivo CSV
        archivo_csv = self.seleccionar_archivo_csv()
        if not archivo_csv:
            return
        
        # Validar que el archivo existe
        if not Path(archivo_csv).exists():
            messagebox.showerror("Error", f"No se puede acceder al archivo: {archivo_csv}")
            return
        
        try:
            # Ejecutar conversión
            self.procesar_csv(archivo_csv)
            self.guardar_archivos()
            
            print("Conversion completada exitosamente")
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "Conversión Completada", 
                f"El archivo CSV se ha convertido exitosamente a RDF.\n\n"
                f"Entidades generadas: {len(self.entities):,}\n"
                f"Archivo de salida: {self.config['output']['main']}"
            )
            
        except Exception as e:
            error_msg = f"Error durante la conversión: {str(e)}"
            print(f"Error: {error_msg}")
            messagebox.showerror("Error de Conversión", error_msg)

    def ejecutar(self, archivo_csv="scopus.csv"):
        """Ejecuta conversión CSV a RDF"""
        print("CONVERTIDOR CSV -> RDF (Version Corregida)")
        print("=" * 45)
        
        if not Path(archivo_csv).exists():
            print(f"Error: No se encuentra {archivo_csv}")
            return
        
        self.procesar_csv(archivo_csv)
        self.guardar_archivos()
        
        print("Conversion completada exitosamente")

if __name__ == "__main__":
    import sys
    
    # Si se ejecuta sin argumentos, usar interfaz gráfica completa
    if len(sys.argv) == 1:
        config_file = "config.json"
        conversor = ConversorRDFScopus(config_file)
        conversor.iniciar_interfaz_grafica()
    else:
        # Modo comando con argumentos
        archivo_csv = sys.argv[1] if len(sys.argv) > 1 else "scopus.csv"
        config_file = sys.argv[2] if len(sys.argv) > 2 else "config.json"
        
        conversor = ConversorRDFScopus(config_file)
        conversor.ejecutar(archivo_csv)