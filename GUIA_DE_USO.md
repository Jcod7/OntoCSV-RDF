# 📖 GUÍA DE USO - CONVERTIDOR SCOPUS CSV → RDF

## 🎯 **¿Qué hace este programa?**

El **Convertidor Scopus CSV → RDF** transforma automáticamente datos bibliográficos exportados desde Scopus (formato CSV) en una ontología RDF estructurada y consultable. Esto permite:

- ✅ **Crear redes de conocimiento** a partir de publicaciones académicas
- ✅ **Generar ontologías semánticas** usando estándares internacionales
- ✅ **Analizar relaciones** entre autores, conceptos y organizaciones
- ✅ **Preparar datos** para consultas SPARQL y análisis avanzados

---

## 🚀 **INICIO RÁPIDO (3 pasos)**

### **Paso 1: Ejecutar el Programa**
```bash
# Opción A: Interfaz Gráfica (Recomendado)
python ejecutar.py

# Opción B: Ejecución Directa
python scopus_converter.py
```

### **Paso 2: Seleccionar Archivo CSV**
- Click en **"Buscar..."**
- Seleccionar su archivo `.csv` exportado de Scopus
- El programa validará automáticamente el formato

### **Paso 3: Convertir**
- Click en **"Convertir a RDF"**
- Esperar el procesamiento (se muestra progreso)
- ¡Listo! Su ontología RDF estará en formato `.ttl`

---

## 🖥️ **INTERFAZ GRÁFICA - Guía Detallada**

### **Pantalla Principal:**

```
┌─────────────────────────────────────────────────┐
│        Convertidor Scopus CSV -> RDF/Turtle    │
├─────────────────────────────────────────────────┤
│                                                 │
│ Archivo CSV de Scopus:                         │
│ [________________________] [Buscar...]         │
│                                                 │
│ Archivo RDF de salida:                          │
│ [________________________] [Guardar como...]   │
│                                                 │
│ Estado: Listo para convertir                    │
│ [████████████████████████████] 100%             │
│                                                 │
│        [Convertir a RDF]  [Salir]               │
│                                                 │
│ Información:                                    │
│ • Selecciona archivo CSV exportado de Scopus   │
│ • La conversión puede tardar varios minutos     │
│ • Se mostrarán estadísticas al finalizar        │
└─────────────────────────────────────────────────┘
```

### **Controles Principales:**

#### **1. 📂 Selección de Archivo CSV**
- **Función:** Permite elegir el archivo CSV de Scopus a convertir
- **Formatos aceptados:** `.csv` (exportado desde Scopus)
- **Validación:** El programa verifica que el archivo tenga las columnas requeridas

#### **2. 💾 Archivo de Salida**
- **Función:** Define dónde guardar la ontología RDF generada
- **Formato:** `.ttl` (Turtle - formato RDF estándar)
- **Auto-naming:** Se sugiere automáticamente basado en el archivo de entrada

#### **3. 🚀 Botón "Convertir a RDF"**
- **Función:** Inicia el proceso de transformación
- **Progreso:** Muestra barra de progreso durante la conversión
- **Estadísticas:** Al finalizar, muestra resumen detallado

---

## ⚙️ **CONFIGURACIÓN AVANZADA**

### **Archivo `config.json`**

El comportamiento del convertidor se controla mediante `config.json`:

```json
{
  "ontology": {
    "base_uri": "https://onto.utpl.edu.ec/scopus/resource/"
  },
  "mappings": {
    "Authors": {"property": "dc:creator", "type": "Person"},
    "Title": {"property": "dc:title", "datatype": "xsd:string"}
  },
  "validation": {
    "required_fields": ["Title", "Authors", "Year"]
  }
}
```

#### **Secciones Configurables:**

**🎯 `ontology.base_uri`**
- **Qué es:** URL base para todas las entidades RDF generadas
- **Personalizar:** Cambiar por su dominio organizacional
- **Ejemplo:** `"https://mi-universidad.edu/ontologia/"`

**🗂️ `mappings`**
- **Qué es:** Define cómo las columnas CSV se transforman en propiedades RDF
- **Estructura:** `"Columna_CSV": {"property": "prefijo:propiedad", "datatype": "tipo"}`
- **Personalizar:** Agregar nuevas columnas o modificar propiedades

