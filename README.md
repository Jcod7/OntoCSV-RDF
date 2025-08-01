# 🌐 Convertidor Scopus CSV → RDF (Interfaz Web)

## 📖 **Descripción**
Herramienta web moderna para transformar datos bibliográficos de Scopus (formato CSV) en ontologías RDF estructuradas y consultables. Incluye interfaz web con configuración avanzada de delimitadores y URL base personalizable.

## ⚡ **Inicio Rápido**

### 🚀 **Instalación y Ejecución**
```bash
# 1. Instalar dependencias
pip install flask pandas werkzeug

# 2. Ejecutar interfaz web
python web_interface.py

# 3. Abrir en navegador
# http://localhost:5000
```

### 📋 **Proceso de Conversión**
1. **📤 Subir archivo CSV** exportado desde Scopus
2. **🌐 Configurar URL base** de tu ontología
3. **⚙️ Configurar delimitadores** CSV y multivalor por columna
4. **🔍 Revisar análisis** con vista previa de datos
5. **🚀 Convertir y descargar** archivo TTL generado

## 📁 **Estructura del Proyecto**
```
scopus-csv-rdf/
├── web_interface.py          # 🌐 Servidor web Flask principal
├── scopus_converter.py       # 🔧 Motor de conversión RDF
├── config.json              # ⚙️ Mapeos CSV→RDF (45+ campos)
├── templates/               # 🎨 Interfaz web HTML
│   ├── index.html           # Página principal
│   ├── configure_delimiter.html  # Configuración
│   ├── convert.html         # Análisis pre-conversión
│   └── result.html          # Resultados y descarga
├── requirements.txt         # 📦 Dependencias Python
├── uploads/                 # 📤 Archivos CSV subidos
├── outputs/                 # 📥 Archivos TTL generados
└── GUIA_DE_USO.md          # 📖 Documentación completa
```

## 🌟 **Características Principales**

### 🌐 **Interfaz Web Avanzada**
- ✅ **URL base personalizable** para entidades RDF institucionales
- ✅ **Configuración inteligente de delimitadores** por columna
- ✅ **Detección automática** de formatos CSV (`,`, `;`, `|`, `\t`)
- ✅ **Vista previa de datos** antes de conversión
- ✅ **Configuración de solo lectura** en análisis final
- ✅ **Validación automática** de URLs y formatos
- ✅ **Interfaz responsive** compatible con cualquier navegador

### 🔧 **Motor de Conversión RDF**
- ✅ **45+ mapeos automáticos** Scopus CSV → propiedades RDF
- ✅ **Vocabularios semánticos estándar** (Dublin Core, FOAF, BIBO, SKOS, Schema.org)
- ✅ **Configuración basada en JSON** (sin código hardcodeado)
- ✅ **Procesamiento de campos multivalor** por columna
- ✅ **Generación de URIs únicas** con validación
- ✅ **Estadísticas detalladas** de conversión

## 📊 **Resultados Típicos**
- **~29,000 entidades RDF** generadas
- **~173,000 tripletas** en formato Turtle
- **6 tipos principales:** Personas, Conceptos, Organizaciones, Publicaciones, Revistas, Eventos

## 🎨 **Ejemplo de Interfaz Web**

### 1. **🌐 Configuración de URL Base**
```
URL Base: https://mi-universidad.edu/ontologia/
Resultado: <https://mi-universidad.edu/ontologia/Person_Smith_J>
```

### 2. **⚙️ Configuración Inteligente por Columna**
| Columna | Delimitador | Resultado |
|---------|-------------|-----------|
| `Authors` | `;` (punto y coma) | `Smith, J.; García, M.` → 2 entidades |
| `Keywords` | `;` (punto y coma) | `AI; ML; NLP` → 3 conceptos |
| `Title` | Sin delimitador | `"AI in Healthcare"` → Literal |

### 3. **📊 Estadísticas de Conversión**
```
✅ Entidades generadas: 4,572
📋 Tripletas RDF: 23,847  
📁 Tamaño archivo: 8.2 MB
⏱️ Tiempo: 2m 34s
```

## 🔧 **Requisitos del Sistema**
- **Python:** 3.7+
- **Dependencias:** `pip install flask pandas werkzeug`
- **Navegador:** Chrome, Firefox, Safari, Edge (moderno)
- **Memoria:** 4GB+ recomendado para archivos grandes
- **Datos:** Archivo CSV exportado desde Scopus

## 🚀 **Casos de Uso**

### 🏛️ **Institucional**
- **Repositorios universitarios** con URIs institucionales
- **Bibliotecas digitales** con metadatos enriquecidos
- **Portales de investigación** con datos abiertos

### 🔬 **Investigación**
- **Análisis bibliométrico** y redes de colaboración  
- **Visualización de tendencias** temáticas
- **Integración con herramientas SPARQL**

## 🌐 **Alternativas de Uso**

### **Interfaz Web (Recomendado)**
```bash
python web_interface.py  # http://localhost:5000
```

### **GUI Tradicional (Fallback)**
```bash
python scopus_converter.py  # Solo si no funciona la web
```

### **Programático (Avanzado)**
```python
from web_interface import EnhancedConversorRDFScopus
converter = EnhancedConversorRDFScopus()
converter.set_base_uri("https://mi-dominio.com/onto/")
# ... resto del proceso
```

## 📚 **Documentación**
- **`GUIA_DE_USO.md`** - Documentación completa con ejemplos
- **`config.json`** - Configuración de mapeos RDF
- **Templates HTML** - Interfaz web personalizable

## 🌟 **Créditos**
**Universidad Técnica Particular de Loja (UTPL)**  
Proyecto de Representación Avanzada de Conocimiento y Razón

**Versión:** 2.0 - Interfaz Web Moderna  
**Licencia:** Académica - UTPL