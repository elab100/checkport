#! /usr/bin/python3
from fastapi import FastAPI, Request, Response
import uvicorn
import socket
import ipaddress


def is_valid_ip(ip):
    try:
        # Try to create an IP address object
        ip_obj = ipaddress.ip_address(ip)
        return True
    except ValueError:
        # If the input is not a valid IP address, an exception will be raised
        try:
            # Try to resolve the domain name to an IP address
            ip_addr = socket.gethostbyname(ip)
            # Check if the resolved IP address is valid
            ip_obj = ipaddress.ip_address(ip_addr)
            return True
        except (socket.gaierror, ValueError):
            # If the input is neither a valid IP address nor a resolvable domain name, return False
            return False


def is_valid_port(port):
    try:
        port = int(port)
        if 0 <= port <= 65535:
            return True
        else:
            return False
    except ValueError:
        return False


def is_accessible(ip, port, timeout=3):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False


app = FastAPI()


@app.get("/ip")
async def get_client_ip(request: Request):
    # Get the client's IP address from the request object
    client_ip = request.client.host
    response = Response(client_ip, media_type="text/plain")
    return response


@app.get("/checkport")
async def checkport(ip: str, port: int):
    if is_valid_ip(ip.strip()) and is_valid_port(port):
        print(ip, port)
        if is_accessible(ip, port, timeout=3):
            print(f"{ip}:{port} is accessible.")
            return {"status": 1, "message": f"{ip}:{port} is accessible."}
        else:
            print(f"{ip}:{port} is not accessible.")
            return {"status": 0, "message": f"{ip}:{port} is not accessible."}


if __name__ == '__main__':
    uvicorn.run(app='checkport:app', host="127.0.0.1",
                port=8800)
