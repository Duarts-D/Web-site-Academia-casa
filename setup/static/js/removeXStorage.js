const dia = document.querySelector('[data-dia]').textContent
let intensStorage = JSON.parse(localStorage.getItem(`Remover-${dia}`)) || [] 


intensStorage.forEach(id => {
    const item = document.getElementById(id)
    if(item){
        item.checked = false
        local = intensStorage.findIndex(function(index){
            return index == id
        })
        intensStorage.splice(local,1)
        localStorage.setItem(`Remover-${dia}`,JSON.stringify(intensStorage))
    }
});