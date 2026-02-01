from collective.transmute.steps.ids.prefixes import _path_prefixes
from collective.transmute.utils import querystring as qs_utils


def cleanup_querystring(
    query, prefixes: tuple[tuple[str, str], ...], subjects: dict[str, str]
) -> tuple[list[dict], bool]:
    query, post_processing = qs_utils.cleanup_querystring(query)
    new_query = []
    for item in query:
        new_item = {**item}
        if new_item.get("o") == "plone.app.querystring.operation.string.path":
            value = new_item.get("v", "")
            if value.startswith("/Plone"):
                value = value[len("/Plone") :]
            new_item["o"] = "plone.app.querystring.operation.string.absolutePath"
            new_item["v"] = _path_prefixes(prefixes, value)
        elif new_item.get("i") == "Subject":
            values = new_item.get("v", [])
            new_values = set()
            for v in values:
                v = v.strip()
                if v in subjects:
                    sub = subjects[v]
                    if sub:
                        new_values.add(sub)
                else:
                    if v:
                        new_values.add(v)
            new_item["v"] = list(new_values)
        new_query.append(new_item)
    return new_query, post_processing
