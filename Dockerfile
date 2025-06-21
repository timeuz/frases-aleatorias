# Usa uma imagem oficial do Python como base
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências, incluindo o Gunicorn
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta 5000 que a aplicação vai escutar
EXPOSE 5000

# Comando para iniciar a aplicação com Gunicorn
# Isso assume que seu arquivo Flask principal é 'app.py' e o objeto Flask é 'app'
# Ajuste 'app:app' se o nome do seu arquivo ou do seu objeto Flask for diferente
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
