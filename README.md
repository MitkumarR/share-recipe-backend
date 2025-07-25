# **Share Recipe API**

This Django app provides a complete **backend API service** for the [**Share Recipe**](https://github.com/MitkumarR/share-recipe-site) platform. It is designed using Django REST Framework (DRF) and offers secure, clean, and scalable endpoints to manage recipes, user interactions, and feedback.

### Live API Documentation

Access the complete, interactive API documentation:

- **Swagger UI**: `/api/schema/swagger-ui/`
- **ReDoc**: `/api/schema/redoc/`

### Key Features 

**Full User & Profile Management:**
- JWT-based user registration and login
- Profile viewing and updating (with bios and profile pictures)
- Secure password change and forgot password via email
- Account deactivation/reactivation and permanent deletion

**Comprehensive Recipe Management:**
- Full CRUD for user-owned recipes
- Nested recipe creation (ingredients, steps) in a single request
- Image uploads for recipes and steps

**Social Interaction:**
- Like/unlike recipes
- Save/unsave recipes
- Post and manage comments
- Recipe view counter

**Advanced Discovery:**
- Filter by category, region, type, session, and ingredients
- Full-text search on titles and descriptions
- Sort by creation date, likes, or views

**Professional Tooling:**
- Swagger/OpenAPI 3.0 documentation via `drf-spectacular`
- JWT token blacklisting after password changes

### Tech Stack

- Framework: ```Django```
- API: ```Django REST Framework (DRF)```
- Database: ```PostgreSQL (production)```
- Authentication: ```Simple JWT```
- Filtering: ```django-filter```
- API Schema: ```drf-spectacular```
- CORS: ```django-cors-headers```

### Getting Started

Prerequisites
- Python 3.10+
- pip, virtualenv
- Git

Installation & Setup


1. Clone the repository
    ```bash
    git clone https://github.com/your-username/share-recipe-backend.git
    cd share-recipe-backend
    ```

2. Create and activate virtual environment

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
   
3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
4. Create and configure environment variables
    ```bash
    cp .env.example .env  # Then fill in the values
    ```

5. Example `.env` file

    ```env
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY='your-super-secret-key'
    
    # Set to False in production
    DEBUG=True
    
    # SQLite (default) or use a PostgreSQL URL in production
    DATABASE_URL=
    ```

6. Run Migrations & Server

    ```bash
    # Apply migrations
    python manage.py makemigrations
    python manage.py migrate
    
    # Create superuser (optional)
    python manage.py createsuperuser
    
    # Run development server
    python manage.py runserver
    ```

    The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)


7. Running Tests

   ```bash
   python manage.py test
   ```

### Project Structure

```
share-recipe-backend/
├── backend/       # Django project settings and root URLConf
├── user/          # User accounts, profiles, authentication logic
├── recipes/       # Recipe creation, interaction, filtering, models
└── ...
```


### API Endpoints Overview

| Method   | Endpoint                         | Description                         |
| -------- |----------------------------------| ----------------------------------- |
| POST     | `/api/user/signup/`              | Register new user                   |
| POST     | `/api/user/signin/`              | Obtain JWT tokens                   |
| GET      | `/api/user/profile/`             | View user profile                   |
| PATCH    | `/api/user/profile/`             | Update user profile                 |
| PUT      | `/api/user/change-password/`     | Change password                     |
| POST     | `/api/user/password-reset/`      | Password reset via email            |
| GET      | `/api/recipes/list/`             | List/filter/search recipes          |
| POST     | `/api/recipes/create/`           | Create a new recipe (auth required) |
| GET      | `/api/recipes/recipe/<id>/`      | View recipe details                 |
| POST     | `/api/recipes/recipe/<id>/like/` | Like/unlike recipe                  |
| POST     | `/api/recipes/recipe/<id>/save/` | Save/unsave recipe                  |
| GET/POST | `/api/recipes/<id>/comments/`    | View or add comments on recipe      |

Visit Swagger for full documentation.


### Contributing

Pull requests, issues, and feature suggestions are welcome!
Check out the [Issues](https://github.com/MitkumarR/share-recipe-backend/issues) tab to get started.

### License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

### Author

[Mit](https://github.com/MitkumarR/)
