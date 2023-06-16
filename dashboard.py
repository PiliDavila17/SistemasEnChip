import os, uvicorn
from threading import Thread
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from gpiozero import DistanceSensor, LED, Button, AngularServo
from time import sleep
from signal import pause

app = FastAPI()

app = FastAPI()

# Define Leds para agua y Leche
bombaagua = LED(17)
bombaleche = LED(16)

# Define los botones para 
Bpa = Button(18) # Agua
Bpl = Button(19) # Leche
Bca = Button(20) # Creatina con agua
Bpea = Button(21) # Pre entreno con agua

# Define los angulos max y min de los servos
servop = AngularServo(13, min_pulse_width=0.00058, max_pulse_width=0.0023)
servopre = AngularServo(12, min_pulse_width=0.00058, max_pulse_width=0.0023)
servocre = AngularServo(6, min_pulse_width=0.00058, max_pulse_width=0.0023)

# Define los angulos de los servo motores
servop.angle = 90
servopre.angle = 90
servocre.angle = 90

# Se definen las conexiones del sensor ultra sonico
sensor = DistanceSensor(23, 24)

# Primer vistazo
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
        <html>
            <head>
                <title>ProteMix</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #000000;
                        text-align: center;
                    }
                    
                    h1 {
                        font-size: 3em;
                        margin-top: 3em;
                        margin-bottom: 3em;
                        color: #fffff0;
                    }

                     h2 {
                        font-size: 2em;
                        margin-top: 2em;
                        margin-bottom: 3em;
                        color: #fffff0;
                    }
                    
                    button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 16px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin-top: 2em;
                        cursor: pointer;
                        border-radius: 4px;
                    }
                    
                    button:hover {
                        background-color: #3e8e41;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>ProteMix</h1>
                    <h2>¡Bienvenido!</h1>
                    <button onclick="location.href='/comenzar';">Comenzar</button>
                </div>
            </body>
        </html>
    """

# Parte de Seleccion de suplemento 
@app.get("/comenzar", response_class=HTMLResponse)
def read_comenzar():
    return """
        <html>
            <head>
                <title>Selecciona tu bebida</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #000000;
                        text-align: center;
                    }
                    
                    h1 {
                        font-size: 3em;
                        margin-top: 3em;
                        margin-bottom: 2em;
                        color: #fffff0;
                    }
                    
                    button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 16px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin-top: 2em;
                        cursor: pointer;
                        border-radius: 4px;
                    }
                    
                    button:hover {
                        background-color: #3e8e41;
                    }
                    
                    .player {
                        width: 50%;
                        margin: 0 auto;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }
                    
                    .player__title {
                        font-size: 2em;
                        margin: 1em 0;
                    }
                    
                    .player__controls {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        margin: 1em;
                    }
                    
                    .player__button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 1em 2em;
                        margin: 0 1em;
                        cursor: pointer;
                        border-radius: 50%;
                    }
                    
                    .player__button:hover {
                        background-color: #3e8e41;
                    }
                    
                    .player__status {
                        font-size: 1.2em;
                        margin: 1em 0;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Selecciona tu Suplemento</h1>
                    <div class="player">
                        <div class="player__controls">
                            <button class="player__button" onclick="location.href='/comenzar/proteina';">Proteina</button>
                            <button class="player__button" onclick="location.href='/comenzar/creatina';">Creatina</button>
                            <button class="player__button" onclick="location.href='/comenzar/preEntreno';">Pre-Entreno</button>  
                        </div>
                        <div class="player__status">Calculando</div>
                    </div>
                </div>
            </body>
        </html>
    """

# Seleccion de Proteina
@app.get("/comenzar/proteina", response_class=HTMLResponse)
def ponle_proteina():
    print("Seleccionaste prote, provecho")
    return """
        <html>
            <head>
                <title>Shaker</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #000000;
                        text-align: center;
                    }
                    
                    h1 {
                        font-size: 3em;
                        margin-top: 3em;
                        margin-bottom: 2em;
                        color: #333;
                    }
                    
                    button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 16px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin-top: 2em;
                        cursor: pointer;
                        border-radius: 4px;
                    }
                    
                    button:hover {
                        background-color: #3e8e41;
                    }
                    
                    .player {
                        width: 50%;
                        margin: 0 auto;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }
                    
                    .player__title {
                        font-size: 2em;
                        margin: 1em 0;
                    }
                    
                    .player__controls {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        margin: 1em;
                    }
                    
                    .player__button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 1em 2em;
                        margin: 0 1em;
                        cursor: pointer;
                        border-radius: 50%;
                    }
                    
                    .player__button:hover {
                        background-color: #3e8e41;
                    }
                    
                    .player__status {
                        font-size: 1.2em;
                        margin: 1em 0;
                    }
                </style>
            </head>
            <body>
                <div class="player">
                        <h1> Selecciona el liquido</h1>
                        <div class="player__controls">
                            <button class="player__button" onclick="location.href='/comenzar/proteina/agua';">Agua</button>
                            <button class="player__button" onclick="location.href='/comenzar/proteina/leche';">Leche</button>
                        </div>
                        <div class="player__status">Calculando</div>
                    </div>
                </div>
            </body>
        </html>
    """

# Define las configuraciones del Agua 
@app.get("/comenzar/proteina/agua", response_class=HTMLResponse)
def ponle_agua():
    print("Seleccionaste awita")
    distancia = 12
    while sensor.distance * 100 >= distancia:
            print('Distancia agua:', sensor.distance * 100, 'cm')
            bombaagua.on()
    bombaagua.off()
    # Dosificador
    for i in range(8):
            servop.angle = 90
            sleep(0.5)
            servop.angle = -90
            sleep(0.5)
    print("Si jalaron los servos de Proteina con Agua")
    return """
        <html>
            <head>
                <title>Shaker</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #000000;
                        text-align: center;
                    }
                    
                    h1 {
                        font-size: 3em;
                        margin-top: 3em;
                        margin-bottom: 2em;
                        color: #333;
                    }
                    button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 16px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin-top: 2em;
                        cursor: pointer;
                        border-radius: 4px;
                    }
                    
                    button:hover {
                        background-color: #3e8e41;
                    }
                    
                    .player {
                        width: 50%;
                        margin: 0 auto;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }
                    
                    .player__title {
                        font-size: 2em;
                        margin: 1em 0;
                    }
                    
                    .player__controls {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        margin: 1em;
                    }
                    
                    .player__button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 1em 2em;
                        margin: 0 1em;
                        cursor: pointer;
                        border-radius: 50%;
                    }
                    
                    .player__button:hover {
                        background-color: #3e8e41;
                    }
                    
                    .player__status {
                        font-size: 1.2em;
                        margin: 1em 0;
                    }
                </style>
            </head>
            <body>
                <h1>Preparando tu bebida...</h1>
                <div class="player">
                        <h1>Cuando este lista tu bebida selecciona el botón de listo</h1>
                        <div class="player__controls">
                            <button class="player__button" onclick="location.href='/comenzar';">Listo</button>
                        </div>
                        <div class="player__status">Calculando</div>
                    </div>
                </div>
            </body>
        </html>
    """

# Define las configuraciones de la leche
@app.get("/comenzar/proteina/leche", response_class=HTMLResponse)
def ponle_leche():
    print("Seleccionaste leche")
    distancia = 12
    while sensor.distance * 100 >= distancia:
            print('Distancia leche:', sensor.distance * 100, 'cm')
            bombaleche.on()
    bombaleche.off()
    # Dosificador
    for i in range(8):
            servop.angle = 90
            sleep(0.5)
            servop.angle = -90
            sleep(0.5)
    print("Si jalaron los servos de Proteina con Leche")
    return """
        <html>
            <head>
                <title>Shaker</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #000000;
                        text-align: center;
                    }
                    
                    h1 {
                        font-size: 3em;
                        margin-top: 3em;
                        margin-bottom: 2em;
                        color: #333;
                    }
                    button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 16px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin-top: 2em;
                        cursor: pointer;
                        border-radius: 4px;
                    }
                    
                    button:hover {
                        background-color: #3e8e41;
                    }
                    
                    .player {
                        width: 50%;
                        margin: 0 auto;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }
                    
                    .player__title {
                        font-size: 2em;
                        margin: 1em 0;
                    }
                    
                    .player__controls {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        margin: 1em;
                    }
                    
                    .player__button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 1em 2em;
                        margin: 0 1em;
                        cursor: pointer;
                        border-radius: 50%;
                    }
                    
                    .player__button:hover {
                        background-color: #3e8e41;
                    }
                    
                    .player__status {
                        font-size: 1.2em;
                        margin: 1em 0;
                    }
                </style>
            </head>
            <body>
                <h1>Preparando tu bebida...</h1>
                <div class="player">
                        <h1>Cuando este lista tu bebida selecciona el botón de listo</h1>
                        <div class="player__controls">
                            <button class="player__button" onclick="location.href='/comenzar';">Listo</button>
                        </div>
                        <div class="player__status">Calculando</div>
                    </div>
                </div>
            </body>
        </html>
    """

# Define las configuraciones de la Creatina
@app.get("/comenzar/creatina", response_class=HTMLResponse)
def ponle_creatina():
    print("Seleccionaste Creatina")
    # Sensor Ultra para distribuir base de la bebida
    distancia = 12
    while sensor.distance * 100 >= distancia:
            print('Distancia agua:', sensor.distance * 100, 'cm')
            bombaagua.on()
    bombaagua.off()
    # Dosificador Creatina
    servocre.angle = 90
    sleep(0.5)
    servocre.angle = -90
    sleep(0.5)
    print("Si jalaron los servos Creatina")
    return """
        <html>
            <head>
                <title>Shaker</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #000000;
                        text-align: center;
                    }
                    
                    h1 {
                        font-size: 3em;
                        margin-top: 3em;
                        margin-bottom: 2em;
                        color: #333;
                    }

                    button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 16px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin-top: 2em;
                        cursor: pointer;
                        border-radius: 4px;
                    }
                    
                    button:hover {
                        background-color: #3e8e41;
                    }
                    
                    .player {
                        width: 50%;
                        margin: 0 auto;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }
                    
                    .player__title {
                        font-size: 2em;
                        margin: 1em 0;
                    }
                    
                    .player__controls {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        margin: 1em;
                    }
                    
                    .player__button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 1em 2em;
                        margin: 0 1em;
                        cursor: pointer;
                        border-radius: 50%;
                    }
                    
                    .player__button:hover {
                        background-color: #3e8e41;
                    }
                    
                    .player__status {
                        font-size: 1.2em;
                        margin: 1em 0;
                    }
                </style>
            </head>
            <body>
                <h1>Preparando tu bebida...</h1>
                <div class="player">
                        <h1>Cuando este lista tu bebida selecciona el botón de listo</h1>
                        <div class="player__controls">
                            <button class="player__button" onclick="location.href='/comenzar';">Listo</button>
                        </div>
                        <div class="player__status">Calculando</div>
                    </div>
                </div>
            </body>
        </html>
    """

# Define las configuraciones del PreEntreno
@app.get("/comenzar/preEntreno", response_class=HTMLResponse)
def ponle_preEntreno():
    print("Seleccionaste Pre-Entreno")
    # Sensor Ultra para distribuir base de la bebida
    distancia = 12
    while sensor.distance * 100 >= distancia:
            print('Distancia agua:', sensor.distance * 100, 'cm')
            bombaagua.on()
    bombaagua.off()
    # Dosificador Pre-Entreno
    for i in range(2):
            servop.angle = 90
            sleep(0.5)
            servop.angle = -90
            sleep(0.5)
    print("Si jalaron los servos Pre-Entreno")
    return """
        <html>
            <head>
                <title>Shaker</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #000000;
                        text-align: center;
                    }
                    
                    h1 {
                        font-size: 3em;
                        margin-top: 3em;
                        margin-bottom: 2em;
                        color: #333;
                    }

                    button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 16px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin-top: 2em;
                        cursor: pointer;
                        border-radius: 4px;
                    }
                    
                    button:hover {
                        background-color: #3e8e41;
                    }
                    
                    .player {
                        width: 50%;
                        margin: 0 auto;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }
                    
                    .player__title {
                        font-size: 2em;
                        margin: 1em 0;
                    }
                    
                    .player__controls {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        margin: 1em;
                    }
                    
                    .player__button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 1em 2em;
                        margin: 0 1em;
                        cursor: pointer;
                        border-radius: 50%;
                    }
                    
                    .player__button:hover {
                        background-color: #3e8e41;
                    }
                    
                    .player__status {
                        font-size: 1.2em;
                        margin: 1em 0;
                    }

                </style>
            </head>
            <body>
                <h1>Preparando tu bebida...</h1>
                <div class="player">
                        <h1>Cuando este lista tu bebida selecciona el botón de listo</h1>
                        <div class="player__controls">
                            <button class="player__button" onclick="location.href='/comenzar';">Listo</button>
                        </div>
                        <div class="player__status">Calculando</div>
                    </div>
                </div>
            </body>
        </html>
    """

def run_app():
    uvicorn.run(app, host="0.0.0.0", port=8000)

first_thread = Thread(target=run_app)
first_thread.start()