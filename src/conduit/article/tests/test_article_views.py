"""Tests for Article related views."""

from conduit.article.models import Article
from conduit.auth.models import User
from conduit.auth.tests.test_auth_views import USER_ONE_JWT
from conduit.auth.tests.test_auth_views import USER_TWO_JWT
from sqlalchemy.orm.session import Session
from webtest import TestApp


def test_feed(testapp: TestApp, democontent: None) -> None:
    """Test GET /api/articles/feed."""
    res = testapp.get(
        "/api/articles/feed",
        headers={"Authorization": f"Token {USER_TWO_JWT}"},
        status=200,
    )

    assert res.json == {
        "articlesCount": 2,
        "articles": [
            {
                "slug": "bar",
                "title": "Bär",
                "description": "Bär desc",
                "body": "Bär body",
                "createdAt": "2019-03-03T03:03:03.000Z",
                "updatedAt": "2019-04-04T04:04:04.000Z",
                "tagList": [],
                "favorited": False,
                "favoritesCount": 0,
                "author": {
                    "username": "one",
                    "bio": None,
                    "image": None,
                    "following": True,
                },
            },
            {
                "slug": "foo",
                "title": "Foö",
                "description": "Foö desc",
                "body": "Foö body",
                "createdAt": "2019-01-01T01:01:01.000Z",
                "updatedAt": "2019-02-02T02:02:02.000Z",
                "tagList": ["dogs", "cats"],
                "favorited": False,
                "favoritesCount": 0,
                "author": {
                    "username": "one",
                    "bio": None,
                    "image": None,
                    "following": True,
                },
            },
        ],
    }


def test_GET_articles(testapp: TestApp, democontent: None) -> None:
    """Test GET /api/articles."""
    res = testapp.get("/api/articles", status=200)

    assert res.json == {
        "articlesCount": 3,
        "articles": [
            {
                "slug": "i-am-johnjacob",
                "title": "I am John Jacob",
                "description": "johnjacob desc",
                "body": "johnjacob body",
                "createdAt": "2019-05-05T05:05:05.000Z",
                "updatedAt": "2019-06-06T06:06:06.000Z",
                "tagList": [],
                "favorited": False,
                "favoritesCount": 0,
                "author": {
                    "username": "johnjacob",
                    "bio": None,
                    "image": None,
                    "following": False,
                },
            },
            {
                "slug": "bar",
                "title": "Bär",
                "description": "Bär desc",
                "body": "Bär body",
                "createdAt": "2019-03-03T03:03:03.000Z",
                "updatedAt": "2019-04-04T04:04:04.000Z",
                "tagList": [],
                "favorited": False,
                "favoritesCount": 0,
                "author": {
                    "username": "one",
                    "bio": None,
                    "image": None,
                    "following": False,
                },
            },
            {
                "slug": "foo",
                "title": "Foö",
                "description": "Foö desc",
                "body": "Foö body",
                "createdAt": "2019-01-01T01:01:01.000Z",
                "updatedAt": "2019-02-02T02:02:02.000Z",
                "tagList": ["dogs", "cats"],
                "favorited": False,
                "favoritesCount": 0,
                "author": {
                    "username": "one",
                    "bio": None,
                    "image": None,
                    "following": False,
                },
            },
        ],
    }


def test_GET_articles_filter_by_author(testapp: TestApp, democontent: None) -> None:
    """Test GET /api/articles, filter by author."""
    res = testapp.get("/api/articles?author=one", status=200)
    assert res.json["articlesCount"] == 2
    assert res.json["articles"][0]["slug"] == "bar"
    assert res.json["articles"][1]["slug"] == "foo"

    res = testapp.get("/api/articles?author=two", status=200)
    assert res.json["articlesCount"] == 0


def test_GET_articles_filter_by_tag(testapp: TestApp, democontent: None) -> None:
    """Test GET /api/articles, filter by author."""
    res = testapp.get("/api/articles?tag=dogs", status=200)
    assert res.json["articlesCount"] == 1
    assert res.json["articles"][0]["slug"] == "foo"


def test_GET_articles_limit(testapp: TestApp, democontent: None) -> None:
    """Test GET /api/articles, but limit to N results."""
    res = testapp.get("/api/articles", status=200)
    assert res.json["articlesCount"] == 3

    res = testapp.get("/api/articles?limit=2", status=200)
    assert res.json["articlesCount"] == 2


def test_GET_articles_offset(testapp: TestApp, democontent: None) -> None:
    """Test GET /api/articles, but limit to N results, offset by M results."""
    res = testapp.get("/api/articles?limit=2", status=200)
    assert res.json["articles"][1]["title"] == "Bär"

    res = testapp.get("/api/articles?limit=2&offset=1", status=200)
    assert res.json["articles"][1]["title"] == "Foö"


