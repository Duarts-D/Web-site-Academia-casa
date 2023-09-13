const iframes = document.querySelectorAll('iframe')
const imagemVideo = document.querySelectorAll('[data-imagem]')
const videoClass = document.querySelectorAll('li.videos__item')
const divBlocoVideo = document.querySelectorAll('[data-bloco-video]')
const buttonConcluido = document.querySelectorAll('[data-button]')
const dia = document.getElementById('dia_semanal').textContent
const buttonXRemover = document.querySelectorAll('[data-button-remove]')
const buttonResetaMarcacao = document.querySelector('.resetbutton')

const listaIframeSrc = []
let lista = []
let intensVideoPlay = []
let intesXStorage = JSON.parse(localStorage.getItem(`Remover-${dia}`)) || []
let intensStorage = JSON.parse(localStorage.getItem(dia)) || [] 
let ok
const reset = setTimeout(apiYotuTubeReativar,2000)

intensStorage.forEach((id) => {
    divBlocoVideoContainer(id)
    buttonActive(id)
})

intesXStorage.forEach((id)=>{
    divDomRemove(id)
})


function apiYotuTubeReativar(){
    if(!ok){
        onYouTubeIframeAPIReady()
    }
}
// -----------------------------------------------------------------------------------------

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
        alert('Removendo!!')
        intesXStorage.push(valor)
        localStorage.setItem(`Remover-${dia}`,JSON.stringify(intesXStorage))
    })
})

imagemVideo.forEach((e) => {
    e.addEventListener('click',()=>{
        let data = document.querySelector(`[data-id="${e.id}"]`)
        e.style.display = "none"
        data.style.display = "block"
        setTimeout(videoPlay,1000,e.id)
        // videoPlay(e.id)
        //iniciar o video
    })
})

//mouseout = volta a imagem e fecha e pausa o video
divBlocoVideo.forEach((e)=>{
    e.addEventListener('mouseleave',()=>{
        // const iframeVideo = e.children[1].lastElementChild// [data-imagem="${e.dataset.blocoVideo}"]
        // const imagem = e.children[1].firstElementChild
        // imagem.style.display = "block"
        // iframeVideo.style.display = "none"
    })
})


function onYouTubeIframeAPIReady() {
    ok = true
    console.log('Iniciado')
    iframes.forEach(elemento =>{
        let id = elemento.id
        player = new YT.Player(id, {
            events: {
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange
            }
        })
        intensVideoPlay.push(player)
    })
}

// let teste = false

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
}

function videoPlay(elemento) {
    let indice = intensVideoPlay.findIndex(function(dados){
        if (dados.g !== null)
            return dados.g.id == `player${elemento}`
    })
    const player = intensVideoPlay[indice]
    player.playVideo()
    player.mute()
}


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
    const info = div.children[0].children[0].childNodes[1].childNodes[1]
    
    timeout = setTimeout(divBlocoVideoContainerEnd,1500,div,button);
    

    div.classList.add('caixas-ativa');

    button.textContent = "Resetar"
    button.style.width = "auto"
}


function divBlocoVideoContainerEnd(elemento,button){
    button.classList.add('borde__style_2px_dourado')
    
    elemento.classList.remove('caixas-ativa')
    elemento.classList.add('video__container__concluido_js')
    ab  = elemento.childNodes[1].childNodes
    ac = elemento.children[0].childNodes[1].childNodes

    ab.forEach( (e)=>{
        if(e.classList){
            e.classList.add('color_dourado')
        }
        node = e.childNodes
        // console.log(node)
        node.forEach((esta)=>{
            // console.log(esta.tagName)
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

    ab  = elemento.childNodes[1].childNodes
    ac = elemento.children[0].childNodes[1].childNodes

    ab.forEach( (e)=>{
        if(e.classList){
            e.classList.remove('color_dourado')
        }
        node = e.childNodes
        // console.log(node)
        node.forEach((esta)=>{
            // console.log(esta.tagName)
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

