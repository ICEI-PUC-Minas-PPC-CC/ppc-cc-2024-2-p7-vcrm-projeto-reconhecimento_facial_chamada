import cv2
import numpy as np
from PIL import Image
import os


if __name__ == "__main__":
    
    # Caminho do diretório onde as imagens de rosto estão armazenadas.
    path = './images/'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    print("\n[INFO] Treinando...")
    # Arquivo Haar cascade para detecção de rosto
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    
    def getImagesAndLabels(path):
        """
        Carregar imagens de rosto e rótulos correspondentes do diretório fornecido.
    
        Parâmetros:
            path (str): Caminho do diretório contendo imagens de rosto.
    
        Retorna:
            list: Lista de amostras de rosto.
            list: Lista de rótulos correspondentes.
        """
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []
    
        for imagePath in imagePaths:
            # Converter imagem para escala de cinza
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')
            
            # Extrair o ID do usuário do nome do arquivo de imagem
            id = int(os.path.split(imagePath)[-1].split("-")[1])
            print(f"[DEBUG] Processando imagem: {imagePath}, ID: {id}")
    
            # Detectar rostos na imagem em escala de cinza
            faces = detector.detectMultiScale(img_numpy)
    
            for (x, y, w, h) in faces:
                # Extrair região do rosto e adicionar às amostras
                faceSamples.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)
    
        return faceSamples, ids
    
    faces, ids = getImagesAndLabels(path)
    
    if len(faces) == 0 or len(ids) == 0:
        print("\n[ERROR] Nenhuma imagem de rosto encontrada para treinamento.")
        exit()
    
    # Treinar o reconhecedor com as amostras de rosto e rótulos correspondentes
    recognizer.train(faces, np.array(ids))
    
    # Salvar o modelo treinado no diretório atual
    recognizer.write('trainer.yml')
    
    if not os.path.exists('trainer.yml'):
        print("\n[ERROR] Falha ao salvar o modelo treinado.")
        exit()
    
    print("\n[INFO] {0} rostos treinados. Saindo do programa".format(len(np.unique(ids))))
