export default  async function sendPostCriaTreino(listPostAdd,ListPostRemv){
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const dia = document.getElementById('dia_semanal').textContent
    const dados = {
      'postAdicionar': listPostAdd,
      'postRemove':ListPostRemv,
      'dia':dia,
    };
    await fetch(`https://academiascasa.com/Adicionar-Treino/${dia}-${dia}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Se você estiver enviando JSON
        'X-CSRFToken': csrfToken, // Envia o token CSRF no cabeçalho
      },
      body: JSON.stringify(dados), // Converte os dados em JSON e envia no corpo
    })
      .then(response => response.json())
      .then(data => {
        console.log(data)
        if (data){
          window.location.href=`../Treino-dia-${dia}/Geral`
        }
      })
      .catch(error => {
        console.error('Erro:', error);
      });
  }
  