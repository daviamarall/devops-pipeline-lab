.PHONY: help install run test lint docker-build docker-run compose-up clean

help:
	@echo "install      - instala dependências"
	@echo "run          - roda a API local (reload)"
	@echo "test         - executa os testes"
	@echo "lint         - roda o ruff"
	@echo "docker-build - build da imagem"
	@echo "docker-run   - roda a imagem"
	@echo "compose-up   - sobe com Docker Compose"
	@echo "clean        - limpa caches"

install:
	pip install -r requirements.txt -r requirements-dev.txt

run:
	uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -q

lint:
	ruff check src tests

docker-build:
	docker build -t devops-pipeline-lab:local .

docker-run:
	docker run --rm -p 8000:8000 devops-pipeline-lab:local

compose-up:
	docker compose up --build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache .mypy_cache