def test_GET_article(testapp: TestApp, democontent: None) -> None:
    """Test GET /api/articles/{slug}."""
    res = testapp.get("/api/articles/foo", status=200)

    assert res.json == {
        "article": {
            "author": {
                "bio": None,
                "following": False,
                "image": None,
                "username": "one",
            },
            "body": "Foö body",
            "createdAt": "2019-01-01T01:01:01.000Z",
            "description": "Foö desc",
            "favorited": False,
            "favoritesCount": 0,
            "slug": "foo",
            "tagList": ["dogs", "cats"],
            "title": "Foö",
            "updatedAt": "2019-02-02T02:02:02.000Z",
        }
    }


def test_GET_article_authenticated(testapp: TestApp, democontent: None) -> None:
    """Test GET /api/articles/{slug}."""
    res = testapp.get(
        "/api/articles/foo",
        headers={"Authorization": f"Token {USER_TWO_JWT}"},
        status=200,
    )

    assert res.json == {
        "article": {
            "author": {
                "bio": None,
                "following": True,
                "image": None,
                "username": "one",
            },
            "body": "Foö body",
            "createdAt": "2019-01-01T01:01:01.000Z",
            "description": "Foö desc",
            "favorited": False,
            "favoritesCount": 0,
            "slug": "foo",
            "tagList": ["dogs", "cats"],
            "title": "Foö",
            "updatedAt": "2019-02-02T02:02:02.000Z",
        }
    }


def test_POST_article(testapp: TestApp, democontent: None) -> None:
    """Test POST /api/articles."""
    res = testapp.post_json(
        "/api/articles",
        {
            "article": {
                "title": "A title",
                "description": "A description",
                "body": "A body",
                "tagList": ["one", "two"],
            }
        },
        headers={"Authorization": f"Token {USER_TWO_JWT}"},
        status=201,
    )

    assert res.json["article"]["author"]["username"] == "two"
    assert res.json["article"]["title"] == "A title"
    assert res.json["article"]["description"] == "A description"
    assert res.json["article"]["body"] == "A body"
    assert res.json["article"]["tagList"] == ["one", "two"]

    # TODO: mock createdAt and updatedAt to be able to compare entire output
    #     "article": {
    #         "author": {"bio": "", "following": True, "image": "", "username": "two"},
    #         "body": "A body",
    #         "createdAt": "2019-01-01T00:00:00Z",
    #         "description": "A description",
    #         "favorited": False,
    #         "favoritesCount": 0,
    #         "slug": "a-title",
    #         "tagList": ["foo", "bar"],  # TODO: taglist support
    #         "title": "A title",
    #         "createdAt": "2019-01-01T00:00:00Z",
    #     }
    # }


def test_PUT_article(testapp: TestApp, democontent: None) -> None:
    """Test PUT /api/articles/{slug}."""
    res = testapp.put_json(
        "/api/articles/foo",
        {
            "article": {
                "title": "New title",
                "description": "New description",
                "body": "New body",
            }
        },
        headers={"Authorization": f"Token {USER_ONE_JWT}"},
        status=200,
    )

    assert res.json == {
        "article": {
            "author": {
                "bio": None,
                "following": False,
                "image": None,
                "username": "one",
            },
            "body": "New body",
            "createdAt": "2019-01-01T01:01:01.000Z",
            "description": "New description",
            "favorited": False,
            "favoritesCount": 0,
            "slug": "foo",
            "tagList": ["dogs", "cats"],
            "title": "New title",
            "updatedAt": "2019-02-02T02:02:02.000Z",
        }
    }


def test_PUT_article_empty_request(testapp: TestApp, democontent: None) -> None:
    """Test PUT /api/articles/{slug} with empty request, nothing happens."""
    testapp.put_json(
        "/api/articles/foo",
        {"article": {}},
        headers={"Authorization": f"Token {USER_ONE_JWT}"},
        status=200,
    )


def test_DELETE_article(testapp: TestApp, db: Session, democontent: None) -> None:
    """Test DELETE /api/articles/{slug}."""
    assert Article.by_slug("foo", db=db) is not None
    testapp.delete(
        "/api/articles/foo",
        headers={"Authorization": f"Token {USER_ONE_JWT}"},
        status=200,
    )

    assert Article.by_slug("foo", db=db) is None


def test_favorite_unfavorite_article(
    testapp: TestApp, db: Session, democontent: None
) -> None:
    """Test POST/DELETE /api/articles/{slug}/favorite."""
    user = User.by_username("one", db=db)
    assert user.favorites == []  # type: ignore

    res = testapp.post_json(
        "/api/articles/foo/favorite",
        headers={"Authorization": f"Token {USER_ONE_JWT}"},
        status=200,
    )
    assert res.json["article"]["favorited"] is True
    assert res.json["article"]["favoritesCount"] == 1
    user = User.by_username("one", db=db)
    assert [article.slug for article in user.favorites] == ["foo"]  # type: ignore

    res = testapp.delete(
        "/api/articles/foo/favorite",
        headers={"Authorization": f"Token {USER_ONE_JWT}"},
        status=200,
    )
    user = User.by_username("one", db=db)
    assert res.json["article"]["favorited"] is False
    assert res.json["article"]["favoritesCount"] == 0
    assert user.favorites == []  # type: ignore