**✅ `validation.required_fields`**
- **Qué es:** Campos obligatorios que debe tener cada registro
- **Por defecto:** `["Title", "Authors", "Year"]`
- **Personalizar:** Agregar/quitar campos según sus necesidades

---

## 💻 **USO POR LÍNEA DE COMANDOS**

### **Ejecución Básica:**
```python
from scopus_converter import ConversorRDFScopus

# Crear instancia del convertidor
converter = ConversorRDFScopus()

# Convertir archivo específico
converter.ejecutar("mi_archivo.csv")
```

### **Con Configuración Personalizada:**
```python
# Usar configuración personalizada
converter = ConversorRDFScopus("mi_config.json")
converter.ejecutar("datos_scopus.csv")
```

---

## 🔧 **FUNCIONES PRINCIPALES DEL CÓDIGO**

### **🎯 CONCEPTOS FUNDAMENTALES**

Antes de explicar las funciones, es importante entender tres tipos de datos que maneja el convertidor:

#### **📄 1. LITERALES (Valores simples)**
```python
# Ejemplo: Título de un artículo
"Title": {"property": "dc:title", "datatype": "xsd:string"}
```
**¿Qué son?** Valores de texto, números o fechas que se almacenan directamente.

**En RDF se ven así:**
```turtle
<pub_123> dc:title "Inteligencia Artificial en Medicina"^^xsd:string .
<pub_123> dcterms:date "2024"^^xsd:gYear .
<pub_123> schema:citedByCount "15"^^xsd:integer .
```

#### **🔗 2. OBJETOS (Entidades relacionadas)**
```python
# Ejemplo: Autores como entidades separadas
"Authors": {"property": "dc:creator", "type": "Person"}
```
**¿Qué son?** Referencias a otras entidades que tienen sus propias propiedades.

**En RDF se ven así:**
```turtle
# El artículo referencia al autor (objeto)
<pub_123> dc:creator <Person_Smith_J> .

# El autor es una entidad separada con sus propiedades
<Person_Smith_J> rdf:type foaf:Person .
<Person_Smith_J> foaf:name "Smith, J."^^xsd:string .
<Person_Smith_J> scopus:authorId "12345"^^xsd:string .
```

#### **📊 3. CAMPOS MULTIVALUADOS (Múltiples valores)**
```python
# Ejemplo: Múltiples autores separados por ';'
"Authors": "Smith, J.; García, M.; Wilson, K."
```
**¿Qué son?** Un campo CSV que contiene varios valores separados por punto y coma.

**En RDF se convierten en múltiples tripletas:**
```turtle
<pub_123> dc:creator <Person_Smith_J> .
<pub_123> dc:creator <Person_García_M> .
<pub_123> dc:creator <Person_Wilson_K> .
```

---

### **Clase `ConversorRDFScopus`**

#### **📋 `__init__(self, ruta_config="config.json")`**
```python
def __init__(self, ruta_config="config.json"):
    self.config = json.loads(Path(ruta_config).read_text(encoding='utf-8'))
    self.base_uri = self.config['ontology']['base_uri']
    self.entities = {}          # Almacena entidades RDF generadas
    self.processed = set()      # URIs ya procesadas (evita duplicados)
    
    # Separar mapeos por tipo
    self.mapeos = self.config['mappings']
    self.datatypes = self.config.get('datatypes', {})
```
**Propósito:** Inicializa el convertidor cargando la configuración y preparando estructuras de datos para manejar objetos, literales y campos multivaluados.

#### **🔄 `procesar_csv(self, archivo_csv)`**
```python
def procesar_csv(self, archivo_csv):
    with open(archivo_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for i, fila in enumerate(reader, 1):
            if i % 500 == 0:
                print(f"   {i} filas procesadas...")
            self.procesar_fila(fila)
```
**Propósito:** Lee el archivo CSV línea por línea y procesa cada registro bibliográfico.

#### **🏷️ `crear_uri(self, prefijo, identificador)`**
```python
def crear_uri(self, prefijo, identificador):
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
    
    return f"<{self.base_uri}{prefijo}_{caracteres_seguros}>"
```
**Propósito:** Genera URIs únicas y válidas para cada entidad RDF, limpiando caracteres especiales.

