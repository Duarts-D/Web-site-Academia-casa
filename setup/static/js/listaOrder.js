import sendPost from "./post_remove.js";

const sortableList = document.getElementById('sortable-list');
const butonOrganizarFechar = document.getElementById('button_organizar__fechar')
const buttonOrganizar = document.getElementById('organizarjs')
const videoLista = document.getElementById('ulVideos')

const url = window.location.href;
const regex = /Geral/;

if (regex.test(url)) {
} else {
    buttonOrganizar.disabled = true
    buttonOrganizar.style.opacity = 0.5
}

buttonOrganizar.addEventListener('click',()=>{
    sortableList.style.display = 'block';
    buttonOrganizar.style.display = 'none'
})


butonOrganizarFechar.addEventListener('click',()=>{
  buttonOrganizar.style.display = 'block'
  sortableList.style.display = 'none'
    loadOrder()
    const order = JSON.parse(localStorage.getItem('itemOrder'));
    sendPost(order)
})

// Função para salvar a ordem dos itens no localStorage
function saveOrder() {
  const items = [...sortableList.children];
  const order = items.map(item => item.dataset.organizacaoId);
  localStorage.setItem('itemOrder', JSON.stringify(order));
}

// Função para carregar a ordem dos itens do localStorage
function loadOrder() {
  const order = JSON.parse(localStorage.getItem('itemOrder'));
  if (order) {
    order.forEach(dataset => {
      const item = [...sortableList.children].find(li => li.dataset.organizacaoId === dataset);
      const videos = [...videoLista.children].find(li => li.dataset.videoId === dataset);
      if (item) {
        sortableList.appendChild(item);
        videoLista.appendChild(videos)
      }
    });
  }
}

// Adicionar eventos de arrastar e soltar
sortableList.addEventListener('dragstart', (e) => {
  e.dataTransfer.setData('text/plain', e.target.outerHTML);
  e.target.classList.add('dragging');
  e.target.style.color = '#b8860b'
});

sortableList.addEventListener('dragend', (e) => {
  e.target.classList.remove('dragging');
  e.target.style.color = 'red'
  saveOrder();
});

sortableList.addEventListener('dragover', (e) => {
  e.preventDefault();
  dragOver(e)
});

function dragOver(e){
  const draggingItem = document.querySelector('.dragging');
  const afterElement = getDragAfterElement(sortableList, e.clientY);
  const index = afterElement ? [...sortableList.children].indexOf(afterElement) : sortableList.children.length;

  if (afterElement !== sortableList.firstElementChild) {
    sortableList.insertBefore(draggingItem, afterElement);
  }
}


function touchMove(e){
  const touchY = e.touches[0].clientY;
  const afterElement = getDragAfterElement(sortableList, touchY);
  if (afterElement !== sortableList.firstElementChild) {
      sortableList.insertBefore(draggedItem, afterElement);
  }
}
// Função para encontrar o elemento após o qual o item está sendo arrastado
function getDragAfterElement(container, y) {
  const draggableElements = [...container.querySelectorAll('li:not(.dragging)')];
  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;
    if (offset < 0 && offset > closest.offset) {
      return { offset, element: child };
    } else {
      return closest;
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element;
}

// Carregar a ordem dos itens ao carregar a página
loadOrder();
// ----------------------------------------------------------------

let draggedItem = null;

sortableList.addEventListener('touchstart', (e) => {
    if(e.target.classList.contains('organiza__titulo__1') || e.target.id == 'button_organizar__fechar'){
      //
    }else {
      draggedItem = e.target.parentNode
      console.log(draggedItem)
      if(draggedItem.classList.contains('organizar__container__img')){
        draggedItem = draggedItem.parentNode
        draggedItem.classList.add('dragging');
        draggedItem.style.color = '#b8860b'
      }
      e.target.classList.add('dragging');
      e.target.style.color = '#b8860b'
      e.preventDefault();
    }

});

sortableList.addEventListener('touchmove', (e) => {
    if (!draggedItem) return;
    e.preventDefault();
    touchMove(e)
});

sortableList.addEventListener('touchend', (e) => {
    if (!draggedItem) return;
    draggedItem.classList.remove('dragging');
    draggedItem.style.color = 'red'
    e.target.style.color = 'red'
    saveOrder();
    draggedItem = null;
});
