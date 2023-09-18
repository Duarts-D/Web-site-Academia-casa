import sendPost from "./post_remove.js";

const sortableList = document.getElementById('sortable-list');
const butonOrganizarFechar = document.getElementById('button_organizar__fechar')
const buttonOrganizar = document.getElementById('organizarjs')
const videoLista = document.getElementById('ulVideos')

const url = window.location.href;
const regex = /Geral/;

if (regex.test(url)) {
  console.log("Estou na página de Treino-dia-Segunda/Geral");
} else {
    buttonOrganizar.disabled = true
    buttonOrganizar.style.opacity = 0.5
}

buttonOrganizar.addEventListener('click',()=>{
    sortableList.style.display = 'block'
    console.log('lick')
})


butonOrganizarFechar.addEventListener('click',()=>{
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
  const draggingItem = document.querySelector('.dragging');
  const afterElement = getDragAfterElement(sortableList, e.clientY);
  const index = afterElement ? [...sortableList.children].indexOf(afterElement) : sortableList.children.length;

  if (afterElement !== sortableList.firstElementChild) {
    sortableList.insertBefore(draggingItem, afterElement);
  }

});

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