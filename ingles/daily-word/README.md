# The Words of Tomorrow · Scale Go

Web estática, sin servidor ni registro. Abre `https://scalego.github.io/ingles/daily-word/`.

## Datos para agentes

`https://scalego.github.io/ingles/daily-word/words.json` es el banco abierto con audio OGG en el subdirectorio `audio/`. `https://scalego.github.io/api/index.json` documenta el algoritmo. Para un día desde el 25-09-2026: `day` = diferencia de días calendario en UTC entre la fecha elegida y el 25-09-2026. Para cada nivel y cantidad `n` (1, 5 o 10), toma los elementos en posiciones `(day*n+i) % total` con `i` desde 0 a `n-1`. Calcula la fecha de hoy en Europe/Madrid; mañana es el siguiente día de calendario. No consultes `/api/today.json`: un archivo estático no puede actualizarse a medianoche. Hay dos muestras explícitas: `/api/2026-09-25.json` y `/api/2026-09-26.json`. Las incorporaciones se agregan al final de cada nivel: las selecciones del 25 y 26 de septiembre de 2026 siguen intactas para 1, 5 y 10 palabras. Los dos archivos fechados de la API son inmutables. Para ampliaciones futuras que alteren selecciones ya vistas, habrá que fijar una tabla por fecha o versionar el algoritmo.

## Audios

Grabaciones humanas de Wikimedia Commons. Cada entrada incluye `source` y `license` propios; atribuye siempre al autor y enlaza a la ficha de origen si reutilizas el audio. Los ejemplos y traducciones de esta herramienta son originales. Se han evitado voces sintéticas. La app incluye el audio en el JSON para no depender de hotlinks.

## Banco

Amplíalo añadiendo objetos a los arrays `A2`, `B1` y `B2` de `words.json`, con `word`, `meaning`, `example`, `translation`, `note`, `ipa` (solo si verificada), `audio` (nombre de archivo OGG), `source` y `license`. A 26-09-2026: A2 56, B1 52, B2 68 (176 en total). Las listas rotan cuando se agotan. Los 97 audios añadidos son grabaciones humanas de Dvortygirl tomadas de Commons bajo CC BY-SA 3.0; cada entrada enlaza su ficha de origen y conserva autor y licencia. Las IPA presentes proceden de la sección inglesa de Wiktionary; si no se verificó una transcripción, el campo queda vacío. Los ejemplos y traducciones añadidos son originales. El progreso de aprendidas y la racha viven solo en localStorage de cada dispositivo.

Nota: los dos archivos `/api/2026-09-25.json` y `/api/2026-09-26.json` son ejemplos concretos, no un endpoint diario que se renueva. Para fechas futuras, consulta `/api/index.json` y el banco con el algoritmo indicado. GitHub Pages no calcula rutas JSON dinámicas ni envía cabeceras CORS personalizadas; los archivos públicos suelen ser accesibles por herramientas HTTP normales, pero una web alojada en otro origen puede tener restricciones CORS.
