from . import activity_pub_object_id_from_html_body, parse_fediverse_handle


def test_parse_fediverse_handle():
    assert parse_fediverse_handle("account") == ("account", None)
    assert parse_fediverse_handle("account@domain") == ("account", "domain")

    assert parse_fediverse_handle("account@domain@@@") == ("account", "domain@@@")
    assert parse_fediverse_handle("@account@domain@@@") == ("account", "domain@@@")
    assert parse_fediverse_handle("@account") == ("account", None)


def test_activity_pub_object_id_from_html_body():
    object_id = "https://bovine.example/object_id"
    body = f"""\
<!DOCTYPE HTML>
<html>
<head>
<link href="{object_id}"
rel="alternate"
type="application/activity+json" />
</head>
<body>
Test case 1; link header in head
</body>
</html>
"""

    result = activity_pub_object_id_from_html_body(body)

    assert result == object_id
