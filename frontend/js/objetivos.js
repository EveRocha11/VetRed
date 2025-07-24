// js/objetivos.js
// Objetivos personalizados del paciente (persistentes en backend)

document.addEventListener('DOMContentLoaded', () => {
  const goalsList = document.querySelector('.goals-list');
  const addGoalBtn = document.querySelector('.btn.btn-secondary');

  // Obtener usuario y token
  const user = JSON.parse(localStorage.getItem('user'));
  const token = localStorage.getItem('token');
  let objetivos = [];

  // Helpers para peticiones al backend
  const API_URL = 'http://localhost:5000/api/objetivos';
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };

  // Validar usuario y token antes de cualquier acción
  if (!user || !token) {
    alert('Tu sesión ha expirado o no has iniciado sesión. Por favor, vuelve a iniciar sesión.');
    window.location.href = 'login.html';
    return;
  }

  // Renderizar objetivos
  function renderGoals() {
    goalsList.innerHTML = '';
    objetivos.forEach((obj, idx) => {
      const div = document.createElement('div');
      div.className = 'goal-item';
      div.innerHTML = `
        <input type="checkbox" ${obj.completado ? 'checked' : ''} data-id="${obj.idObjetivo}" data-idx="${idx}"> 
        <span contenteditable="true" class="goal-text" data-id="${obj.idObjetivo}" data-idx="${idx}">${obj.texto}</span>
        <button class="btn btn-small btn-delete-goal" data-id="${obj.idObjetivo}" data-idx="${idx}">🗑️</button>
      `;
      goalsList.appendChild(div);
    });
  }

  // Obtener objetivos del backend
  async function fetchGoals() {
    try {
      const res = await fetch(`${API_URL}/usuario/${user.idUsuario}`, { headers });
      if (!res.ok) throw new Error('Error al obtener objetivos');
      objetivos = await res.json();
      console.log('Objetivos recibidos:', objetivos); // Debug
      if (!Array.isArray(objetivos) || objetivos.length === 0) {
        goalsList.innerHTML = '<div class="error">No tienes objetivos guardados.</div>';
        return;
      }
      renderGoals();
    } catch (err) {
      goalsList.innerHTML = '<div class="error">No se pudieron cargar los objetivos.</div>';
      console.error('Error al obtener objetivos:', err);
    }
  }

  // Agregar objetivo
  addGoalBtn.addEventListener('click', async () => {
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          idPaciente: user.idUsuario, // Cambiado de idUsuario a idPaciente
          texto: 'Nuevo objetivo',
          completado: false
        })
      });
      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Error al agregar objetivo: ${res.status} - ${errorText}`);
      }
      // En vez de push y render, recarga la lista para asegurar ids correctos
      await fetchGoals();
    } catch (err) {
      alert('No se pudo agregar el objetivo.\n' + err.message);
      console.error(err);
    }
  });

  // Marcar como completado
  goalsList.addEventListener('change', async (e) => {
    if (e.target.type === 'checkbox') {
      const idx = e.target.dataset.idx;
      const id = e.target.dataset.id;
      const completado = e.target.checked;
      try {
        const res = await fetch(`${API_URL}/${id}`, {
          method: 'PATCH', // Cambiado de PUT a PATCH
          headers,
          body: JSON.stringify({ completado })
        });
        if (!res.ok) throw new Error();
        objetivos[idx].completado = completado;
      } catch {
        alert('No se pudo actualizar el objetivo');
        e.target.checked = !completado;
      }
    }
  });

  // Editar texto del objetivo
  goalsList.addEventListener('input', async (e) => {
    if (e.target.classList.contains('goal-text')) {
      const idx = e.target.dataset.idx;
      const id = e.target.dataset.id;
      const texto = e.target.textContent;
      try {
        const res = await fetch(`${API_URL}/${id}`, {
          method: 'PATCH', // Cambiado de PUT a PATCH
          headers,
          body: JSON.stringify({ texto })
        });
        if (!res.ok) throw new Error();
        objetivos[idx].texto = texto;
      } catch {
        alert('No se pudo editar el objetivo');
      }
    }
  });

  // Eliminar objetivo
  goalsList.addEventListener('click', async (e) => {
    if (e.target.classList.contains('btn-delete-goal')) {
      const idx = e.target.dataset.idx;
      let id = e.target.dataset.id;
      // Validar que el id es un número válido
      if (!id || isNaN(Number(id))) {
        alert('ID de objetivo inválido. No se puede eliminar.');
        return;
      }
      id = Number(id);
      try {
        const res = await fetch(`${API_URL}/${id}`, {
          method: 'DELETE',
          headers
        });
        if (!res.ok) {
          const errorText = await res.text();
          throw new Error(`Error al eliminar objetivo: ${res.status} - ${errorText}`);
        }
        objetivos.splice(idx, 1);
        renderGoals();
      } catch (err) {
        alert('No se pudo eliminar el objetivo.\n' + err.message);
        console.error(err);
      }
    }
  });

  fetchGoals();
});
