from __future__ import annotations

from slingshot.inference import InferenceModel, Prediction


class MyDeployment(InferenceModel):
    async def load(self) -> None:
        """
        Slingshot will call this method to load the model.

        Implementation example:
            self.model = torch.load("/mnt/model/model.pt")
        """
        ...

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
        return {}


if __name__ == "__main__":
    model = MyDeployment()
    model.start()
