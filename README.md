# **Share Recipe API**

This Django app provides a complete **backend API service** for the [**Share Recipe**](https://github.com/MitkumarR/share-recipe-site) platform. It is designed using Django REST Framework (DRF) and offers secure, clean, and scalable endpoints to manage recipes, user interactions, and feedback.


### What is used?

**Django** — high-level Python web framework for rapid development. <br>
**Django REST Framework (DRF)** — for building robust and flexible APIs.<br>
**PostgreSQL** — database for storing recipe, user, and related data.<br>
**JWT Authentication** — for secure user login and actions.<br>
**CORS Headers** — for cross-origin requests support.<br>

### What does it solve?

* Provides **API endpoints** to create, update, delete, and retrieve recipes.
* Allows **user authentication and authorization** (only logged-in users can post).
* Supports **filtering, searching, and ordering** recipes (by category, region, session, type, etc.).
* Handles **image uploads** securely for recipes.
* Supports **likes** and feedback functionality.
* Modular design to easily extend features (e.g., reviews, favorites, bookmarks).

### How to implement?
    
1. Clone & Install

```bash
git clone <your-repo-url>
cd backend
pip install -r requirements.txt
```
2. Setup environment

Create `.env` or set your environment variables:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
```

3. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```


4. Create superuser (optional)

```bash
python manage.py createsuperuser
```

5. Start server

```bash
python manage.py runserver
```

<!---
### Workflow & Structure

```

```
-->

### Key Features

* **Recipe CRUD APIs**: Create, list, update, delete.
* **Advanced filtering & search**: Filter by region, type, session, category.
* **Likes and comments**: Social interactions on recipes.
* **User authentication**: JWT-secured endpoints.
* **Image upload support**: Manage recipe photos.
* **Feedback system**: Collect user suggestions or issues.


### API Endpoints (example)

| Endpoint                         | Method | Description                |
|----------------------------------| ------ | -------------------------- |
| `/api/recipes/list/`             | GET    | List all published recipes |
| `/api/recipes/create/`           | POST   | Create new recipe          |
| `/api/recipes/recipe/<id>/`      | GET    | Get recipe detail          |
| `/api/recipes/recipe/<id>/like/` | POST   | Like a recipe              |
| `/api/recipes/feedback/`         | POST   | Send feedback              |
| `/api/token/`                    | POST   | Obtain JWT token           |


### Contribution
Feel free to fork and contribute!<br>
Create issues for bugs or feature requests.


### Notes

* Make sure to configure your `MEDIA_URL` and `MEDIA_ROOT` properly for images.
* In production, serve static & media files via proper web server (e.g., Nginx).


### Final words

> This API backend is designed to be **modular, secure, and developer-friendly**, making it easy to extend and integrate with any frontend or mobile app.


