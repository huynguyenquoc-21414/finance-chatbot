from typing import Optional
from langchain_core.tools import BaseTool
from langchain_core.callbacks import BaseCallbackManager
from langchain_core._api import deprecated
from pydantic import Field
from pydantic.json_schema import SkipJsonSchema


class CustomBaseTool(BaseTool):
    callback_manager: SkipJsonSchema[Optional[BaseCallbackManager]] = deprecated(
        name="callback_manager", since="0.1.7", removal="1.0", alternative="callbacks"
    )(
        Field(
            default=None,
            exclude=True,
            description="Callback manager to add to the run trace.",
        )
    )
