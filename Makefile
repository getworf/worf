SETTINGS := postgres
WORF_SETTINGS_D := settings:tests/settings:tests/settings/$(SETTINGS)

# we add the virtualenv path to the PATH
export PATH := venv/bin:$(PATH)

.PHONY: format wheels update release

all: format test test-plugins

setup: virtualenv requirements node

node:
	npm ci

virtualenv:
	virtualenv --python python3 venv

requirements:
	# we install Worf itself
	pip install -e .

setup-plugins:
	# we install the plugins as well
	pip install -e ../worf-plugins/newsletter
	pip install -e ../worf-plugins/contact

test: test-api test-plugins

test-api:
	WORF_SETTINGS_D=$(WORF_SETTINGS_D) pytest $(args) tests
	
test-plugins:
	WORF_SETTINGS_D=$(WORF_SETTINGS_D) pytest $(args) worf/plugins

format:
	black worf/
	black tests/

mypy:
	mypy worf/
	mypy tests/

wheels:
	pip wheel --wheel-dir wheels -r requirements.txt

update:
	pip3 install pur
	pur -r requirements.txt

release:
	python3 setup.py sdist
	twine upload --skip-existing dist/* -u ${TWINE_USER} -p ${TWINE_PASSWORD}

assets: tailwind

tailwind:
	npx tailwindcss -i ./worf/app/assets/css/main.css -o ./worf/app/static/css/main.css --watch

sass:
	node_modules/.bin/sass worf/app/assets/scss/main.scss worf/app/static/css/main.css

