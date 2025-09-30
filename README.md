# :email: Classificador de e-mails

Aplicação desenvolvida a partir do case prático proposto no processo seletivo da empresa [AutoU](https://www.autou.io/)

O case prático consistia em criar um aplicativo que pudesse Classificar e-mails em diferentes categorias baseado em seu conteúdo e gerar possíveis respostas para eles, facilitando em muito o trabalho dentro de empresas

A descrição completa do desafio pode ser encontrada [aqui](https://autou-digital.notion.site/Case-Pr-tico-AutoU-Desenvolvimento-18836ce78e5580d0b59bcf9610b27769) e o aplicativo desenvolvido pode ser acessado por meio do  [link](https://classificador-de-emails.up.railway.app/)

## Menu
- [Propósito](#email-classificador-de-e-mails)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Elaboração](#elaboração)
- [Utilização](#utilização)
  -[Usando o serviço no Railway](#usando-o-serviço-no-railway)
  -[Hospedando localmente](#hospedando-localmente)
  -[Uso da interface de usuário](#uso-da-interface-de-usuário)

## Tecnologias utilizadas

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Google Gemini](https://img.shields.io/badge/google%20gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

## Elaboração

A ideia geral utilizada na elaboração da solução desse case prático foi tornar o aplicativo simples, rápido e que pudesse ser facilmente modificado por qualquer pessoa, até por alguma sem conhecimento prévio de programação.

O programa consiste em um frontend que recebe um ou múltiplos arquivos .PDF ou .txt com e-mails e possíveis comentários adicionais que o usuário queira adicionar (Por exemplo alguma palavra chave que faça o e-mail ser considerado importante) e após o envio o backend em Python, utilizando-se do framework Flask, ele processa esses arquivos como uma string e envia ele, conjuntamente aos comentários do usuário para o Gemini, por meio da API do mesmo.

O prompt do Gemini possui diversos critérios de avaliação em que ele utilizará para categorizar o e-mail, o que torna muito fácil para um usuário não especialista alterar o mesmo, tornando ele intuitivo e prático para o uso geral.

Contudo, a parte mais importante do programa, que é a parte que torna ele muito mais eficiente e amigável é o fato de o prompt exigid para a Gemini ser necessariamente uma string no formato JSON. O programa em Python transforma essa string em uma estrutura em JSON e após isso, ele envia para o Javascript, que por ter recebido um JSON ele consegue interpretar de forma muito mais fácil e fazendo com que consigamos separar cada e-mail individulamente, podendo alterar futuramente como quiser o resultado apresentado ao usuário.

## Utilização

O programa pode ser utilizado tanto de forma online como na prórpia máquina do usuário, ambas as formas serão apresentadas.

### Usando o serviço no Railway

Para acessar ao programa hospedado por meio do Railway basta ter acesso a um navegador e acessar ao [link](https://classificador-de-emails.up.railway.app/)

### Hospedando localmente

Para acessar em sua máquina primeiro deve-se clonar o repositório em um local a escolha em seu computador e, no terminal digitar

```bash
git clone https://github.com/arthurhdr/classificador-de-emails
```

Na pasta criada baixar os requerimentos necessários

```bash
pip install -r requirements.txt
```

E então inicie o servidor de desenvolvimento

```bash
flask run
```

Após isso, se acessa o link fornecido pelo Flask

### Uso da interface de usuário

Para utilizar o aplicativo basta anexar todos os arquivos que devem ser lidos para análise do programa, colocar os comentários adicionais (se necessários) e pedir a análise, após alguns segundos o programa retornará como a análise completa indicando os e-mails importantes e não-importantes dos arquivos. 