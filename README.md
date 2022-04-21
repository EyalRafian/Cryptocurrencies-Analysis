# Cryptocurrencies Analysis (Streamlit + FastAPI)

-   [Description](#description)
-   [Quick start](#quick-start)
-   [Walk through](#walk-through)
    -   [File structure](#file-structure)
    -   [Demo](#Demo)
        
## Description

A streamlit app with FastAPI backend for crypto screening and analysis.
These microservices communicate with each other through HTTP.

## Quick start

Spin it all up

```sh
docker-compose build
```

```sh
docker-compose up -d
```

To visit the FastAPI documentation, visit http://localhost:8000/docs with a web browser.  
To visit the Streamlit UI, visit http://localhost:8501.

To bring it all down

```sh
docker-compose down --rmi all 
```

## Walk through

### Apps

The repository contains two microservices: FastAPI and Streamlit, using `FastAPI` for the backend service and `streamlit` for the frontend service. 
`docker-compose` orchestrates the two services and allows communication between them.

### File structure

```sh
├── README.md
├── docker-compose.yaml
├── backend
│   ├── Dockerfile
│   ├── main.py
│   ├── coins.db
│   ├── database.py
│   ├── models.py
│   └── requirements.txt
└── frontend
    ├── Dockerfile
    ├── streamlit.py
    └── requirements.txt
```

## Demo

![](Demo.gif)
