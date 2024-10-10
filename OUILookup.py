import requests
import getopt
import sys
import os

# URL de la API pública para consulta de MACs
API_URL = "https://api.maclookup.app/v2/macs/"

# Función para consultar el fabricante de una dirección MAC
def get_vendor_by_mac(mac):
    try:
        response = requests.get(API_URL + mac)
        if response.status_code == 200:
            data = response.json()
            vendor = data.get('company', 'Not found')
            return vendor
        else:
            return "Not found"
    except Exception as e:
        return f"Error: {str(e)}"

# Función para obtener la tabla ARP en Windows utilizando 'arp -a'
def get_arp_table():
    print("Obteniendo la tabla ARP en Windows...")
    arp_table = os.popen("arp -a").read().splitlines()  # Ejecuta arp -a en Windows y lee la salida
    devices = []
    
    for line in arp_table:
        if "dynamic" in line or "static" in line:  # Filtrar solo las líneas relevantes con MACs
            parts = line.split()
            ip = parts[0]  # La IP está en la primera posición
            mac = parts[1]  # La MAC está en la segunda posición
            vendor = get_vendor_by_mac(mac)  # Obtener el fabricante desde la API
            devices.append((ip, mac, vendor))
    
    return devices

# Función para imprimir el uso del programa
def print_help():
    print("Uso: python OUILookup.py --mac <mac> | --arp | [--help]")
    print("--mac <mac>: Consulta el fabricante de una dirección MAC.")
    print("--arp: Muestra los fabricantes de las MAC en la tabla ARP.")
    print("--help: Muestra este mensaje de ayuda.")

# Función principal para procesar los parámetros
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "", ["mac=", "arp", "help"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    if len(opts) == 0:
        print_help()
        sys.exit()

    for opt, arg in opts:
        if opt == "--help":
            print_help()
            sys.exit()
        elif opt == "--mac":
            mac = arg
            vendor = get_vendor_by_mac(mac)
            print(f"MAC address: {mac}")
            print(f"Fabricante: {vendor}")
        elif opt == "--arp":
            arp_entries = get_arp_table()
            if arp_entries:
                for ip, mac, vendor in arp_entries:
                    print(f"IP: {ip}, MAC: {mac}, Fabricante: {vendor}")
            else:
                print("No se encontraron dispositivos en la tabla ARP.")

if __name__ == "__main__":
    main(sys.argv[1:])
