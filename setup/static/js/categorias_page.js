import viewPort from "./viewport.js"
import sendPostCriaTreino from "./postRemoveAdicionar.js"

const queryGeral = document.getElementById('ulVideos')
const queryCategoria = document.querySelectorAll('.categorias')
let dadosQuery =  [...queryGeral.children];
const buttonXRemover = document.querySelectorAll('[data-button-remove]')
let lastElement
let lista = document.querySelectorAll('input[type="checkbox"][name="videos"]')
export let listaAdicionar = []
export let listRemover = []
const buttonSalve = document.getElementById('teste_botton')
// var resultado = window.confirm("Pressione 'Sim' ou 'Não'");

if(buttonSalve){
    buttonSalve.addEventListener('click',(e)=>{
        e.preventDefault()
        sendPostCriaTreino(listaAdicionar,listRemover)
    })
}


lista.forEach((element)=>{
    element.addEventListener('change',()=>{
        const id = element.id
        
        if (element.checked){
            listaAdicionar.push(id)
            removeArrayRemove(id)
        }else{
            listRemover.push(id)
            removerArrayAdicionar(id)
        }
        console.log('Adicionar',listaAdicionar)
        console.log('Remover',listRemover)
    })
})

function removerArrayAdicionar(valor){
    const indice = listaAdicionar.findIndex(item => item === `${valor}`)
    if (indice !== -1){
        listaAdicionar.splice(indice,1)
    }
    console.log(listaAdicionar)
}

function removeArrayRemove(valor){
    const indice = listRemover.findIndex(item => item === `${valor}`)
    if (indice != -1){
        listRemover.splice(indice,1)
    }
}

buttonXRemover.forEach((elemento)=>{
    elemento.addEventListener('click',(e)=>{
        const numero = e.target.dataset.buttonRemove
        const num = dadosQuery.findIndex(elemento=> elemento.dataset.videoId == numero)
        dadosQuery.splice(num,1)
    })
})


queryCategoria.forEach((element) =>{
    element.addEventListener('click',(e)=>{
        e.preventDefault()
        const valor = e.target.text//valor
        if(valor){
            firstElementLastElement(e)
            if ( valor != 'Geral'){
                filtroCategoria(valor)
            }else{
                queryGeralAll()
            }
        }
        viewPort()
    })
});

function filtroCategoria(valor){
    const filtro = dadosQuery.filter(li=> li.dataset.categoriaTag == valor)
    queryGeral.innerHTML = ""
    if(filtro.length != 0){
        filtro.forEach((e)=>{
            queryGeral.appendChild(e)
        })
    }else{
        const li = document.createElement('li')
        li.classList.add('video__container')
        li.innerHTML = '<div  style="font-size: 3em; text-align: center; width: 100%;">Video Indiponivel !</div>'
        queryGeral.appendChild(li)
    }
}

function queryGeralAll(){
    queryGeral.innerHTML = ""
    if(dadosQuery.length != 0){
        dadosQuery.forEach((elemento)=>{
            queryGeral.appendChild(elemento)    
        })
    }else{
        const li = document.createElement('li')
        li.classList.add('video__container')
        li.innerHTML = '<div  style="font-size: 3em; text-align: center; width: 100%;">Lista Vazia !</div>'
        queryGeral.appendChild(li)
    }
}

function firstElementLastElement(valor){
    const buttonGeralAtivo = document.getElementById('Geral_ativo')
    buttonGeralAtivo.dataset.used = 'true'
    if(buttonGeralAtivo.classList.contains('categorias_ativa')){
       buttonGeralAtivo.classList.remove('categorias_ativa')
    }
    valor.target.classList.add('categorias_ativa')
    if (lastElement){
        if(lastElement.target.text != valor.target.text){
            lastElement.target.classList.remove('categorias_ativa') 
        }
    }
    lastElement = valor
}

