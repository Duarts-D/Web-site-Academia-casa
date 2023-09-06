const iframes = document.querySelectorAll('iframe')
const imagemVideo = document.querySelectorAll('[data-imagem]')
const videoClass = document.querySelectorAll('li.videos__item')
const divBlocoVideo = document.querySelectorAll('[data-bloco-video]')

const listaIframeSrc = []
let lista = []
let intensVideoPlay = []
let numero = 0

// -----------------------------------------------------------------------------------------
// console.log(iframes[0].id)




imagemVideo.forEach((e) => {
    e.addEventListener('click',()=>{
        let data = document.querySelector(`[data-id="${e.id}"]`)
        videoPlay(e.id)
        e.classList.add('video__none')

        data.classList.remove('video__none')
        console.log(data.id)
        //iniciar o video
    })
})

//mouseout = volta a imagem e fecha e pausa o video
divBlocoVideo.forEach((e)=>{
    e.addEventListener('mouseleave',()=>{
        console.log('sair')
    })
})


function onYouTubeIframeAPIReady() {
    console.log('Iniciado')
    iframes.forEach(elemento =>{
        let id = elemento.id
        id = new YT.Player(elemento.id, {
            events: {
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange
            }
        })
        intensVideoPlay.push(id)
    })
}

// let teste = false

function onPlayerReady(event) {
    //   console.log(event.target.id)
}

function onPlayerStateChange(event) {
    // Eventos de mudança de estado do jogador (por exemplo, pausa, reprodução, etc.).
    if (event.data == YT.PlayerState.PAUSED) {
        console.log('chegou a final')
    }
}

function videoPlay(elemento) {
    console.log(elemento)
    let indice = intensVideoPlay.findIndex(function(dados){
        return dados.g.id == `player${elemento}`
    })
    const player = intensVideoPlay[indice]
    player.playVideo()
}

// function pauseButton(elemento) {
//     const player = iframes[elemento]
//     player.pauseVideo()
//     // console.log(intens[3].playVideo())
//     // if(elemento == player.id){
//     //     player.playVideo();
//     // }
// }


