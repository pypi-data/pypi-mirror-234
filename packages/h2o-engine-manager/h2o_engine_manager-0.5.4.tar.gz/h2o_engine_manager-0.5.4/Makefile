build:
	hatch build

clean-build:
	rm -rf dist

test-unit:
	hatch run test:unit -v

test-api:
	hatch run test:api -v

test-e2e:
	hatch run test:e2e -v

test-admission-webhook:
	hatch run test:admission-webhook

lint-check:
	hatch run lint:check -v

lint-fix:
	hatch run lint:fix -v

generate-docs:
	hatch run docs:generate