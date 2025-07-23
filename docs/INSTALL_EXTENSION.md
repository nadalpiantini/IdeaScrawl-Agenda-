# Instalar Extensión IdeaScrawl

## Pasos para Chrome

1. **Abrir extensiones**: Ve a `chrome://extensions/`

2. **Modo desarrollador**: Activa el switch "Modo desarrollador" (Developer mode)

3. **Cargar extensión**: 
   - Clic en "Cargar extensión descomprimida" (Load unpacked)
   - Selecciona esta carpeta: `/Users/nadalpiantini/Documents/Github/IdeaScrawl Agenda`

4. **Verificar instalación**:
   - Deberías ver "IdeaScrawl Agenda" en la lista
   - El icono aparecerá en la barra de extensiones

## Probar Funcionamiento

1. **Ir a ChatGPT**: Abre [chat.openai.com](https://chat.openai.com)

2. **Escribir mensajes**: Envía 2-3 mensajes normales

3. **Ver resultados**: 
   - Clic en el icono de IdeaScrawl
   - Deberías ver tus mensajes capturados
   - Clic en "Ver página" para ver la imagen simulada

## Estado Actual

✅ **API funcionando** en `http://localhost:8000`  
✅ **Modo demo** con imágenes placeholder  
⏳ **Esperando**: Tu dataset + Leonardo API key para generación real

## Troubleshooting

**No captura mensajes**: Verifica que estés en chat.openai.com  
**Error de conexión**: Confirma que API esté corriendo en puerto 8000  
**No aparece la extensión**: Recarga la página de extensiones  

## Próximo Paso

Una vez que veas funcionar el demo:
1. Crear dataset manuscrito (ver DATASET_GUIDE.md)
2. Obtener Leonardo API key
3. Actualizar .env con la key real
4. ¡Disfrutar páginas manuscritas reales!