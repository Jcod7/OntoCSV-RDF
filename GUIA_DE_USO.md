# 📖 GUÍA DE USO - CONVERTIDOR SCOPUS CSV → RDF

## 🎯 **¿Qué hace este programa?**

El **Convertidor Scopus CSV → RDF** transforma automáticamente datos bibliográficos exportados desde Scopus (formato CSV) en una ontología RDF estructurada y consultable. Incluye una interfaz web moderna con configuración avanzada de delimitadores.

### 🌟 **Características principales:**
- ✅ **Interfaz web moderna** con configuración visual
- ✅ **URL base personalizable** para ontologías organizacionales
- ✅ **Configuración inteligente de delimitadores** por columna
- ✅ **Detección automática** de formatos CSV
- ✅ **Vista previa de datos** antes de conversión
- ✅ **45+ mapeos automáticos** CSV → propiedades RDF
- ✅ **Vocabularios semánticos estándar** (Dublin Core, FOAF, BIBO, SKOS, Schema.org)

---

## 🚀 **INICIO RÁPIDO**

### **Paso 1: Instalar Dependencias**
```bash
pip install flask pandas werkzeug
```

### **Paso 2: Ejecutar la Aplicación Web**
```bash
python web_interface.py
```

Abrir en el navegador: **http://localhost:5000**

### **Paso 3: Proceso de Conversión**
1. **📤 Subir archivo CSV** exportado de Scopus
2. **🌐 Configurar URL base** de tu ontología (opcional)
3. **⚙️ Configurar delimitadores** CSV y multivalor
4. **🔍 Revisar análisis** con configuración aplicada
5. **🚀 Convertir y descargar** archivo TTL generado

---

## 🌐 **INTERFAZ WEB - Guía Detallada**

### **🎨 Flujo Visual Completo:**

#### **1. 📤 Página de Inicio**
```
┌─────────────────────────────────────────────────┐
│         Scopus CSV to RDF Converter             │
├─────────────────────────────────────────────────┤
│                                                 │
│  📁 Convertidor de Datos Bibliográficos        │
│                                                 │
│  Transforma archivos CSV de Scopus en          │
│  ontologías RDF/Turtle estructuradas           │
│                                                 │
│  [📂 Seleccionar archivo CSV...]               │
│                                                 │
│  Formatos soportados: .csv, .txt               │
│  Tamaño máximo: 50MB                           │
└─────────────────────────────────────────────────┘
```

#### **2. ⚙️ Página de Configuración**
```
┌─────────────────────────────────────────────────┐
│          Configurar Delimitadores               │
├─────────────────────────────────────────────────┤
│                                                 │
│ 🌐 URL Base de la Ontología:                   │
│ [https://mi-universidad.edu/ontologia/____] 🔄  │
│                                                 │
│ 📋 Delimitador CSV detectado: , (coma) ✅       │
│ ○ , (coma)     ○ ; (punto y coma)              │
│ ○ ⭾ (tab)      ○ | (pipe)                      │
│                                                 │
│ 📊 Configuración por columna:                  │
│ Authors      [; (punto y coma) ▼] ✅           │
│ Keywords     [; (punto y coma) ▼] ✅           │
│ Title        [-- Sin separar -- ▼] ➖          │
│ Year         [-- Sin separar -- ▼] ➖          │
│                                                 │
│ 👁️ Vista previa (2 primeras filas):            │
│ ┌─────────────────────────────────────────────┐ │
│ │Authors    │Title         │Year    │Keywords │ │
│ │Smith,J.;  │AI Research   │2024    │ML;AI;NN │ │
│ │García,M.  │              │        │         │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│        [🔍 Analizar con esta Configuración]    │
└─────────────────────────────────────────────────┘
```

#### **3. 📊 Página de Análisis**
```
┌─────────────────────────────────────────────────┐
│            Archivo Analizado ✅                 │
├─────────────────────────────────────────────────┤
│                                                 │
│ 📄 scopus_data.csv                             │
│ 📊 1,250 registros │ 📋 25 columnas            │
│ 🔧 Delimitador: , (coma)                       │
│                                                 │
│ 🌐 URL Base Configurada:                       │
│ https://mi-universidad.edu/ontologia/           │
│                                                 │
│ ⚙️ Configuración de delimitadores aplicada:    │
│ Authors      [; (punto y coma) ✅] Manual       │
│ Keywords     [; (punto y coma) ✅] Manual       │
│ Title        [Sin separar      ➖] Literal      │
│                                                 │
│ 🎛️ Opciones adicionales:                       │
│ Limitar registros: [_____] (opcional)          │
│                                                 │
│    [🚀 Convertir a RDF]                       │
│                                                 │
│  [🔧 Cambiar Config] [🏠 Inicio]               │
└─────────────────────────────────────────────────┘
```

