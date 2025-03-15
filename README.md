# Alx_DjangoLearnLab

Tasks
0. Introduction to Django Development Environment Setup
1. Implementing and Interacting with Django Models
2. Utilizing the Django Admin Interface

## API Endpoints

### Book API

#### Authentication
All book endpoints require authentication. Include your token in the Authorization header:
`Authorization: Token your_token_here`

#### Available Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/books/` | GET | List all books | `username` (optional): Filter by purchaser |
| `/api/books/<pk>/` | GET | Retrieve a specific book | `pk`: Book ID |
| `/api/books/create/` | POST | Create a new book | Book data in request body |
| `/api/books/<pk>/update/` | PUT/PATCH | Update a book | `pk`: Book ID, Book data in request body |
| `/api/books/<pk>/delete/` | DELETE | Delete a book | `pk`: Book ID |

#### Custom Behavior
- List and Detail views support filtering by username via the `username` query parameter
- Authentication is enforced using Django REST Framework's `IsAuthenticated` permission class