from collective.transmute import _types as t
from {{ cookiecutter.python_package_name }}.utils.querystring import cleanup_querystring


POST_PROCESSING_STEP = "collective.transmute.steps.post_querystring.process_querystring"


async def process_collection(
    item: t.PloneItem, state: t.PipelineState
) -> t.PloneItemGenerator:
    anno = state.annotations
    prefixes = anno.get("paths", {}).get("prefix_replacement", ())
    subjects = anno.get("subjects_mapping", {})
    query = item.get("query", [])
    if query:
        item["query"], post_processing = cleanup_querystring(query, prefixes, subjects)
        if post_processing:
            uid = item["UID"]
            if uid not in state.post_processing:
                state.post_processing[uid] = []
            state.post_processing[uid].append(POST_PROCESSING_STEP)
    yield item
