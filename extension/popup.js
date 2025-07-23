// ID: POPJS-001-V02
// IdeaScrawl Agenda - Popup Script
// Muestra las ideas capturadas y sus páginas generadas

document.addEventListener('DOMContentLoaded', async () => {
  const container = document.getElementById('ideas');
  
  try {
    // Primero verificar conexión con API
    await checkApiConnection();
    
    // Cargar ideas desde Chrome storage local
    const stored = await chrome.storage.local.get(['ideascrawl_ideas']);
    const ideas = stored.ideascrawl_ideas || [];
    
    container.innerHTML = ''; // Limpiar "Cargando..."
    
    if (ideas.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <p>✅ Conexión API funcionando</p>
          <p>No hay ideas capturadas aún.</p>
          <p style="font-size: 12px; color: #666; margin-top: 8px;">
            Ve a <a href="https://chat.openai.com" target="_blank">ChatGPT</a> y escribe algunos mensajes para generar tu primera página manuscrita.
          </p>
          <p style="font-size: 11px; color: #999; margin-top: 4px;">
            Asegúrate de estar en chat.openai.com
          </p>
        </div>
      `;
      return;
    }
    
    // Mostrar las ideas más recientes primero
    ideas.slice(0, 10).forEach((idea) => {
      const div = document.createElement('div');
      div.className = 'idea';
      
      // Formatear fecha
      const date = new Date(idea.timestamp || idea.created_at);
      const dateStr = date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
      
      // Truncar texto para el preview
      const previewText = idea.text.length > 120 
        ? idea.text.substring(0, 120) + '...' 
        : idea.text;
      
      // Determinar estado de generación
      let statusIndicator = '';
      if (idea.generated && idea.image_url) {
        statusIndicator = '<span class="status generated">📝</span>';
      } else if (idea.error) {
        statusIndicator = '<span class="status error">❌</span>';
      } else {
        statusIndicator = '<span class="status processing">⏳</span>';
      }
      
      div.innerHTML = `
        <div class="idea-header">
          <div class="title">
            ${statusIndicator}
            ${dateStr} – ${idea.title || 'Sin título'}
          </div>
          ${idea.image_url ? `<button class="view-page" data-url="${idea.image_url}">Ver página</button>` : ''}
        </div>
        <div class="text">${previewText}</div>
        ${idea.error ? `<div class="error-msg">Error: ${idea.error}</div>` : ''}
      `;
      
      container.appendChild(div);
    });
    
    // Agregar event listeners para botones "Ver página"
    container.addEventListener('click', (e) => {
      if (e.target.classList.contains('view-page')) {
        const imageUrl = e.target.dataset.url;
        openImageModal(imageUrl);
      }
    });
    
    // Agregar stats al final
    const statsDiv = document.createElement('div');
    statsDiv.className = 'stats';
    const generatedCount = ideas.filter(i => i.generated).length;
    const errorCount = ideas.filter(i => i.error).length;
    
    statsDiv.innerHTML = `
      <div class="stats-summary">
        Total: ${ideas.length} | 
        Generadas: ${generatedCount} | 
        Errores: ${errorCount}
      </div>
    `;
    container.appendChild(statsDiv);
    
  } catch (err) {
    console.error('Error loading ideas:', err);
    container.innerHTML = `
      <div class="error-state">
        <p>❌ Error de conexión</p>
        <p style="font-size: 12px; color: #666; margin-top: 8px;">
          ${err.message}
        </p>
        <p style="font-size: 11px; color: #999; margin-top: 8px;">
          Asegúrate de que la API esté corriendo en http://localhost:8000
        </p>
        <button onclick="location.reload()" style="margin-top: 8px; padding: 4px 8px; font-size: 11px;">
          Reintentar
        </button>
      </div>
    `;
  }
});

async function checkApiConnection() {
  try {
    const response = await fetch('http://localhost:8000/health', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error(`API responded with status: ${response.status}`);
    }
    
    const result = await response.json();
    console.log('🎯 IdeaScrawl: API connection verified', result);
    return true;
  } catch (error) {
    console.error('🚨 IdeaScrawl: API connection failed', error);
    throw new Error(`No se puede conectar a la API: ${error.message}`);
  }
}

function openImageModal(imageUrl) {
  // Crear modal simple para mostrar la imagen
  const modal = document.createElement('div');
  modal.className = 'image-modal';
  modal.innerHTML = `
    <div class="modal-overlay">
      <div class="modal-content">
        <button class="close-modal">&times;</button>
        <img src="${imageUrl}" alt="Página manuscrita" style="max-width: 100%; max-height: 80vh;">
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  // Event listeners para cerrar
  modal.querySelector('.close-modal').onclick = () => document.body.removeChild(modal);
  modal.querySelector('.modal-overlay').onclick = (e) => {
    if (e.target === modal.querySelector('.modal-overlay')) {
      document.body.removeChild(modal);
    }
  };
}

// Auto-refresh cada 30 segundos para mostrar nuevas generaciones
setInterval(() => {
  location.reload();
}, 30000);
