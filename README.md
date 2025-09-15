# my-backend-fastapi

1) backend_app.py ---> deploying on Web-server

2) models_data.json ---> list of available {models\weights}

3) Procfile.txt ---> used for: server Build Command, but some servers ask to fill in manually

4) requirements.txt ---> used for: install the dependencies

5) install_weights.sh ---> used for: download model weights from another source {currently from hugging_face_hub storage}

 Work sequence:
     If the server asks, Build Command fill in manually then:
                       - backend_app.py --> models_data.json --> requirements.txt --> install_weights.sh
     else:
                       - backend_app.py --> models_data.json --> Procfile.txt


# BUILDING SCRIPT/BUILDING COMMAND
  In the command prompt fill in --> pip install -r requirements.txt && bash install_weights.sh

# STARTING COMMAND
  In the command prompt fill in --> uvicorn backend_app:app --host 0.0.0.0 --port $PORT

After the server is deployed, it will give a URL like --> "https://my-backend-fastapi.onrender.com/models"
