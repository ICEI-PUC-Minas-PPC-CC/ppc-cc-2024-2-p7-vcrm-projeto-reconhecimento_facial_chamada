import numpy as np
import json
import cv2
import os
from datetime import datetime, timedelta

def create_directory(directory: str) -> None:
    """
    Criar um diretório se ele não existir.

    Parâmetros:
        directory (str): O caminho do diretório a ser criado.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_face_id(directory: str) -> int:
    """
    Obter o primeiro identificador disponível

    Parâmetros:
        directory (str): O caminho do diretório de imagens.
    """
    user_ids = []
    for filename in os.listdir(directory):
        number = int(os.path.split(filename)[-1].split("-")[1])
        user_ids.append(number)
    user_ids = sorted(list(set(user_ids)))
    max_user_ids = 1 if len(user_ids) == 0 else max(user_ids) + 1
    for i in sorted(range(0, max_user_ids)):
        try:
            if user_ids.index(i):
                face_id = i
        except ValueError as e:
            return i
    return max_user_ids

def save_name(face_id: int, face_name: str, matricula: str, sobrenome: str, periodo: str, curso: str, filename: str) -> None:
    """
    Salvar nome e outras informações no JSON de nomes

    Parâmetros:
        face_id (int): O identificador do usuário.
        face_name (str): O nome do usuário.
        matricula (str): O número de matrícula do usuário.
        sobrenome (str): O sobrenome do usuário.
        periodo (str): O período/semestre do usuário.
        curso (str): O curso do usuário.
        filename (str): O nome do arquivo onde salvar as informações.
    """
    names_json = None
    if os.path.exists(filename):
        with open(filename, 'r') as fs:
            names_json = json.load(fs)
    if names_json is None:
        names_json = {}
    names_json[face_id] = {
        "name": face_name,
        "matricula": matricula,
        "sobrenome": sobrenome,
        "periodo": periodo,
        "curso": curso,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(filename, 'w') as fs:
        json_dump = json.dumps(names_json, ensure_ascii=False, indent=4)
        fs.write(json_dump)

def is_recently_registered(matricula: str, filename: str) -> bool:
    """
    Verificar se o usuário com a matrícula fornecida foi registrado na última semana.

    Parâmetros:
        matricula (str): O número de matrícula do usuário.
        filename (str): O nome do arquivo onde as informações estão salvas.

    Retorna:
        bool: True se o usuário foi registrado na última semana, False caso contrário.
    """
    if not os.path.exists(filename):
        return False

    with open(filename, 'r') as fs:
        names_json = json.load(fs)

    one_week_ago = datetime.now() - timedelta(weeks=1)
    for user_data in names_json.values():
        if user_data['matricula'] == matricula:
            registration_date = datetime.strptime(user_data['datetime'], "%Y-%m-%d %H:%M:%S")
            if registration_date > one_week_ago:
                return True
    return False

if __name__ == '__main__':
    directory = 'images'
    cascade_classifier_filename = 'haarcascade_frontalface_default.xml'
    names_json_filename = 'names.json'

    # Criar diretório 'images' se ele não existir
    create_directory(directory)
    
    # Carregar o classificador Haar cascade pré-treinado
    faceCascade = cv2.CascadeClassifier(cascade_classifier_filename)
    
    # Abrir uma conexão com a câmera padrão (índice da câmera 0)
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Erro ao abrir a câmera")
        exit()
    
    # Definir dimensões da câmera (é possivel aumentar/diminuir resolução para acelerar)
    cam.set(3, 640)  # Largura
    cam.set(4, 480)  # Altura
    
    # Inicializar variáveis de captura de rosto
    count = 0
    face_name = input('\nDigite o nome do usuário e pressione <enter> -->  ')
    sobrenome = input('\nDigite o sobrenome e pressione <enter> -->  ')
    matricula = input('\nDigite o número de matrícula e pressione <enter> -->  ')
    
    if is_recently_registered(matricula, names_json_filename):
        print('\n[INFO] Usuário já registrado na última semana. Saindo do programa.')
        exit()
    
    periodo = input('\nDigite o período/semestre e pressione <enter> -->  ')
    curso = input('\nDigite o curso e pressione <enter> -->  ')
    face_id = get_face_id(directory)
    save_name(face_id, face_name, matricula, sobrenome, periodo, curso, names_json_filename)
    print('\n[INFO] Inicializando captura de rosto. Olhe para a câmera e pressione "c" para capturar uma foto...')

    while True:
        # Ler um quadro da câmera
        ret, img = cam.read()
        if not ret:
            print("Falha ao capturar imagem")
            break
    
        # Converter o quadro para escala de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        # Detectar rostos no quadro (ajustar parâmetros para melhorar a velocidade)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
        # Processar cada rosto detectado
        for (x, y, w, h) in faces:
            # Desenhar um retângulo ao redor do rosto detectado
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
        # Exibir a imagem com retângulos ao redor dos rostos
        cv2.imshow('image', img)
    
        # Pressione 'c' para capturar a imagem
        k = cv2.waitKey(1) & 0xff
        if k == ord('c'):
            if len(faces) == 0:
                print("Nenhum rosto detectado. Tente novamente.")
                continue
            for (x, y, w, h) in faces:
                count += 1
                # Salvar a imagem capturada no diretório 'images'
                cv2.imwrite(f'./images/Users-{face_id}-{count}.jpg', gray[y:y+h, x:x+w])
                print(f"Imagem {count} capturada e salva com sucesso.")
            if count >= 30:
                break
        elif k == 27:  # Pressione 'ESC' para sair
            break
    
    print('\n[INFO] Sucesso! Saindo do programa.')
    
    # Liberar a câmera
    cam.release()
    
    # Fechar todas as janelas do OpenCV
    cv2.destroyAllWindows()
