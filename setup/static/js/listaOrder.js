const sortableList = document.getElementById('sortable-list');



// Função para salvar a ordem dos itens no localStorage
function saveOrder() {
  const items = [...sortableList.children];
  const order = items.map(item => item.innerText);
  localStorage.setItem('itemOrder', JSON.stringify(order));
}

// Função para carregar a ordem dos itens do localStorage
function loadOrder() {
  const order = JSON.parse(localStorage.getItem('itemOrder'));
  if (order) {
    order.forEach(itemText => {
      const item = [...sortableList.children].find(li => li.innerText === itemText);
      if (item) {
        sortableList.appendChild(item);
      }
    });
  }
}

// Adicionar eventos de arrastar e soltar
sortableList.addEventListener('dragstart', (e) => {
  e.dataTransfer.setData('text/plain', e.target.outerHTML);
  e.target.classList.add('dragging');
  e.target.classList.add('animar')
});

sortableList.addEventListener('dragend', (e) => {
  e.target.classList.remove('dragging');
  saveOrder();
});

sortableList.addEventListener('dragover', (e) => {
  e.preventDefault();
  const draggingItem = document.querySelector('.dragging');
  const afterElement = getDragAfterElement(sortableList, e.clientY);
  const index = afterElement ? [...sortableList.children].indexOf(afterElement) : sortableList.children.length;
  sortableList.insertBefore(draggingItem, afterElement);
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




