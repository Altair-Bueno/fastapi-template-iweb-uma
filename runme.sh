#!/bin/zsh

VENV_FOLDER='.venv'
ACTIVATE_VENV="source '$VENV_FOLDER/bin/activate'"
ART='
              _
            ,/A\\,
          .//`_`\\\\,
        ,//`____-`\\\\,
      ,//`[_CORE__]`\\\\,
    ,//`=  ==  __-  _`\\\\,
   //|__=  __- == _  __|\\\\
   ` |  __ .-----.  _  | `
     | - _/       \-   |
     |__  | .-"-. | __=|
     |  _=|/)   (\|    |
     |-__ (/ a a \) -__|
jgs  |___ /`\_Y_/`\____|
          \)8===8(/'

echo "Creating virtual environment"
python3 -m venv "$VENV_FOLDER"
eval $ACTIVATE_VENV

echo "Installing requirements"
python3 -m pip install -r requirements.txt

echo "Generating .env"
echo "mongo_url=mongodb://iweb:strongpassword@localhost:27017
mongo_collection=TODO
mongo_database=TODO
" > .env

echo "
############################################################

$ART

## TODO LIST ##
- Update Docker Compose with the required environment variables
- Update .env with the required environment variables
- Update iweb/iweb.py with the required variables

Before doing anything:

  docker compose up -d mongodb
  $ACTIVATE_VENV
  uvicorn --reload --port 8000 --host 127.0.0.1 src:app

Before finishing the exam:

  curl localhost:8000/openapi.json > openapi.json

Good luck!
"