#### **📝 `procesar_fila(self, fila)` - 🎯 FUNCIÓN CLAVE**
```python
def procesar_fila(self, fila):
    # 1. Validar campos requeridos
    campos_requeridos = self.config.get('validation', {}).get('required_fields', ['Title'])
    for campo in campos_requeridos:
        if not fila.get(campo):
            return  # Saltar fila si falta información crítica
    
    # 2. Crear URI del documento principal
    id_doc = self._obtener_identificador_documento(fila)
    uri_doc = self.crear_uri('pub', id_doc)
    
    # 3. Procesar todas las propiedades según mapeos
    propiedades = []
    for columna_csv, mapeo in self.mapeos.items():
        if columna_csv in fila and fila[columna_csv]:
            valor = fila[columna_csv]
            
            # DECISIÓN: ¿Es literal u objeto?
            if isinstance(mapeo, str):
                # LITERAL SIMPLE
                self._procesar_literal_simple(propiedades, mapeo, valor, columna_csv)
            
            elif isinstance(mapeo, dict):
                if 'type' in mapeo:
                    # OBJETO (crea entidades relacionadas)
                    self._procesar_objeto(propiedades, mapeo, valor, columna_csv)
                else:
                    # LITERAL CON DATATYPE
                    self._procesar_literal_tipado(propiedades, mapeo, valor, columna_csv)
```

**🔍 Propósito:** Esta es la función más importante. Decide cómo tratar cada campo CSV:

**📄 LITERALES:** Valores directos como títulos, años, números
```python
# Ejemplo: "Title": "Inteligencia Artificial" 
# → Se convierte en: <pub_123> dc:title "Inteligencia Artificial"^^xsd:string
```

**🔗 OBJETOS:** Referencias a otras entidades
```python  
# Ejemplo: "Authors": "Smith, J.; García, M."
# → Se convierte en: <pub_123> dc:creator <Person_Smith_J>
#                    <pub_123> dc:creator <Person_García_M>
```

#### **🔗 `_procesar_objeto(self, propiedades, mapeo, valor, columna)` - MANEJO DE OBJETOS**
```python
def _procesar_objeto(self, propiedades, mapeo, valor, columna):
    tipo_entidad = mapeo['type']      # Ej: "Person", "Organization"
    propiedad = mapeo['property']     # Ej: "dc:creator", "foaf:workplaceHomepage"
    
    # PASO 1: Procesar campo multivaluado (si tiene ';')
    uris_relacionadas = self.procesar_multivalor(valor, tipo_entidad, columna)
    
    # PASO 2: Crear tripletas que conectan documento con objetos
    for uri in uris_relacionadas:
        propiedades.append((propiedad, uri, None))  # None = es URI, no literal
```

**🎯 Ejemplo práctico:**
```python
# CSV: "Authors" = "Smith, J. (12345); García, M. (67890)"
# mapeo = {"property": "dc:creator", "type": "Person"}

# RESULTADO:
# <pub_123> dc:creator <Person_Smith_J_12345> .
# <pub_123> dc:creator <Person_García_M_67890> .

# Y además se crean las entidades:
# <Person_Smith_J_12345> rdf:type foaf:Person .
# <Person_Smith_J_12345> foaf:name "Smith, J." .
# <Person_Smith_J_12345> scopus:authorId "12345" .
```

#### **📄 `_procesar_literal_simple(self, propiedades, propiedad, valor, columna)` - LITERALES**
```python
def _procesar_literal_simple(self, propiedades, propiedad, valor, columna):
    datatype = self.obtener_datatype(columna, valor)  # Ej: xsd:string, xsd:integer
    propiedades.append((propiedad, valor, datatype))
```

**🎯 Ejemplo práctico:**
```python
# CSV: "Title" = "Inteligencia Artificial en Medicina" 
# mapeo = "dc:title"

# RESULTADO:
# <pub_123> dc:title "Inteligencia Artificial en Medicina"^^xsd:string .
```

