import { listaAdicionar,listRemover } from "./categorias_page.js"
import sendPostCriaTreino from "./postRemoveAdicionar.js"

const ancoras = document.querySelectorAll('a')
const buttonCotainerAlert = document.querySelector('.container_buttao_alert')
const button_alert = document.querySelectorAll('.button_alert')

ancoras.forEach((element)=>{
    element.addEventListener('click',(e)=>{
        e.preventDefault()
        ancoraFormSave(element)
    }
    )   
})

buttonCotainerAlert.addEventListener('mouseenter',(e)=>{
    e.target.style.animationIterationCount = '1'
    e.target.style.animationPlayState = 'paused'
})

buttonCotainerAlert.addEventListener('mouseleave',(e)=>{
    e.target.style.animationIterationCount = 'infinite'
    e.target.style.animationPlayState = 'running'
})

function ancoraFormSave(element){
    const url = element.getAttribute('href')
    const data = element.dataset.categoria
    if(!data){
        if(listaAdicionar.length >= 1 || listRemover.length >=1){
            buttonCotainerAlert.style.display = 'block'
            button_alert.forEach((element)=>{
                element.addEventListener('click',()=>{
                    const resultado = element.value
                    if(resultado === 'Sim'){
                        sendPostCriaTreino(listaAdicionar,listRemover)
                        window.location.href= url
                    }else{
                        window.location.href= url
                    }
                })
            })
        }else{
        window.location.href= url
        }
    }
}