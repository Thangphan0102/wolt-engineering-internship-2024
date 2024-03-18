# Wolt engineering internship assignment 2024

## Running the application

### With Docker

**Running the app**

Run the app:

```bash
docker compose up
```

The API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:800/docs).

### Without Docker

**Prerequisites:**

- Python 3.10 or later

Setting up the environment:

**Create a virtual environment:**

```bash
python3 -m venv venv
```

**Activate the virtual environment:**

- Linux / MacOS:

    ```bash
    source .venv/bin/activate
    ```

**Install the dependencies:**

```bash
pip install -r dev-requirements.txt
```

**Running the app:**

```bash
uvicorn app.main:app
```

The API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:800/docs).

**Tests**

```bash
pytest
```

## Using the API

### Available endpoint(s)

| URL                             | Method     | Functionality              |
|---------------------------------|------------|----------------------------|
| ```api/v1/fees/calculate_fee``` | ```POST``` | Calculate the delivery fee |

### ```/api/v1```
- #### ```/fees```
    - ##### ```/calculate_fee```

        **Example request:**

        Request body:

        ```json
        {
        "cart_value": 790,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z"
        }
        ```

        Using curl:

        ```bash
        curl -X "POST" \
            "http://127.0.0.1:8000/api/v1/fees/calculate_fee" \
            -H "accept: application/json" \
            -H "Content-Type: application/json" \
            -d "{\"cart_value\": 790, \"delivery_distance\": 2235, \"number_of_items\": 4, \"time\": \"2024-01-15T13:00:00Z\"}"
        ```

        **Example response:**

        ```json
        {"delivery_fee": 710}
        ```