#### **📊 `procesar_multivalor(self, texto, tipo_entidad, columna_origen)` - CAMPOS MULTIVALUADOS**
```python
def procesar_multivalor(self, texto, tipo_entidad, columna_origen):
    # PASO 1: Separar por ';' (formato estándar Scopus)
    elementos = [e.strip() for e in str(texto).split(';') 
                if e.strip() and e.strip() not in self._valores_nulos]
    
    # PASO 2: Procesar cada elemento individualmente
    uris = []
    for elemento in elementos:
        uri = self._procesar_elemento_individual(elemento, tipo_entidad, columna_origen)
        if uri:
            uris.append(uri)
    return uris
```

**🎯 Propósito:** Convierte campos multivaluados en múltiples entidades RDF.

**📊 Ejemplos de Campos Multivaluados:**

#### **👥 AUTORES:**
```python
# CSV: "Authors" = "Smith, J.; García, M.; Wilson, K."
# tipo_entidad = "Person"

# PASO 1: Separar
elementos = ["Smith, J.", "García, M.", "Wilson, K."]

# PASO 2: Crear URIs individuales
uris = [
    "<Person_Smith_J>",
    "<Person_García_M>", 
    "<Person_Wilson_K>"
]

# RESULTADO EN RDF:
# <pub_123> dc:creator <Person_Smith_J> .
# <pub_123> dc:creator <Person_García_M> .
# <pub_123> dc:creator <Person_Wilson_K> .
```

#### **🏷️ PALABRAS CLAVE:**
```python
# CSV: "Author Keywords" = "machine learning; artificial intelligence; neural networks"
# tipo_entidad = "Concept"

# RESULTADO EN RDF:
# <pub_123> dc:subject <Concept_machine_learning> .
# <pub_123> dc:subject <Concept_artificial_intelligence> .
# <pub_123> dc:subject <Concept_neural_networks> .
```

#### **🏢 ORGANIZACIONES:**
```python
# CSV: "Affiliations" = "MIT; Stanford University; Harvard Medical School"
# tipo_entidad = "Organization"

# RESULTADO EN RDF:
# <pub_123> foaf:workplaceHomepage <Organization_MIT> .
# <pub_123> foaf:workplaceHomepage <Organization_Stanford_University> .
# <pub_123> foaf:workplaceHomepage <Organization_Harvard_Medical_School> .
```

#### **🔧 `_procesar_elemento_individual(self, elemento, tipo_entidad, columna)` - ELEMENTOS INDIVIDUALES**
```python
def _procesar_elemento_individual(self, elemento, tipo_entidad, columna):
    # MANEJO ESPECIAL: Formato "Nombre (ID)" común en Scopus
    if '(' in elemento and ')' in elemento:
        partes = elemento.split('(')
        nombre = partes[0].strip()              # "Smith, J."
        id_elemento = partes[-1].replace(')', '').strip()  # "12345"
        
        # Crear URI usando ID si está disponible
        uri = self.crear_uri(tipo_entidad, id_elemento if id_elemento else nombre)
        
        # Propiedades según el tipo de entidad
        if tipo_entidad == 'Person':
            propiedades = [
                ('foaf:name', nombre),           # Nombre legible
                ('scopus:authorId', id_elemento) # ID único de Scopus
            ]
        elif tipo_entidad == 'Organization':
            propiedades = [('foaf:name', nombre)]
        elif tipo_entidad == 'Concept':
            propiedades = [('skos:prefLabel', nombre)]
    else:
        # Formato simple sin ID
        uri = self.crear_uri(tipo_entidad, elemento)
        propiedades = self._obtener_propiedades_tipo(tipo_entidad, elemento)
    
    # IMPORTANTE: Registrar la entidad en el sistema
    if uri:
        tipo_rdf = self.tipo_entidad_a_rdf.get(tipo_entidad, 'schema:Thing')
        self.agregar_entidad(uri, tipo_rdf, propiedades)
    
    return uri
```

**🎯 Ejemplos de Procesamiento Individual:**

#### **👤 AUTOR CON ID:**
```python
# Entrada: "Smith, John (12345678)"
# tipo_entidad = "Person"

# RESULTADO:
uri = "<Person_12345678>"
propiedades = [
    ('foaf:name', 'Smith, John'),
    ('scopus:authorId', '12345678')
]

# EN RDF:
# <Person_12345678> rdf:type foaf:Person .
# <Person_12345678> foaf:name "Smith, John"^^xsd:string .
# <Person_12345678> scopus:authorId "12345678"^^xsd:string .
```

