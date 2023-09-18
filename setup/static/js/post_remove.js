export default  async function sendPost(id){
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  const dia = document.getElementById('dia_semanal').textContent
  const dados = {
    'id': id,
    'dia':dia,
  };
  
  await fetch('http://127.0.0.1:8000/Treino-dia-Segunda/Geral', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json', // Se você estiver enviando JSON
      'X-CSRFToken': csrfToken, // Envia o token CSRF no cabeçalho
    },
    body: JSON.stringify(dados), // Converte os dados em JSON e envia no corpo
  })
    .then(response => response.json())
    .then(data => {
      //
    })
    .catch(error => {
      console.error('Erro:', error);
    });
}