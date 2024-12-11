# Sistema de Controle de Presença Acadêmica

Este projeto visa desenvolver um **sistema de controle de presença** para ambientes acadêmicos utilizando técnicas de **visão computacional** e **reconhecimento facial**. O objetivo é **automatizar e modernizar** o sistema tradicional de chamada, atualmente feito manualmente ou com lista de presença.

### Visão Geral

O sistema realiza a captura de imagens em tempo real através de câmeras estrategicamente posicionadas para identificar os alunos presentes e registrar suas presenças em um banco de dados. Esse processo visa ser **intuitivo e fácil de usar**, tanto para alunos quanto para professores, contribuindo para um ambiente de aprendizado mais moderno e eficiente.

### Tecnologias Utilizadas

- **Linguagem**: Python
  - **OpenCV**: Utilizado para processamento de imagens e detecção facial.
  - **NumPy**: Utilizado para manipulação de arrays.
  - **Pillow**: Utilizado para manipulação de imagens.
  - **Flask**: Utilizado para criar uma interface web simples.
- **Banco de Dados**: JSON para armazenar informações dos alunos.

### Funcionamento

1. **Captura de Imagens**: Utilizando a câmera, o sistema captura imagens dos alunos.
2. **Detecção Facial**: As faces são detectadas nas imagens capturadas utilizando um classificador Haar Cascade.
3. **Treinamento**: As imagens de rosto são utilizadas para treinar um modelo de reconhecimento facial (LBPH).
4. **Reconhecimento**: O modelo treinado é utilizado para reconhecer os alunos em tempo real.
5. **Registro de Presença**: As presenças são registradas e armazenadas em um arquivo JSON.
6. **Interface Web**: Uma interface web permite visualizar e exportar os dados de presença.

### Como Usar

1. **Instalar Dependências**:
Execute o script pip install -r requirements.txt no terminal para instalar as dependências
   
2. **Capturar Imagens de Treinamento**: 
Execute o script face_taker.py no terminal para capturar imagens de treinamento dos alunos.

3. **Treinar o Modelo**:
Treinar o Modelo: Execute o script face_train.py no terminal para treinar o modelo de reconhecimento facial.

4. **Iniciar o Sistema de Reconhecimento**: 
Execute o script face_recognizer.py no terminal para iniciar o sistema de reconhecimento facial e a interface web.

5. **Acessar a Interface Web**: 
Abra o navegador e acesse http://localhost:5000 para visualizar e exportar os dados de presença.