# backend/Dockerfile

# --- Stage 1: Build LaTeX documents ---
FROM ubuntu:latest as latex_builder

# Instalar TeX Live completo (pode levar tempo e espaço)
# Para um ambiente de produção, considere instalar apenas os pacotes TeX Live necessários
RUN apt-get update && \
    apt-get install -y texlive-full latexmk git curl wget make && \
    rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho para os arquivos LaTeX
WORKDIR /latex_project

# Copiar os arquivos LaTeX necessários para a compilação
# Ajuste este COPY para os seus arquivos .tex e .bib, etc.
# Exemplo: Se os arquivos LaTeX estiverem em 'back-end/src/report/latex_templates/'
COPY ./src/report/latex_templates/ .

# Compilar seus documentos LaTeX
# Este é um exemplo. Adapte para o seu script de compilação.
# Por exemplo, se você tem um script para compilar o relatório principal:
# COPY ./path/to/your/compile_latex_script.sh .
# RUN ./compile_latex_script.sh
# Ou, se você quer apenas compilar um main.tex:
# RUN latexmk -pdf main.tex
# Seus arquivos LaTeX podem estar em um subdiretório dentro de 'report'.
# Exemplo de como usar os arquivos 'main.tex', 'preambulo.tex', 'referencias.bib'
# e 'shared/relatorios/Exemplo/RelatorioExemplo'
# Você precisará ajustar os caminhos de cópia para seus arquivos LaTeX
# e garantir que o comando de compilação os encontre.

# Supondo que seus arquivos LaTeX para o relatório final estão em back-end/src/report/templates_latex/
# E seus dados (json, etc.) para os relatórios estão em 'shared/relatorios/Exemplo/' (via volume)
# O script de geração de relatório Python é o que realmente usa o LaTeX.
# O Dockerfile aqui só precisa garantir que o compilador LaTeX esteja disponível.

# Você só precisa do LaTeX neste estágio se for *compilar* PDFs dentro do Dockerfile.
# Se seu Flask app gera .tex e compila *em tempo de execução*, você precisa do TeX Live na imagem final.
# Se você *realmente* precisa que o MikTeX esteja na imagem final do Python, instale-o diretamente.

# Vamos assumir que você PRECISA do TeX Live na imagem final para compilar PDFs em tempo de execução com plasTeX/outras libs
# OU
# Se você *só* compila os PDFs durante o build do Docker, e depois só serve eles,
# então esta etapa é para compilação.
# Mas como você está usando plasTeX, que provavelmente é chamado pelo Flask,
# O TeX Live precisa estar no ambiente final.

# --- Stage 2: Build the Python application ---
FROM python:3.9-slim-buster

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Definir a variável de ambiente para o Flask encontrar a aplicação
ENV FLASK_APP=src/main.py

# Copiar o arquivo de requisitos e instalar as dependências
COPY requirements.txt .
# Adicione pacotes de sistema necessários para bibliotecas Python que dependam deles (como plasTeX)
# plasTeX pode precisar de pacotes de LaTeX ou utilitários para funcionar.
# Se plasTeX é uma biblioteca Python para interagir com LaTeX, ela pode precisar de um compilador LaTeX.
# TeX Live é a distribuição LaTeX para Linux.
RUN apt-get update && \
    apt-get install -y \
    build-essential \          
    python3-dev \              
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-extra \
    latexmk \
    dvipng \
    texlive-xetex \
    texlive-luatex \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação (Python)
COPY . .

# Expor a porta que sua aplicação Flask está ouvindo
EXPOSE 5000

# Comando para iniciar a aplicação Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]