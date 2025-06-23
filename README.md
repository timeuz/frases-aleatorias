# 🎯 Gerador de Frases Aleatórias

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

*Uma API divertida e um frontend moderno para gerar frases aleatórias de diferentes categorias, agora com suporte a Inteligência Artificial e Redis para maior robustez\!*

[[ 🚀 Demo ]](https://frasesaleatorias.timeu.com.br/)

</div>

-----

## ✨ **Sobre o Projeto**

O **Gerador de Frases Aleatórias** é uma aplicação web que combina uma API Flask robusta com um frontend moderno e interativo. Oferece diversas categorias de frases e, agora, pode gerar frases dinamicamente usando Inteligência Artificial, persistindo-as em um banco de dados Redis para reuso.

### 🎭 **Categorias Disponíveis**

| Categoria | Endpoint | Descrição |
|-----------|----------|-----------|
| 🚫 **Não's Criativos** | `/naos` | Formas elegantes e divertidas de dizer "não" |
| 🔬 **Ciência & Fatos** | `/curiosidades` | Curiosidades científicas e fatos históricos |
| 🎮 **Citações Geek** | `/frases_geek` | Frases icônicas de filmes, séries e jogos |
| 😏 **Insultos Sutis** | `/insultis` | Críticas elegantes e sarcasmo refinado |
| 😔 **(des)Motivacionais** | `/desmotivacionais` | Frases para quando você precisa de um pouco de realidade |
| 🌞 **Bom dia pra quem?** | `/bomdia` | Frases para começar o dia bem... ou não |

-----

## 🚀 **Como Usar**

### Opção 1: Interface Web

1.  Acesse a página principal: `http://localhost:5000`
2.  Clique em qualquer um dos 6 botões temáticos
3.  Aproveite as frases aleatórias\! 🎉

### Opção 2: API Direta

```bash
# Exemplos de requisições
curl http://localhost:5000/naos
curl http://localhost:5000/curiosidades
curl http://localhost:5000/frases_geek
curl http://localhost:5000/insultis
curl http://localhost:5000/desmotivacionais
curl http://localhost:5000/bomdia
```

-----

## 📦 **Instalação com Docker Compose**

Esta aplicação utiliza Docker Compose para orquestrar dois contêineres: a aplicação Flask e um servidor Redis.

### **Pré-requisitos**

  - Docker Desktop (ou Docker Engine e Docker Compose CLI) instalado.

### **Passos de Instalação e Execução**

1.  **Clone o repositório**

    ```bash
    git clone https://github.com/timeuz/frases-aleatorias.git
    cd frases-aleatorias
    ```

2.  **Estruture os arquivos de dados**

    Certifique-se de que a estrutura de arquivos do projeto está correta. Os arquivos JSON com as frases devem estar no diretório `data/`.

    ```
    projeto/
    ├── app.py
    ├── compose-example.yml
    ├── Dockerfile
    ├── requirements.txt
    ├── LICENSE
    ├── README.md
    ├── templates/
    │   └── index.html
    ├── static/
    │   └── css
    |   |   └── styles.css
    │   └── images
    |   |   └── apple-touch-icon.png
    |   |   └── favicon-16x16.png
    |   |   └── favicon-32x32.png
    |   |   └── og-image.png
    │   └── js
    |       └── app.js
    └── data/
        ├── naos.json
        ├── curiosidades.json
        ├── frases_geek.json
        ├── insultis.json
        ├── desmotivacionais.json
        └── bomdia.json
    ```

3.  **Configure as variáveis de ambiente (IA)**

    Edite o arquivo `docker-compose.yml` e substitua `"SUA_VERDADEIRA_CHAVE_AQUI"` pela sua chave da API do Google Gemini. Você também pode ajustar `IA_ATIVADA` e `PERCENTUAL_IA`.

    ```yaml
    # Exemplo no docker-compose.yml
    services:
      web:
        environment:
          IA_ATIVADA: "True" # Define se a IA está ativa ("True" ou "False")
          PERCENTUAL_IA: "25" # Porcentagem de vezes que a IA será usada (0-100)
          GEMINI_API_KEY: "SUA_VERDADEIRA_CHAVE_AQUI" # Sua chave da API do Google Gemini
    ```

4.  **Suba os contêineres com Docker Compose**

    Este comando construirá a imagem da sua aplicação (`web`) e iniciará os contêineres `web` e `redis`.

    ```bash
    docker compose up --build -d
    ```

      * `--build`: Garante que a imagem da aplicação seja reconstruída. Use sempre após alterações no código ou no `Dockerfile`.
      * `-d`: Executa os contêineres em segundo plano.

5.  **Acesse no navegador**

    ```
    http://localhost:5000
    ```

6.  **Verifique os logs (para depuração)**

    Para ver a saída dos contêineres, incluindo erros e mensagens de depuração:

    ```bash
    docker compose logs -f web
    ```

    Para derrubar os contêineres e limpar os volumes (importante para um "reset" completo, pois remove os dados do Redis):

    ```bash
    docker compose down -v
    ```

-----

## 🤖 Inteligência Artificial

A aplicação agora integra Inteligência Artificial para gerar frases dinamicamente, complementando o banco de dados existente.

### **Uso e Configuração**

  * **API Suportada:** Atualmente, apenas a API **Google Gemini** é suportada para a geração de frases.
  * **Controle de Uso:** A utilização da IA é controlada por uma porcentagem definida por você. Se a IA estiver ativada e um número aleatório cair dentro da porcentagem configurada, a API do Gemini será chamada para gerar uma frase para aquela categoria.
  * **Persistência:** Frases geradas pela IA são automaticamente armazenadas no Redis para a categoria correspondente. Isso enriquece o banco de dados de frases da sua aplicação ao longo do tempo, reduzindo a necessidade de futuras chamadas à API da IA para frases já criadas.
  * **Configuração:** A IA é configurada através de **variáveis de ambiente** no seu `docker-compose.yml` (conforme o passo de instalação):
      * `IA_ATIVADA`: `True` ou `False` (ativa/desativa a funcionalidade de IA).
      * `PERCENTUAL_IA`: Um número inteiro de 0 a 100 (probabilidade de a IA ser chamada).
      * `GEMINI_API_KEY`: Sua chave de API do Google Gemini.
  * **Justificativa de Latência:** Para manter o usuário informado, uma pequena tag `(Gerado por IA)` será exibida no frontend ao lado da frase quando ela for gerada pela inteligência artificial. Isso justifica qualquer pequena demora na resposta, que é inerente a chamadas de API externas. A tag *não* é armazenada no Redis, apenas a frase bruta.

-----

## 🎨 **Frontend**

O frontend foi desenvolvido com foco na experiência do usuário, oferecendo:

### **🌟 Características Visuais**

  - **Design Glassmorphism**: Efeito de vidro fosco
  - **Partículas Flutuantes**: Elementos visuais que dão vida à interface
  - **Animações Suaves**: Transições elegantes em todos os elementos

### **📱 Funcionalidades**

  - ✅ **Responsivo**: Funciona perfeitamente em desktop e mobile
  - ✅ **Loading States**: Feedback visual durante o carregamento
  - ✅ **Tratamento de Erros**: Mensagens amigáveis para problemas
  - ✅ **Contador**: Acompanha quantas frases foram geradas
  - ✅ **Efeitos Hover**: Interações visuais nos botões

### **🎯 Botões Temáticos**

Cada categoria possui sua própria identidade visual

-----

## 📡 **Endpoints da API**

### **Rate Limiting**

Todos os endpoints possuem limitação de requisições para evitar abuso, utilizando Redis para consistência em ambientes conteinerizados:

  - **Limite Global**: 200/dia, 50/hora
  - **Limite por Endpoint**: 5/segundo, 10/minuto

### **Respostas**

As respostas da API são agora formatadas em JSON para incluir a frase e sua origem (existente ou IA).

| Endpoint | Método | Resposta de Sucesso (Exemplo) | Tipo |
|----------|--------|-------------------------------|------|
| `/naos` | GET | `{"frase": "Sua frase aqui.", "tipo": "existente"}` ou `{"frase": "Sua frase de IA aqui.", "tipo": "IA"}` | `application/json` |
| `/curiosidades` | GET | `{"frase": "Sua curiosidade aqui.", "tipo": "existente"}` ou `{"frase": "Sua curiosidade de IA aqui.", "tipo": "IA"}` | `application/json` |
| ... (outros endpoints seguem o mesmo padrão) | | | |

### **Códigos de Status**

  - `200`: Sucesso
  - `429`: Limite de requisições excedido
  - `500`: Erro interno (arquivo não encontrado, JSON inválido, erro de IA, etc.)

-----

## 🛠️ **Tecnologias Utilizadas**

### **Backend**

  - **Flask**: Framework web minimalista e flexível
  - **Flask-Limiter**: Controle de rate limiting com backend Redis
  - **Google Generative AI SDK**: Integração com a API Google Gemini
  - **Redis**: Banco de dados em memória para armazenamento de frases e contadores
  - **Python JSON**: Manipulação de dados estruturados

### **Frontend**

  - **HTML5**: Estrutura semântica moderna
  - **CSS3**: Animações, gradientes e efeitos visuais
  - **Vanilla JavaScript**: Funcionalidades interativas (sem dependências)
  - **Fetch API**: Requisições assíncronas para a API

### **Dados**

  - **JSON**: Formato para carregamento inicial das frases estáticas
  - **Redis**: Armazenamento principal das frases (estáticas e geradas por IA)
  - **UTF-8**: Suporte completo a caracteres especiais

### **Orquestração**

  - **Docker Compose**: Para definir e rodar a aplicação multi-contêiner

-----

## 🔧 **Personalização**

### **Adicionar Novas Frases (JSONs)**

1.  Edite os arquivos JSON em `/data/`.
2.  Mantenha a estrutura simplificada: **uma lista de strings**.
    ```json
    // Exemplo para qualquer arquivo JSON como naos.json, desmotivacionais.json, etc.
    [
      "Sua primeira nova frase aqui.",
      "Sua segunda nova frase aqui.",
      "Outra frase interessante."
    ]
    ```
3.  As frases serão carregadas para o Redis na primeira inicialização do contêiner `web` (ou se o volume do Redis for limpo). Frases geradas por IA serão automaticamente adicionadas ao Redis também.

### **Modificar Rate Limits**

Edite as configurações no `app.py`:

```python
limiter = Limiter(
    default_limits=["500 per day", "100 per hour"],  # Ajuste aqui
    # ...
)

@app.route('/endpoint')
@limiter.limit("10 per second;20 per minute")  # Ou aqui
```

### **Configurar a IA**

A configuração da IA é feita via variáveis de ambiente no `docker-compose.yml` (veja a seção "Instalação").

### **Personalizar Visual**

O CSS está separado no diretório `static/css` para facilitar modificações. Principais variáveis para customizar:

  - **Cores dos botões**: Classes `.btn-naos`, `.btn-curiosidades`, etc.
  - **Animações de fundo**: Keyframe `@backgroundShift`
  - **Efeitos**: Propriedades `backdrop-filter`, `box-shadow`
  - **Estilo da Tag de IA**: Classe `.ia-tag` para o aviso `(Gerado por IA)`.

-----

## 🤝 **Contribuindo**

Contribuições são sempre bem-vindas\! Para contribuir:

1.  **Fork** o projeto
2.  Crie uma **branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3.  **Commit** suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4.  **Push** para a branch (`git push origin feature/MinhaFeature`)
5.  Abra um **Pull Request**

### **Ideias para Contribuições**

  - 🎯 Novas categorias de frases e prompts de IA.
  - 🤖 Suporte a múltiplas IAs.
  - 🌍 Suporte a múltiplos idiomas.
  - 📊 Dashboard com estatísticas de uso (e.g., quantas frases de IA foram geradas vs. existentes).
  - 🔔 Sistema de favoritos.
  - 🎨 Novos temas visuais.
  - 📱 App mobile nativo.
  - 💾 Migração para um banco de dados relacional (ex: PostgreSQL) para gestão de frases mais complexa.

-----

## 📜 **Licença**

Este projeto está sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.

-----

## 🎉 **Sobre**

Este projeto foi criado como uma forma divertida de praticar desenvolvimento web full-stack, combinando uma API robusta com um frontend moderno e interativo.

A ideia surgiu da necessidade de ter respostas criativas e elegantes para diferentes situações do dia a dia, desde recusar convites até quebrar o gelo em conversas\!

### **Créditos e Inspiração**

Este projeto foi inspirado no repositório [no-as-a-service](https://github.com/hotheadhacker/no-as-a-service), criado por [hotheadhacker](https://github.com/hotheadhacker).

Foi reescrito completamente em Python, com frases já existentes traduzidas para o português e novas frases e elementos adicionados.

-----

<div align="center">

**⭐ Se você gostou do projeto, deixe uma estrela\! ⭐**

*Feito com 🤘 e muito ☕*

</div>