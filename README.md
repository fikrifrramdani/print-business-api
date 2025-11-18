# Print Business Management System

A full‑stack application for managing printing business operations including products, orders, finance, stores, and user authentication. Built with **FastAPI** (Backend) and **Next.js** (Frontend).

---

## 🚀 Features

* User Authentication (JWT)
* Product Management
* Order Management
* Financial Records
* Store Data
* Admin Dashboard (Next.js)
* Modular backend architecture (routers, models, schemas, services)

---

# 📂 Project Structure

```
print-business-api/
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models/
│       ├── routers/
│       ├── schemas/
│       ├── services/
│       └── seeders/
│
└── frontend/
    └── printing-dashboard/
        ├── src/
        ├── public/
        └── package.json
```

---

# ⚙️ Backend Setup (FastAPI)

## 1. Create virtual environment

```
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\\Scripts\\activate   # Windows
```

## 2. Install dependencies

```
pip install -r requirements.txt
```

## 3. Create `.env`

```
DATABASE_URL=sqlite:///./app.db
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
```

## 4. Run backend

```
uvicorn app.main:app --reload --port 8000
```

API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

# 🎨 Frontend Setup (Next.js)

## 1. Install dependencies

```
cd frontend/printing-dashboard
npm install
```

## 2. Configure API URL

Create `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 3. Run Dev Server

```
npm run dev
```

Dashboard: [http://localhost:8000](http://localhost:8000)

---

# 🧱 Database ERD

Using **Mermaid ERD** (works in GitHub README):

```mermaid
erDiagram
    USER ||--o{ ORDER : "has"
    USER {
        int id
        string name
        string email
        string password
    }

    PRODUCT ||--o{ ORDER : "ordered in"
    PRODUCT {
        int id
        string name
        float price
        string category
    }

    ORDER {
        int id
        int user_id
        int product_id
        int qty
        float total_price
        datetime created_at
    }

    STORE ||--o{ PRODUCT : "provides"
    STORE {
        int id
        string name
        string address
    }

    FINANCE ||--o{ ORDER : "records"
    FINANCE {
        int id
        int order_id
        float amount
        string type
        datetime created_at
    }
```

---

# 🏗️ System Architecture Diagram

```mermaid
graph TD;
    A[Frontend - Next.js] -- REST API --> B[FastAPI Backend]
    B -- ORM --> C[(Database)]

    A -- Auth Token --> B
    B -- JSON Response --> A

    subgraph Backend
        B
        C
    end

    subgraph Frontend
        A
    end
```

---

# 🔄 Sequence Diagram (User Login → View Dashboard)

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend (Next.js)
    participant B as Backend (FastAPI)
    participant DB as Database

    U->>F: Open Login Page
    F->>B: POST /auth/login (email, password)
    B->>DB: Validate user
    DB-->>B: User data
    B-->>F: JWT Token
    F-->>U: Redirect to Dashboard

    U->>F: Access Dashboard
    F->>B: GET /products (Authorization: Bearer Token)
    B->>DB: Fetch products
    DB-->>B: Product list
    B-->>F: JSON response
    F-->>U: Display Dashboard
```

---

# 📜 License

MIT — free to use and modify.

---

# 📞 Support

Jika ingin menambah fitur, optimasi, atau dokumentasi tambahan, hubungi developer atau open issue di repository.
