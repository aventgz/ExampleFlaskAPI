# Example API built with Python, Flask and MongoDB

This repository provides an API built using Python, Flask and MongoDB. The API includes endpoints for searching/managing items and categories with basic CRUD operations.

## Features

- API built with Flask
- Supports `GET`, `HEAD`, `POST`, `PUT`, `PATCH` and `DELETE` operations
- Support for authorization with permissions
- Input data integrity checking
- MongoDB as the database

---

## Requirements

- **Minimal Python Version:** 3.13
- MongoDB instance (local or remote)

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/aventgz/ExampleFlaskAPI.git
   cd ExampleFlaskAPI
   ```

2. Edit the MongoDB URI in `ExampleFlaskAPI/example/main.py`:

   ```python
   MONGO_URI = 'mongodb+srv://<nickname>:<password>@<server_ip>/<database_name>?retryWrites=true&w=majority'
   ```

3. Create a virtual environment (**OPTIONAL**):

   ```bash
   python -m venv venv
   ```

    - **For activate on Windows, run:**
        ```bash
        .\venv\Scripts\activate
        ```

    - **For activate on macOS/Linux, run:**
        ```bash
        source venv/bin/activate
        ```

4. Install the package using `setup.py`:

   ```bash
   python setup.py install
   ```

---

## Running the Application

1. Ensure MongoDB is running and accessible.

2. Start application with example data:

   ```bash
   ExampleFlaskAPI
   ```
3. Access API at `http://127.0.0.1:5000/api/v1`.

---

## General API Informations

### API Authorization

To access the API, you must include an API key in the `Authorization` header of each request. Every API key is a unique token and can be created by `Authorization.create_session(key, permissions)` function. This key allows the server to identify and authenticate your requests.

#### Example Header
```http
Authorization: <YOUR_API_KEY>
```

### General Response Structure

Every API response have a standardized structure to ensure consistency and clarity. The response includes the following fields:

- `response`: Contains HTTP informations:
  - `code`: Result code of a HTTP action.
  - `status`: HTTP response status.
- `status`: Contains API response about request status:
  - `success`: Indicate whether the request was completed successfully.
  - `code`: Code of error/success.
  - `message`: Message of request status.   
- `timestamp`: The server's timestamp when the response was generated.
- `results`: Contains the data returned by the request or error details if applicable.

#### Example Response
```json
{
  "response": {
  "code": 401, 
  "status": "Unauthorized"
  }, 
  "status": {
    "success": false,
    "code": 0,
    "message": ""
  }, 
  "timestamp": 1237227214,
  "result": []
}
```
---

## API Endpoints

## Endpoint `/category`

### `/category` **GET**

- **Description:** Retrieve category by name.
- **Parameters:**
  - `name` (query parameter or URL path): Name of the categories to retrieve, separated by commas (e.g. `name`,`name`,`name`).
- **Example Request:**
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/category?name=test_name,test_name2" \
       -H "Authorization: <YOUR_API_KEY>"
  ```
- **Alternative URL Structure:** Retrieve a category by name directly in the URL path.
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/category/test_name" \
       -H "Authorization: <YOUR_API_KEY>"
  ```

- **Response Result Structure**
  ```json
  [
    {
      "name": "<name>",
      "parent_name": "<parent_name>"
    }
  ]
  ```

### `/category` **POST**

- **Description:** Add a new category to the database.
- **Request Body Parameters:**
  - `name` (string): Name of the category.
  - `parent_name` (string): Name of parent category.
- **Example Request:**
  ```bash
  curl -X POST "http://127.0.0.1:5000/api/v1/category" \
       -H "Authorization: <YOUR_API_KEY>" \
       -H "Content-Type: application/json" \
       -d '{"name": "test_name", "parent_name": ""}'
  ```

- **Response Result Structure**
  ```json
  [
    {
      "id": "<name>",
      "status": "<true/false>", 
      "message": "<message>"
    } 
  ]
  ```

### `/category` **PUT**

