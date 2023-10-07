import json
from typing import Any, Optional

import requests

from ..configuration import Configuration, config
from ..util import unwrap
from .api_http import headers
from .api_request import provision_req


class SubstationAPI:
    """
    Class for handle Substation API calls.
    """

    def __init__(self, configuration: Configuration = config) -> None:
        self.url = f"{configuration.substation_endpoint}/completions"
        self.req = provision_req(configuration._token_api)

    # This is the template that works best with the mpt-30b-instruct model;
    # strongly advised to use this format.
    # TODO: Generalize this to support other models
    def _format_prompt(self, instruction: str) -> str:
        template = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n###Instruction\n{instruction}\n\n### Response\n"  # noqa
        return template.format(instruction=instruction)

    def predict(
        self,
        prompt: str,
        max_output_length: Optional[int] = 3000,
        model_specific_prompt: Optional[bool] = True,
    ) -> Any:
        if model_specific_prompt:
            prompt = self._format_prompt(prompt)
        result = unwrap(
            self.req(
                lambda access_token: requests.post(
                    self.url,
                    headers=headers(access_token),
                    json={"max_tokens": max_output_length, "prompt": prompt},
                )
            )
        )

        if (
            type(result) is str
        ):  # Substation FIX, It needs to returns content-type: application/json
            return json.loads(result)
        else:
            return result
