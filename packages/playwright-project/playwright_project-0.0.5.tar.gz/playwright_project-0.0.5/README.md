# Playwright and Pytest

## Install Pytest Plugin

```pip
pip install pytest-playwright
```

## Install the required browsers

```playwright
playwright install
```

## test_example.py

[test example](tests/test_example.py)

## Running the Example Test

```pytest
pytest
```

## Using Test Hooks

````python
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    
    print("before the test runs")

    # Go to the starting url before each test.
    page.goto("https://playwright.dev/")
    yield
    
    print("after the test runs")

def test_main_navigation(page: Page):
    # Assertions use the expect API.
    expect(page).to_have_url("https://playwright.dev/")
````

## Running tests headed

````pytest
pytest --headed
````

## Running tests on different browsers and multiple browser

````pytest
pytest --browser webkit
````

````pytest
pytest --browser webkit --browser firefox
````

## Running specific tests

````pytest
pytest test_login.py
````

> To run a set of test files pass in the names of the test files that you want to run.

````pytest
pytest tests/test_todo_page.py tests/test_landing_page.py
````

> To run a specific test pass in the function name of the test you want to run.

````pytest
pytest -k test_add_a_todo_item
````

## Run tests in Parallel

````pytest
pytest --numprocesses 2
````
