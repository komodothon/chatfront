
# 📘 Testing Strategy for Chat Application

This document outlines the testing approach for our chat application deployed across two OCI VMs. Testing ensures reliability, correctness, security, and maintainability of our codebase. We categorize testing into four main types:

---

## 🧪 1. Unit Testing

- **Scope:** Test small, isolated functions/methods.
- **Example:** Validating user input, JWT parsing, utility functions.
- **Tools:** [`pytest`](https://docs.pytest.org/en/stable/), Python `unittest`.

## 🔁 2. Integration Testing

- **Scope:** Test interaction between components.
- **Example:** Login route calling database and returning JWT.
- **Tools:** `pytest`, Flask's `test_client`, Docker test containers.

## 🌐 3. End-to-End (E2E) Testing

- **Scope:** Simulate full flow as a real user.
- **Example:** Register user → log in → send message → see reply.
- **Tools:** `Selenium`, `Playwright`, `Cypress` (if UI is SPA), or programmatic HTTP/WebSocket clients.

## 🚦 4. Load/Stress Testing

- **Scope:** Simulate many users to test scalability.
- **Example:** 1000 users connected to WebSocket, sending messages.
- **Tools:** [`Locust`](https://locust.io/), `k6`, `Artillery`

---

# 🧰 Unit Testing with Pytest

## ✅ Why Pytest?

- Simple, readable syntax (`assert`-based)
- Auto-discovery of tests
- Extensive plugin ecosystem
- Great for both small and large codebases

## 🧪 Pytest Workflow

1. Install: `pip install pytest`
2. Create test files: Named like `test_*.py` or `*_test.py`
3. Write functions prefixed with `test_`
4. Run tests: `pytest`
5. Optional: Add fixtures, mocking, parametrize, coverage

## 📄 Example Test (Flask route)

```python
# test_auth.py
from app.auth import create_jwt_token

def test_create_jwt_token():
    payload = {"user_id": 123, "role": "admin"}
    token = create_jwt_token(payload)
    assert isinstance(token, str)
    assert len(token.split('.')) == 3  # JWT format
