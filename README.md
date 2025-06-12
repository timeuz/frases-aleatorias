# 🎯 Gerador de Frases Aleatórias

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

*Uma API divertida e um frontend moderno para gerar frases aleatórias de diferentes categorias*

[🚀 Demo](#-como-usar) • [📁 Instalação](#-instalação) • [🎨 Frontend](#-frontend) • [📡 API](#-endpoints-da-api)

</div>

---

## ✨ **Sobre o Projeto**

O **Gerador de Frases Aleatórias** é uma aplicação web que combina uma API Flask robusta com um frontend moderno e interativo. Oferece quatro categorias distintas de frases para diferentes ocasiões e humores!

### 🎭 **Categorias Disponíveis**

| Categoria | Endpoint | Descrição | Exemplo |
|-----------|----------|-----------|---------|
| 🚫 **Não's Criativos** | `/naos` | Formas elegantes e divertidas de dizer "não" | *"Meu comitê de paz interior vetou essa ideia por unanimidade."* |
| 🔬 **Ciência & Fatos** | `/curiosidades` | Curiosidades científicas e fatos históricos | *"Um raio é cinco vezes mais quente que a superfície do sol."* |
| 🎮 **Citações Geek** | `/frases_geek` | Frases icônicas de filmes, séries e jogos | *"Que a Força esteja com você." - Obi-Wan Kenobi (Star Wars)* |
| 😏 **Insultos Sutis** | `/insultis` | Críticas elegantes e sarcasmo refinado | *"Admiro a sua coragem em ser tão... autêntico."* |
| 😔 **(des)Motivacionais** | `/desmotivacionais` | Frases para quando você precisa de um pouco de realidade | *"Dê o seu melhor — e descubra que nem isso adianta."* |
| 🌞 **Bom dia pra quem?** | `/bomdia` | Frases para começar o dia bem... ou não | *"Bom dia para você que acordou pronto para nada."* |

---

## 🚀 **Como Usar**

### Opção 1: Interface Web (Recomendado)
1. Acesse a página principal: `http://localhost:5000`
2. Clique em qualquer um dos 4 botões temáticos
3. Aproveite as frases aleatórias! 🎉

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

---

## 📦 **Instalação**

### **Pré-requisitos**
- Python 3.8+
- pip (gerenciador de pacotes Python)

### **Passos de Instalação**

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/gerador-frases-aleatorias.git
   cd gerador-frases-aleatorias
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Estruture os arquivos de dados**
   ```
   projeto/
   ├── app.py
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
       └── insultis.json
       └── desmotivacionais.json
       └── bomdia.json
   ```

5. **Execute a aplicação**
   ```bash
   python app.py
   ```

6. **Acesse no navegador**
   ```
   http://localhost:5000
   ```

---

## 🎨 **Frontend**

O frontend foi desenvolvido com foco na experiência do usuário, oferecendo:

### **🌟 Características Visuais**
- **Design Glassmorphism**: Efeito de vidro fosco moderno
- **Gradientes Animados**: Fundo que muda de cor suavemente
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

---

## 📡 **Endpoints da API**

### **Rate Limiting**
Todos os endpoints possuem limitação de requisições para evitar abuso:
- **Limite Global**: 200/dia, 50/hora
- **Limite por Endpoint**: 5/segundo, 10/minuto

### **Respostas**

| Endpoint | Método | Resposta | Tipo |
|----------|--------|----------|------|
| `/naos` | GET | Frase de recusa criativa | `text/plain` |
| `/curiosidades` | GET | Curiosidade científica | `text/plain` |
| `/frases_geek` | GET | Citação formatada com autor e fonte | `text/plain` |
| `/insultis` | GET | Insulto sutil ou sarcástico | `text/plain` |
| `/desmotivacionais` | GET | Motivadas ao fracasso | `text/plain` |
| `/bomdia` | GET | Para quem não acorda feliz | `text/plain` |

### **Códigos de Status**
- `200`: Sucesso
- `429`: Limite de requisições excedido
- `500`: Erro interno (arquivo não encontrado, JSON inválido, etc.)

---

## 🛠️ **Tecnologias Utilizadas**

### **Backend**
- **Flask**: Framework web minimalista e flexível
- **Flask-Limiter**: Controle de rate limiting
- **Python JSON**: Manipulação de dados estruturados

### **Frontend**
- **HTML5**: Estrutura semântica moderna
- **CSS3**: Animações, gradientes e efeitos visuais
- **Vanilla JavaScript**: Funcionalidades interativas (sem dependências)
- **Fetch API**: Requisições assíncronas para a API

### **Dados**
- **JSON**: Armazenamento estruturado das frases
- **UTF-8**: Suporte completo a caracteres especiais

---

## 🔧 **Personalização**

### **Adicionar Novas Frases**
1. Edite os arquivos JSON em `/data/`
2. Mantenha a estrutura existente:
   ```json
   // Para naos.json, desmotivacionais.json e bomdia.json
   ["Sua nova frase aqui"]
   
   // Para science_facts.json
   [{"fact": "Seu fato científico aqui"}]
   
   // Para geek_quotes.json
   [{"quote": "Citação", "character": "Personagem", "source": "Fonte"}]
   
   // Para insultis.json
   [{"insult": "Seu insulto sutil aqui"}]
   ```

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

### **Personalizar Visual**
O CSS está separado no diretório `static/css` para facilitar modificações. Principais variáveis para customizar:
- **Cores dos botões**: Classes `.btn-naos`, `.btn-curiosidades`, etc.
- **Animações de fundo**: Keyframe `@backgroundShift`
- **Efeitos**: Propriedades `backdrop-filter`, `box-shadow`

---

## 🤝 **Contribuindo**

Contribuições são sempre bem-vindas! Para contribuir:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. **Push** para a branch (`git push origin feature/MinhaFeature`)
5. Abra um **Pull Request**

### **Ideias para Contribuições**
- 🎯 Novas categorias de frases
- 🌍 Suporte a múltiplos idiomas
- 📊 Dashboard com estatísticas de uso
- 🔔 Sistema de favoritos
- 🎨 Novos temas visuais
- 📱 App mobile nativo

---

## 📜 **Licença**

Este projeto está sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🎉 **Sobre**

Este projeto foi criado como uma forma divertida de praticar desenvolvimento web full-stack, combinando uma API robusta com um frontend moderno e interativo. 

A ideia surgiu da necessidade de ter respostas criativas e elegantes para diferentes situações do dia a dia, desde recusar convites até quebrar o gelo em conversas!

### **Créditos e Inspiração**

Este projeto foi inspirado no repositório [no-as-a-service](https://github.com/hotheadhacker/no-as-a-service), criado por [hotheadhacker](https://github.com/hotheadhacker).

Foi reescrito completamente em Python, com frases traduzidas para o português e novos elementos adicionados.


---

<div align="center">

**⭐ Se você gostou do projeto, deixe uma estrela! ⭐**

*Feito com 🤘 e muito ☕*

</div>