#### **🏷️ CONCEPTO SIN ID:**
```python
# Entrada: "machine learning"  
# tipo_entidad = "Concept"

# RESULTADO:
uri = "<Concept_machine_learning>"
propiedades = [('skos:prefLabel', 'machine learning')]

# EN RDF:
# <Concept_machine_learning> rdf:type skos:Concept .
# <Concept_machine_learning> skos:prefLabel "machine learning"^^xsd:string .
```

#### **💾 `generar_ttl(self)` - GENERACIÓN DEL ARCHIVO FINAL**
```python
def generar_ttl(self):
    buffer = StringIO()
    
    # PASO 1: Escribir prefijos de vocabularios
    self._escribir_prefijos(buffer)
    
    # PASO 2: Escribir todas las entidades y sus propiedades
    for uri, (tipo_rdf, propiedades) in self.entities.items():
        # Declarar tipo de entidad
        buffer.write(f"{uri} rdf:type {tipo_rdf} .\n")
        
        # Escribir cada propiedad
        for prop in propiedades:
            if len(prop) == 3:
                propiedad, valor, datatype = prop
                
                # DECISIÓN: ¿Es URI (objeto) o literal?
                if datatype is None:
                    # ES UN OBJETO: Referencia a otra entidad
                    buffer.write(f"{uri} {propiedad} {valor} .\n")
                else:
                    # ES UN LITERAL: Valor con tipo de dato
                    valor_limpio = self.limpiar_cadena(valor)
                    buffer.write(f'{uri} {propiedad} "{valor_limpio}"^^{datatype} .\n')
    
    return buffer.getvalue()
```

**🎯 Propósito:** Convierte todas las entidades en memoria al formato TTL final.

**📝 Ejemplo de Generación TTL Completa:**

#### **🔤 PASO 1: Prefijos**
```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
```

#### **📚 PASO 2: Entidades y Propiedades**

**🔗 OBJETOS (Referencias a entidades):**
```turtle
# PUBLICACIÓN que referencia OBJETOS
<pub_10.1234_example> rdf:type bibo:AcademicArticle .
<pub_10.1234_example> dc:creator <Person_Smith_J_12345> .      # ← OBJETO (URI)
<pub_10.1234_example> dc:subject <Concept_machine_learning> .  # ← OBJETO (URI)
<pub_10.1234_example> foaf:workplaceHomepage <Organization_MIT> . # ← OBJETO (URI)
```

**📄 LITERALES (Valores directos):**
```turtle
# PUBLICACIÓN con propiedades LITERALES
<pub_10.1234_example> dc:title "AI in Healthcare"^^xsd:string .        # ← LITERAL texto
<pub_10.1234_example> dcterms:date "2024"^^xsd:gYear .                # ← LITERAL año
<pub_10.1234_example> schema:citedByCount "15"^^xsd:integer .         # ← LITERAL número
<pub_10.1234_example> schema:isAccessibleForFree "true"^^xsd:boolean . # ← LITERAL booleano
```

**👤 ENTIDAD PERSONA (creada por campo multivaluado):**
```turtle
# Las ENTIDADES referenciadas también se escriben
<Person_Smith_J_12345> rdf:type foaf:Person .
<Person_Smith_J_12345> foaf:name "Smith, J."^^xsd:string .       # ← LITERAL
<Person_Smith_J_12345> scopus:authorId "12345"^^xsd:string .     # ← LITERAL
```

**🏷️ ENTIDAD CONCEPTO (creada por keywords multivaluadas):**
```turtle
<Concept_machine_learning> rdf:type skos:Concept .
<Concept_machine_learning> skos:prefLabel "machine learning"^^xsd:string . # ← LITERAL
```

