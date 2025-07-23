# IdeaScrawl Agenda 📝

> Transforma tus chats de ChatGPT en páginas de agenda manuscritas con IA

**Estado**: MVP Fase 1 ✅ Completado | GitHub Ready 🚀

## 🎯 Concepto

IdeaScrawl Agenda es una extensión de Chrome + SaaS que indexa tus conversaciones de ChatGPT y las convierte en páginas de agenda manuscritas personalizadas usando IA visual (Leonardo API).

**Flujo**: Chat → Extensión → API → Leonardo IA → Imagen manuscrita → Storage → Dashboard

## 📁 Estructura del Proyecto

```
IdeaScrawl-Agenda/
├── 📱 extension/          # Chrome Extension
│   ├── manifest.json      # Extension config (fixed JSON)
│   ├── background.js      # Service worker + queue system
│   ├── content.js         # ChatGPT message capture
│   ├── popup.html         # Extension UI
│   └── popup.js           # Popup logic + modal
├── 🔧 api/               # FastAPI Backend
│   ├── generate_page.py   # Main API endpoint
│   └── storage.py         # Supabase integration
├── 📚 docs/              # Documentation
│   ├── requirements.md    # Technical specs
│   ├── DATASET_GUIDE.md   # Leonardo training guide
│   ├── DEMO_STATUS.md     # Current capabilities
│   └── INSTALL_EXTENSION.md
├── 🛠️ scripts/           # Development utilities
│   ├── start_dev.sh       # Dev environment setup
│   └── test_api.sh        # API testing suite
├── .env.example          # Environment template
├── .gitignore           # Git ignore rules
├── .metadata            # File version tracking
└── requirements.txt     # Python dependencies
```

## 🏗️ Arquitectura Técnica

```
[ChatGPT] → [Extension] → [FastAPI] → [Leonardo*] → [Storage*] → [UI]
    ✅         ✅           ✅          🎨 DEMO      ⏳ TODO      ✅
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Clone repository
git clone https://github.com/your-username/IdeaScrawl-Agenda.git
cd IdeaScrawl-Agenda

# Start development environment (installs deps + starts API)
./scripts/start_dev.sh

# Test API is working
./scripts/test_api.sh
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys (Leonardo, Supabase)

# 3. Start API server
uvicorn api.generate_page:app --reload --port 8000
```

### Chrome Extension Installation

1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" → Select `/extension` folder
4. Go to [chat.openai.com](https://chat.openai.com) and start chatting
5. Click extension icon to see captured ideas

## ✅ Verification Steps

After setup, verify everything works:

```bash
# 1. API Health Check
curl http://localhost:8000/health

# 2. Test page generation
curl -X POST http://localhost:8000/generate-page \
  -H "Content-Type: application/json" \  
  -d '{"title":"Test","text":"Hello world","timestamp":1690995200000}'

# 3. Expected response (demo mode)
{
  "success": true,
  "image_url": "https://via.placeholder.com/...", 
  "idea_id": "uuid-generated"
}
```

## 📋 Uso

### Flujo Básico
1. **Chatear en ChatGPT**: Escribe normalmente en chat.openai.com
2. **Procesamiento automático**: La extensión captura mensajes y los envía a la API  
3. **Generación IA**: Leonardo API crea la página manuscrita en tu estilo
4. **Ver resultados**: Clic en el icono de la extensión para ver tus páginas

### Estados de las Ideas
- 📝 **Generada**: Página manuscrita lista
- ⏳ **Procesando**: En cola o generándose
- ❌ **Error**: Falló la generación (ver detalles)

### Ver Páginas Generadas
- Clic en "Ver página" en el popup de la extensión
- Modal con imagen full-size de tu página manuscrita
- Scroll para ver múltiples páginas

## 🛠️ Endpoints API

### `POST /generate-page`
Genera página manuscrita desde texto de ChatGPT

```json
{
  "title": "Título del chat",
  "text": "Contenido del mensaje",  
  "timestamp": 1640995200000,
  "estilo": {
    "modelId": "alan-lora-v1",
    "cfgScale": 7.5,
    "detalles": "garabatos y flechas",
    "width": 1024,
    "height": 1024
  }
}
```

**Response**:
```json
{
  "success": true,
  "image_url": "https://supabase.co/storage/...",
  "idea_id": "uuid-123"
}
```

### `GET /health`
Health check del servicio

### `GET /api/get_ideas` (legacy)
Compatibilidad con versión anterior

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Leonardo API
LEONARDO_API_KEY=your_key_here

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key

# Ollama Fallback
OLLAMA_IMAGE_MODEL=stable-diffusion
OLLAMA_TIMEOUT=120

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### Personalizar Estilo de Generación
Edita `background.js` línea 64-70:
```javascript
estilo: {
  modelId: 'tu-modelo-lora-id', // Tu modelo entrenado
  cfgScale: 7.5,                // Control de fidelidad (5-15)
  detalles: 'tu estilo único',  // Descripción personalizada
  width: 1024,
  height: 1024
}
```

## 📊 Monitoring

### Logs de la Extensión
```javascript
// Chrome DevTools → Console
// Buscar logs con prefijo "🚀 IdeaScrawl:"
```

### API Logs
```bash
# FastAPI logs con uvicorn
tail -f api.log
```

### Storage Local
```javascript
// Inspeccionar datos en Chrome DevTools
chrome.storage.local.get(['ideascrawl_ideas'])
```

## 🚧 Próximas Fases

### Fase 2: SaaS Infrastructure (3-4 semanas)
- Dashboard web con Next.js + Tailwind
- Autenticación multi-usuario con Supabase Auth
- Sistema de suscripciones con Stripe
- RLS (Row Level Security) para multi-tenancy

### Fase 3: Features Avanzadas
- Búsqueda semántica en páginas
- Exportación a PDF/PNG
- Integración con otros chats (Discord, Slack)
- App móvil para visualización

## 🐛 Troubleshooting

### La extensión no captura mensajes
1. Verifica que esté en chat.openai.com
2. Recarga la página y la extensión
3. Revisa permisos en chrome://extensions/

### API no responde
1. Verifica que FastAPI esté corriendo en puerto 8000
2. Revisa las variables de entorno en `.env`
3. Confirma que Leonardo API key sea válida

### Imágenes no se generan
1. Verifica créditos en cuenta de Leonardo AI
2. Confirma que el model_id del LoRA sea correcto
3. Revisa configuración de Supabase Storage

### Storage local lleno
```javascript
// Limpiar storage manualmente
chrome.storage.local.clear()
```

## 📚 Documentación Adicional

- **[requirements.md](requirements.md)**: Especificación técnica completa
- **[DATASET_GUIDE.md](DATASET_GUIDE.md)**: Cómo crear tu dataset de entrenamiento
- **[API Docs](http://localhost:8000/docs)**: Documentación automática de FastAPI

## 🤝 Contribuir

1. Fork el proyecto
2. Crea feature branch (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Abre Pull Request

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles

## 🎉 Créditos

- **Inspiración**: Edward Honour's AI workflow methodology
- **IA Visual**: Leonardo AI para generación de imágenes
- **Storage**: Supabase para backend como servicio
- **Framework**: FastAPI para API rápida y tipada

---

**¿Preguntas?** Abre un issue o contacta al equipo de desarrollo.

*Última actualización: 2025-07-23*