import pytest
from django.test import Client

from blog.models import Post, Tag, User


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user(db):
    return User.objects.create(
        username="alice",
        email="alice@example.com",
        display_name="Alice",
    )


@pytest.mark.django_db
def test_list_posts_returns_published(client, user):
    tag = Tag.objects.create(name="Python", slug="python")

    post = Post.objects.create(
        author=user,
        title="Hello",
        body="World",
    )
    post.tags.add(tag)

    Post.objects.create(
        author=user,
        title="Draft",
        body="...",
        is_published=False,
    )

    response = client.get("/api/posts")

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 1
    assert data["page"] == 1
    assert data["page_size"] == 50

    titles = [p["title"] for p in data["results"]]

    assert "Hello" in titles
    assert "Draft" not in titles


@pytest.mark.django_db
def test_get_post_returns_detail(client, user):
    post = Post.objects.create(
        author=user,
        title="Hello",
        body="World",
    )

    response = client.get(f"/api/posts/{post.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Hello"
    assert data["author"]["username"] == "alice"
    assert data["comments"] == []
    assert data["view_count"] == 1

@pytest.mark.django_db
def test_list_posts_pagination(client, user):

    for i in range(60):
        Post.objects.create(
            author=user,
            title=f"Post {i}",
            body="Body",
        )

    response = client.get("/api/posts?page=2&page_size=20")

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 60
    assert data["page"] == 2
    assert data["page_size"] == 20
    assert len(data["results"]) == 20

@pytest.mark.django_db
def test_create_post(client, user):
    tag = Tag.objects.create(name="Python", slug="python")

    payload = {
        "author_id": user.id,
        "title": "Nuevo Post",
        "body": "Contenido",
        "tag_slugs": ["python"],
    }

    response = client.post(
        "/api/posts",
        data=payload,
        content_type="application/json",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Nuevo Post"

    post = Post.objects.get(id=data["id"])

    assert post.author == user
    assert post.tags.count() == 1
    assert post.tags.first().slug == "python"

@pytest.mark.django_db
def test_search_posts(client, user):
    Post.objects.create(
        author=user,
        title="Django Ninja",
        body="Framework",
    )

    Post.objects.create(
        author=user,
        title="FastAPI",
        body="API",
    )

    response = client.get(
        "/api/posts/search",
        {"q": "django", "page": 1, "page_size": 10},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 1
    assert len(data["results"]) == 1
    assert data["results"][0]["title"] == "Django Ninja"

@pytest.mark.django_db
def test_posts_by_tag(client, user):
    python = Tag.objects.create(
        name="Python",
        slug="python",
    )

    django = Tag.objects.create(
        name="Django",
        slug="django",
    )

    post_python = Post.objects.create(
        author=user,
        title="Python Post",
        body="Body",
    )

    post_python.tags.add(python)

    post_django = Post.objects.create(
        author=user,
        title="Django Post",
        body="Body",
    )

    post_django.tags.add(django)

    response = client.get(
        "/api/posts/by-tag/python?page=1&page_size=10"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 1
    assert len(data["results"]) == 1
    assert data["results"][0]["title"] == "Python Post"

@pytest.mark.django_db
def test_get_post_increments_view_count(client, user):
    post = Post.objects.create(
        author=user,
        title="Hello",
        body="World",
    )

    assert post.view_count == 0

    response = client.get(f"/api/posts/{post.id}")

    assert response.status_code == 200

    post.refresh_from_db()

    assert post.view_count == 1