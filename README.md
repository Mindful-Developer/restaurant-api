# Restaurant Ordering System API

A Python-based restaurant ordering system using FastAPI and DynamoDB.

## Setup

1. Create virtual environment:
```python -m venv venv```

2. Activate virtual environment:
- Windows: ```venv\Scripts\activate```
- macOS/Linux: ```source venv/bin/activate```

3. Install dependencies:
```pip install -r requirements.txt```

4. Set up AWS credentials (instructions coming soon)

5. Run the development server:
```uvicorn api.app:app --reload```

## Project Structure

- `/api`: Main application code
  - `/controllers`: API route handlers
  - `/models`: Data models
  - `/schemas`: Pydantic schemas
  - `/repositories`: Database interaction layer
- `/client`: API client implementation