"""Integration layer for the deep research LangGraph within Open Notebook."""

from typing import Any, Dict, Optional

from langchain_core.runnables import RunnableConfig

from open_deep_research.deep_researcher import deep_researcher_builder


# Compile the deep research graph without persistent checkpointing for now.
graph = deep_researcher_builder.compile()


def build_runnable_config(
    notebook_id: Optional[str],
    overrides: Optional[Dict[str, Any]] = None,
) -> RunnableConfig:
    """Prepare a runnable config that injects notebook-aware defaults."""

    configurable: Dict[str, Any] = {}

    if notebook_id:
        configurable["notebook_id"] = notebook_id
        configurable.setdefault("notebook_search", {"enabled": True})
    else:
        configurable.setdefault("notebook_search", {"enabled": True})

    if overrides:
        sanitized_overrides = dict(overrides)
        sanitized_overrides.pop("mcp_config", None)
        notebook_search_override = sanitized_overrides.pop("notebook_search", None)
        configurable.update(sanitized_overrides)
        if notebook_search_override is not None:
            base_notebook_search = configurable.get("notebook_search", {"enabled": True})
            configurable["notebook_search"] = {**base_notebook_search, **notebook_search_override}

    if "notebook_search" not in configurable:
        configurable["notebook_search"] = {"enabled": True}

    return RunnableConfig(configurable=configurable)
