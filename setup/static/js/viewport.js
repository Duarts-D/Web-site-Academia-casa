export default function viewPort(){
    const footer = document.getElementById('footer')
    const body = document.body;
    const viewportHeight = window.innerHeight;
    const bodyHeight = body.clientHeight;
    // Verifica se a altura do corpo é igual à altura da viewport
    if (bodyHeight >= viewportHeight) {
        //
    } else {
        footer.classList.add('rodapebottom')
        footer.style.opacity = 1
    }
}