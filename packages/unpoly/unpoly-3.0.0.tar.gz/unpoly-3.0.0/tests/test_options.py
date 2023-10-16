import json

from unpoly.adapter import BaseAdapter
from unpoly.options import Options


def test_parsing_from_request_headers():
    options = Options.parse(
        {
            "version": "2.2.1",
            "target": "[up-main~=modal]",
            "mode": "modal",
            "context": '{"test": "test"}',
            "fail_target": "[up-main~=fail]",
            "fail_mode": "fail",
            "fail_context": '{"fail": "fail"}',
            "validate": "field",
            "dismiss_layer": "null",
        },
        BaseAdapter(),
    )

    assert options.version == "2.2.1"
    assert options.target == "[up-main~=modal]"
    assert options.mode == "modal"
    assert options.context == {"test": "test"}
    assert options.fail_target == "[up-main~=fail]"
    assert options.fail_mode == "fail"
    assert options.fail_context == {"fail": "fail"}
    assert options.validate == "field"
    assert options.dismiss_layer is None


def test_parse_broken_options():
    options = Options.parse({"context": "'a'a", "events": "'b'b"}, BaseAdapter())
    assert options.context == {}
    assert options.events == []


def test_parsing_with_diff():
    initial = {"existing": 1, "to_delete": True, "do_no_touch": "yes"}
    diff = {"to_delete": None, "existing": 2, "new_thing": 3}
    options = Options.parse(
        {"context": json.dumps(initial), "context_diff": json.dumps(diff)},
        BaseAdapter(),
    )
    assert options.initial_context == initial
    assert options.context_diff == diff
    assert options.context == {"existing": 2, "do_no_touch": "yes", "new_thing": 3}


def test_context_diff():
    options = Options(context={"existing": 1, "to_delete": True, "do_no_touch": "yes"})
    del options.context["to_delete"]
    options.context["existing"] = 2
    options.context["new_thing"] = 3
    assert options.context_diff == {
        "to_delete": None,
        "existing": 2,
        "new_thing": 3,
    }


def test_serialize():
    assert Options(target="target").serialize(BaseAdapter()) == {}

    options = Options(
        context={"test": "test"},
        events=[{"test": "event"}],
        title="test",
        accept_layer=None,
        dismiss_layer={"test": "layer"},
        expire_cache="users/*",
    )
    options.context["change"] = "yes"  # Triggers diff rendering
    options.server_target = "new_target"  # Trigger target

    assert options.serialize(BaseAdapter()) == {
        "context": '{"change":"yes"}',  # This is just the diff!
        "events": '[{"test":"event"}]',
        "title": '"test"',
        "accept_layer": "null",
        "dismiss_layer": '{"test":"layer"}',
        "target": "new_target",
        "expire_cache": "users/*",
    }
