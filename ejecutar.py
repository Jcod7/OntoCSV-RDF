#!/usr/bin/env python3
"""
Launcher script for Scopus CSV to RDF Converter
Runs the GUI version with optimized configuration
"""

import sys
import os
from pathlib import Path

def main():
    print("=== CONVERTIDOR SCOPUS CSV -> RDF ===")
    print("Version optimizada con configuracion simplificada")
    print("Iniciando interfaz grafica...")
    print()
    
    try:
        # Import and run the converter with default config.json
        from scopus_converter import ConversorRDFScopus
        
        # Start the GUI (uses config.json by default)
        converter = ConversorRDFScopus()
        converter.iniciar_interfaz_grafica()
        
    except ImportError as e:
        print(f"Error: No se pudo importar el convertidor: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()