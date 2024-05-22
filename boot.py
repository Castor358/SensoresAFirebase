from time import sleep
from machine import Pin
from firebase import firebase
import network
import requests
import dht
import socket
import _thread

humedad = 0
temperatura = 0
led = Pin(2,Pin.OUT)
sensor = dht.DHT22(Pin(5))

def webpage(temperatura,humedad):
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estacion Meteorologica Personal</title>
    <!--link rel="preconnect" href="https://fonts.googleapis.com"-->
    <!--link rel="preconnect" href="https://fonts.gstatic.com" crossorigin-->
    <link href="https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=PT+Sans:ital,wght@0,400;0,700;1,400;1,700&family=Raleway:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
    <style>
        body{
            display: block;
            justify-content: center;
            text-align: center;
            background-color: #ffffff;
            color: #171717;
            margin: 0 auto;
            .panel{
                width: 100%; height: 100%;
                background-color: #ececec;
                .mainTitle{
                    font-family: "Raleway", sans-serif;
                    font-weight: 700; font-size: 25px;
                    margin: 0px 0px 30px 0px ;
                    padding: 10px;
                }
            }
        }
        .mainFrame{
            display: grid; width: 100%; height: 100%;
            justify-content: center;
            .temperature{
                width: 100%; display: grid; 
                justify-content: center;
                background-color: #fafafa; border-radius: 10px;
                margin: 10px 50px 20px 0px ;
                box-shadow: 5px 4px 4px rgba(0, 0, 0, 0.3);
                .tempHead{
                    display: flex; align-items: center; justify-content: center;
                    img{margin: 0 auto; padding: 0 auto;}
                    .title{
                        font-family: "PT Sans", sans-serif; font-size: 20px; 
                        font-weight: 600; padding-left:5px;
                    }
                }
                .tempTail{
                    margin: 0 auto; padding-bottom: 23px;
                    display: flex;
                    .paramESP32{ 
                        display: flex; justify-content: center;
                        font-family: Arial; font-size: 35px;
                        margin: auto; font-weight: 400;
                    }
                }
            }
            .humidity{
                width: 100%; display: grid;
                justify-content: center;
                background-color: #fafafa; border-radius: 10px;
                margin: 0px 50px 200px 0px ;
                box-shadow: 5px 4px 4px rgba(0, 0, 0, 0.3);
                .humHead{
                    display: flex; align-items: center; justify-content: center;
                    img{margin: 0 auto; padding: 0 auto;}
                    .title{
                        font-family: "PT Sans", sans-serif; font-size: 20px; 
                        font-weight: 600; padding-left:5px;
                    }
                }
                .humTail{
                    margin: 0 auto; padding-bottom: 23px;
                    display: flex;
                    .paramESP32{ 
                        display: flex; justify-content: center;
                        font-family: Arial; font-size: 35px;
                        margin: auto; font-weight: 400;
                    }
                }
            }
        }
        
        .loadingCircle {
            width: 30px;
            height: 30px;
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            margin: 4px 15px 0px 0px;
            animation: spin 1.5s linear infinite;
        }
        .loadingHum {border-left: 4px solid #3498db;}
        .loadingTemp {border-left: 4px solid #FF6F56;}

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        } 

        .btn{
            display: flex;
            width: 100%; height: 100%;
            .similar{
                box-shadow: 5px 4px 4px rgba(0, 0, 0, 0.3);
                text-align: center; justify-content: center; align-content: center;
                width: 145px; height: 60px;
                border: 0px solid #000000;
                text-decoration: none;
                text-decoration-color: #000000;
                font-family: "PT Sans", sans-serif; font-size: 30px; 
            }
            .btn_top{
                background-color: #79b8e2; color: #ececec;
                border-radius: 7px 0px 0px 7px ;
            }
            .btn_bot{
                background-color: #fafafa; color: #000000;
                border-radius: 0px 7px 7px 0px ;
            }

        }


    </style>
</head>
<body>
    <header class="panel"><h1 class="mainTitle">Clima Espresso</h1></header>
    <div class="mainFrame" >
        <div class="temperature">
            <div class="tempHead">
                <img width="40" height="40" src="https://img.icons8.com/pulsar-color/48/hex-burner.png"/>
                <!--img width="48" height="48" src="https://img.icons8.com/pulsar-color/48/light-rain.png"/-->
                <p class="title">Temperature in celcius</p>
            </div>
            <div class="tempTail">
                <div class="loadingCircle loadingTemp"></div>
                <p class="paramESP32">'''+str(temperatura)+'''°</p><!---->
            </div>
        </div>
        <div class="humidity">
            <div class="humHead">
                <!--img width="44" height="44" src="https://img.icons8.com/pulsar-color/48/fire-element.png"/-->
                <img width="40" height="40" src="https://img.icons8.com/pulsar-color/48/snowflake.png"/>
                <p class="title">Humidity in the area</p>
            </div>
            <div class="humTail">
                <div class="loadingCircle loadingHum"></div>
                <p class="paramESP32">'''+str(humedad)+'''°</p><!---->
            </div>
        </div>

        <div class="btn">
            <a class="similar btn_top" href="/on">I</a> 
            <a class="similar btn_bot" href="/off">O</a>
        </div>


    </div>
                  <script>
                    function autoReloadPage() {
                        // Reload the entire page
                        location.reload();
                    }

                    // Auto-reload the page every 20 seconds
                    setInterval(autoReloadPage, 20000);
                </script>
</body>
</html>
'''

firebase = Firebase(
    url = "AQUI VA EL LINK DE TU BASE DE DATOS FIREBASE",
    auth = "AQUI VA LA PRIVATE KEY ID"
    )

def conectar(ssid, passw):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected() is False:
        wlan.connect(ssid,passw)
        print("Intentando conectar...")
        while wlan.isconnected() is False:
            pass

    print(f"Pon esta IP en tu navegador: {wlan.ifconfig()[0]}")
      
def obtenerdatosfb(route):
    datos = firebase.get(route)
    return datos

def subirdatosfb():
    global temperatura, humedad
    while True:
        try:
            firebase.set("tabla",{
                "campo1":humedad,
                "campo2":temperatura,
            })
            sleep(10)
        except OSError as e:
            print(f'Error: {e}')

def sensores():
    global temperatura, humedad
    while True:
        try:
            sleep(8)
            sensor.measure()
            temperatura = sensor.temperature()
            humedad = sensor.humidity()
            sleep(12)
        except OSError as e:
                print(f'El sensor fallo: {e}')
                sleep(5)

#===============================================
conectar('NOMBREDETURED','TUCONTRASENA')
_thread.start_new_thread(sensores, ())
_thread.start_new_thread(subirdatosfb, ())
    
conexion=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
conexion.bind(('127.0.0.221',80)) 
conexion.listen(5)
        
while True:
    usuario, direccionip = conexion.accept()
    print(f"New connection from: {direccionip}")
            
    request = usuario.recv(1024)
    if request.find('/off') == 6 :
        led.off()
    if request.find('/on') == 6 :
        led.on()
            
    response = webpage(temperatura,humedad)
    conexion.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    conexion.sendall(response)
    usuario.close