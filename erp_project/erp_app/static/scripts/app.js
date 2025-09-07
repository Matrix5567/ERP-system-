// app.js - simple frontend behaviour for Kanban and modal
document.addEventListener('DOMContentLoaded', () => {
  // Enable HTML5 drag and drop on .task-card
  const taskCards = () => Array.from(document.querySelectorAll('.task-card'));
  let dragged = null;

  function onDragStart(e) {
    dragged = this;
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', this.dataset.taskId || '');
  }
  function onDragEnd() {
    this.classList.remove('dragging');
    dragged = null;
  }

  function onDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    this.classList.add('drop-target');
  }
  function onDragLeave() {
    this.classList.remove('drop-target');
  }
  function onDrop(e) {
    e.preventDefault();
    this.classList.remove('drop-target');
    const taskId = e.dataTransfer.getData('text/plain');
    const el = dragged;
    if (!el) return;

    // append to column
    this.appendChild(el);

    // (Optional) call backend to update status/column
    const columnId = this.closest('.column').dataset.columnId;
    // Example fetch - implement route on backend to persist
    /*
    fetch(BOARD_API, {
      method: 'POST',
      headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
      body: JSON.stringify({task_id: taskId, column_id: columnId})
    }).then(...)
    */
  }

  function wireDrags() {
    taskCards().forEach(tc => {
      tc.setAttribute('draggable','true');
      tc.addEventListener('dragstart', onDragStart);
      tc.addEventListener('dragend', onDragEnd);
    });
    const columns = Array.from(document.querySelectorAll('.column'));
    columns.forEach(col => {
      col.addEventListener('dragover', onDragOver);
      col.addEventListener('dragleave', onDragLeave);
      col.addEventListener('drop', onDrop);
    });
  }
  wireDrags();

  // Task open: example - show modal populated with content via fetch or DOM
  window.openTask = function(taskId) {
    const modalEl = document.getElementById('taskModal');
    const modalBody = document.getElementById('taskModalBody');
    // In production fetch task details from backend; here we mock
    modalBody.innerHTML = `<div><strong>Task #${taskId}</strong></div><p class="text-muted">Task details would be loaded from server.</p>`;
    const taskModal = new bootstrap.Modal(modalEl);
    taskModal.show();
  };

  // Create task (client-side demo)
  window.createTask = function(e) {
    e.preventDefault();
    const title = document.getElementById('newTaskTitle').value;
    const desc = document.getElementById('newTaskDesc').value;
    const pr = document.getElementById('newTaskPriority').value;
    const due = document.getElementById('newTaskDue').value;
    const col = document.getElementById('newTaskColumn').value;

    const columnEl = document.querySelector(`.column[data-column-id="${col}"]`);
    if (!columnEl) {
      alert('Column not found');
      return;
    }
    const id = 'tmp-' + Math.floor(Math.random()*10000);
    const task = document.createElement('div');
    task.className = 'task-card mb-2';
    task.dataset.taskId = id;
    task.innerHTML = `<div class="d-flex justify-content-between"><div><div class="fw-semibold">${escapeHtml(title)}</div><div class="small text-muted">${escapeHtml(desc).slice(0,50)}</div></div><div class="text-end small"><div>${due ? due : ''}</div><div class="badge bg-light text-dark small">${pr}</div></div></div>`;
    task.addEventListener('dragstart', function(e){ onDragStart.call(this,e); });
    task.addEventListener('dragend', onDragEnd);
    task.addEventListener('click', ()=> openTask(id));
    columnEl.appendChild(task);
    // reset and close modal
    document.getElementById('createTaskForm').reset();
    bootstrap.Modal.getInstance(document.getElementById('createTaskModal')).hide();
  };

  // small helper
  function escapeHtml(text) {
    return text.replace(/[&<>"']/g, function(m){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]; });
  }
});