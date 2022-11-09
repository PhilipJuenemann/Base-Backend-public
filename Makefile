install:
	@pip install -e ./packagefunctions

install_requirements:
	@pip install -r requirements.txt

run:
	uvicorn api.app:app --reload