#### **4. ✅ Página de Resultados**
```
┌─────────────────────────────────────────────────┐
│         🎉 Conversión Completada               │
├─────────────────────────────────────────────────┤
│                                                 │
│ ✅ Archivo procesado exitosamente               │
│                                                 │
│ 📊 Estadísticas de conversión:                 │
│ • Entidades generadas: 4,572                   │
│ • Tripletas RDF: 23,847                        │
│ • Tamaño archivo: 8.2 MB                       │
│ • Tiempo procesamiento: 2m 34s                 │
│                                                 │
│ 📈 Tipos de entidades:                         │
│ • 👥 Personas: 1,256                           │
│ • 🏷️ Conceptos: 2,104                          │
│ • 🏢 Organizaciones: 567                       │
│ • 📚 Publicaciones: 645                        │
│                                                 │
│ 👁️ Vista previa TTL (primeras líneas):         │
│ ┌─────────────────────────────────────────────┐ │
│ │@prefix rdf: <http://www.w3.org/1999/02/... │ │
│ │<https://mi-universidad.edu/ontologia/...   │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│     [📥 Descargar TTL] [🔄 Convertir Nuevo]    │
└─────────────────────────────────────────────────┘
```

### **🎛️ Características Avanzadas:**

#### **🌐 URL Base Personalizable**
- **Función:** Define el prefijo de todas las entidades RDF
- **Por defecto:** `https://onto.utpl.edu.ec/scopus/resource/`
- **Personalizable:** Cambiar por tu dominio organizacional
- **Ejemplo:** `https://mi-universidad.edu/ontologia/`
- **Validación:** Automática con formato URL correcto

#### **🔧 Configuración Inteligente de Delimitadores**
- **Detección automática:** Identifica el mejor delimitador CSV
- **Configuración por columna:** Cada campo puede tener su propio delimitador
- **Sugerencias inteligentes:** 
  - `Authors, Keywords, Affiliations` → `;` (punto y coma)
  - `Title, DOI, Year, Abstract` → Sin delimitador (literal)
- **Vista previa:** Muestra cómo se procesarán los datos

#### **📊 Análisis Pre-conversión**
- **Campos de solo lectura:** Configuración bloqueada en página de análisis
- **Estadísticas del archivo:** Filas, columnas, tamaño
- **Configuración confirmada:** Resumen visual de toda la configuración
- **Opción de modificar:** Botón para volver a configurar si es necesario

---

## ⚙️ **CONFIGURACIÓN AVANZADA**

### **🔧 Archivo `config.json`**

El convertidor utiliza un archivo de configuración JSON que define cómo se mapean las columnas CSV a propiedades RDF. Este archivo se puede personalizar para diferentes tipos de datos bibliográficos.

#### **📋 Estructura Principal:**

```json
{
  "ontology": {
    "base_uri": "https://onto.utpl.edu.ec/scopus/resource/"
  },
  "prefixes": {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "bibo": "http://purl.org/ontology/bibo/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "schema": "http://schema.org/"
  },
  "entity_type_mappings": {
    "Person": "foaf:Person",
    "Concept": "skos:Concept", 
    "Organization": "foaf:Organization",
    "Journal": "bibo:Journal"
  },
  "mappings": {
    "Authors": {"property": "dc:creator", "type": "Person"},
    "Title": {"property": "dc:title", "datatype": "xsd:string"},
    "Author Keywords": {"property": "dc:subject", "type": "Concept"},
    "Year": {"property": "dcterms:date", "datatype": "xsd:gYear"}
  }
}
```

#### **🌐 Configuración Web vs Archivo**

| Elemento | Configurable en Web | Archivo config.json |
|----------|---------------------|-------------------|
| **URL Base** | ✅ Campo editable | ✅ `ontology.base_uri` |
| **Delimitadores CSV** | ✅ Detección automática | ❌ No aplica |
| **Delimitadores Multivalor** | ✅ Por columna | ❌ No aplica |
| **Mapeos RDF** | ❌ Solo lectura | ✅ Completamente editable |
| **Vocabularios** | ❌ Solo lectura | ✅ `prefixes` |
| **Validación** | ❌ Solo lectura | ✅ `validation` |

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