- **Description:** Change category in the database.
- **Request Body Parameters:**
  - `name` (string): Name of the category.
  - `change` (object): Object for changing parameters:
    - `parent_name` (string): Name of parent category.
- **Example Request:**
  ```bash
  curl -X POST "http://127.0.0.1:5000/api/v1/category" \
       -H "Authorization: <YOUR_API_KEY>" \
       -H "Content-Type: application/json" \
       -d '{"name": "test_name", "change": {"parent_name": "parent_name"}}'
  ```

- **Response Result Structure**
  ```json
  [
    {
      "id": "<name>",
      "status": "<true/false>", 
      "message": "<message>"
    } 
  ]
  ```

### `/category` **PATCH**

- **Description:** Change category in the database.
- **Request Body Parameters:**
  - `name` (string): Name of the category.
  - `change` (object): Object for changing parameters:
    - `parent_name` (optional, string): Name of parent category.
- **Example Request:**
  ```bash
  curl -X POST "http://127.0.0.1:5000/api/v1/category" \
       -H "Authorization: <YOUR_API_KEY>" \
       -H "Content-Type: application/json" \
       -d '{"name": "test_name", "change": {"parent_name": ""}}'
  ```

- **Response Result Structure**
  ```json
  [
    {
      "id": "<name>",
      "status": "<true/false>", 
      "message": "<message>"
    } 
  ]
  ```

### `/category` **DELETE**

- **Description:** Remove a category by name.
- **Parameters:**
  - `name` (query parameter or URL path): Name/s of the categories to delete, separated by commas (e.g. `name`,`name`,`name`).
- **Example Request:**
  ```bash
  curl -X DELETE "http://127.0.0.1:5000/api/v1/category?name=test_name,test_name2" \
       -H "Authorization: <YOUR_API_KEY>"
  ```
- **Alternative URL Structure:** Delete a category by name directly in the URL path.
  ```bash
  curl -X DELETE "http://127.0.0.1:5000/api/v1/category/test_name" \
       -H "Authorization: <YOUR_API_KEY>"
  ```

- **Response Result Structure**
  ```json
  [
    {
      "id": "<name>",
      "status": "<true/false>", 
      "message": "<message>"
    } 
  ]
  ```

---

## Endpoint `/item`

### `/item` **GET**

- **Description:** Retrieve specific item by serial number.
- **Parameters:**
  - `serial_number` (query parameter or URL path): The serial number/s of the item/s to retrieve, separated by commas (e.g. `serial_number`,`serial_number`,`serial_number`).
- **Example Request:**
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/item?serial_number=41472458-f86c-416a-bb1f-15779557eb2b,40f9c83e-a6a0-446f-91f6-c87363c23ece" \
       -H "Authorization: <YOUR_API_KEY>"
  ```
- **Alternative URL Structure:** Retrieve a item by a serial number directly in the URL path.
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/item/41472458-f86c-416a-bb1f-15779557eb2b" \
       -H "Authorization: <YOUR_API_KEY>"
  ```

- **Response Result Structure**
  ```json
  [
    {
      "serial_number": "<serial_number>",
      "name": "<name>",
      "description": "<description>",
      "category": "<category>",
      "price": "<price>",
      "location": {
        "room": "<room>",
        "bookcase": "<bookcase>",
        "shelf": "<shelf>",
        "cuvette": "<cuvette>",
        "column": "<column>",
        "row": "<row>"
      }
    }
  ]
  ```

### `/item` **POST**

- **Description:** Add a new item to the database.
- **Request Body Parameters:**
  - `serial_number` (string): Serial number of the item.
  - `name` (string): Name of the item.
  - `description` (string): Description of the item.
  - `category` (string): Choose category from existing for the item (can be empty).
  - `price` (float): Price of the single item.
  - `location` (object): Object that includes:
    - `room` (integer): Room location of the item.
    - `bookcase` (integer): Bookcase location of the item.
    - `shelf` (integer): Shelf location of the item.
    - `cuvette` (integer): Cuvette location of the item.
    - `column` (integer): Column location of the item.
    - `row` (integer): Row location of the item.
