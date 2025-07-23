# IdeaScrawl Agenda - Especificación de Requisitos

**ID Documento**: DOC-REQ-001-V01  
**Fecha**: 2025-07-23  
**Versión**: 1.0  
**Autor**: Sistema de Documentación Automática  

## Control de Versiones del Documento

| Versión | Fecha | Cambios | ID Actualizado |
|---------|-------|---------|----------------|
| 1.0 | 2025-07-23 | Creación inicial del documento | DOC-REQ-001-V01 |

## Información del Proyecto

**Nombre**: IdeaScrawl Agenda  
**Tipo**: Extensión de Chrome  
**Versión**: 0.1.0  
**Propósito**: Captura automática de ideas desde ChatGPT y gestión centralizada

## Arquitectura de Componentes

| Componente | Archivo | ID Tag | Versión | Responsabilidad |
|------------|---------|--------|---------|-----------------|
| Manifiesto | manifest.json | MAN-001 | V01 | Configuración de extensión |
| Service Worker | background.js | BG-001 | V01 | Procesamiento de mensajes |
| Content Script | content.js | CNT-001 | V01 | Observación DOM de ChatGPT |
| Popup UI | popup.html | POP-001 | V01 | Interfaz de usuario |
| Popup Logic | popup.js | POPJS-001 | V01 | Lógica de visualización |

## Requisitos Funcionales

### REQ-F-001-V01: Captura Automática de Mensajes
**Descripción**: El sistema debe capturar automáticamente mensajes nuevos en ChatGPT  
**Prioridad**: Alta  
**Componentes**: CNT-001, BG-001  
**Criterios de Aceptación**:
- Detectar mensajes añadidos al DOM de ChatGPT
- Extraer título del chat y contenido del mensaje
- Enviar datos al service worker

### REQ-F-002-V01: Transmisión de Datos
**Descripción**: Los mensajes capturados deben enviarse a una API externa  
**Prioridad**: Alta  
**Componentes**: BG-001  
**Criterios de Aceptación**:
- Envío POST a endpoint configurado
- Formato JSON con título, texto y timestamp  
- Manejo de errores de red

### REQ-F-003-V01: Visualización de Ideas
**Descripción**: Mostrar ideas guardadas en popup de extensión  
**Prioridad**: Media  
**Componentes**: POP-001, POPJS-001  
**Criterios de Aceptación**:
- Cargar ideas desde API externa
- Mostrar fecha, título y resumen
- Manejo de estados vacío y error

### REQ-F-004-V01: Gestión de Estado de Carga
**Descripción**: Indicar estados de carga y error al usuario  
**Prioridad**: Media  
**Componentes**: POPJS-001  
**Criterios de Aceptación**:
- Mostrar "Cargando..." durante fetch
- Mostrar "No hay ideas aún" si lista vacía
- Mostrar mensaje de error en caso de fallo

## Requisitos Técnicos

### REQ-T-001-V01: Manifest V3 Compliance
**Descripción**: Cumplir con especificaciones de Manifest V3  
**Prioridad**: Alta  
**Componentes**: MAN-001  
**Detalles**:
- Service worker en lugar de background pages
- Permisos mínimos necesarios
- Host permissions específicos

### REQ-T-002-V01: Permisos de Seguridad
**Descripción**: Configurar permisos mínimos necesarios  
**Prioridad**: Alta  
**Componentes**: MAN-001  
**Permisos Requeridos**:
- `storage`: Almacenamiento local
- `tabs`: Acceso a información de pestañas  
- `activeTab`: Interacción con pestaña activa
- `scripting`: Inyección de scripts
- `https://chat.openai.com/*`: Acceso a ChatGPT

### REQ-T-003-V01: Observación DOM Eficiente
**Descripción**: Monitorear cambios DOM sin impacto en rendimiento  
**Prioridad**: Media  
**Componentes**: CNT-001  
**Especificaciones**:
- MutationObserver con configuración optimizada
- Filtrado específico de elementos relevantes
- Prevención de eventos duplicados

### REQ-T-004-V01: API Externa Integration
**Descripción**: Comunicación con endpoints externos  
**Prioridad**: Alta  
**Componentes**: BG-001, POPJS-001  
**Endpoints**:
- POST `/api/crear_idea`: Crear nueva idea
- GET `/api/get_ideas`: Obtener lista de ideas
- Content-Type: application/json
- Credentials: include para autenticación

### REQ-T-005-V01: UI Responsiva
**Descripción**: Interfaz adaptable y usable  
**Prioridad**: Media  
**Componentes**: POP-001  
**Especificaciones**:
- Ancho fijo: 320px
- Tipografía sans-serif
- Separadores visuales entre elementos
- Colores accesibles (#333, #ddd)

## Matriz de Trazabilidad

| Requisito | Componente Principal | Componentes Secundarios | Prioridad |
|-----------|---------------------|-------------------------|-----------|
| REQ-F-001-V01 | CNT-001 | BG-001 | Alta |
| REQ-F-002-V01 | BG-001 | - | Alta |
| REQ-F-003-V01 | POPJS-001 | POP-001 | Media |
| REQ-F-004-V01 | POPJS-001 | - | Media |
| REQ-T-001-V01 | MAN-001 | - | Alta |
| REQ-T-002-V01 | MAN-001 | - | Alta |
| REQ-T-003-V01 | CNT-001 | - | Media |
| REQ-T-004-V01 | BG-001 | POPJS-001 | Alta |
| REQ-T-005-V01 | POP-001 | - | Media |

## Control de Cambios de Componentes

### Proceso de Actualización
1. **Identificación**: Cada cambio debe incluir actualización de ID tag
2. **Versionado**: Incrementar versión en formato VXX
3. **Trazabilidad**: Actualizar matriz de trazabilidad si es necesario
4. **Documentación**: Registrar cambio en tabla de control de versiones

### Formato de ID Tags
- **Archivos de configuración**: `<!-- ID: XXX-YYY-VZZ -->`
- **Archivos JavaScript**: `// ID: XXX-YYY-VZZ`
- **Archivos HTML**: `<!-- ID: XXX-YYY-VZZ -->`

Donde:
- XXX: Prefijo del componente (MAN, BG, CNT, POP, POPJS)
- YYY: Número secuencial (001, 002, ...)
- VZZ: Versión (V01, V02, ...)

## Notas de Implementación

### Dependencias Externas
- API externa en `https://tu-dominio.com/`
- DOM de ChatGPT (selectores: `h1`, `.group > div`)

### Consideraciones de Seguridad
- Validación de mensajes entre componentes
- Sanitización de contenido HTML en popup
- Manejo seguro de credenciales en API calls

### Limitaciones Conocidas
- Dependiente de estructura DOM específica de ChatGPT
- URL de API hardcodeada (requiere configuración)
- Sin manejo de offline/retry logic

## Próximos Pasos
1. Configurar URL de API externa
2. Implementar manejo de errores robusto
3. Añadir tests unitarios
4. Considerar persistencia local como fallback