## 💻 **USO PROGRAMÁTICO Y LÍNEA DE COMANDOS**

### **🌐 Interfaz Web (Recomendado)**
```bash
# Ejecutar servidor web
python web_interface.py

# Acceder en navegador
# http://localhost:5000
```

### **🔧 Uso Programático Básico:**
```python
from web_interface import EnhancedConversorRDFScopus

# Crear instancia del convertidor
converter = EnhancedConversorRDFScopus()

# Configurar URL base personalizada
converter.set_base_uri("https://mi-universidad.edu/ontologia/")

# Configurar delimitadores multivalor por columna
delimitadores = {
    "Authors": ";",
    "Keywords": ";", 
    "Title": "",  # Sin delimitador (literal)
    "Year": ""    # Sin delimitador (literal)
}
converter.set_multi_value_delimiters(delimitadores)

# Procesar archivo
converter.procesar_csv("datos_scopus.csv")

# Generar RDF
rdf_content = converter.generar_ttl()

# Guardar archivo
with open("ontologia.ttl", "w", encoding="utf-8") as f:
    f.write(rdf_content)
```

### **🎯 Uso con GUI Tradicional (Alternativo)**
```bash
# Solo si no se puede usar la interfaz web
python scopus_converter.py
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

### **🏗️ Arquitectura de Clases**

El proyecto incluye dos clases principales:

#### **📋 `ConversorRDFScopus` (Clase Base)**
- **Ubicación:** `scopus_converter.py`
- **Propósito:** Funcionalidad core de conversión CSV → RDF
- **Interfaz:** GUI tradicional con Tkinter (opcional)

#### **🌐 `EnhancedConversorRDFScopus` (Clase Extendida)**
- **Ubicación:** `web_interface.py`  
- **Propósito:** Extiende la clase base con funcionalidades web
- **Características adicionales:**
  - URL base personalizable por conversión
  - Delimitadores multivalor configurables por columna
  - Integración con interfaz web Flask

```python
# Jerarquía de herencia
class ConversorRDFScopus:           # Clase base
    # Funcionalidad core...

class EnhancedConversorRDFScopus(ConversorRDFScopus):  # Clase extendida
    def set_base_uri(self, base_uri)
    def set_multi_value_delimiters(self, delimiters_dict)
    # Hereda toda la funcionalidad base...
```

---

### **Clase `ConversorRDFScopus` (Base)**

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

## 🎯 **CASOS DE USO Y EJEMPLOS PRÁCTICOS**

### **1. 🏛️ Universidad con Repositorio Institucional**

**Escenario:** Una universidad quiere convertir sus publicaciones Scopus para integrarlas en su repositorio institucional.

**Proceso con Interfaz Web:**
1. **🌐 URL Base:** `https://biblioteca.universidad.edu/ontologia/`
2. **📊 Configuración:** Delimitadores automáticos para autores y palabras clave
3. **🎯 Resultado:** Ontología con URIs institucionales únicas

**Beneficios:**
- URIs consistentes con el dominio institucional
- Fácil integración con sistemas existentes
- Procesamiento masivo de datos bibliográficos

### **2. 🔬 Grupo de Investigación Multidisciplinario**

**Escenario:** Investigadores quieren analizar tendencias y colaboraciones en su área.

**Proceso:**
1. **📤 Datos:** Exportar CSV desde Scopus con sus publicaciones
2. **⚙️ Configuración:** Definir delimitadores específicos por revista/conferencia
3. **📈 Análisis:** Usar SPARQL para consultar redes de colaboración

**Consulta de ejemplo:**
```sparql
SELECT ?autor1 ?autor2 (COUNT(?pub) as ?colaboraciones)
WHERE {
  ?pub dc:creator ?autor1 .
  ?pub dc:creator ?autor2 .
  FILTER(?autor1 != ?autor2)
}
GROUP BY ?autor1 ?autor2
ORDER BY DESC(?colaboraciones)
```

### **3. 🌐 Portal de Conocimiento Abierto**

**Escenario:** Organización que mantiene un portal público de conocimiento científico.

