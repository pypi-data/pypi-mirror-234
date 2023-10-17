python3.10 -m venv venv  ## Use python 3.10.6 or higher
source venv/bin/activate
pip install poetry
poetry shell

poetry install
poetry publish --build