import sendPost from "./post_remove.js";
import viewPort from "./viewport.js"

const imagemVideo = document.querySelectorAll('[data-imagem]')
// const divBlocoVideo = document.querySelectorAll('[data-bloco-video]')
const buttonConcluido = document.querySelectorAll('[data-button]')
const dia = document.getElementById('dia_semanal').textContent
const buttonXRemover = document.querySelectorAll('[data-button-remove]')
const buttonResetaMarcacao = document.querySelector('.resetbutton')

let intensVideoPlay = []
let intesXStorage = JSON.parse(localStorage.getItem(`Remover-${dia}`)) || []
let intensStorage = JSON.parse(localStorage.getItem(dia)) || [] 


window.addEventListener('load', function() {
viewPort()
});

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
    buttonStorageRemove(`player${id}`)
    viewPort()
    blocoDom.remove()
    const ulVideos  = document.querySelector('#ulVideos')
    if (ulVideos.children.length == 0){
        const li = document.createElement('li')
        li.classList.add('video__container')
        li.innerHTML = '<div  style="font-size: 3em; text-align: center; width: 100%;">Lista Vazia !</div>'
        ulVideos.appendChild(li)
    }
}
function removerOrdemLista(id){
    const elements =  document.querySelector(`[data-organizacao-id="${id}"]`)
    elements.remove()
}


buttonXRemover.forEach((elemento) =>{
    elemento.addEventListener('click', (e) => {
        const valor = e.target.dataset.buttonRemove
        const div1 = e.target.parentNode
        const div2 = div1.parentNode
        div2.parentNode.classList.add('ativar')
        const timenow = setTimeout(divDomRemove,3000,valor)
        sendPost(valor)
        removerOrdemLista(valor)
        // intesXStorage.push(valor)
        localStorage.setItem(`Remover-${dia}`,JSON.stringify(intesXStorage))
    });
    elemento.addEventListener('mouseover',(e)=>{
        e.target.textContent = 'Remover';
    })
    elemento.addEventListener('mouseout',(e)=>{
        e.target.textContent = 'X'
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
    const buttonAncoraGeral = document.getElementById('Geral_ativo')
    if(!buttonAncoraGeral.classList.contains('categorias_ativa') || buttonAncoraGeral.dataset.used){
        event.target.stopVideo()
    }
}


function onPlayerStateChange(event) {
    // Eventos de mudança de estado do jogador (por exemplo, pausa, reprodução, etc.).
    
    if (event.data == YT.PlayerState.PLAYING ){
        let id = event.target.g.id
        id = idVerificarString(id)
        divBlocoVideoRemover(id)
        buttonStorageRemove(id)
    }


    if (event.data == YT.PlayerState.PAUSED) {
        let id = event.target.g.id
        id = idVerificarString(id)
        buttonActive(id)
    }
    if (event.data === YT.PlayerState.ENDED) {
        // O vídeo terminou, reinicie automaticamente
        const name = event.target.g.id
        videoPlay(name)
    }

}

function constPlayer(id){
    let indice = intensVideoPlay.findIndex(function(dados){
        if (dados.g !== null)
            return dados.g.id == id//`player${elemento}`
    })
    const player = intensVideoPlay[indice]
    return player
}

function videoPlay(id) {
    const player = constPlayer(id)
    player.playVideo()
}

function videoPause(id){
    const player = constPlayer(id)
    player.pauseVideo()
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
            buttonStorageRemove(data_button)
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
    if(button.classList.contains('borde__style_2px_dourado')){
        button.classList.remove('borde__style_2px_dourado')
    }

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

const button = document.querySelectorAll('#button-alterna_video')
button.forEach((elemento)=>{
    elemento.addEventListener('click',(e)=>{
        const id = e.target.dataset.idFull
        const img = document.getElementById(id)
        img.classList.add('animation_img')
        setTimeout(video_animation,2000,e,img)
    })
}
)

function video_animation(elemento,img){
    const ativo = elemento.target.dataset.ativo
    const id = elemento.target.dataset.idFull
    const video_1 = document.getElementById(`player${id}`)
    const video_2 = document.getElementById(`player${id}/`)
    let url_full = elemento.target.dataset.urlFull
    if(ativo){
        elemento.target.removeAttribute('data-ativo')
        videoAnimatioTwooff(video_2,id)
        setTimeout(videoAnimationOneOn,3200,video_1,id)
    }else{
        elemento.target.dataset.ativo = 'true'
        if(video_1.tagName == 'IFRAME'){
            videoAnimatioOneoff(video_1,id)
            setTimeout(videoAnimationTwoOn,3000,video_2,url_full,id)
        }else{
            setTimeout(videoAnimationTwoOn,1000,video_2,url_full,id)
        }

    }
    animationSeta(elemento.target,ativo)

    setTimeout(animationImagem,2000,img)
}

function animationImagem(img){
    img.style.display = 'none'
    img.classList.remove('animation_img')
}


function videoAnimationTwoOn(videoSimple,url,id){
    styleRemove(videoSimple)
    videoSimple.style.display = 'block'
    videoSimple.parentNode.style.transform = 'rotateY(90deg)'
    videoSimple.parentNode.classList.add('animation__video')
    onYouTubeIframeAPIReady(`${id}/`,url)
    setTimeout(videoPlay,1500,`player${id}/`)

}

function videoAnimatioTwooff(videoSimple,id){
    videoSimple.parentNode.style.transform = 'rotateY(0)'
    videoSimple.parentNode.classList.remove('animation__video')
    videoSimple.parentNode.classList.add('animation_img')
    videoPause(`player${id}/`)
}

function videoAnimatioOneoff(videoSimple,id){
    videoSimple.parentNode.classList.remove('animation__video')
    videoSimple.parentNode.classList.add('animation_img')
    setTimeout(styleRemove,4000,videoSimple)
    videoPause(`player${id}`)
}

function videoAnimationOneOn(videoSimple,id){
    const url = document.getElementById(id).dataset.url
    videoSimple.style.display = 'block'
    videoSimple.style.transform = 'rotateY(90deg)'
    videoSimple.classList.add('animation__video')
    onYouTubeIframeAPIReady(id,url)
    setTimeout(videoPlay,1500,`player${id}`)
}

function animationSeta(seta,ativo){
    if(ativo){
        seta.style.transform = 'rotateY(0)'
    }else{
        seta.style.transform = 'rotateY(160deg)'
    }
}

function styleRemove(video){
    video.style.display = 'none'
    video.classList.remove('animation__video')
    video.classList.remove('animation_img')
    if(video.parentNode){
        video.parentNode.classList.remove('animation_img')
    }
}

function idVerificarString(id){
    if(id.includes('/')){
        const string = id.substring(0,id.length - 1)
        return string
    }
    return id
}