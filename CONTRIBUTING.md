# Contributing to IdeaScrawl Agenda

¡Gracias por tu interés en contribuir! 🎉

## 🚀 Quick Start for Contributors

1. **Fork** el repositorio
2. **Clone** tu fork localmente
3. **Setup** el entorno de desarrollo:
   ```bash
   ./scripts/start_dev.sh
   ```
4. **Create** una nueva branch para tu feature:
   ```bash
   git checkout -b feature/amazing-feature
   ```

## 📋 Development Workflow

### Before Starting
- [ ] Revisa issues existentes para evitar duplicados
- [ ] Comenta en el issue que planeas trabajar en él
- [ ] Fork el repo y crea tu branch

### While Developing
- [ ] Sigue las convenciones de código existentes
- [ ] Añade tests si es posible
- [ ] Actualiza documentación si es necesario
- [ ] Usa commits descriptivos

### Before Submitting
- [ ] Prueba tu código localmente
- [ ] Ejecuta `./scripts/test_api.sh`
- [ ] Verifica que la extensión Chrome funciona
- [ ] Actualiza .metadata si añades nuevos archivos

## 🏗️ Architecture Overview

```
extension/     # Chrome Extension (JavaScript)
api/          # FastAPI Backend (Python)
docs/         # Documentation (Markdown)
scripts/      # Development utilities (Bash)
```

## 🔧 Component Guidelines

### Chrome Extension
- Mantén manifest.json como JSON válido (sin comentarios)
- Usa console.log con prefijo "🚀 IdeaScrawl:"
- Implementa error handling robusto
- Rate limiting para API calls

### FastAPI Backend
- Usa type hints en Python
- Implementa proper error responses
- Documenta endpoints con docstrings
- Mantén compatibilidad con demo mode

### Documentation
- Mantén README.md actualizado
- Usa emojis para mejor legibilidad
- Incluye ejemplos prácticos
- Actualiza .metadata para nuevos archivos

## 🐛 Bug Reports

Cuando reportes un bug, incluye:
- Descripción clara del problema
- Pasos para reproducir
- Entorno (OS, Chrome version, etc.)
- Logs relevantes
- Screenshots si aplica

## ✨ Feature Requests

Para nuevas features:
- Explica el caso de uso
- Describe la solución propuesta
- Considera alternativas
- Piensa en backward compatibility

## 📝 Commit Messages

Usa mensajes descriptivos:
```
feat: add Leonardo API integration
fix: resolve manifest JSON parsing error
docs: update installation guide
refactor: organize extension folder structure
```

## 🧪 Testing

Antes de hacer PR:

```bash
# Test API
./scripts/test_api.sh

# Test Extension manually
# 1. Load in Chrome
# 2. Go to ChatGPT  
# 3. Verify capture works
# 4. Check popup displays ideas
```

## 📦 Pull Request Process

1. **Update** documentation si es necesario
2. **Test** thoroughly en tu entorno local
3. **Create** PR con descripción clara
4. **Link** related issues
5. **Wait** for review y address feedback

### PR Template
```markdown
## Changes
- [ ] Bug fix
- [ ] New feature  
- [ ] Documentation
- [ ] Refactoring

## Description
Brief description of changes...

## Testing
- [ ] API tests pass
- [ ] Extension loads without errors
- [ ] Manual testing completed

## Related Issues
Fixes #123
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Leonardo API error handling improvements
- [ ] Extension UI/UX enhancements
- [ ] Better test coverage
- [ ] Performance optimizations

### Medium Priority  
- [ ] Supabase integration completion
- [ ] Dashboard web development
- [ ] Mobile compatibility
- [ ] Internationalization

### Documentation
- [ ] API documentation improvements
- [ ] Video tutorials
- [ ] Troubleshooting guides
- [ ] Architecture diagrams

## 🤝 Community

- **Issues**: Para bugs y feature requests
- **Discussions**: Para preguntas generales
- **Code Review**: Todos los PRs necesitan review

## 📄 License

Al contribuir, aceptas que tu código será licenciado bajo la misma licencia que el proyecto.

---

¿Questions? ¡Abre un issue y te ayudamos! 🚀