import socket
"""
模拟本地服务器
"""

# 服务器地址和端口
server_address = ('localhost', 8080)

# 创建一个TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    # 绑定到服务器地址和端口
    server_socket.bind(server_address)

    # 启动服务器，设置最大连接数为5
    server_socket.listen(5)
    print("Server is listening on", server_address)

    while True:
        # 等待客户端连接
        print("Waiting for a client to connect...")
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from", client_address)

        # 与客户端通信
        while True:
            data = client_socket.recv(1024)
            if not data:
                break  # 如果客户端关闭连接，跳出循环

            # 将收到的数据返回给客户端
            print("Received:", data)
            client_socket.send(data)
