// ID: BG-001-V02
// IdeaScrawl Agenda - Background Script
// Maneja mensajes del content script y los procesa via API

const API_BASE_URL = 'http://localhost:8000'; // TODO: Cambiar en producción
const RATE_LIMIT_DELAY = 2000; // 2 segundos entre requests

// Queue para evitar spam de requests
let processingQueue = [];
let isProcessing = false;

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'newMessage') {
    // Agregar a queue para procesamiento
    processingQueue.push({
      title: msg.chatTitle,
      text: msg.text,
      timestamp: Date.now(),
      sender: sender
    });
    
    // Procesar queue
    processMessageQueue();
    
    // Responder inmediatamente al content script
    sendResponse({ status: 'queued' });
  }
  
  return true; // Mantener canal abierto para respuesta asíncrona
});

async function processMessageQueue() {
  if (isProcessing || processingQueue.length === 0) {
    return;
  }
  
  isProcessing = true;
  
  while (processingQueue.length > 0) {
    const messageData = processingQueue.shift();
    
    try {
      await processIdeaMessage(messageData);
      
      // Rate limiting: esperar entre requests
      if (processingQueue.length > 0) {
        await new Promise(resolve => setTimeout(resolve, RATE_LIMIT_DELAY));
      }
      
    } catch (error) {
      console.error('Error processing message:', error);
      // Continuar con el siguiente mensaje aunque falle uno
    }
  }
  
  isProcessing = false;
}

async function processIdeaMessage(messageData) {
  const payload = {
    title: messageData.title || 'Sin título',
    text: messageData.text,
    timestamp: messageData.timestamp,
    estilo: {
      modelId: 'alan-lora-v1', // Modelo personalizado
      cfgScale: 7.5,
      detalles: 'garabatos y flechas, escritura natural',
      width: 1024,
      height: 1024
    }
  };
  
  console.log('🚀 IdeaScrawl: Processing new idea:', {
    title: payload.title.substring(0, 50) + '...',
    textLength: payload.text.length
  });
  
  try {
    const response = await fetch(`${API_BASE_URL}/generate-page`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
      throw new Error(`API responded with status: ${response.status}`);
    }
    
    const result = await response.json();
    
    if (result.success) {
      console.log('✅ IdeaScrawl: Page generated successfully:', {
        ideaId: result.idea_id,
        imageUrl: result.image_url ? 'Generated' : 'Failed'
      });
      
      // Guardar en storage local para acceso rápido
      await saveToLocalStorage(result, messageData);
      
    } else {
      console.error('❌ IdeaScrawl: Generation failed:', result.error);
    }
    
  } catch (error) {
    console.error('❌ IdeaScrawl: Network/API error:', error);
    
    // Fallback: guardar solo los datos de texto
    await saveToLocalStorage({
      success: false,
      idea_id: generateLocalId(),
      image_url: null,
      error: error.message
    }, messageData);
  }
}

async function saveToLocalStorage(result, messageData) {
  try {
    // Obtener ideas existentes
    const stored = await chrome.storage.local.get(['ideascrawl_ideas']);
    const ideas = stored.ideascrawl_ideas || [];
    
    // Crear nuevo registro
    const newIdea = {
      id: result.idea_id,
      title: messageData.title,
      text: messageData.text,
      timestamp: messageData.timestamp,
      image_url: result.image_url,
      generated: result.success,
      error: result.error || null,
      created_at: new Date().toISOString()
    };
    
    // Agregar al inicio (más reciente primero)
    ideas.unshift(newIdea);
    
    // Mantener solo últimas 100 ideas localmente
    if (ideas.length > 100) {
      ideas.splice(100);
    }
    
    // Guardar
    await chrome.storage.local.set({ 'ideascrawl_ideas': ideas });
    
    console.log('💾 IdeaScrawl: Saved to local storage');
    
  } catch (error) {
    console.error('Error saving to local storage:', error);
  }
}

function generateLocalId() {
  return 'local_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Cleanup periódico del storage local
setInterval(async () => {
  try {
    const stored = await chrome.storage.local.get(['ideascrawl_ideas']);
    const ideas = stored.ideascrawl_ideas || [];
    
    // Eliminar ideas más antiguas de 30 días
    const thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000);
    const recentIdeas = ideas.filter(idea => idea.timestamp > thirtyDaysAgo);
    
    if (recentIdeas.length !== ideas.length) {
      await chrome.storage.local.set({ 'ideascrawl_ideas': recentIdeas });
      console.log('🧹 IdeaScrawl: Cleaned old ideas from storage');
    }
    
  } catch (error) {
    console.error('Error during storage cleanup:', error);
  }
}, 60 * 60 * 1000); // Cada hora

console.log('🎯 IdeaScrawl Agenda - Background script loaded');
