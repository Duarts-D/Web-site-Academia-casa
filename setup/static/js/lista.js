const buttonLista = document.getElementById('input__lista')
const form = document.getElementById('formulario')
const ul = document.getElementById('lista2')
const inputName = document.getElementById('input__name')
const msgError = document.getElementById('error')
let buttonDeleteLista = document.querySelectorAll('.container__lista__2_button__X')

const menssagem = {
    name:{
        valueMissing: "O campo não pode estar vazio.",
        customError:"Atigiu o limite de lista",
    }
}

function removerError(){
    msgError.textContent = ''
}

function verificarCampo(input){
    const validadorDeInput = input.checkValidity()

    if (!validadorDeInput){// checando se e valido
        msgError.textContent = 'Atigiu o limite de lista,Apague uma lista';
        setTimeout(removerError,5000)
    } else {
        msgError.textContent = "";
    }
}


ul.addEventListener('click',(evento)=>{
    const input = document.getElementById('form')
    if (evento.target.id == 'input__lista' && quantidade()){
        formInputOn(input);
    }
    if (evento.target.id == 'input__lista' && !quantidade()){
        formInputOff(input)
        inputName.setCustomValidity('x')
        verificarCampo(inputName)
    }
})

function formInputOn(input){
    if(input.classList.contains('display__none')){
        input.classList.remove('display__none')
    }
    input.classList.add('display__flex')
}

function formInputOff(input){
    if(input.classList.contains('display__flex')){
        input.classList.remove('display__flex')
    }
    input.classList.add('display__none')
}



form.addEventListener('submit',(evento)=>{
    evento.preventDefault()
    const input = document.getElementById('form')
    const nome = evento.target.elements['name']
    var regex = /[^a-zA-Z0-9\s]/;
    msgError.textContent = ""
    const a = regex.test(nome.value) 
    if(!a){
        formInputOff(input)
        if(quantidade()){
            postNomeLista(nome)
            nome.value = ''
        }else{
            formInputOff(input)
        }
    }else{
        msgError.textContent = 'Não e permitido carateristicos especiais!'
    }
})

inputName.addEventListener('invalid',(evento) => {
    evento.preventDefault()})

async function postNomeLista(nome){
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const removeDiv = nome
    const condicional = nome.value || nome.target.id
    var dados = ''    
    if(nome.value){
        dados = {
            'nome' : condicional
        }
    }else{
        dados={
            'remove':condicional
        }
    }
    await fetch('http://127.0.0.1:8000/Listas/', {
    
    method: 'POST',
    headers: {
      'Content-Type': 'application/json', // Se você estiver enviando JSON
      'X-CSRFToken': csrfToken, // Envia o token CSRF no cabeçalho
    },
    body: JSON.stringify(dados), // Converte os dados em JSON e envia no corpo
  })
    .then(response => response.json())
    .then(data => {
        if(data.id){
            nomeListaInner(data.id,data.nome)
        }else{
            removeDiv.target.parentNode.remove()
        }
    })
    .catch(error => {
      console.error('Erro:', error);
    });
}

function nomeListaInner(id,nome){
    const novoli = document.createElement('li')
    const novoAc = document.createElement('a')
    const novoA = document.createElement('a')
    const novoButton = document.createElement('button')
    novoli.classList.add('container__lista__2__item')
    novoAc.classList.add('container__lista__2__texto')
    novoA.classList.add('container__lista__2_ancora')
    novoButton.classList.add('container__lista__2_button__X')

    novoA.textContent = 'Add'
    novoAc.textContent = nome
    novoAc.href=`/Treino-dia-${nome}/Geral`

    novoButton.textContent = 'X'
    novoA.href = `/Adicionar-Treino/${nome}-${nome}`

    novoButton.id = `${id}`
    novoButton.type = 'button'

    novoli.appendChild(novoAc)
    novoli.appendChild(novoA)
    novoli.appendChild(novoButton)
    ul.appendChild(novoli)
    buttonDeleteLista = document.querySelectorAll('.container__lista__2_button__X')
    buttonDeleteListaClick()
}


function quantidade(){
    if(ul.children.length < 13){
        return true
    }else{
        return false
    }
}

function buttonDeleteListaClick(){
    buttonDeleteLista.forEach((evento)=>{
        evento.addEventListener('click',(evento)=>{
            const numero = evento
            postNomeLista(numero)
        })
    })
}

buttonDeleteListaClick()