# Web Chat IA v2

## Descripcion
Proyecto serverless con una web estilo ChatGPT y un microservicio (agente-ia) con memoria en DynamoDB. La web consume un API REST y muestra respuestas en Markdown.

## Arquitectura
- Frontend: React + Vite (Node.js >= 24), desplegado en S3 publico
 - Frontend: React + Vite (Node.js >= 22), desplegado en S3 publico
- Backend: API Gateway + Lambda (Python 3.14) + DynamoDB
- IA: Groq API con modelo `llama-3.3-70b-versatile`
- IaC: Serverless Framework v4

## Estructura
- frontend/: web responsiva
- backend/: microservicio agente-ia

## Requisitos
- Node.js 22+
- Python 3.14 (local)
- Serverless Framework v4
- Credenciales AWS configuradas
- Variable `GROQ_API_KEY`

> Nota: AWS Lambda no ofrece runtime oficial para Python 3.14. El despliegue usa `python3.12` como runtime, pero el codigo y las dependencias estan preparados para Python 3.14 en desarrollo local.

## Despliegue
### 1) Backend
Sigue las instrucciones en [backend/README.md](backend/README.md).

### 2) Frontend
Sigue las instrucciones en [frontend/README.md](frontend/README.md).

## Creditos
Creado con GitHub Copilot usando el modelo GPT-5.2-Codex.
Fecha de creacion: 8 de febrero de 2026.

## Prompt utilizado
Nota: el prompt original menciona Node.js 24 o superior. El proyecto fue ajustado a Node.js 22+.
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
- Para la web responsiva (FrontEnd) utiliza react.js con node.js version 24 o superior. Utiliza el servicio S3 de AWS para alojar la web. Automatiza la creacion de un bucket S3 publico, la construccion y el despliegue de la web con el framework serverless considerando el uso del rol de IAM LabRole existente.
- Para el BackEnd crea 1 microservicio o api rest (agente-ia). Utiliza estos servicios de AWS (Api Gateway, Lambda y para la memoria del historial de chat usa DynamoDB). Utiliza lenguaje de programacion python version 3.14. Debe utilizar el Api IA de Groq con el modelo "llama-3.3-70b-versatile". Automatiza el despliegue con el framework serverless considerando el uso del rol de IAM LabRole existente.
- Genera un readme.md para el proyecto completo y uno individual para la web y el microservicio con las funcionalidades que contiene y todas las instrucciones para hacer el despliegue automatico. Adicionalmente indica explicitamente que ha sido creado con GitHub Copilot, el modelo LLM usado, la fecha de creacion e incluye como referencia todo el texto del prompt utilizado.

## Elementos adicionales
- La web debe ser parecida a la de ChatGPT
"""
