from __future__ import annotations

import abc
import json
import time
from base64 import b64decode
from logging import getLogger
from typing import Any, Literal

import uvicorn
from fastapi import FastAPI, Request

MODEL_NAME = "slingshot-model"

logger = getLogger(__name__)

Prediction = dict[str, Any]


class InferenceModel(abc.ABC):
    """
    Base class for starting a Slingshot deployment, aka inference model server.
    Extend this class and implement the load and predict methods to create a Slingshot deployment.
    """

    def __init__(self) -> None:
        self.is_ready: bool = False

        self.app = FastAPI()
        self.app.get("/")(self.v1_liveness_check)
        self.app.get("/v1/models")(self.v1_models)
        self.app.get("/v1/models/{model_name}")(self.v1_model_metadata)
        self.app.post(f"/v1/models/{MODEL_NAME}:predict", response_model=dict[str, Any])(self.v1_predict)
        self.app.on_event("startup")(self.startup_event)

    @abc.abstractmethod
    async def load(self) -> None:
        """
        Slingshot will call this method to load the model.

        Implementation example:
            self.model = torch.load("/mnt/model/model.pt")
        """
        ...

    @abc.abstractmethod
    async def predict(self, examples: list[bytes]) -> Prediction | list[Prediction]:
        """
        Slingshot will call this method to make predictions, passing in the raw request bytes and returns a dictionary.
        For text inputs, the bytes will be the UTF-8 encoded string.

        If the model is not batched, the input will be a list with a single element and the output should be a single
        dictionary as the prediction response. Otherwise, the input will be a list of examples and the output should be
        a list of dictionaries with the same length and order as the input.

        Implementation example:
            example_text = examples[0].decode("utf-8")
            return self.model(example_text)
        """
        ...

    @staticmethod
    async def v1_liveness_check() -> dict[str, str]:
        return {"status": "alive"}

    @staticmethod
    async def v1_models() -> dict[str, list[str]]:
        return {"models": [MODEL_NAME]}

    async def v1_model_metadata(self, model_name: str) -> Prediction:
        return {"name": MODEL_NAME, "ready": self.is_ready}

    async def v1_predict(self, request: "Request") -> Prediction | dict[Literal["predictions"], list[Prediction]]:
        req_body = await request.body()
        payload = json.loads(req_body)

        # If not batched, return single prediction
        if "example" in payload:
            raw_input = b64decode(payload["example"])
            prediction = await self._predict_with_latency([raw_input])
            if isinstance(prediction, dict):
                return prediction
            assert len(prediction) == 1, "Non-batched predict must return a single prediction"
            return prediction[0]

        # If batched, return batched predictions
        assert "instances" in payload, "Batched payload must contain 'instances' key"
        logger.debug(f"Received {len(payload['instances'])} batched examples")
        examples = [b64decode(example_obj['example']) for example_obj in payload['instances']]
        predictions = await self._predict_with_latency(examples)
        return {"predictions": predictions}

    async def startup_event(self) -> None:
        await self.load()
        self.is_ready = True

    async def _predict_with_latency(self, examples: list[bytes]) -> Prediction | list[Prediction]:
        """Returns prediction result and logs model latency in milliseconds"""
        start = time.time()
        result = await self.predict(examples)
        end = time.time()
        elapsed_ms = (end - start) * 1000
        logger.debug(f"predict_ms: {elapsed_ms:.2f}")
        return result

    def start(self) -> None:
        uvicorn.run(self.app, host="0.0.0.0", port=8080)
