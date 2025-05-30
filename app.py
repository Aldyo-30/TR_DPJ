from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API URL untuk ports, bridges, IP address, dan IP pool
BRIDGE_API_URL = "http://172.19.20.29/rest/interface/bridge"
PORT_API_URL = "http://172.19.20.29/rest/interface/bridge/port"
INTERFACE_API_URL = "http://172.19.20.29/rest/interface"  
IP_ADDRESS_API_URL = "http://172.19.20.29/rest/ip/address"  
IP_POOL_API_URL = "http://172.19.20.29/rest/ip/pool"  
AUTH = ('admin', 'admin')

# Fungsi untuk mengambil data semua ports
def fetch_ports():
    try:
        response = requests.get(PORT_API_URL, auth=AUTH, timeout=10)  
        if response.status_code == 200:
            return response.json()
        else:
            return []  
    except requests.exceptions.Timeout:
        print("Error fetching ports: Request timed out")
        return []
    except Exception as e:
        print("Error fetching ports:", e)
        return []

# Fungsi untuk mengambil data semua bridges
def fetch_bridges():
    try:
        response = requests.get(BRIDGE_API_URL, auth=AUTH, timeout=10)  
        if response.status_code == 200:
            return response.json()
        else:
            return []  
    except requests.exceptions.Timeout:
        print("Error fetching bridges: Request timed out")
        return []
    except Exception as e:
        print("Error fetching bridges:", e)
        return []

# Fungsi untuk mengambil data semua interfaces
def fetch_interfaces():
    try:
        response = requests.get(INTERFACE_API_URL, auth=AUTH, timeout=10)  
        if response.status_code == 200:
            return response.json()
        else:
            return []  
    except requests.exceptions.Timeout:
        print("Error fetching interfaces: Request timed out")
        return []
    except Exception as e:
        print("Error fetching interfaces:", e)
        return []

# Fungsi untuk mengambil data semua IP address
def fetch_ip_addresses():
    try:
        response = requests.get(IP_ADDRESS_API_URL, auth=AUTH, timeout=10)  
        if response.status_code == 200:
            return response.json()
        else:
            return []  
    except requests.exceptions.Timeout:
        print("Error fetching IP addresses: Request timed out")
        return []
    except Exception as e:
        print("Error fetching IP addresses:", e)
        return []

# Fungsi untuk mengambil data semua IP pool
def fetch_ip_pools():
    try:
        response = requests.get(IP_POOL_API_URL, auth=AUTH, timeout=10)  
        if response.status_code == 200:
            return response.json()
        else:
            return []  
    except requests.exceptions.Timeout:
        print("Error fetching IP pools: Request timed out")
        return []
    except Exception as e:
        print("Error fetching IP pools:", e)
        return []

# Halaman utama: Menampilkan daftar bridges
@app.route('/')
def index():
    bridges = fetch_bridges()  
    return render_template('index.html', bridges=bridges)

@app.route('/port')
def port_index():
    ports = fetch_ports()
    bridges = fetch_bridges()  
    interfaces = fetch_interfaces()  
    return render_template('port.html', ports=ports, bridges=bridges, interfaces=interfaces)

@app.route('/ip')
def ip_index():
    ip_addresses = fetch_ip_addresses()  
    interfaces = fetch_interfaces()  
    return render_template('ip_address.html', ip_addresses=ip_addresses, interfaces=interfaces)  

@app.route('/pool')
def ip_pool_index():
    ip_pools = fetch_ip_pools()  
    return render_template('ip_pool.html', ip_pools=ip_pools)  

# CRUD untuk Bridge
@app.route('/bridge/<id>', methods=['GET'])
def bridge_detail(id):
    try:
        response = requests.get(f"{BRIDGE_API_URL}/{id}", auth=AUTH, timeout=10)  
        if response.status_code == 200:
            return jsonify(response.json())  
        else:
            return jsonify({})  
    except requests.exceptions.Timeout:
        print(f"Error fetching bridge {id} details: Request timed out")
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
        response = requests.get(f"{PORT_API_URL}/{id}", auth=AUTH, timeout=10) 
        if response.status_code == 200:
            return jsonify(response.json())  
        else:
            return jsonify({})  
    except requests.exceptions.Timeout:
        print(f"Error fetching port {id} details: Request timed out")
        return jsonify({})  
    except Exception as e:
        print(f"Error fetching port {id} details:", e)
        return jsonify({})  

