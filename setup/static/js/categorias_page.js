import viewPort from "./viewport.js"
import sendPostCriaTreino from "./postRemoveAdicionar.js"

const queryGeral = document.getElementById('ulVideos')
const queryCategoria = document.querySelectorAll('#categorias')
let dadosQuery =  [...queryGeral.children];
const buttonXRemover = document.querySelectorAll('[data-button-remove]')
let lastElement
let lista = document.querySelectorAll('input[type="checkbox"][name="videos"]')
export let listaAdicionar = []
export let listRemover = []
const buttonSalve = document.getElementById('teste_botton')
// var resultado = window.confirm("Pressione 'Sim' ou 'Não'");
let itensOptionSelect = document.querySelectorAll('#option input')
const selectEquipamento = document.getElementById('checkbox')
let buttonCheck = document.getElementById('checkequipamento')

function alternacaSetaAcima(){
    const buttonSelect = document.querySelector('.position_equipamento')
    if (buttonSelect.classList.contains('position_equipamento_open')){
        buttonSelect.classList.remove('position_equipamento_open')
    }else{
        buttonSelect.classList.add('position_equipamento_open')
    }
}

buttonCheck.addEventListener('change',(e)=>{
    alternacaSetaAcima()
})

if (itensOptionSelect.length == 1){
    criandoItensOptionsSelect()
    itensOptionSelect = document.querySelectorAll('#option input')
}



function criandoItensOptionsSelect(){
    const itens = document.querySelectorAll('[data-categoria-equipamento]')
    let listaItens = []
    itens.forEach((e)=>{
        const valor = e.dataset.categoriaEquipamento
        if(valor != 'None' && !listaItens.includes(valor)){
            listaItens.push(valor)
        }
    })
    listaItens.forEach(e=>{
        criarElementoOption(e)
    })
}

function criarElementoOption(valor){
    const li = document.createElement('li')
    li.classList = 'categorias_equipamento_item'
    li.id = 'option'
    li.innerHTML =`<input type="radio" name="${valor}" value="${valor}">
    <span>${valor}</span>`
    const elementoDom = document.querySelector('.categorias_equipamento')
    elementoDom.appendChild(li)
}

export default function removendoElementOption(){
    const listaElement = document.querySelector('.categorias_equipamento')
    const itensRemoviveis = Array.from(listaElement.children).slice(1)
    itensRemoviveis.forEach(e=>{
        e.remove()
    })
    criandoItensOptionsSelect()
}

function categoriaAtiva(){
    const categoria = document.querySelectorAll('#categorias a')
    let valor 
    categoria.forEach((e)=>{
        if(e.classList.contains('categorias_ativa')){
            valor = e.textContent
            }
        })
    return valor
}

itensOptionSelect.forEach((input) => {
    input.addEventListener('click', (e) => {
        const valor = input.value
        const bloco = document.querySelector('.position_equipamento')
        const categoriaAtv = categoriaAtiva()

        selectEquipamento.textContent = valor

        if (buttonCheck.checked){
            buttonCheck.checked = false
            alternacaSetaAcima()
        }
        if (valor !== 'Equipamento'){
            
            if (categoriaAtv !== 'Geral'){
                filtroCategoria(categoriaAtv,valor)
            }else{
                filtroCategoria(valor)
            }
            bloco.style.boxShadow = '0px 0px 5px white'
        
        }else{
            if (categoriaAtv === 'Geral'){
                queryGeralAll()
            }else{
                filtroCategoria(categoriaAtv)
            }
            bloco.style.boxShadow = 'none'
        }
        viewPort()
    })
})



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
    })
})

function removerArrayAdicionar(valor){
    const indice = listaAdicionar.findIndex(item => item === `${valor}`)
    if (indice !== -1){
        listaAdicionar.splice(indice,1)
    }
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
        const id = e.target.id
        if (id === 'checkbox'){
            return e
        }else{
            const valor = e.target.text//valor
            e.preventDefault()
            if(valor){
                firstElementLastElement(e)
                if ( valor != 'Geral'){
                    if (selectEquipamento.textContent !== 'Equipamento'){
                        filtroCategoria(valor,selectEquipamento.textContent)
                    }else{
                        filtroCategoria(valor)
                    }
                }else{
                    if (selectEquipamento.textContent !== 'Equipamento'){
                        filtroCategoria(selectEquipamento.textContent)
                    }else{
                        queryGeralAll()
                    }
                }
            }
        }

        viewPort()
    })
});

function filtroCategoria(valor,filtro_2){
    let filtro = dadosQuery.filter(li=> li.dataset.categoriaTag == valor || li.dataset.categoriaEquipamento == valor)
    if (filtro_2){
        filtro = filtro.filter(li => li.dataset.categoriaEquipamento == filtro_2)
    }
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