- **Example Request:**
  ```bash
  curl -X POST "http://127.0.0.1:5000/api/v1/item" \
       -H "Authorization: <YOUR_API_KEY>" \
       -H "Content-Type: application/json" \
       -d '{"serial_number": "41472458-f86c-416a-bb1f-15779557eb2b",
            "name": "test_name",
            "description": "test_description",
            "category": "",
            "price": 1.0,
            "location": {
                "room": 1,
                "bookcase": 1,
                "shelf": 1,
                "cuvette": 1,
                "column": 1,
                "row": 1
            }
        }'
  ```

- **Response Result Structure**
  ```json
  [
    {
      "id": "<serial_number>",
      "status": "<true/false>", 
      "message": "<message>"
    } 
  ]
  ```

### `/item` **PUT**

- **Description:** Edit existing item in the database.
- **Request Body Parameters:**
  - `serial_number` (string): Serial number of the item.
  - `change` (object): Object that contains values to change:
    - `name` (string): Name of the item.
    - `description` (string): Description of the item.
    - `category` (string): Choose category from existing for the item (can be empty).
    - `price` (float): Price of the single item.
    - `location` (object): Object that includes:
        - `room` (integer): Room location of the item.
        - `bookcase` (integer): Bookcase location of the item.
        - `shelf` (integer): Shelf location of the item.
        - `cuvette` (integer): Cuvette location of the item.
        - `column` (integer): Column location of the item.
        - `row` (integer): Row location of the item.
- **Example Request:**
  ```bash
  curl -X POST "http://127.0.0.1:5000/api/v1/item" \
       -H "Authorization: <YOUR_API_KEY>" \
       -H "Content-Type: application/json" \
       -d '{"serial_number": "41472458-f86c-416a-bb1f-15779557eb2b",
            "change": {
                "name": "changed_test_name",
                "description": "test_description",
                "category": "",
                "price": 1.0,
                "location": {
                    "room": 1,
                    "bookcase": 1,
                    "shelf": 1,
                    "cuvette": 1,
                    "column": 1,
                    "row": 1
                }
            }
        }'
  ```

- **Response Result Structure**
  ```json
  [
    {
      "id": "<serial_number>",
      "status": "<true/false>", 
      "message": "<message>"
    } 
  ]
  ```

### `/item` **PATCH**

- **Description:** Edit existing item in the database.
- **Request Body Parameters:**
  - `serial_number` (string): Serial number of the item.
  - `change` (object): Object that contains values to change:
    - `name` (optional, string): Name of the item.
    - `description` (optional, string): Description of the item.
    - `category` (optional, string): Choose category from existing for the item (can be empty).
    - `price` (optional, float): Price of the single item.
    - `location` (optional, object): Object that includes:
        - `room` (optional, integer): Room location of the item.
        - `bookcase` (optional, integer): Bookcase location of the item.
        - `shelf` (optional, integer): Shelf location of the item.
        - `cuvette` (optional, integer): Cuvette location of the item.
        - `column` (optional, integer): Column location of the item.
        - `row` (optional, integer): Row location of the item.
- **Example Request:**
  ```bash
  curl -X POST "http://127.0.0.1:5000/api/v1/item" \
       -H "Authorization: <YOUR_API_KEY>" \
       -H "Content-Type: application/json" \
       -d '{"serial_number": "41472458-f86c-416a-bb1f-15779557eb2b",
            "change": {
                "description": "changed_test_description",
                "location": {
                    "room": 2,
                    "shelf": 3,
                }
            }
        }'
  ```

- **Response Result Structure**
  ```json
  [
    {
      "id": "<serial_number>",
      "status": "<true/false>", 
      "message": "<message>"
    } 
  ]
  ```

### `/item` **DELETE**

