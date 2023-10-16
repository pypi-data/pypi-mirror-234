from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest

try:
    from django.conf import settings
except ImportError:
    pytest.skip()

from django.http import HttpResponse, HttpResponseRedirect
from django.test import RequestFactory

from unpoly import Unpoly
from unpoly.contrib.django import UnpolyMiddleware

if TYPE_CHECKING:  # pragma: no cover
    from django.http import HttpRequest


settings.configure()


def get_response(request: HttpRequest):  # noqa: ARG001
    return HttpResponse("")


@pytest.fixture()
def mw() -> UnpolyMiddleware:
    return UnpolyMiddleware(get_response)


@pytest.fixture()
def factory() -> RequestFactory:
    return RequestFactory()


def test_django_middleware_headers(mw: UnpolyMiddleware, factory: RequestFactory):
    req = factory.get("/test", HTTP_X_UP_VERSION="2.2.1")
    response = mw(req)
    assert response.headers["X-Up-Method"] == "GET"
    assert "X-Up-Location" not in response.headers


def test_django_up_cookie(mw: UnpolyMiddleware, factory: RequestFactory):
    # Setting the cookie
    req = factory.post("/test")
    response = mw(req)
    assert response.cookies["_up_method"].value == "POST"

    # Deleting the cookie if set
    req = factory.get("/test", HTTP_COOKIE="_up_method=POST", HTTP_X_UP_VERSION="2.2.1")
    response = mw(req)
    assert response.cookies["_up_method"].value == ""

    # Not doing anything
    req = factory.get("/test", HTTP_X_UP_VERSION="2.2.1")
    response = mw(req)
    assert "_up_method" not in response.cookies


def test_django_redirect_up_params(factory: RequestFactory):
    def get_response(request: HttpRequest):
        up = cast(Unpoly, request.up)  # type: ignore[reportGeneralTypeIssues,attr-defined]
        up.set_title("Testing")
        return HttpResponseRedirect("/redirect?test=abc")

    mw = UnpolyMiddleware(get_response)

    req = factory.get("/test", HTTP_X_UP_VERSION="2.2.1")
    response = mw(req)
    assert response.headers["Location"] == "/redirect?test=abc&_up_title=%22Testing%22"
