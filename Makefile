ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.DEFAULT_GOAL := help

.PHONY: help
help:	## Show this help
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: run
run: ## Run development environment
	cd ccpsite && python manage.py runserver

.PHONY: clean
clean: ## Clean environment
	rm ccpsite/db.sqlite3 || true

.PHONY: clean-migrations
clean-migrations: ## Clean environment
	rm -rf ccpsite/results/migrations/00*.py
	rm -rf ccpsite/tournamentsw/migrations/00*.py
	rm -rf ccpsite/universaltennis/migrations/00*.py
	rm -rf ccpsite/ranking/migrations/00*.py

.PHONY: initialize
initialize: clean clean-migrations migrations migrate ## Initialize environment
	cd ccpsite && python manage.py createsuperuser --noinput || true
	cd ccpsite && python manage.py loaddata --app universaltennis */fixtures/*.json
	cd ccpsite && python manage.py loaddata --app ranking */fixtures/*.json
	cd ccpsite && python manage.py loaddata --app results */fixtures/*.json

.PHONY: migrations
migrations: ## Make migrations files
	cd ccpsite && python manage.py makemigrations

.PHONY: migrate
migrate: ## Apply migrations
	cd ccpsite && python manage.py migrate

.PHONY: fixtures
fixtures: ## Create fixtures
	cd ccpsite && python manage.py dumpdata ranking.category --format=json > ranking/fixtures/category.json
	cd ccpsite && python manage.py dumpdata ranking.player --format=json > ranking/fixtures/player.json
	cd ccpsite && python manage.py dumpdata results.matchtype --format=json > results/fixtures/matchtype.json
	cd ccpsite && python manage.py dumpdata results.source --format=json > results/fixtures/source.json
	cd ccpsite && python manage.py dumpdata results.singlesresult --format=json > results/fixtures/singlesresult.json
	cd ccpsite && python manage.py dumpdata universaltennis.player --format=json > universaltennis/fixtures/player.json
