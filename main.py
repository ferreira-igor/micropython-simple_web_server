from machine import Pin
try:
  import usocket as socket
except:
  import socket

# Set this with the corresponding pin of your board.
led_gpio = 2
led = Pin(led_gpio, Pin.OUT)

web_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
web_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
web_server.bind(("", 80))
web_server.listen(5)

# Just a simple web interface for reference.
def web_page():
    if led.value() == 0:
        led_state = "ON"
    else:
        led_state = "OFF"  
    html = """
        <html>
            <head>
                <title>ESP Web Server</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
                <h1>ESP Web Server</h1>
                <p>GPIO state:&nbsp;<strong>{0}</strong></p>
                <form>
                <p><button name="led" value="on">ON</button></p>
                <p><button name="led" value="off">OFF</button></p>
                </form>
            </body>
        </html>
          """.format(led_state)
    return html

def main():
    client, addr = web_server.accept()
    request = b""
    while "\r\n\r\n" not in request:
        request += client.recv(128)
    request = str(request)
    led_on = request.find("/?led=on")
    led_off = request.find("/?led=off")
    if led_on == 6:
        led.value(0)
        print("LED IS ON!")
    if led_off == 6:
        led.value(1)
        print("LED IS OFF!")
    client.send("HTTP/1.1 200 OK\r\n")
    client.send("Content-Type: text/html\r\n")
    client.sendall(web_page())
    client.close()

print("Starting web server...")

while True:
    main()

