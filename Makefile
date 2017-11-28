# make install args=-vvv
.DEFAULT_GOAL := help
INVENTORY=$(realpath ./inventory.ini)

.PHONY: help
help: ## provides cli help for this make file (default)
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: ansible_documentation
ansible_documentation: ## show the task list ansible will execute
	ansible-playbook --list-tasks -i "localhost," playbooks/site.yml

.PHONY: lint
lint: ## check ansible playbooks syntax
	ansible-playbook --syntax-check -i "localhost," playbooks/site.yml

.PHONY: tests
tests: ## run automatic testings
	python -u -m unittest discover tests '*_test.py'

.PHONY: install
install: ssh.config ## install the infrastructure on vagrant vm
	ansible-playbook -i ${INVENTORY} ${args} playbooks/site.yml

.PHONY: install_requirements
install_requirements: ## install ansible galaxy requirements from requirements.yml in roles subdirectory
	ansible-galaxy install ${args} -r requirements.yml

.PHONY: ping
ping: ## check if ansible can communicate with the hosts referenced in inventory.ini
	ansible -i ${INVENTORY} all -m ping
