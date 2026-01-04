.PHONY: ruff-format ruff-check run-api install-deps help tf-init tf-plan tf-apply  aws-configure

aws-configure:
	cd scripts && chmod +x configure.sh && ./configure.sh

help:
	echo "ruff-check"
	echo "ruff-format"
	echo "install-deps" 

ruff-check:
	echo "Running ruff..."
	poetry run ruff check --fix src/

ruff-format: ruff-check
	echo "Running ruff..."
	poetry run ruff format src/

install-deps:
	poetry lock && poetry install 
	cd .devcontainer && pip3 install -r requirements.txt --break-system-packages

run-api:
	echo "Running FastAPI Server..."
	python3 -m src.main

# Terraform targets
tf-init:
	cd src/infra/terraform && terraform init
	cd src/infra/terraform && terraform validate

tf-plan: tf-init
	cd src/infra/terraform && terraform plan

tf-apply: tf-plan
	cd src/infra/terraform && terraform apply -auto-approve

tf-destroy:
	cd src/infra/terraform && terraform destroy -auto-approve