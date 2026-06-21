.PHONY: install build run test clean

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

build-indices:
	cd backend && python -c "from knowledge_base.builder import build_all; build_all()"

run-backend:
	cd backend && uvicorn main:app --reload --port 8000

run-frontend:
	cd frontend && npm run dev

run:
	docker-compose up --build

test:
	cd backend && pytest tests/ -v

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
