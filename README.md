Solstrom app build using [React.js](https://react.dev/)

## Prerequisite

| Prerequisite | Version          |
| ------------ | ---------------- |
| Node         | Latest (v21.2.0) |
| NPM          | Latest (v10.2.3) |
| Python       | >= v3.10         |
| Typescript   | Latest (v4.8.3)  |
| FastAPI      | >= 0.115.0       |
| Uvicorn      | >= 0.34.0        |

## Getting Started

### Installation (Frontend)

Navigate to the strom-app directory:

```bash
  cd strom-app
  npm install
```

Copy the contents of .env.template into a new .env file and update the variables:

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Installation (Backend)

Navigate to the solstrom-server directory:

```bash
  cd solstrom-server
  pip install -r requirements.txt
```

Create a .env file using the below template:

```py
  QDRANT_API_KEY=
  QDRANT_API_URL=
  CLAUDE_API_KEY=
```

Run the backend server:

```bash
python main.py
```

API will be available at [http://localhost:8001](http://localhost:8001)

## Frontend File Structure

    .
    ├── public/
    ├── src/
    │   ├── common/
    │   │   ├── api.service.ts
    │   │   └── types.ts
    │   ├── components/
    │   │   ├── TypingLoader/
    │   ├── styles/
    │   ├── utils/
    │   └── App.tsx
    ├── .env
    └── package.json

## Backend File Structure

    .
    ├── app/
    │   ├── agent/
    │   ├── dbhandlers/
    │   ├── external_service/
    │   ├── models/
    │   ├── routes/
    │   ├── services/
    │   ├── utils/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── constants.py
    │   └── custom_fastapi/
    ├── .env
    ├── main.py
    └── requirements.txt


## Design Overview

- Frontend (React):

    - Built using React with Typescript and SCSS.

    - Clean and modular component structure.

    - Centralized API handling and type definitions.

    - Easily customizable and maintainable codebase.

- Backend (FastAPI + Claude + Qdrant):
    
    - FastAPI-based backend serving REST APIs.

    - Claude AI integration for intelligent responses.
    
    - Qdrant vector search service used for semantic indexing.
    
    - Environment-variable-based config for secure and flexible deployments.


## Hosted URL
[https://solstrom.web.app](https://solstrom.web.app)