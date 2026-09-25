# The Words of Tomorrow · Scale Go

Web estática, sin servidor ni registro. Abre `https://scalego.github.io/ingles/daily-word/`.

## Datos para agentes

`https://scalego.github.io/ingles/daily-word/words.json` es el banco abierto con audio OGG en el subdirectorio `audio/`. `https://scalego.github.io/api/index.json` documenta el algoritmo. Para un día desde el 25-09-2026: `day` = diferencia de días calendario en UTC entre la fecha elegida y el 25-09-2026. Para cada nivel y cantidad `n` (1, 5 o 10), toma los elementos en posiciones `(day*n+i) % total` con `i` desde 0 a `n-1`. Calcula la fecha de hoy en Europe/Madrid; mañana es el siguiente día de calendario. No consultes `/api/today.json`: un archivo estático no puede actualizarse a medianoche. Hay dos muestras explícitas: `/api/2026-09-25.json` y `/api/2026-09-26.json`. La selección cambia de orden si se amplía la lista; para preservar un archivo inmutable habrá que fijar una tabla por fecha.

## Audios

Grabaciones humanas de Wikimedia Commons. Cada entrada incluye `source` y `license` propios; atribuye siempre al autor y enlaza a la ficha de origen si reutilizas el audio. Los ejemplos y traducciones de esta herramienta son originales. Se han evitado voces sintéticas. La app incluye el audio en el JSON para no depender de hotlinks.

## Banco

Amplíalo añadiendo objetos a los arrays `A2`, `B1` y `B2` de `words.json`, con `word`, `meaning`, `example`, `translation`, `note`, `ipa` (solo si verificada), `audio` (nombre de archivo OGG), `source` y `license`. A 25-09-2026: A2 30, B1 27, B2 22. No llega aún a 300 por nivel: las listas rotan cuando se agotan. El progreso de aprendidas y la racha viven solo en localStorage de cada dispositivo.

Nota: los dos archivos `/api/2026-09-25.json` y `/api/2026-09-26.json` son ejemplos concretos, no un endpoint diario que se renueva. Para fechas futuras, consulta `/api/index.json` y el banco con el algoritmo indicado. GitHub Pages no calcula rutas JSON dinámicas ni envía cabeceras CORS personalizadas; los archivos públicos suelen ser accesibles por herramientas HTTP normales, pero una web alojada en otro origen puede tener restricciones CORS.
