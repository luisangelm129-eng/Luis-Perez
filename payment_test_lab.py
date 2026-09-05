#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PAYMENT TEST LAB
Proyecto educativo para Termux.

IMPORTANTE:
Este programa NO consulta PayPal, bancos, pasarelas ni servicios externos.
Solo trabaja con datos de prueba ficticios y valida su formato.
"""

import re
from pathlib import Path

# Colores ANSI
MORADO = "\033[95m"
CIAN = "\033[96m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
BLANCO = "\033[97m"
RESET = "\033[0m"

CARPETA = Path("resultados")
CARPETA.mkdir(exist_ok=True)


def limpiar():
    print("\033[2J\033[H", end="")


def banner():
    limpiar()
    print(f"""{MORADO}
╔══════════════════════════════════════════════╗
║              PAYMENT TEST LAB                ║
║                 PYTHON / TERMUX              ║
╠══════════════════════════════════════════════╣
║       Herramienta educativa de pruebas       ║
║       SIN conexiones a servicios externos     ║
╚══════════════════════════════════════════════╝
{RESET}""")


def es_formato_valido(cadena):
    """
    Acepta SOLO tarjetas de prueba oficiales de laboratorio:
    4111111111111111 | 12 | 30 | 123
    No realiza ninguna comprobación real.
    """
    patron = r"^(\d{16})\|(\d{2})\|(\d{2,4})\|(\d{3})$"
    return bool(re.fullmatch(patron, cadena.strip()))


def prueba_individual():
    print(f"{CIAN}FORMATO DE PRUEBA:{RESET}")
    print("TEST-4111111111111111|12|30|123")
    print()
    dato = input(f"{AMARILLO}Introduce un dato ficticio: {RESET}").strip()

    # Para evitar procesar credenciales reales, exigimos prefijo TEST-
    if not dato.startswith("TEST-"):
        print(f"{ROJO}Solo se aceptan datos con prefijo TEST-.{RESET}")
        return

    limpio = dato[5:]

    if es_formato_valido(limpio):
        print(f"{VERDE}✓ Formato válido para el laboratorio.{RESET}")
    else:
        print(f"{ROJO}✗ Formato incorrecto.{RESET}")

    print(f"{CIAN}Nota: esto NO verifica saldo, autorización ni una cuenta real.{RESET}")


def generar_datos_prueba():
    """
    Genera ejemplos sintéticos. No son tarjetas utilizables.
    """
    cantidad_texto = input(f"{AMARILLO}¿Cuántos registros de prueba? {RESET}")

    try:
        cantidad = int(cantidad_texto)
    except ValueError:
        print(f"{ROJO}Cantidad no válida.{RESET}")
        return

    if not 1 <= cantidad <= 1000:
        print(f"{ROJO}Usa una cantidad entre 1 y 1000.{RESET}")
        return

    # Marcadores claramente ficticios, no números de pago reales.
    datos = [
        f"TEST-CARD-{i:04d}|12|30|XXX"
        for i in range(1, cantidad + 1)
    ]

    archivo = CARPETA / "datos_prueba.txt"
    archivo.write_text("\n".join(datos) + "\n", encoding="utf-8")

    print(f"{VERDE}✓ {cantidad} registros ficticios creados.{RESET}")
    print(f"{CIAN}✓ Guardados en: {archivo}{RESET}")


def eliminar_duplicados():
    archivo = CARPETA / "datos_prueba.txt"

    if not archivo.exists():
        print(f"{ROJO}No existe datos_prueba.txt todavía.{RESET}")
        return

    lineas = archivo.read_text(encoding="utf-8").splitlines()
    unicas = list(dict.fromkeys(lineas))

    salida = CARPETA / "datos_prueba_sin_duplicados.txt"
    salida.write_text(
        "\n".join(unicas) + ("\n" if unicas else ""),
        encoding="utf-8"
    )

    print(f"{VERDE}✓ Registros originales: {len(lineas)}{RESET}")
    print(f"{VERDE}✓ Duplicados eliminados: {len(lineas) - len(unicas)}{RESET}")
    print(f"{CIAN}✓ Resultado: {salida}{RESET}")


def ver_archivos():
    archivos = list(CARPETA.glob("*.txt"))

    if not archivos:
        print(f"{AMARILLO}No hay resultados guardados.{RESET}")
        return

    print(f"{CIAN}ARCHIVOS DEL PROYECTO:{RESET}")
    for archivo in archivos:
        lineas = archivo.read_text(encoding="utf-8").splitlines()
        print(f"  📄 {archivo.name} — {len(lineas)} registros")


def menu():
    while True:
        banner()
        print(f"""{BLANCO}
  [1] ⚡ Prueba individual de formato
  [2] 🧪 Generar datos de prueba
  [3] 🧹 Eliminar duplicados
  [4] 📁 Ver archivos
  [5] 🚪 Salir
{RESET}""")

        opcion = input(f"{AMARILLO}➤ Selecciona una opción: {RESET}").strip()

        if opcion == "1":
            prueba_individual()
        elif opcion == "2":
            generar_datos_prueba()
        elif opcion == "3":
            eliminar_duplicados()
        elif opcion == "4":
            ver_archivos()
        elif opcion == "5":
            print(f"{VERDE}Programa terminado. ¡Gracias!{RESET}")
            break
        else:
            print(f"{ROJO}Opción no válida.{RESET}")

        input(f"\n{CIAN}Pulsa ENTER para volver al menú...{RESET}")


if __name__ == "__main__":
    menu()
