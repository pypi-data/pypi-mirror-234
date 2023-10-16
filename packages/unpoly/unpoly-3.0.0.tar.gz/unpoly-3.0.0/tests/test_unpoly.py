from typing import Any
from unittest.mock import Mock

from unpoly.adapter import SimpleAdapter
from unpoly.up import Unpoly


def make_up(**kwargs: Any):
    adapter = SimpleAdapter(**kwargs)
    up = Unpoly(adapter)
    return up, adapter


def test_is_up_request():
    up, _ = make_up()
    assert bool(up) is not True

    up, _ = make_up(headers={"X-Up-Version": "2.2.1"})
    assert bool(up) is True


def test_needs_cookie():
    up, _ = make_up()
    assert up.needs_cookie is False

    up, _ = make_up(method="POST", headers={"X-Up-Version": "2.2.1"})
    assert up.needs_cookie is False

    up, _ = make_up(method="POST")
    assert up.needs_cookie is True


def test_set_title():
    up, _ = make_up()
    up.set_title("Testing")
    assert up.options.title == "Testing"


def test_emit_events():
    up, _ = make_up()

    up.emit("test", {"k": "v"})
    up.layer.emit("test2", {"k2": "v2"})

    assert up.options.events == [
        {"type": "test", "k": "v"},
        {"type": "test2", "layer": "current", "k2": "v2"},
    ]


def test_layer():
    up, _ = make_up(
        headers={
            "X-Up-Mode": "modal",
            "X-Up-Fail-Mode": "fail",
            "X-Up-Context": '{"k":"v"}',
            "X-Up-Fail-Context": '{"k2":"v2"}',
        }
    )
    assert up.layer.mode == "modal"
    assert up.layer.context == {"k": "v"}
    assert up.fail_layer.mode == "fail"
    assert up.fail_layer.context == {"k2": "v2"}


def test_layer_accept():
    up, _ = make_up(headers={"X-Up-Mode": "modal"})

    assert up.layer.is_overlay
    up.layer.accept("test")
    assert up.options.accept_layer == "test"

    up.layer.accept()
    assert up.options.accept_layer is None


def test_layer_dismiss():
    up, _ = make_up(headers={"X-Up-Mode": "modal"})

    assert up.layer.is_overlay
    up.layer.dismiss("test")
    assert up.options.dismiss_layer == "test"


def test_layer_mode():
    up, _ = make_up(headers={"X-Up-Mode": "modal"})
    assert up.layer.is_overlay

    up, _ = make_up(headers={"X-Up-Mode": "root"})
    assert up.layer.is_root


def test_cache():
    up, _ = make_up(headers={"X-Up-Mode": "modal"})

    up.cache.expire("test/*")
    assert up.options.expire_cache == "test/*"

    up.cache.keep()
    assert up.options.expire_cache == "false"


def test_parsing_from_request():
    up, _ = make_up(
        headers={
            "X-Up-Version": "2.2.1",
            "X-Up-Target": "[up-main~=modal]",
            "X-Up-Mode": "modal",
            "X-Up-Context": '{"test":"test"}',
            "X-Up-Fail-Target": "[up-main~=fail]",
        },
        params={
            "_up_fail_mode": "fail",
            "_up_fail_context": '{"fail":"fail"}',
            "_up_validate": "field",
        },
    )

    assert up.version == "2.2.1"
    assert up.target == "[up-main~=modal]"
    assert up.mode == "modal"
    assert up.context == {"test": "test"}
    assert up.fail_target == "[up-main~=fail]"
    assert up.fail_mode == "fail"
    assert up.fail_context == {"fail": "fail"}
    assert up.validate == ["field"]


def test_target_change():
    up, _ = make_up(headers={"X-Up-Target": "[up-main~=modal]"})
    up.target = "new_target"
    assert up.options.target == "[up-main~=modal]"
    assert up.options.server_target == "new_target"


def test_finalize_cookie():
    up, adapter = make_up(method="POST")
    adapter.set_cookie = Mock()
    up.finalize_response(None)
    adapter.set_cookie.assert_called_once_with(None, True)

    up, adapter = make_up()
    adapter.set_cookie = Mock()
    up.finalize_response(None)
    adapter.set_cookie.assert_called_once_with(None, False)


def test_no_rewrite_if_not_unpoly():
    up, adapter = make_up()
    adapter.set_headers = Mock()
    adapter.set_redirect_uri = Mock()
    up.finalize_response(None)
    adapter.set_headers.assert_not_called()
    adapter.set_redirect_uri.assert_not_called()


def test_response_headers():
    up, adapter = make_up(
        location="/test", method="POST", headers={"X-Up-Version": "2.1.1"}
    )
    up.finalize_response(None)
    assert adapter.response_headers == {"X-Up-Method": "POST"}


def test_response_headers_with_location():
    up, adapter = make_up(
        location="/test?_up_test=123", method="POST", headers={"X-Up-Version": "2.1.1"}
    )
    up.finalize_response(None)
    assert adapter.response_headers == {"X-Up-Location": "/test", "X-Up-Method": "POST"}


def test_redirect_params():
    up, adapter = make_up(headers={"X-Up-Version": "2.1.1"}, redirect_uri="/redirect")
    up.set_title("test")
    up.context["new"] = "yes"
    up.finalize_response(None)
    assert adapter.response_headers is None
    assert (
        adapter.response_redirect_uri
        == "/redirect?_up_title=%22test%22&_up_context_diff=%7B%22new%22%3A%22yes%22%7D"
    )


def test_up_param_stripping():
    up, adapter = make_up(
        location="/test?a=b&_up_title=test&_up_target=gone",
        headers={"X-Up-Version": "2.1.1"},
    )
    up.finalize_response(None)
    assert adapter.response_headers == {
        "X-Up-Location": "/test?a=b",  # _up_ params are dropped (history support)
        "X-Up-Method": "GET",
    }
