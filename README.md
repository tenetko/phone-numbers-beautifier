# phone-numbers-beautifier

This program takes several ugly Excel files and makes a finalized file with properly translated and extended values, along with some calculations based on quotas.

### Start backend locally

1. Install poetry as a dependency manager by [instructions](https://python-poetry.org/docs/#installation) (if you have already installed it, skip this step).

2. Proceed to the backend directory and install project dependencies using poetry:
    ```zsh
    cd backend
    poetry install
    ```

3. Create `.env` file:
    ```zsh
    PYTHONPATH=./
    ```

4. Launch the backend:
    ```zsh
    poetry run python -m uvicorn src.main:app --reload
    ```

5. Tests:
    ```zsh
    make test
    ```

6. Black:
     ```zsh
     make black
     make black-fix
     ```

7. Isort:
   ```zsh
   make isort
   make isort-fix
   ```

### Start frontend locally

1. Install yarn as a dependency manager: by [instructions](https://yarnpkg.com/getting-started/install) (if you have already installed it, skip this step).

2. Install project dependencies using yarn:
    ```zsh
    cd frontend
    yarn install
    ```

3. Launch the frontend:
    ```zsh
    yarn start
    ```
