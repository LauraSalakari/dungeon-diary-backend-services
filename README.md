# Dungeon Diary
## AI-powered solutions to Dungeons & Dragons problems

### Project Goal
I wanted to solve problems I encounter around the table: 
knowing the intricacies of rules and requirements, and keeping up with what's going on.
- Retrieval-Augmented Generation to support a chatbot to answer questions about the basics and rules of the game
- LLM-powered summary generation to ease collaborative note-taking


### Technical Overview
This repository contains the python server that serves as the brains of the application.
It handles all API calls from the web application, and communicates with the database, vector store and LLM.
- API/Web Framework: FastAPI
- Database: MongoDB
- Vector Store: ChromaDB (contained in this repo)
- Embedding model: [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- LLM: Ministral-3 (Ministral-3-8B-Instruct-2512, deployed locally in a Docker container with the [vllm/vllm-openai](https://hub.docker.com/r/vllm/vllm-openai/tags) image)

The web-UI built with React and TypeScript can be found in a separate repository [here](https://github.com/LauraSalakari/dungeon-diary-frontend).

### Future feature wishlist
- Notes from voice memos or recordings
- Notes from OCR
- RAG for world lore and notes
- RAG memory/context
- AI-powered character creation assistant
- Character Sheets
- Character/NPC Compendium
- UI Improvements
- Deployment