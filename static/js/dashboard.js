function mostrarSecao(secaoId) {
  const secoes = document.querySelectorAll('.secao');
  secoes.forEach(secao => {
    secao.classList.remove('ativa');
  });
  const secaoSelecionada = document.getElementById(secaoId);
  if (secaoSelecionada) {
    secaoSelecionada.classList.add('ativa');
  }
}

// ENTRADA
document.getElementById('formEntrada')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const valor = e.target.valor_entrada.value;
  const resposta = await fetch('/entrada', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ valor })
  });
  const json = await resposta.json();
  alert(json.mensagem || 'Entrada enviada!');
});

// STOP
document.getElementById('formStop')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const valor = e.target.valor_stop.value;
  const resposta = await fetch('/stop', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ valor })
  });
  const json = await resposta.json();
  alert(json.mensagem || 'Stop configurado!');
});

// ALVO
document.getElementById('formAlvo')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const valor = e.target.valor_alvo.value;
  const resposta = await fetch('/alvo', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ valor })
  });
  const json = await resposta.json();
  alert(json.mensagem || 'Alvo configurado!');
});

// CONFIGURAR CHAVES
document.getElementById('formChaves')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const binance_key = e.target.binance_key.value;
  const binance_secret = e.target.binance_secret.value;
  const openai_key = e.target.openai_key.value;
  const resposta = await fetch('/salvar_chaves', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ binance_key, binance_secret, openai_key })
  });
  const json = await resposta.json();
  alert(json.mensagem || 'Chaves salvas!');
});

// MODO AUTOMÁTICO
async function ativarModoAuto() {
  const confirmar = confirm("Tem certeza que deseja ativar o modo automático?");
  if (!confirmar) return;
  const resposta = await fetch('/automatico', { method: 'POST' });
  const json = await resposta.json();
  alert(json.mensagem || 'Modo automático ativado!');
}