@app.route('/add/port', methods=['POST'])
def add_port():
    try:
        data = request.json  
        print("Data received:", data)  
        response = requests.put(PORT_API_URL, auth=AUTH, json={
            "interface": data["interface"],
            "bridge": data["bridge"], 
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
        response = requests.patch(f"{PORT_API_URL}/{port_id}", auth=AUTH, json=data)
        if response.status_code == 200:
            return jsonify({"message": "Port updated successfully"}), 200  
        return jsonify({"error": "Failed to update port"}), 400  
    except Exception as e:
        print(f"Error updating port {port_id}:", e)
        return jsonify({"error": "An error occurred"}), 500  

@app.route('/delete/port/<port_id>', methods=['DELETE'])
def delete_port(port_id):
    response = requests.delete(f"{PORT_API_URL}/{port_id}", auth=AUTH)
    if response.status_code == 204:
        return jsonify({"message": "Port deleted successfully"}), 204
    return jsonify({"error": "Failed to delete port"}), response.status_code

# CRUD untuk IP Address
@app.route('/ip/<id>', methods=['GET'])
def ip_detail(id):
    try:
        response = requests.get(f"{IP_ADDRESS_API_URL}/{id}", auth=AUTH, timeout=10)  
        if response.status_code == 200:
            return jsonify(response.json())  
        else:
            return jsonify({})  
    except requests.exceptions.Timeout:
        print(f"Error fetching IP address {id} details: Request timed out")
        return jsonify({})  
    except Exception as e:
        print(f"Error fetching IP address {id} details:", e)
        return jsonify({})  

@app.route('/add/ip', methods=['POST'])
def add_ip():
    try:
        data = request.json  
        print("Data received:", data)  
        response = requests.put(IP_ADDRESS_API_URL, auth=AUTH, json={
            "address": data["address"],
            "interface": data["interface"], 
        })
        if response.status_code == 201:
            return jsonify({"message": "IP Address created successfully"}), 201  
        return jsonify({"error": "Failed to create IP Address"}), response.status_code  
    except Exception as e:
        print("Exception occurred:", e)  
        return jsonify({"error": "An error occurred"}), 500  

@app.route('/update/ip/<ip_id>', methods=['PUT'])
def update_ip(ip_id):
    try:
        data = request.json  
        response = requests.patch(f"{IP_ADDRESS_API_URL}/{ip_id}", auth=AUTH, json=data)
        if response.status_code == 200:
            return jsonify({"message": "IP Address updated successfully"}), 200  
        return jsonify({"error": "Failed to update IP Address"}), 400  
    except Exception as e:
        print(f"Error updating IP Address {ip_id}:", e)
        return jsonify({"error": "An error occurred"}), 500  

@app.route('/delete/ip/<ip_id>', methods=['DELETE'])
def delete_ip(ip_id):
    response = requests.delete(f"{IP_ADDRESS_API_URL}/{ip_id}", auth=AUTH)
    if response.status_code == 204:
        return jsonify({"message": "IP Address deleted successfully"}), 204
    return jsonify({"error": "Failed to delete IP Address"}), response.status_code
# CRUD untuk IP Pool
@app.route('/pool/<id>', methods=['GET'])
def ip_pool_detail(id):
    try:
        response = requests.get(f"{IP_POOL_API_URL}/{id}", auth=AUTH, timeout=10)  
        if response.status_code == 200:
            return jsonify(response.json())  
        else:
            return jsonify({})  
    except requests.exceptions.Timeout:
        print(f"Error fetching IP pool {id} details: Request timed out")
        return jsonify({})  
    except Exception as e:
        print(f"Error fetching IP pool {id} details:", e)
        return jsonify({})  

@app.route('/add/pool', methods=['POST'])
def add_ip_pool():
    try:
        data = request.json  
        print("Data received:", data)  
        response = requests.put(IP_POOL_API_URL, auth=AUTH, json={
            "name": data["name"],
            "ranges": data["ranges"],  
        })
        if response.status_code == 201:
            return jsonify({"message": "IP Pool created successfully"}), 201  
        return jsonify({"error": "Failed to create IP Pool"}), response.status_code  
    except Exception as e:
        print("Exception occurred:", e)  
        return jsonify({"error": "An error occurred"}), 500  

@app.route('/update/pool/<pool_id>', methods=['PUT'])
def update_ip_pool(pool_id):
    try:
        data = request.json  
        response = requests.patch(f"{IP_POOL_API_URL}/{pool_id}", auth=AUTH, json=data)
        if response.status_code == 200:
            return jsonify({"message": "IP Pool updated successfully"}), 200  
        return jsonify({"error": "Failed to update IP Pool"}), 400  
    except Exception as e:
        print(f"Error updating IP Pool {pool_id}:", e)
        return jsonify({"error": "An error occurred"}), 500  

@app.route('/delete/pool/<pool_id>', methods=['DELETE'])
def delete_ip_pool(pool_id):
    response = requests.delete(f"{IP_POOL_API_URL}/{pool_id}", auth=AUTH)
    if response.status_code == 204:
        return jsonify({"message": "IP Pool deleted successfully"}), 204
    return jsonify({"error": "Failed to delete IP Pool"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
