let phraseCounter = 0;
const API_BASE = window.location.origin; // Usa a mesma origem da página

async function getFrase(tipo) {
    const display = document.getElementById('phraseDisplay');
    const phraseText = display.querySelector('.phrase-text');
    const counter = document.getElementById('counter');
    phraseText.innerHTML = '<span class="loading">Carregando frase</span>';
    display.classList.add('show');
    const buttons = document.querySelectorAll('.phrase-button');
    buttons.forEach(btn => btn.style.pointerEvents = 'none');
    
    try {
        const endpoint = tipo === 'naos' ? 'naos' : 
                       tipo === 'desmotivacionais' ? 'desmotivacionais' : 
                       tipo === 'bomdia' ? 'bomdia' : tipo;
        const response = await fetch(`${API_BASE}/${endpoint}`);
        
        if (!response.ok) {
            throw new Error(`Erro ${response.status}: ${response.statusText}`);
        }
        
        const frase = await response.text();
        
        setTimeout(() => {
            phraseText.innerHTML = frase;
            phraseCounter++;
            counter.textContent = phraseCounter;
            
            buttons.forEach(btn => btn.style.pointerEvents = 'auto');
        }, 500);
        
    } catch (error) {
        console.error('Erro ao buscar frase:', error);
        phraseText.innerHTML = `<span class="error">Ops! Não foi possível carregar a frase. Tente novamente em alguns segundos. 😅</span>`;
        
        buttons.forEach(btn => btn.style.pointerEvents = 'auto');
    }
}

function createParticle() {
    const particle = document.createElement('div');
    particle.style.cssText = `
        position: fixed;
        width: 4px;
        height: 4px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        pointer-events: none;
        z-index: -1;
        left: ${Math.random() * 100}vw;
        top: ${Math.random() * 100}vh;
        animation: float ${3 + Math.random() * 4}s linear infinite;
    `;
    
    document.body.appendChild(particle);
    
    setTimeout(() => {
        particle.remove();
    }, 7000);
}

setInterval(createParticle, 500);

document.addEventListener('DOMContentLoaded', function() {
    if (!document.getElementById('particle-animation')) {
        const style = document.createElement('style');
        style.id = 'particle-animation';
        style.textContent = `
            @keyframes float {
                0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
});