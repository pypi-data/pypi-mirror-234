from io import BytesIO
from typing import Callable, Optional, Union, IO

import numpy as np

from .interfaces import ModelProvider, DeepLearningClass
from .LocalModelProvider import LocalModelProvider
from .RemoteModelProvider import RemoteModelProvider


class MixedModelProvider(ModelProvider):
    """
    This class is a wrapper for both the LocalModelProvider and RemoteModelProvider classes, returning both local and remote models.
    """
    def __init__(self, models_path, url_base, api_key, temp_upload_dir, delete_old_models = True):
        self.remote_model_provider = RemoteModelProvider(models_path, url_base, api_key, temp_upload_dir, delete_old_models)
        self.local_model_provider = LocalModelProvider(models_path, temp_upload_dir)
        # load model lists
        self._refresh_model_lists()

    def _refresh_model_lists(self):
        self.remote_models = self.remote_model_provider.available_models()
        self.local_models = self.local_model_provider.available_models()

    def load_model(self, model_name: str, progress_callback: Optional[Callable[[int, int], None]] = None,
                   force_download: bool = False,
                   timestamp: Optional[Union[int, str]] = None) -> DeepLearningClass:
        """
        Loads a deep learning model.

        Parameters
        ----------
        model_name : str
            The name of the model to load.
        progress_callback: Callable[[int, int], None] (optional)
            Callback function for progress
        force_download: bool
            Sets the forced redownload of models
        timestamp: int or None
            Return a specific model version (default: latest)

        Returns
        -------
        The model object.

        """
        if model_name in self.remote_models:
            return self.remote_model_provider.load_model(model_name, progress_callback, force_download, timestamp)

        # this will fail if the model name is wrong
        return self.local_model_provider.load_model(model_name, progress_callback, force_download, timestamp)


    def model_details(self, model_name: str) -> dict:
        if model_name in self.remote_models:
            return self.remote_model_provider.model_details(model_name)
        return self.local_model_provider.model_details(model_name)

    def available_models(self) -> Optional[list[str]]:
        self._refresh_model_lists()
        return self.remote_models + [m for m in self.local_models if m not in self.remote_models]

    def get_local_models(self):
        return [m for m in self.local_models if m not in self.remote_models]

    def upload_model(self, model_name: str, model: DeepLearningClass, dice_score: float = 0.0) -> None:
        """
        Parameters
        ----------
        model_name : str
            The name of the model to upload.
        model:
            The model to be uploaded
        dice_score:
            The average dice score of the client
        """
        if model_name in self.remote_models:
            self.remote_model_provider.upload_model(model_name, model, dice_score)
            return
        self.local_model_provider.upload_model(model_name, model, dice_score)

    def upload_data(self, data: dict) -> None:
        """
        Uploads data to the server. Converts the data into a stream before calling _upload_bytes

        Parameters
        ----------
        data: dict
            Dictionary of objects that can be saved by Numpy and loaded without using pickle (which is unsafe)
        """
        bytes_io = BytesIO()
        np.savez_compressed(bytes_io, **data)
        self._upload_bytes(bytes_io)
        bytes_io.close()

    def _upload_bytes(self, data: IO):
        """
        Uploads generic data to the server. This is an internal function that implements the server communication.
        The actual function to be called by the client is upload_data with a dict

        Parameters
        ----------
        data: IO
            byte stream that is sent to the server.
        """
        self.remote_model_provider._upload_bytes(data)

    def log(self, msg: str):
        """
        Sends a message to the server to be logged

        Parameters
        ----------
        msg: str
            the message.
        """
        self.remote_model_provider.log(msg)

    def import_model(self, file_path, model_name):
        self.local_model_provider.import_model(file_path, model_name)