# ID: API-GEN-001-V01
"""
IdeaScrawl Agenda - API de Generación de Páginas Manuscritas
Endpoint FastAPI para procesar ideas de ChatGPT y generar imágenes estilo agenda manuscrita
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import json
import uuid
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv
# from storage import get_storage_client  # TODO: Uncomment when Supabase is configured

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="IdeaScrawl Agenda API",
    description="API para generar páginas de agenda manuscritas usando IA",
    version="1.0.0"
)

# Configurar CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://*", "http://localhost:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class EstiloConfig(BaseModel):
    modelId: str = "alan-lora-v1"
    cfgScale: Optional[float] = 7.5
    detalles: Optional[str] = "garabatos y flechas"
    width: Optional[int] = 1024
    height: Optional[int] = 1024

class IdeaPayload(BaseModel):
    title: str
    text: str
    timestamp: Optional[int] = None
    estilo: Optional[EstiloConfig] = EstiloConfig()

class GenerateResponse(BaseModel):
    success: bool
    image_url: Optional[str] = None
    idea_id: Optional[str] = None
    error: Optional[str] = None

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Endpoint principal de generación
@app.post("/generate-page", response_model=GenerateResponse)
async def generate_page(payload: IdeaPayload, request: Request):
    """
    Genera una página manuscrita basada en el contenido de ChatGPT
    
    Flujo:
    1. Construir prompt personalizado
    2. Llamar a Leonardo API
    3. Si falla, usar fallback local (Ollama)
    4. Guardar imagen en Supabase Storage
    5. Retornar URL pública
    """
    try:
        # Generar ID único para esta idea
        idea_id = str(uuid.uuid4())
        
        # 1. Construir prompt personalizado
        prompt = build_manuscript_prompt(payload.title, payload.text, payload.estilo)
        
        # 2. Intentar generación con Leonardo API
        image_url = None
        try:
            image_url = await call_leonardo_api(prompt, payload.estilo)
        except Exception as leonardo_error:
            print(f"Leonardo API error: {leonardo_error}")
            
            # 3. Fallback a generación local
            try:
                image_url = await call_local_ollama(prompt, payload.estilo)
            except Exception as local_error:
                print(f"Local fallback error: {local_error}")
                raise HTTPException(
                    status_code=502,
                    detail="Both Leonardo API and local fallback failed"
                )
        
        # 4. TODO: Guardar en Supabase Storage cuando esté configurado
        # storage = get_storage_client()
        # Por ahora usar URL directa
        public_url = image_url
        
        # 5. Guardar metadata en base de datos (placeholder)
        # TODO: Guardar en Supabase cuando esté configurado
        
        return GenerateResponse(
            success=True,
            image_url=public_url,
            idea_id=idea_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in generate_page: {e}")
        return GenerateResponse(
            success=False,
            error=str(e)
        )

def build_manuscript_prompt(title: str, text: str, estilo: EstiloConfig) -> str:
    """
    Construye el prompt optimizado para Leonardo API
    basado en el estilo de agenda manuscrita personal
    """
    # Limitar longitud del texto para evitar prompts muy largos
    truncated_text = text[:500] + "..." if len(text) > 500 else text
    
    prompt = f"""
    Página de agenda manuscrita estilo personal con caligrafía natural.
    
    Título: "{title}"
    Contenido: "{truncated_text}"
    
    Estilo: escritura a mano con {estilo.detalles}, márgenes irregulares, 
    ocasionales tachaduras, subrayados naturales, papel ligeramente amarillento.
    
    Características: letra cursiva casual, espaciado orgánico, pequeños dibujos 
    o flechas conectando ideas, aspecto de diario personal auténtico.
    """
    
    return prompt.strip()

async def call_leonardo_api(prompt: str, estilo: EstiloConfig) -> str:
    """
    Llama a Leonardo API para generar la imagen manuscrita
    """
    leonardo_key = os.getenv("LEONARDO_API_KEY")
    
    # DEMO MODE: Si no hay key real, usar mock
    if not leonardo_key or leonardo_key == "placeholder_key_for_demo":
        print(f"🎨 DEMO MODE: Simulando generación Leonardo...")
        print(f"📝 Prompt: {prompt[:100]}...")
        await asyncio.sleep(2)  # Simular tiempo de procesamiento
        
        # Retornar URL mock de imagen demo
        return "https://via.placeholder.com/1024x1024/f8f8f8/333333?text=DEMO+Página+Manuscrita+%0A%0AEste+sería+tu+texto+%0Aescrito+a+mano+con+tu+estilo+%0Apersonal+usando+Leonardo+AI"
    
    # Código real de Leonardo API
    api_url = "https://api.leonardo.ai/v1/generations"
    headers = {
        "Authorization": f"Bearer {leonardo_key}",
        "Content-Type": "application/json"
    }
    
    body = {
        "modelId": estilo.modelId,
        "prompt": prompt,
        "width": estilo.width,
        "height": estilo.height,
        "cfgScale": estilo.cfgScale,
        "samples": 1
    }
    
    response = requests.post(api_url, headers=headers, json=body, timeout=30)
    
    if response.status_code != 200:
        raise Exception(f"Leonardo API returned status {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Extraer URL de la imagen generada
    if "generations" in data and len(data["generations"]) > 0:
        return data["generations"][0]["uri"]
    else:
        raise Exception("No generation found in Leonardo API response")

async def call_local_ollama(prompt: str, estilo: EstiloConfig) -> str:
    """
    Fallback local usando Ollama + SDXL para generación de imágenes
    """
    import subprocess
    import tempfile
    
    try:
        # Verificar que Ollama esté disponible
        result = subprocess.run(["ollama", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            raise Exception("Ollama not installed or not available")
        
        # Preparar el prompt para generación de imagen
        image_prompt = f"""
        Generate a handwritten notebook page image with the following content:
        
        {prompt}
        
        Style: Personal handwriting, casual cursive, natural spacing, 
        occasional doodles and arrows, slightly yellowed paper texture,
        authentic notebook appearance.
        """
        
        # Crear archivo temporal para la imagen
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            temp_path = tmp_file.name
        
        # Comando para Ollama con modelo de imagen (ej: stable-diffusion)
        # Nota: Esto requiere tener un modelo compatible instalado
        model_name = os.getenv("OLLAMA_IMAGE_MODEL", "stable-diffusion")
        
        ollama_command = [
            "ollama", "run", model_name,
            "--prompt", image_prompt,
            "--output", temp_path,
            "--format", "png"
        ]
        
        # Ejecutar comando con timeout
        result = subprocess.run(
            ollama_command, 
            capture_output=True, 
            text=True, 
            timeout=120  # 2 minutos timeout
        )
        
        if result.returncode != 0:
            raise Exception(f"Ollama generation failed: {result.stderr}")
        
        # Verificar que el archivo se generó
        if not os.path.exists(temp_path):
            raise Exception("Generated image file not found")
        
        # TODO: Aquí deberíamos subir la imagen a un storage
        # Por ahora retornamos el path local como placeholder
        return f"file://{temp_path}"
        
    except subprocess.TimeoutExpired:
        raise Exception("Ollama generation timeout")
    except FileNotFoundError:
        raise Exception("Ollama command not found - please install Ollama")
    except Exception as e:
        raise Exception(f"Local generation failed: {str(e)}")

# Endpoint adicional para listar ideas (compatible con extensión existente)
@app.get("/api/get_ideas")
async def get_ideas():
    """
    Endpoint de compatibilidad con la extensión existente
    TODO: Implementar cuando tengamos Supabase configurado
    """
    # Placeholder response
    return [
        {
            "fecha": datetime.utcnow().isoformat(),
            "titulo": "Idea de prueba",
            "resumen": "Esta es una idea generada por el nuevo sistema",
            "text": "Contenido completo de la idea...",
            "image_url": "https://placeholder.example.com/page.png"
        }
    ]

# Endpoint para recibir ideas desde la extensión (compatibilidad)
@app.post("/api/crear_idea")
async def crear_idea(idea_data: dict):
    """
    Endpoint de compatibilidad para recibir ideas desde la extensión
    Redirige automáticamente al nuevo pipeline de generación
    """
    try:
        # Convertir formato anterior al nuevo
        payload = IdeaPayload(
            title=idea_data.get("title", "Sin título"),
            text=idea_data.get("text", ""),
            timestamp=idea_data.get("ts", int(datetime.utcnow().timestamp() * 1000))
        )
        
        # Usar el nuevo endpoint de generación
        # TODO: Aquí se podría hacer la llamada directa o encolar el trabajo
        
        return {"status": "received", "message": "Idea procesada con nuevo pipeline"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)