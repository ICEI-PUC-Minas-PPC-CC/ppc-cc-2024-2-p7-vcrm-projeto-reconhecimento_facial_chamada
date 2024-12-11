# Chamada de Presença Automatizada Utilizando Reconhecimento Facial e Visão Computacional

`PPC-CC: PUC Poços de Caldas - Ciência da Computação`
`Disciplina: Visão Computacional e Realidade Misturada`
`2024 - Semestre 2`

## Integrantes

- Lucca Pagin Barbosa Rios
- Nicole Carvalho Lisboa

## Professor

- Will Ricardo dos Santos Machado

## **1. Descrição Geral**
Este projeto tem como objetivo desenvolver um sistema de controle de presença automatizado para ambientes acadêmicos utilizando visão computacional e reconhecimento facial. Ele visa substituir métodos tradicionais como a chamada manual e listas de presença, promovendo eficiência, precisão e modernização.

O sistema fará uso de câmeras estrategicamente posicionadas para capturar imagens em tempo real, identificar alunos e registrar suas presenças em um banco de dados centralizado. Será projetado para ser intuitivo e acessível tanto para professores quanto para alunos, contribuindo para um ambiente de aprendizado mais tecnológico e prático.

---

## **2. Ferramentas Tecnológicas**

### **Linguagens e Bibliotecas**
- **Python**: Escolhida por sua robustez em bibliotecas de visão computacional e aprendizado de máquina.
- **OpenCV**: Para captura e pré-processamento de imagens, detecção facial e manipulação de dados visuais.
- **Face Recognition**: Para geração e comparação de embeddings faciais com alta precisão.
- **Flask**: Framework para a construção de uma interface web simples para visualização e gerenciamento de presenças.

---

## **3. Requisitos de Instalação**
Para instalar as dependências necessárias, execute o seguinte comando:

```bash
pip install pillow opencv-python opencv-contrib-python flask
```

---

## **4. Ordem de Execução**
1. **`face_taker.py`**: Rode este script para capturar as fotos. Aperte **`c`** para tirar as fotos.
2. **`face_train.py`**: Execute este script para treinar o modelo com as fotos capturadas.
3. **`face_recognizer.py`**: Inicie este script para realizar o reconhecimento facial.

Ao rodar o último script, um link será exibido no terminal. Clique nele para acessar a interface do sistema.

---
## **5. Detalhes de Funcionamento**

### **Aquisição de Dados**
- As imagens são capturadas manualmente por meio do script **`face_taker.py`**.
- O usuário deve pressionar a tecla **`c`** para registrar cada imagem.

### **Registro de Presenças**
- Durante o reconhecimento, o sistema registra os dados no formato **`.log`**, incluindo a data e hora exatas (formato `dd:mm:yyyy hh:mm:ss`).
- Caso uma pessoa seja reconhecida dentro de um intervalo de tempo predefinido, sua presença não será registrada novamente, evitando duplicatas.

### **Prevenção de Duplicatas**
- O sistema verifica se a mesma pessoa foi reconhecida em um curto intervalo de tempo. Se sim, o registro é ignorado para evitar redundâncias no banco de dados.

### **Armazenamento em JSON**
- As informações dos alunos, como número de matrícula, nome completo, período, semestre e ID do curso, são armazenadas em um arquivo JSON para acesso estruturado e reutilização futura.

### **Exportação para CSV**
- Os registros de presença são organizados por data e exportados automaticamente para arquivos **CSV** no formato `dd-mm-yyyy.csv`. Isso facilita a análise e o compartilhamento dos dados.
