# 🔄 OntoCSV-RDF - Convertidor Scopus CSV → RDF

## 📖 **Descripción**
Herramienta completa para transformar datos bibliográficos de Scopus (formato CSV) en ontologías RDF estructuradas y consultables. Incluye interfaz gráfica amigable y configuración personalizable.

## ⚡ **Inicio Rápido**
```bash
# Ejecutar interfaz gráfica
python ejecutar.py

# O ejecutar directamente
python scopus_converter.py
```

## 📁 **Archivos Principales**
- `scopus_converter.py` - Convertidor principal con GUI
- `ejecutar.py` - Launcher recomendado
- `config.json` - Configuración optimizada (46 mapeos CSV→RDF)
- `GUIA_DE_USO.md` - **Guía completa para usuarios finales**

## 🎯 **Características**
- ✅ **Interfaz gráfica completa** con Tkinter
- ✅ **46 mapeos automáticos** de columnas CSV a propiedades RDF
- ✅ **Configuración simplificada** para usuarios externos
- ✅ **Validación automática** de datos de entrada
- ✅ **Estadísticas detalladas** de conversión
- ✅ **Vocabularios estándar** (Dublin Core, FOAF, BIBO, SKOS, Schema.org)

## 📊 **Resultados Típicos**
- **~29,000 entidades RDF** generadas
- **~173,000 tripletas** en formato Turtle
- **6 tipos principales:** Personas, Conceptos, Organizaciones, Publicaciones, Revistas, Eventos

## 🔧 **Requisitos**
- Python 3.7+
- Bibliotecas: `tkinter`, `csv`, `json`, `pathlib`
- Archivo CSV exportado desde Scopus

## 📚 **Documentación Completa**
👉 **Ver `GUIA_DE_USO.md`** para:
- Tutorial paso a paso con capturas
- Explicación de funciones principales del código
- Configuración avanzada
- Resolución de problemas
- Casos de uso típicos

## 🌟 **Desarrollado por**
Universidad Técnica Particular de Loja (UTPL)  
Proyecto de Representación Avanzada de Conocimiento y Razón