#### **🔍 `_escribir_instancias(self, buffer)` - LÓGICA DE ESCRITURA**
```python
def _escribir_instancias(self, buffer):
    for uri, (tipo_rdf, propiedades) in self.entities.items():
        if not uri or "<None>" in uri:
            continue  # Saltar URIs inválidas
        
        # Escribir tipo de entidad
        buffer.write(f"{uri} rdf:type {tipo_rdf} .\n")
        
        # Escribir cada propiedad
        for prop in propiedades:
            if len(prop) == 3:
                propiedad, valor, datatype = prop
                
                if datatype is None:
                    # OBJETO: Es una referencia a otra entidad
                    buffer.write(f"{uri} {propiedad} {valor} .\n")
                else:
                    # LITERAL: Es un valor con tipo de dato
                    valor_limpio = self.limpiar_cadena(valor)
                    if valor_limpio:
                        buffer.write(f'{uri} {propiedad} "{valor_limpio}"^^{datatype} .\n')
        
        buffer.write("\n")  # Línea en blanco entre entidades
```

**🎯 Diferencias Clave en la Escritura:**

#### **🔗 OBJETOS** (sin comillas, sin datatype):
```turtle
<pub_123> dc:creator <Person_Smith_J> .           # ← Sin comillas
<pub_123> dc:subject <Concept_AI> .               # ← Sin comillas  
```

#### **📄 LITERALES** (con comillas y datatype):
```turtle
<pub_123> dc:title "Título del artículo"^^xsd:string .    # ← Con comillas y ^^xsd:
<pub_123> dcterms:date "2024"^^xsd:gYear .                # ← Con comillas y ^^xsd:
<pub_123> schema:citedByCount "15"^^xsd:integer .         # ← Con comillas y ^^xsd:
```

#### **🖥️ `crear_interfaz_grafica(self)`**
```python
def crear_interfaz_grafica(self):
    # Crear ventana principal
    self.root = tk.Tk()
    self.root.title("Convertidor Scopus CSV → RDF/Turtle")
    self.root.geometry("600x500")
    
    # Variables para archivos
    self.archivo_csv_var = tk.StringVar()
    self.archivo_salida_var = tk.StringVar(value="ontologia_scopus.ttl")
    
    # Crear widgets (botones, labels, etc.)
    self._crear_widgets()
```
**Propósito:** Construye la interfaz gráfica completa usando Tkinter para facilitar el uso.

---

## 🎯 **RESUMEN: OBJETOS vs LITERALES vs MULTIVALUADOS**

### **📋 TABLA COMPARATIVA**

| Tipo | Config.json | CSV Input | RDF Output | Características |
|------|-------------|-----------|------------|----------------|
| **📄 LITERAL** | `"Title": {"property": "dc:title", "datatype": "xsd:string"}` | `"AI in Medicine"` | `<pub> dc:title "AI in Medicine"^^xsd:string .` | Valor directo con tipo |
| **🔗 OBJETO** | `"Authors": {"property": "dc:creator", "type": "Person"}` | `"Smith, J."` | `<pub> dc:creator <Person_Smith_J> .` | Referencia a entidad |
| **📊 MULTIVALUADO** | `"Authors": {"property": "dc:creator", "type": "Person"}` | `"Smith, J.; García, M."` | `<pub> dc:creator <Person_Smith_J> .`<br>`<pub> dc:creator <Person_García_M> .` | Múltiples objetos |

### **🔧 IDENTIFICACIÓN EN CONFIG.JSON**

#### **📄 LITERAL SIMPLE:**
```json
"Title": "dc:title"
```
- **Clave:** Solo string como valor
- **Resultado:** Valor directo al documento

#### **📄 LITERAL CON DATATYPE:**
```json
"Year": {
  "property": "dcterms:date",
  "datatype": "xsd:gYear"
}
```
- **Clave:** Tiene `"datatype"`, no tiene `"type"`
- **Resultado:** Valor directo con tipo específico

#### **🔗 OBJETO (ENTIDAD):**
```json
"Authors": {
  "property": "dc:creator",
  "type": "Person"
}
```
- **Clave:** Tiene `"type"` (Person, Organization, Concept, etc.)
- **Resultado:** Crea entidades separadas y las referencia

#### **📊 MULTIVALUADO (Cualquier tipo con `;`):**
```json
# Si el CSV contiene: "Smith, J.; García, M.; Wilson, K."
# El sistema automáticamente detecta ';' y procesa cada elemento
```

### **🎯 EJEMPLOS COMPLETOS DEL CONFIG.JSON**

