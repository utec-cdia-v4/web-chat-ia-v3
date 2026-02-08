# Frontend Web Chat IA

## Funcionalidades
- UI responsiva estilo ChatGPT
- Crear chats y mostrar historial
- Envio de prompts al backend y render de respuestas en Markdown

## Requisitos
- Node.js 22+
- Serverless Framework v4
- Variable `VITE_API_BASE` apuntando al API Gateway desplegado

## Despliegue a S3 con Serverless
1) Actualizar variable de entorno:
```
export VITE_API_BASE=Reemplaza_enlace_api
Ejemplo: export VITE_API_BASE=https://xxxxxxxx.execute-api.us-east-1.amazonaws.com/dev
```   
3) Instala dependencias:
```
npm install
```
3) Compila y despliega:
```
serverless deploy
```

El hook `before:deploy:deploy` construye la web automaticamente con Vite y sincroniza `dist/` al bucket S3 publico.

## Creditos
Creado con GitHub Copilot usando el modelo GPT-5.2-Codex.
Fecha de creacion: 8 de febrero de 2026.

## Prompt utilizado
"""
## Rol / Persona
Actua como un experto en crear Agentes de IA con servicios de AWS y apis de IA

## Contexto
Se necesita tener un Agente de IA que tenga memoria, para que pueda retener el contexto, y que sea completamente serverless

## Tarea / Objetivo 
Crea una web responsiva con estas funcionalidades:
- Crear un nuevo chat y colocar un titulo. Una vez dentro del chat:
  - Escribir una pregunta (prompt) que se enviara a la IA
  - Mostrar la respuesta de la IA que envia en formato markdown
  - Y asi sucesivamente
- Listar todos los chats:
  - Al elegir un chat se muestra todo el historial de preguntas y respuestas y se permite continuar el chat 

## Requisitos de la respuesta
- Para toda la IaC (Infraestructura como codigo) utiliza el framework serverless version 4.
- Para la web responsiva (FrontEnd) utiliza react.js con node.js version 22 o superior. Utiliza el servicio S3 de AWS para alojar la web. Automatiza la creacion de un bucket S3 publico, la construccion y el despliegue de la web con el framework serverless considerando el uso del rol de IAM LabRole existente.
- Para el BackEnd crea 1 microservicio o api rest (agente-ia). Utiliza estos servicios de AWS (Api Gateway, Lambda y para la memoria del historial de chat usa DynamoDB). Utiliza lenguaje de programacion python version 3.14. Debe utilizar el Api IA de Groq con el modelo "llama-3.3-70b-versatile". Automatiza el despliegue con el framework serverless considerando el uso del rol de IAM LabRole existente.
- Genera un readme.md para el proyecto completo y uno individual para la web y el microservicio con las funcionalidades que contiene y todas las instrucciones para hacer el despliegue automatico. Adicionalmente indica explicitamente que ha sido creado con GitHub Copilot, el modelo LLM usado, la fecha de creacion e incluye como referencia todo el texto del prompt utilizado.

## Elementos adicionales
- La web debe ser parecida a la de ChatGPT
"""

