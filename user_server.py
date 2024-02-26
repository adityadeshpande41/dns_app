from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def fibonacci_request():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Check if any parameters are missing
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify({'error': 'Missing parameters'}), 400

    # Query AS for the IP address of FS
    message = f"TYPE=A\nNAME={hostname}"
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(message.encode(), (as_ip, int(as_port)))
    response, _ = udp_socket.recvfrom(1024)
    fs_ip = response.decode().split("\n")[2].split("=")[1]
    udp_socket.close()

    # Make HTTP request to FS
    try:
        response = request.get(f"http://{fs_ip}:{fs_port}/fibonacci?number={number}")
        if response.status_code == 200:
            return response.json(), 200
        else:
            return jsonify({'error': 'Failed to get Fibonacci number from FS'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080)
