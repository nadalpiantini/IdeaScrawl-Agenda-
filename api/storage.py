# ID: API-STORAGE-001-V01
"""
IdeaScrawl Agenda - Supabase Storage Integration
Módulo para manejar almacenamiento de imágenes generadas
"""

import os
import uuid
import requests
from typing import Optional, Tuple
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseStorage:
    """
    Cliente para manejar storage de imágenes en Supabase
    """
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.bucket_name = os.getenv("STORAGE_BUCKET", "pages")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be configured")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
    
    async def upload_image_from_url(self, image_url: str, idea_id: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Descarga una imagen desde una URL y la sube a Supabase Storage
        
        Args:
            image_url: URL de la imagen generada (Leonardo API o local)
            idea_id: ID único de la idea para nombrar el archivo
            
        Returns:
            Tuple[success, public_url, error_message]
        """
        try:
            # Descargar imagen
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            image_data = response.content
            file_extension = self._get_file_extension(image_url)
            file_path = f"generated/{idea_id}{file_extension}"
            
            # Subir a Supabase Storage
            result = self.client.storage.from_(self.bucket_name).upload(
                file_path, 
                image_data,
                file_options={"content-type": "image/png"}
            )
            
            if result.error:
                return False, None, f"Upload failed: {result.error.message}"
            
            # Obtener URL pública
            public_url = self.client.storage.from_(self.bucket_name).get_public_url(file_path)
            
            return True, public_url.public_url, None
            
        except requests.RequestException as e:
            return False, None, f"Failed to download image: {str(e)}"
        except Exception as e:
            return False, None, f"Storage error: {str(e)}"
    
    async def upload_local_file(self, file_path: str, idea_id: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Sube un archivo local a Supabase Storage
        
        Args:
            file_path: Path local del archivo (ej: desde Ollama)
            idea_id: ID único de la idea
            
        Returns:
            Tuple[success, public_url, error_message]
        """
        try:
            if not os.path.exists(file_path):
                return False, None, "Local file not found"
            
            with open(file_path, 'rb') as file:
                file_data = file.read()
            
            file_extension = os.path.splitext(file_path)[1] or '.png'
            storage_path = f"generated/{idea_id}{file_extension}"
            
            # Subir a Supabase
            result = self.client.storage.from_(self.bucket_name).upload(
                storage_path,
                file_data,
                file_options={"content-type": "image/png"}
            )
            
            if result.error:
                return False, None, f"Upload failed: {result.error.message}"
            
            # Obtener URL pública
            public_url = self.client.storage.from_(self.bucket_name).get_public_url(storage_path)
            
            # Limpiar archivo temporal
            try:
                os.unlink(file_path)
            except:
                pass  # No es crítico si no se puede borrar
            
            return True, public_url.public_url, None
            
        except Exception as e:
            return False, None, f"Local upload error: {str(e)}"
    
    def _get_file_extension(self, url: str) -> str:
        """
        Extrae la extensión del archivo desde una URL
        """
        # Intentar extraer de la URL
        if url.lower().endswith('.jpg') or url.lower().endswith('.jpeg'):
            return '.jpg'
        elif url.lower().endswith('.png'):
            return '.png'
        elif url.lower().endswith('.webp'):
            return '.webp'
        else:
            return '.png'  # Default
    
    async def delete_image(self, file_path: str) -> bool:
        """
        Elimina una imagen del storage
        
        Args:
            file_path: Path del archivo en storage (ej: "generated/idea-123.png")
            
        Returns:
            True si se eliminó correctamente
        """
        try:
            result = self.client.storage.from_(self.bucket_name).remove([file_path])
            return not result.error
        except:
            return False
    
    async def list_user_images(self, user_id: str, limit: int = 50) -> list:
        """
        Lista las imágenes de un usuario específico
        TODO: Implementar cuando tengamos autenticación
        
        Args:
            user_id: ID del usuario
            limit: Número máximo de imágenes a retornar
            
        Returns:
            Lista de URLs públicas
        """
        try:
            # Por ahora retornamos lista vacía
            # En el futuro aquí filtraremos por user_id
            result = self.client.storage.from_(self.bucket_name).list(
                path="generated/",
                limit=limit
            )
            
            if result.error:
                return []
            
            # Convertir a URLs públicas
            public_urls = []
            for file_info in result.data:
                if file_info.get('name'):
                    public_url = self.client.storage.from_(self.bucket_name).get_public_url(
                        f"generated/{file_info['name']}"
                    )
                    public_urls.append(public_url.public_url)
            
            return public_urls
            
        except:
            return []

# Instancia global para usar en la API
storage_client = None

def get_storage_client() -> SupabaseStorage:
    """
    Obtiene una instancia del cliente de storage (singleton)
    """
    global storage_client
    if storage_client is None:
        storage_client = SupabaseStorage()
    return storage_client