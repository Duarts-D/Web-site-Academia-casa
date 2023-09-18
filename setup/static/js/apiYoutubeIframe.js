const imagemVideo = document.querySelectorAll('[data-imagem]')
let intensVideoPlay = []



function onYouTubeIframeAPIReady(id,url) {
    console.log('Iniciado')
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
        // main.divBlocoVideoRemover(id)
        // main.buttonStorageRemove(id)
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
    // player.mute()
}

imagemVideo.forEach((e) => {
    e.addEventListener('click',()=>{
        const id = e.id
        const url = e.dataset.url
        onYouTubeIframeAPIReady(id,url)
        e.style.display = "none"
    })
})