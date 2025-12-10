# social_media_api

## Setup
1. Python + virtualenv
2. pip install -r requirements.txt
3. Add env variables (SECRET_KEY, DEBUG, DB settings)
4. python manage.py migrate
5. python manage.py runserver

## Endpoints
- POST /api/accounts/register/ -> register, returns token
- POST /api/accounts/login/ -> login, returns token
- GET/PUT /api/accounts/profile/ -> current user profile
- POST /api/accounts/follow/<id>/ -> follow user (DELETE to unfollow)
- /api/posts/ -> CRUD posts (GET supports search & pagination)
- /api/posts/{id}/like/ -> like a post
- /api/posts/{id}/unlike/ -> unlike
- /api/posts/feed/ -> feed of posts by people you follow
- /api/notifications/ -> list notifications

## Running tests
`python manage.py test`

## Notes
- Auth: TokenAuthentication (use header `Authorization: Token <token>`)
