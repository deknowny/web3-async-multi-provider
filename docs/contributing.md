### Fork the project
Fork the project. All changes will be pushed to your own remote

### Clone the project
To contribute the project, firstly, fork it in GitHub and then clone the project from `main` branch of your fork

### Make a new branch
Create a new branch from `main`. You will do any changes in this branch

### Install project
Now we should create an environment for developing (requires poetry)
```shell
make install-dev-all
```
Now you are ready for integrating new features ✨

### Test your changes
Sure that your changes do not break anything and run unit test locally:
```shell
make test
```
Also check `mypy` report:
```shell
make check
```

### Push your changes
Push your changes to remote, and then you can view code tested in different platforms and python versions

### Prepare your code
The project uses `pre-commit` for linting, but if you have some troubles with git hooks, use linting by hand:
```shell
make format
```

### Create a pull request
Now you are ready to create a pull request with your new changes! We will answer you as soon as possible ☺️