#### **📄 MAPEOS LITERALES:**
```json
{
  "_core_fields": "Campos principales del documento",
  "Title": {"property": "dc:title", "datatype": "xsd:string"},
  "Year": {"property": "dcterms:date", "datatype": "xsd:gYear"},
  "Abstract": {"property": "dcterms:abstract", "datatype": "xsd:string"},
  
  "_metrics": "Métricas y citas",
  "Cited by": {"property": "schema:citedByCount", "datatype": "xsd:integer"},
  "Open Access": {"property": "schema:isAccessibleForFree", "datatype": "xsd:boolean"}
}
```

#### **🔗 MAPEOS DE OBJETOS:**
```json
{
  "_core_fields": "Campos principales del documento",
  "Authors": {"property": "dc:creator", "type": "Person"},
  "Author full names": {"property": "foaf:name", "type": "Person"},
  
  "_affiliations": "Afiliaciones y contactos", 
  "Affiliations": {"property": "foaf:workplaceHomepage", "type": "Organization"},
  "Publisher": {"property": "dc:publisher", "type": "Organization"},
  
  "_subjects": "Temas y palabras clave",
  "Author Keywords": {"property": "dc:subject", "type": "Concept"},
  "Index Keywords": {"property": "dcterms:subject", "type": "Concept"},
  
  "_conference": "Información de conferencias",
  "Conference name": {"property": "bibo:presentedAt", "type": "Event"}
}
```

### **🔄 FLUJO COMPLETO DE PROCESAMIENTO**

#### **1. 📥 ENTRADA CSV:**
```csv
Authors,Title,Year,Author Keywords,Cited by
"Smith, J.; García, M.","AI in Medicine",2024,"machine learning; neural networks",15
```

#### **2. ⚙️ PROCESAMIENTO:**
```python
# OBJETOS (Authors): "Smith, J.; García, M."
# → Se divide en: ["Smith, J.", "García, M."]
# → Se crean: <Person_Smith_J>, <Person_García_M>

# LITERAL (Title): "AI in Medicine" 
# → Se convierte directamente: "AI in Medicine"^^xsd:string

# LITERAL (Year): "2024"
# → Se convierte: "2024"^^xsd:gYear

# OBJETOS MULTIVALUADOS (Keywords): "machine learning; neural networks"
# → Se divide en: ["machine learning", "neural networks"] 
# → Se crean: <Concept_machine_learning>, <Concept_neural_networks>

# LITERAL (Cited by): "15"
# → Se convierte: "15"^^xsd:integer
```

#### **3. 📤 SALIDA RDF:**
```turtle
# DOCUMENTO PRINCIPAL con LITERALES y referencias a OBJETOS
<pub_AI_Medicine> rdf:type bibo:AcademicArticle .
<pub_AI_Medicine> dc:title "AI in Medicine"^^xsd:string .           # ← LITERAL
<pub_AI_Medicine> dcterms:date "2024"^^xsd:gYear .                  # ← LITERAL  
<pub_AI_Medicine> schema:citedByCount "15"^^xsd:integer .           # ← LITERAL
<pub_AI_Medicine> dc:creator <Person_Smith_J> .                     # ← OBJETO
<pub_AI_Medicine> dc:creator <Person_García_M> .                    # ← OBJETO
<pub_AI_Medicine> dc:subject <Concept_machine_learning> .           # ← OBJETO
<pub_AI_Medicine> dc:subject <Concept_neural_networks> .            # ← OBJETO

# ENTIDADES OBJETOS creadas automáticamente
<Person_Smith_J> rdf:type foaf:Person .
<Person_Smith_J> foaf:name "Smith, J."^^xsd:string .

<Person_García_M> rdf:type foaf:Person .
<Person_García_M> foaf:name "García, M."^^xsd:string .

<Concept_machine_learning> rdf:type skos:Concept .
<Concept_machine_learning> skos:prefLabel "machine learning"^^xsd:string .

<Concept_neural_networks> rdf:type skos:Concept .
<Concept_neural_networks> skos:prefLabel "neural networks"^^xsd:string .
```

---

## 📊 **TIPOS DE ENTIDADES GENERADAS**

### **🧑 Personas (`foaf:Person`)**
```turtle
<https://onto.utpl.edu.ec/scopus/resource/Person_Smith_J> rdf:type foaf:Person .
<https://onto.utpl.edu.ec/scopus/resource/Person_Smith_J> foaf:name "Smith, J."^^xsd:string .
<https://onto.utpl.edu.ec/scopus/resource/Person_Smith_J> scopus:authorId "12345678"^^xsd:string .
```