- **Description:** Remove item by serial number.
- **Parameters:**
  - `serial_number` (query parameter or URL path): The serial number/s of the item/s to delete, separated by commas (e.g. `serial_number`,`serial_number`,`serial_number`).
- **Example Request:**
  ```bash
  curl -X DELETE "http://127.0.0.1:5000/api/v1/item?serial_number=41472458-f86c-416a-bb1f-15779557eb2b,40f9c83e-a6a0-446f-91f6-c87363c23ece" \
       -H "Authorization: <YOUR_API_KEY>"
  ```
- **Alternative URL Structure:** Delete item by serial number directly in the URL path.
  ```bash
  curl -X DELETE "http://127.0.0.1:5000/api/v1/item/41472458-f86c-416a-bb1f-15779557eb2b" \
       -H "Authorization: <YOUR_API_KEY>"
  ```

- **Response Result Structure**
  ```json
  [
    {
      "id": "<serial_number>",
      "status": "<true/false>", 
      "message": "<message>"
    } 
  ]
  ```

---

## Endpoint `/search/items`

### `/search/items` **GET**

- **Description:** Search for items with multiple parameters.
- **Parameters:**
  - `skip` (optional, integer): Skip the number of items.
  - `limit` (optional, integer): Limit number of items returned at once.
  - `serial_number` (optional, string): Serial numbers of the items to search for, separated by commas (e.g. `serial_number`,`serial_number`,`serial_number`).
  - `name` (optional, string): Names of the items, separated by commas (e.g. `name`,`name`,`name`).
  - `category` (optional, string): Select categories from existing ones for the item (may be empty), separated by commas (e.g. `category`,`category`,`category`).
  - `price` (optional, float): Price of items, separated by commas (e.g. `price`,`price`,`price`), or a designated range with parameters: `min_price` for minimum price, `max_price` for maximum price.
  - `location_room` (optional, integer): Room location of the item, separated by commas (e.g. `location_room`,`location_room`,`location_room`), or a designated range with parameters: `min_location_room` for minimum room location, `max_location_room` for maximum room location.
  - `location_bookcase` (optional, integer): Bookcase locations of the items, separated by commas (e.g. `location_bookcase`,`location_bookcase`,`location_bookcase`), or a designated range with parameters: `min_location_bookcase` for minimum bookcase location, `max_location_bookcase` for maximum bookcase location.
  - `location_shelf` (optional, integer): Shelf locations of the items, separated by commas (e.g. `location_shelf`,`location_shelf`,`location_shelf`), or a designated range with parameters: `min_location_shelf` for minimum shelf location, `max_location_shelf` for maximum shelf location.
  - `location_cuvette` (optional, integer): Cuvette locations of the items, separated by commas (e.g. `location_cuvette`,`location_cuvette`,`location_cuvette`), or a designated range with parameters: `min_location_cuvette` for minimum cuvette location, `max_location_cuvette` for maximum cuvette location.
  - `location_column` (optional, integer): Column locations of the items, separated by commas (e.g. `location_column`,`location_column`,`location_column`), or a designated range with parameters: `min_location_column` for minimum column location, `max_location_column` for maximum column location.
  - `location_row` (optional, integer): Row locations of the items, separated by commas (e.g. `location_row`,`location_row`,`location_row`), or a designated range with parameters: `min_location_row` for minimum row location, `max_location_row` for maximum row location.
- **Example Request:**
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/search/items?max_price=10.5&location_room=1&min_location_column=1&max_location_column=5" \
       -H "Authorization: <YOUR_API_KEY>"
  ```

- **Response Result Structure**
  ```json
  [
    {
      "serial_number": "<serial_number>",
      "name": "<name>",
      "description": "<description>",
      "category": "<category>",
      "price": "<price>",
      "location": {
        "room": "<room>",
        "bookcase": "<bookcase>",
        "shelf": "<shelf>",
        "cuvette": "<cuvette>",
        "column": "<column>",
        "row": "<row>"
      }
    }
  ]
  ```

---

## License

This project is licensed under the MIT License.
