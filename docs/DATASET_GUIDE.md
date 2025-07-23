# ID: DOC-DATASET-001-V01
# Guía del Dataset Manuscrito - IdeaScrawl Agenda

## Objetivo
Crear un dataset de imágenes de tu agenda manuscrita para entrenar un modelo LoRA personalizado en Leonardo AI que reproduzca tu estilo de escritura único.

## Especificaciones del Dataset

### Cantidad Requerida
- **Mínimo**: 15 imágenes
- **Recomendado**: 20-25 imágenes  
- **Óptimo**: 30+ imágenes (para mejor calidad)

### Tipos de Páginas a Incluir

#### 1. Páginas de Texto Puro (40% del dataset)
- Notas extensas en tu letra normal
- Párrafos completos con diferentes densidades de texto
- Páginas con lista de tareas o bullet points
- Texto en diferentes tamaños (títulos, subtítulos, contenido)

#### 2. Páginas con Elementos Gráficos (35% del dataset)
- Garabatos y doodles marginales
- Flechas conectando ideas
- Diagramas simples o mapas mentales
- Subrayados y círculos de énfasis
- Números y viñetas decorativas

#### 3. Páginas Mixtas/Orgánicas (25% del dataset)
- Combinación de texto limpio y elementos gráficos
- Correcciones y tachaduras naturales
- Diferentes presiones de escritura
- Espaciado irregular y natural
- Margenes utilizados creativamente

## Criterios de Calidad

### ✅ Características Deseadas
- **Resolución**: Mínimo 1024x1024 píxeles
- **Iluminación**: Natural y uniforme, sin sombras duras
- **Ángulo**: Perpendicular a la página, sin distorsión
- **Enfoque**: Completamente nítido en toda la imagen
- **Contraste**: Buena diferenciación entre tinta y papel

### ❌ Evitar
- Imágenes borrosas o desenfocadas
- Sombras que oculten parte del texto
- Ángulos inclinados > 5 grados
- Reflejos de flash o luces artificiales
- Páginas con muy poco contenido (< 30% ocupado)
- Tinta corrida o manchas extremas

## Variabilidad Necesaria

### Contenido
- **Idiomas**: Español principalmente, algo de inglés si es natural en tu escritura
- **Temas**: Variados (trabajo, personal, ideas, listas, reflexiones)
- **Longitud**: Desde frases cortas hasta páginas completas
- **Estructura**: Párrafos, listas, esquemas, texto libre

### Estilo Visual
- **Herramientas**: Bolígrafo azul/negro, lápiz, marcadores
- **Presión**: Variada (trazo ligero y fuerte)  
- **Velocidad**: Letra rápida y cuidadosa
- **Estado**: Páginas nuevas y algo usadas

### Elementos Gráficos
- **Flechas**: Rectas, curvas, decorativas
- **Marcos**: Cajas alrededor de texto importante
- **Conectores**: Líneas uniendo conceptos
- **Decoraciones**: Estrellas, círculos, puntos de énfasis

## Proceso de Captura

### 1. Preparación
- Limpia el espacio de trabajo
- Usa iluminación natural (cerca de ventana) o lámpara LED blanca
- Prepara cámara/smartphone con buena resolución
- Selecciona las páginas más representativas

### 2. Fotografía
```
Configuración recomendada:
- Resolución: Máxima disponible
- Formato: JPG (calidad alta)
- Flash: Desactivado
- HDR: Activado si disponible
- Estabilización: Activada
```

### 3. Naming Convention
Nombra los archivos de forma descriptiva:
```
alan_agenda_001_texto_puro.jpg
alan_agenda_002_garabatos_flechas.jpg  
alan_agenda_003_mixto_notas.jpg
alan_agenda_004_lista_tareas.jpg
```

## Preparación para Leonardo AI

### Tags Recomendados para el Entrenamiento
Al subir a Leonardo, usa estos tags descriptivos:

```
handwriting, personal notebook, alan style, cursive writing, 
natural spacing, doodles, arrows, organic layout, 
notebook page, handwritten notes, personal journal,
casual writing, blue ink, lined paper, authentic handwriting
```

### Prompt Base Sugerido
Para las generaciones, usa este prompt como base:
```
Handwritten notebook page in Alan's personal style, 
natural cursive writing with organic spacing, 
occasional doodles and arrows connecting ideas, 
authentic personal journal appearance, 
slightly yellowed paper texture
```

## Checklist de Validación

Antes de subir tu dataset, verifica:

- [ ] Al menos 15 imágenes de alta calidad
- [ ] Variedad en tipos de contenido (texto, gráficos, mixto)
- [ ] Diferentes herramientas de escritura representadas
- [ ] Buena iluminación y enfoque en todas las imágenes
- [ ] Resolución mínima de 1024x1024
- [ ] Naming convention consistente
- [ ] Sin información personal sensible visible
- [ ] Representativo de tu estilo natural de escritura

## Próximos Pasos

1. **Capturar dataset** siguiendo esta guía
2. **Subir a Leonardo AI** para entrenamiento LoRA
3. **Probar modelo** con 5 prompts de prueba
4. **Ajustar** si es necesario con imágenes adicionales
5. **Integrar** modelo ID en la configuración de la API

## Notas Adicionales

- **Privacidad**: Asegúrate de que no haya información personal sensible
- **Derechos**: Todas las imágenes deben ser de tu propia escritura
- **Tiempo de entrenamiento**: Leonardo suele tardar 15-30 minutos
- **Costo**: Verifica los créditos necesarios en tu cuenta de Leonardo

---

**¿Necesitas ayuda?** 
Si tienes dudas sobre algún aspecto del dataset, consulta la documentación de Leonardo AI o contacta soporte técnico.