### **🏢 Organizaciones (`foaf:Organization`)**
```turtle
<https://onto.utpl.edu.ec/scopus/resource/Organization_MIT> rdf:type foaf:Organization .
<https://onto.utpl.edu.ec/scopus/resource/Organization_MIT> foaf:name "MIT"^^xsd:string .
```

### **🏷️ Conceptos (`skos:Concept`)**
```turtle
<https://onto.utpl.edu.ec/scopus/resource/Concept_Machine_Learning> rdf:type skos:Concept .
<https://onto.utpl.edu.ec/scopus/resource/Concept_Machine_Learning> skos:prefLabel "Machine Learning"^^xsd:string .
```

### **📚 Publicaciones (`bibo:AcademicArticle`)**
```turtle
<https://onto.utpl.edu.ec/scopus/resource/pub_10.1234_example> rdf:type bibo:AcademicArticle .
<https://onto.utpl.edu.ec/scopus/resource/pub_10.1234_example> dc:title "AI in Healthcare"^^xsd:string .
<https://onto.utpl.edu.ec/scopus/resource/pub_10.1234_example> dc:creator <Person_Smith_J> .
<https://onto.utpl.edu.ec/scopus/resource/pub_10.1234_example> dc:subject <Concept_Machine_Learning> .
```

---

## 🔍 **RESOLUCIÓN DE PROBLEMAS**

### **❌ Error: "No se encuentra el archivo CSV"**
- **Causa:** Ruta incorrecta o archivo no existe
- **Solución:** Verificar que el archivo existe y la ruta es correcta

### **❌ Error: "Columnas requeridas faltantes"**
- **Causa:** El CSV no tiene las columnas mínimas requeridas
- **Solución:** Ajustar `required_fields` en `config.json` o usar CSV completo de Scopus

### **❌ Error: "Memoria insuficiente"**
- **Causa:** Archivo CSV muy grande
- **Solución:** Procesar por lotes o aumentar memoria disponible

### **❌ Error: "Caracteres especiales en URIs"**
- **Causa:** Datos con caracteres no válidos para URIs
- **Solución:** El programa limpia automáticamente, pero verificar `base_uri` en config

---

## 📈 **INTERPRETACIÓN DE RESULTADOS**

### **Estadísticas Típicas:**
```
Completado: 29,322 entidades generadas
Tripletas: 173,544

Entidades por tipo:
   skos:Concept: 14,583        # Keywords y temas
   foaf:Person: 8,676          # Autores y colaboradores  
   foaf:Organization: 3,367    # Universidades e instituciones
   bibo:Proceedings: 1,409     # Artículos de conferencia
   bibo:AcademicArticle: 385   # Artículos de revista
```

### **Archivo TTL Generado:**
- **Tamaño típico:** 20-40 MB para 1,000+ publicaciones
- **Formato:** Turtle (.ttl) - estándar RDF
- **Uso:** Consultable con SPARQL, importable en herramientas semánticas

---

## 🎯 **CASOS DE USO TÍPICOS**

### **1. 🔬 Investigación Académica**
- Analizar redes de colaboración entre autores
- Identificar tendencias temáticas en publicaciones
- Mapear relaciones institucionales

### **2. 📊 Bibliometría**
- Generar métricas de impacto por autor/institución
- Analizar evolución temporal de conceptos
- Crear visualizaciones de redes de conocimiento

### **3. 🌐 Web Semántica**
- Integrar datos bibliográficos en portales web
- Crear endpoints SPARQL para consultas
- Interoperar con otras ontologías académicas

---

## 🚀 **PRÓXIMOS PASOS**

Una vez generada la ontología RDF:

1. **📊 Análisis:** Usar herramientas como Gephi o Cytoscape
2. **🔍 Consultas:** Implementar queries SPARQL personalizadas  
3. **🌐 Publicación:** Servir datos via endpoint SPARQL
4. **🔗 Integración:** Conectar con otras ontologías existentes

---

**¿Necesitas ayuda adicional?** Consulta el archivo `REPORTE_EJECUCION.md` para detalles técnicos completos.