**Implementación:**
- **🔄 Procesamiento periódico:** Interfaz web para convertir nuevas exportaciones
- **🎛️ Configuraciones múltiples:** Diferentes URL base por área temática
- **📊 Integración:** Conexión con endpoints SPARQL públicos

### **4. 📚 Biblioteca Digital con Metadatos Enriquecidos**

**Ventajas del enfoque web:**
1. **👥 Acceso múltiple:** Bibliotecarías pueden procesar archivos sin conocimientos técnicos
2. **🔧 Configuración visual:** Ajustar delimitadores según fuentes diversas
3. **📋 Validación:** Vista previa antes de conversión definitiva
4. **🌐 Consistencia:** URL base unificada para toda la institución

---

## 🚀 **PRÓXIMOS PASOS Y HERRAMIENTAS**

Una vez generada la ontología RDF con la interfaz web:

### **📊 Análisis y Visualización**
1. **Gephi:** Importar TTL para visualizar redes de colaboración
2. **Cytoscape:** Análisis de redes complejas de citaciones
3. **Apache Jena:** Procesamiento programático de RDF
4. **Protégé:** Edición y validación de ontologías

### **🔍 Consultas SPARQL**
```sparql
# Ejemplo: Top 10 autores más productivos
SELECT ?autor (COUNT(?pub) as ?publicaciones)
WHERE {
  ?pub dc:creator ?autor .
}
GROUP BY ?autor
ORDER BY DESC(?publicaciones)
LIMIT 10
```

### **🌐 Publicación y Integración**
1. **Fuseki/Virtuoso:** Montar endpoint SPARQL público
2. **GitHub Pages:** Publicar ontologías con documentación
3. **LOD Cloud:** Conectar con Linked Open Data
4. **APIs REST:** Exponer datos vía servicios web

### **🔧 Automatización**
```python
# Script para procesamiento batch
import os
from web_interface import EnhancedConversorRDFScopus

def procesar_directorio(directorio_csv, base_uri):
    converter = EnhancedConversorRDFScopus()
    converter.set_base_uri(base_uri)
    
    for archivo in os.listdir(directorio_csv):
        if archivo.endswith('.csv'):
            print(f"Procesando {archivo}...")
            converter.procesar_csv(os.path.join(directorio_csv, archivo))
            
    # Generar ontología combinada
    with open("ontologia_completa.ttl", "w") as f:
        f.write(converter.generar_ttl())
```

### **📚 Recursos Adicionales**
- **RDF Primer:** https://www.w3.org/TR/rdf-primer/
- **SPARQL Tutorial:** https://www.w3.org/TR/sparql11-query/
- **Linked Data:** https://linkeddata.org/
- **Vocabularios:** https://lov.linkeddata.es/

---

## 🔧 **SOPORTE Y DESARROLLO**

### **📁 Estructura del Proyecto**
```
scopus-csv-rdf/
├── web_interface.py          # 🌐 Interfaz web principal
├── scopus_converter.py       # 🔧 Convertidor base  
├── config.json              # ⚙️ Configuración RDF
├── templates/               # 🎨 Plantillas HTML
│   ├── index.html
│   ├── configure_delimiter.html
│   ├── convert.html
│   └── result.html
├── requirements.txt         # 📦 Dependencias
├── uploads/                # 📤 Archivos CSV subidos
├── outputs/                # 📥 Archivos TTL generados
└── README.md               # 📖 Documentación
```

### **🛠️ Requisitos del Sistema**
- **Python:** 3.7+
- **Dependencias:** Flask, pandas, werkzeug
- **Navegador:** Chrome, Firefox, Safari, Edge (moderno)
- **Memoria:** 4GB+ (para archivos CSV grandes)
- **Disco:** 100MB+ espacio libre

### **🐛 Resolución de Problemas**
| Problema | Solución |
|----------|----------|
| **Error al subir archivo** | Verificar tamaño < 50MB y formato CSV |
| **Delimitadores incorrectos** | Usar vista previa para validar configuración |
| **URIs malformadas** | Verificar URL base termina en `/` |
| **Memoria insuficiente** | Procesar por lotes o usar menos registros |
| **Puerto ocupado** | Cambiar puerto en `web_interface.py` línea 377 |

**¿Necesitas ayuda técnica?** La interfaz web incluye validación automática y mensajes de error descriptivos para facilitar el uso.