import cv2
import numpy as np
import json
import os
from flask import Flask, render_template, send_file
import csv
import threading 
import signal
import sys
from datetime import datetime

app = Flask(__name__)

recognized_users = {}

@app.route('/')
def index():
    return render_template('index.html', users=recognized_users)

@app.route('/export')
def export():
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')  # Corrigir formato do timestamp
    filename = f'chamada_{timestamp}.csv'
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Nome do Usuário', 'Reconhecido', 'Data e Hora da Coleta', 'Número de Matrícula', 'Sobrenome', 'Período/Semestre', 'Curso']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, data in recognized_users.items():
            writer.writerow({
                'Nome do Usuário': user,
                'Reconhecido': 'Sim' if data['recognized'] else 'Não',
                'Data e Hora da Coleta': data['datetime'],
                'Número de Matrícula': data['matricula'],
                'Sobrenome': data['sobrenome'],
                'Período/Semestre': data['periodo'],
                'Curso': data.get('curso', 'N/A')  # Use 'N/A' if 'curso' is not present
            })
    return send_file(filename, as_attachment=True)

def start_camera():
    global recognized_users
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read('trainer.yml')
        print("[INFO] Modelo carregado com sucesso.")
    except cv2.error as e:
        print(f"[ERROR] Falha ao carregar o modelo treinado: {e}")
        exit()
    face_cascade_Path = "haarcascade_frontalface_default.xml"
    
    faceCascade = cv2.CascadeClassifier(face_cascade_Path)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    names = {}
    with open('names.json', 'r') as fs:
        names = json.load(fs)
    
    print("[DEBUG] Conteúdo do names.json:", names)
    
    recognized_users = {name['name']: {
        'recognized': False,
        'datetime': '',
        'matricula': name['matricula'],
        'sobrenome': name['sobrenome'],
        'periodo': name['periodo'],
        'curso': name.get('curso', 'N/A')  
    } for name in names.values()}
    
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # Definir largura
    cam.set(4, 480)  # Definir altura
    
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    
    while True:
        ret, img = cam.read()
        if not ret:
            print("[ERROR] Falha ao capturar imagem da câmera.")
            break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )
        recognized_names_in_frame = set()
        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            print(f"[DEBUG] ID: {id}, Confiança: {confidence}")
            if confidence > 51:
                if str(id) in names:
                    try:
                        name = names[str(id)]['name']
                        if name not in recognized_names_in_frame:
                            print(f"[DEBUG] Rosto reconhecido: {name}")
                            recognized_users[name]['recognized'] = True
                            recognized_users[name]['datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            recognized_names_in_frame.add(name)
                            confidence = "  {0}%".format(round(confidence))
                        else:
                            name = "Desconhecido"
                            confidence = "N/A"                 
                    except IndexError as e:
                        print(f"[ERROR] IndexError: {e}")
                        name = "Desconhecido"
                        confidence = "N/A"
                else:
                    print(f"[ERROR] ID {id} não encontrado em names.")
                    name = "Desconhecido"
                    confidence = "N/A"
            else:
                name = "Desconhecido"
                confidence = "N/A"
    
            cv2.putText(img, name, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, confidence, (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
    
        cv2.imshow('camera', img)
    
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break
    
    print("\n [INFO] Saindo do programa.")
    cam.release()
    cv2.destroyAllWindows()
    os._exit(0)

def signal_handler(sig, frame):
    print("\n [INFO] Encerrando o programa.")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    flask_thread = threading.Thread(target=lambda: app.run(debug=False, use_reloader=False))
    flask_thread.start()
    start_camera()
    flask_thread.join()
