from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API URL untuk ports dan bridges
API_URL = "http://192.168.18.24/rest/interface/bridge/port"
BRIDGE_API_URL = "http://192.168.18.24/rest/interface/bridge"
INTERFACE_API_URL = "http://192.168.18.24/rest/interface"  # Tambahkan URL API untuk interfaces
AUTH = ('admin', 'admin')

# Fungsi untuk mengambil data semua ports
def fetch_ports():
    try:
        response = requests.get(API_URL, auth=AUTH)
        if response.status_code == 200:
            return response.json()
        else:
            return []  
    except Exception as e:
        print("Error fetching ports:", e)
        return []

# Fungsi untuk mengambil data semua bridges
def fetch_bridges():
    try:
        response = requests.get(BRIDGE_API_URL, auth=AUTH)
        if response.status_code == 200:
            return response.json()
        else:
            return []  
    except Exception as e:
        print("Error fetching bridges:", e)
        return []

# Fungsi untuk mengambil data semua interfaces
def fetch_interfaces():
    try:
        response = requests.get(INTERFACE_API_URL, auth=AUTH)  # Mengambil data dari API interfaces
        if response.status_code == 200:
            return response.json()
        else:
            return []  
    except Exception as e:
        print("Error fetching interfaces:", e)
        return []

# Halaman utama: Menampilkan daftar bridges
@app.route('/')
def index():
    bridges = fetch_bridges()  
    return render_template('index.html', bridges=bridges)

@app.route('/port')
def port_index():
    ports = fetch_ports()
    bridges = fetch_bridges()  # Ambil daftar bridges
    interfaces = fetch_interfaces()  # Ambil daftar interfaces
    return render_template('port.html', ports=ports, bridges=bridges, interfaces=interfaces)

# CRUD untuk Bridge
@app.route('/bridge/<id>', methods=['GET'])
def bridge_detail(id):
    try:
        response = requests.get(f"{BRIDGE_API_URL}/{id}", auth=AUTH)
        if response.status_code == 200:
            return jsonify(response.json())  
        else:
            return jsonify({})  
    except Exception as e:
        print(f"Error fetching bridge {id} details:", e)
        return jsonify({})  

@app.route('/add/bridge', methods=['POST'])
def add_bridge():
    try:
        data = request.json  
        print("Data received:", data)  
        response = requests.put(BRIDGE_API_URL, auth=AUTH, json={
            "name": data["name"],
            "arp": data["arp"],
            "protocol-mode": data["protocol-mode"],
            "vlan-filtering": data["vlan-filtering"]
        })
        if response.status_code == 201:
            return jsonify({"message": "Bridge created successfully"}), 201  
        print("Error from API:", response.text)  
        return jsonify({"error": "Failed to create bridge"}), response.status_code  
    except Exception as e:
        print("Exception occurred:", e)  
        return jsonify({"error": "An error occurred"}), 500  

@app.route('/update/bridge/<bridge_id>', methods=['PUT'])
def update_bridge(bridge_id):
    try:
        data = request.json  
        response = requests.patch(f"{BRIDGE_API_URL}/{bridge_id}", auth=AUTH, json=data)
        if response.status_code == 200:
            return jsonify({"message": "Bridge updated successfully"}), 200  
        return jsonify({"error": "Failed to update bridge"}), 400  
    except Exception as e:
        print(f"Error updating bridge {bridge_id}:", e)
        return jsonify({"error": "An error occurred"}), 500  

@app.route('/delete/bridge/<bridge_id>', methods=['DELETE'])
def delete_bridge(bridge_id):
    response = requests.delete(f"{BRIDGE_API_URL}/{bridge_id}", auth=AUTH)
    if response.status_code == 204:
        return jsonify({"message": "Bridge deleted successfully"}), 204
    return jsonify({"error": "Failed to delete bridge"}), response.status_code



# CRUD untuk Port
@app.route('/port/<id>', methods=['GET'])
def port_detail(id):
    try:
        response = requests.get(f"{API_URL}/{id}", auth=AUTH)
        if response.status_code == 200:
            return jsonify(response.json())  
        else:
            return jsonify({})  
    except Exception as e:
        print(f"Error fetching port {id} details:", e)
        return jsonify({})  

@app.route('/add/port', methods=['POST'])
def add_port():
    try:
        data = request.json  
        print("Data received:", data)  
        response = requests.put(API_URL, auth=AUTH, json={
            "interface": data["interface"],
            "bridge": data["bridge"],  # Menambahkan bridge yang dipilih
        })
        if response.status_code == 201:
            return jsonify({"message": "Port created successfully"}), 201  
        return jsonify({"error": "Failed to create port"}), response.status_code  
    except Exception as e:
        print("Exception occurred:", e)  
        return jsonify({"error": "An error occurred"}), 500  

@app.route('/update/port/<port_id>', methods=['PUT'])
def update_port(port_id):
    try:
        data = request.json  
        response = requests.patch(f"{API_URL}/{port_id}", auth=AUTH, json=data)
        if response.status_code == 200:
            return jsonify({"message": "Port updated successfully"}), 200  
        return jsonify({"error": "Failed to update port"}), 400  
    except Exception as e:
        print(f"Error updating port {port_id}:", e)
        return jsonify({"error": "An error occurred"}), 500  

@app.route('/delete/port/<port_id>', methods=['DELETE'])
def delete_port(port_id):
    response = requests.delete(f"{API_URL}/{port_id}", auth=AUTH)
    if response.status_code == 204:
        return jsonify({"message": "Bridge deleted successfully"}), 204
    return jsonify({"error": "Failed to delete bridge"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
