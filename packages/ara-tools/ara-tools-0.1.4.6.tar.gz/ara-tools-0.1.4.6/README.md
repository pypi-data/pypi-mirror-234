- [ara-tool](#ara-tool)
  - [best practices commit and merge and recreate workspace](#best-practices-commit-and-merge-and-recreate-workspace)
  - [test and run during development](#test-and-run-during-development)
  - [build and install locally for testing](#build-and-install-locally-for-testing)
  - [upload to test pypi with test pypi API key](#upload-to-test-pypi-with-test-pypi-api-key)
  - [upload to live pypi with talsen team production API key](#upload-to-live-pypi-with-talsen-team-production-api-key)


# ara-tool
## best practices commit and merge and recreate workspace
1. commit and publish everything in the branch
2. go to git and merge
3. destroy old workspace from merged branch from within the working directory
   > workspace destroy
4. go back in to top level working directory and check which repos are available for branching
   > workspace repos
5. create new workspacce with workspace command: workspace new <repo> <new-workspace-name>
   > workspace new ara-cmd hans-ara-cmd
6. switch to new workspace 
   
## test and run during development
1. run `bash deploy.sh`
2. run `bash login.sh`
3. --> in container --> for behave BDD tests `bash test-feature.sh` 
4. --> in container --> for unit tests in folder ara_tools `pytest --cov=. --cov-report term-missing tests/ `
5. --> in container --> example for running a single unit test in ara_tools folder `pytest tests/test_template_manager.py::test_files_created_from_template`
6. if change is successfull always commit before proceeding with next change
7. if change was successfully reviewd merge in gitlab: https://git.talsen.team/talsen-products/ara-tool/-/merge_requests/new

## build and install locally for testing
1. use `bash local_install.sh` to control local setup procedure

## upload to test pypi with test pypi API key
1. run `bash deploy.sh`
2. run `login.sh`
3. in `setup.py` increment `version` otherwise upload will fail! 
4. from inside container run `python setup.py sdist bdist_wheel`
5. run the following command: 
```bash
twine upload --repository testpypi dist/* --verbose -u __token__ -p pypi-AgENdGVzdC5weXBpLm9yZwIkZGI5YzUyZTUtNDhjMy00NmI3LTgxNmMtY2QwMTRjYjZmZjlmAAIqWzMsImM3ZTM0MDRmLWU1MzUtNDliMi05ZDhiLWQ0NGUyNzlmYTU0MiJdAAAGID-dX7aQZZimTyUQeKPzbP0TlqMEpLQlzRW7VJr1JKab
```

this will upload to a test pypi account
5. run `python3 -m pip install --index-url https://test.pypi.org/simple/ ara_tools==0.1.4` #you need to define the correct version number here
6. run `ara -h`
7. if everything has worked (upload, installation and usage) you can now continue to upload the package to pypi (live)


## upload to live pypi with talsen team production API key
1. run `bash deploy.sh`
2. run `login.sh`
3. `dist`should still be there from the testupload, do NOT upload to live without previously testing in test pypi!
4. run the following command: 
```bash
twine upload dist/* --verbose -u __token__ -p pypi-<API-Key>
``` 