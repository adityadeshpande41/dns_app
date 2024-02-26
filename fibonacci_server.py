from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

@app.route('/register', methods=['PUT'])
def register():
    data = request.json
    as_ip = data['as_ip']
    message = f"TYPE=A\nNAME={data['hostname']}\nVALUE={data['ip']}\nTTL=10"
    
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(message.encode(), (as_ip, 53533))
    udp_socket.close()

    return '', 201

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    try:
        number = int(request.args.get('number'))
        return jsonify({'result': fibonacci(number)}), 200
    except ValueError:
        return jsonify({'error': 'Bad format'}), 400

if __name__ == '__main__':
    app.run(port=9090)
