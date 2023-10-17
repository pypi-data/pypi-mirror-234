```markdown
# asyncpgdb

`asyncpgdb` is a Python library that provides an asynchronous database interface built on top of `asyncpg`. One of its unique features is a custom query formatting style that allows you to write parameterized queries using a more readable syntax.

## Installation

You can install `asyncpgdb` using pip:

```bash
pip install asyncpgdb
```

## Features

- Asynchronous database operations.
- Connection pooling for efficient resource management.
- Simplified query execution and result handling.
- Custom query formatting style for better readability.

## Usage

### Database Connection

To establish a connection to your PostgreSQL database, create an instance of the `Database` class:

```python
from asyncpgdb import Database

db = Database(dsn="your_database_dsn_here")
await db.connect()
```

### Executing Queries

You can execute queries using the `execute` method. The library supports a custom query formatting style that allows you to parameterize your queries using named variables, enclosed in `$( )`:

```python
query = "SELECT name, age FROM users WHERE name = $(name) AND age > $(age)"
result = await db.execute(query, vars={"name": "John", "age": 30})

# For SELECT queries, you can fetch the results in various formats
rows = await result.fetch_all()
```

### Connection Management

`asyncpgdb` provides automatic connection management, so you don't need to worry about acquiring and releasing connections manually:

```python
async with db.acquire_connection() as conn:
    # Use the connection for queries within this block
    pass  # Connection is automatically released after this block
```

### Connection Pool

`asyncpgdb` manages a connection pool by default, so you can specify the minimum and maximum number of connections in the pool when creating a `Database` instance:

```python
db = Database(dsn="your_database_dsn_here", min_size=2, max_size=10)
```

## Examples

### Selecting Data

```python
query = "SELECT name, age FROM users WHERE age > $(age)"
results = await db.execute(query, vars={"age": 30})
users = await results.fetch_all()
```

### Inserting Data

```python
query = "INSERT INTO products (name, price) VALUES ($(name), $(price))"
await db.execute(query, vars={"name": "Widget", "price": 19.99})
```

### Updating Data

```python
query = "UPDATE orders SET status = $(status) WHERE id = $(id)"
await db.execute(query, vars={"status": "shipped", "id": 123})
```

## Documentation

For more details and advanced usage, refer to the [documentation](link_to_docs).

## License

This library is licensed under the MIT License.

```

Please replace `"your_database_dsn_here"` with your actual database DSN, and ensure that you have the required dependencies installed to use `asyncpgdb`. You can find detailed documentation and usage examples in the official documentation.
```