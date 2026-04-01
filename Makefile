.PHONY: git-init

git-init:
	git config core.hooksPath .githooks
	@echo "Git hooks configured."
