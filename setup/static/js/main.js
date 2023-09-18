import sendPost from "./post_remove.js";
const imagemVideo = document.querySelectorAll('[data-imagem]')
// const divBlocoVideo = document.querySelectorAll('[data-bloco-video]')
const buttonConcluido = document.querySelectorAll('[data-button]')
const dia = document.getElementById('dia_semanal').textContent
const buttonXRemover = document.querySelectorAll('[data-button-remove]')
const buttonResetaMarcacao = document.querySelector('.resetbutton')

let intensVideoPlay = []
let intesXStorage = JSON.parse(localStorage.getItem(`Remover-${dia}`)) || []
let intensStorage = JSON.parse(localStorage.getItem(dia)) || [] 


intensStorage.forEach((id) => {
    divBlocoVideoContainer(id)
    buttonActive(id)
})


buttonResetaMarcacao.addEventListener('click',function removeLocalStorage(){
    localStorage.removeItem(dia)
    location.reload()
})


function divDomRemove(id){
    const blocoDom = document.querySelector(`[data-bloco-video="player${id}"]`)
    blocoDom.remove()
}

buttonXRemover.forEach((elemento) =>{
    elemento.addEventListener('click', (e) => {
        const valor = e.target.dataset.buttonRemove
        divDomRemove(valor)
        sendPost(valor)
        alert('Removendo!!')
        intesXStorage.push(valor)
        localStorage.setItem(`Remover-${dia}`,JSON.stringify(intesXStorage))
    })
})


function onYouTubeIframeAPIReady(id,url) {
    console.log('Iniciado')
    var player;
    player = new  YT.Player(`player${id}`,{
        width: '100%',
        height: '300px',
        videoId: url,
        playerVars:{
            'autoplay':1,
            'rel':0,
            'loop':1,
            'mute':1,
            'showinfo':0,
        },
        events:{
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    })
    intensVideoPlay.push(player)
}


function onPlayerReady(event) {
    //
}


function onPlayerStateChange(event) {
    // Eventos de mudança de estado do jogador (por exemplo, pausa, reprodução, etc.).
    
    if (event.data == YT.PlayerState.PLAYING ){
        const id = event.target.g.id
        divBlocoVideoRemover(id)
        buttonStorageRemove(id)
    }


    if (event.data == YT.PlayerState.PAUSED) {
        buttonActive(event.target.g.id)
    }
    if (event.data === YT.PlayerState.ENDED) {
        // O vídeo terminou, reinicie automaticamente
        const name = event.target.g.id
        videoPlay(name)
    }

}

function videoPlay(elemento) {
    let indice = intensVideoPlay.findIndex(function(dados){
        if (dados.g !== null)
            return dados.g.id == elemento//`player${elemento}`
    })
    const player = intensVideoPlay[indice]
    player.playVideo()
}


imagemVideo.forEach((e) => {
    e.addEventListener('click',()=>{
        const id = e.id
        const url = e.dataset.url
        onYouTubeIframeAPIReady(id,url)
        e.style.display = "none"
    })
})



function buttonActive (elemento){
    const buttonActive = document.querySelector(`[data-button="${elemento}"]`)
    buttonActive.style.display ="inline"
}

buttonConcluido.forEach((e) =>
    e.addEventListener('click',() => {
        const data_button = e.dataset.button
        if(e.classList.contains('borde__style_2px_dourado')){
            divBlocoVideoRemover(data_button)
        }else{
            divBlocoVideoContainer(data_button)
            buttonStorageAdd(data_button)
        }
    })
)

function divBlocoVideoContainer(data_button){
    const div = document.querySelector(`[data-bloco-video="${data_button}"]`);
    const button = document.querySelector(`[data-button="${data_button}"]`)
    
    const timeoutDivBloco = setTimeout(divBlocoVideoContainerEnd,1500,div,button);
    

    div.classList.add('caixas-ativa');

    button.textContent = "Resetar"
    button.style.width = "auto"
}


function divBlocoVideoContainerEnd(elemento,button){
    button.classList.add('borde__style_2px_dourado')
    
    elemento.classList.remove('caixas-ativa')
    elemento.classList.add('video__container__concluido_js')
    
    const ab  = elemento.childNodes[1].childNodes

    ab.forEach( (e)=>{
        if(e.classList){
            e.classList.add('color_dourado')
        }
        const node = e.childNodes
        node.forEach((esta)=>{
            if(esta.tagName == "UL" || esta.tagName == "BUTTON"){
                if(esta.tagName =="BUTTON"){
                    esta.classList.add("color_dourado")
                    esta.classList.add('borde__style_2px_dourado')
                }
                if(esta.tagName=="UL"){
                    esta.childNodes.forEach((eb)=>{
                    if(eb.classList){
                           if(eb.classList.contains("border__style_2px")){
                            eb.classList.add('borde__style_2px_dourado')
                    }}
                })
                }

            }
        })
    })
}



function divBlocoVideoRemover(elemento){
    const div = document.querySelector(`[data-bloco-video="${elemento}"]`)
    const button = document.querySelector(`[data-button="${elemento}"]`)
    divRemoverClasses(div,button)

    button.textContent = "Concluir"

    div.classList.remove('caixas-ativa')
    div.classList.remove('video__container__concluido_js')
}


function divRemoverClasses(elemento,button){
    button.classList.remove('borde__style_2px_dourado')

    const divremover  = elemento.childNodes[1].childNodes

    divremover.forEach((e)=>{
        if(e.classList){
            e.classList.remove('color_dourado')
        }
        const node = e.childNodes
        node.forEach((esta)=>{
            if(esta.tagName == "UL" || esta.tagName == "BUTTON"){
                if(esta.tagName =="BUTTON"){
                    esta.classList.remove("color_dourado")
                    esta.classList.remove('borde__style_2px_dourado')
                }
                if(esta.tagName=="UL"){
                    esta.childNodes.forEach((eb)=>{
                    if(eb.classList){
                           if(eb.classList.contains("border__style_2px")){
                            eb.classList.remove('borde__style_2px_dourado')
                    }}
                })
                }

            }
        })
    })
}

function buttonStorageAdd(id){
    const existe = intensStorage.find(elemento => elemento === id)

    if (!existe){
        intensStorage.push(id)
    }

    localStorage.setItem(dia,JSON.stringify(intensStorage))
}

function buttonStorageRemove(id){
    const indice = intensStorage.indexOf(id)

    if (indice !== -1 ){
        intensStorage.splice(indice, 1)
        localStorage.setItem(dia,JSON.stringify(intensStorage))
    }
}

