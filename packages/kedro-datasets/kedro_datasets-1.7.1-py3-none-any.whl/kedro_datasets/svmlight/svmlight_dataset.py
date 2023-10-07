"""``SVMLightDataset`` loads/saves data from/to a svmlight/libsvm file using an
underlying filesystem (e.g.: local, S3, GCS). It uses sklearn functions
``dump_svmlight_file`` to save and ``load_svmlight_file`` to load a file.
"""
import warnings
from copy import deepcopy
from pathlib import PurePosixPath
from typing import Any, Dict, Optional, Tuple, Union

import fsspec
from kedro.io.core import Version, get_filepath_str, get_protocol_and_path
from numpy import ndarray
from scipy.sparse.csr import csr_matrix
from sklearn.datasets import dump_svmlight_file, load_svmlight_file

from kedro_datasets import KedroDeprecationWarning
from kedro_datasets._io import AbstractVersionedDataset, DatasetError

# NOTE: kedro.extras.datasets will be removed in Kedro 0.19.0.
# Any contribution to datasets should be made in kedro-datasets
# in kedro-plugins (https://github.com/kedro-org/kedro-plugins)

# Type of data input
_DI = Tuple[Union[ndarray, csr_matrix], ndarray]
# Type of data output
_DO = Tuple[csr_matrix, ndarray]


class SVMLightDataset(AbstractVersionedDataset[_DI, _DO]):
    """``SVMLightDataset`` loads/saves data from/to a svmlight/libsvm file using an
    underlying filesystem (e.g.: local, S3, GCS). It uses sklearn functions
    ``dump_svmlight_file`` to save and ``load_svmlight_file`` to load a file.

    Data is loaded as a tuple of features and labels. Labels is NumPy array,
    and features is Compressed Sparse Row matrix.

    This format is a text-based format, with one sample per line. It does
    not store zero valued features hence it is suitable for sparse datasets.

    This format is used as the default format for both svmlight and the
    libsvm command line programs.

    Example usage for the
    `YAML API <https://kedro.readthedocs.io/en/stable/data/\
    data_catalog_yaml_examples.html>`_:

    .. code-block:: yaml

        svm_dataset:
          type: svmlight.SVMLightDataset
          filepath: data/01_raw/location.svm
          load_args:
            zero_based: False
          save_args:
            zero_based: False

        cars:
          type: svmlight.SVMLightDataset
          filepath: gcs://your_bucket/cars.svm
          fs_args:
            project: my-project
          credentials: my_gcp_credentials
          load_args:
            zero_based: False
          save_args:
            zero_based: False

    Example usage for the
    `Python API <https://kedro.readthedocs.io/en/stable/data/\
    advanced_data_catalog_usage.html>`_:
    ::

        >>> from kedro_datasets.svmlight import SVMLightDataset
        >>> import numpy as np
        >>>
        >>> # Features and labels.
        >>> data = (np.array([[0, 1], [2, 3.14159]]), np.array([7, 3]))
        >>>
        >>> dataset = SVMLightDataset(filepath="test.svm")
        >>> dataset.save(data)
        >>> reloaded_features, reloaded_labels = dataset.load()
        >>> assert (data[0] == reloaded_features).all()
        >>> assert (data[1] == reloaded_labels).all()

    """

    DEFAULT_LOAD_ARGS: Dict[str, Any] = {}
    DEFAULT_SAVE_ARGS: Dict[str, Any] = {}

    def __init__(  # noqa: PLR0913
        self,
        filepath: str,
        load_args: Dict[str, Any] = None,
        save_args: Dict[str, Any] = None,
        version: Optional[Version] = None,
        credentials: Dict[str, Any] = None,
        fs_args: Dict[str, Any] = None,
        metadata: Dict[str, Any] = None,
    ) -> None:
        """Creates a new instance of SVMLightDataset to load/save data from a svmlight/libsvm file.

        Args:
            filepath: Filepath in POSIX format to a text file prefixed with a protocol like `s3://`.
                If prefix is not provided, `file` protocol (local filesystem) will be used.
                The prefix should be any protocol supported by ``fsspec``.
            load_args: Arguments passed on to ``load_svmlight_file``.
                See the details in
                https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_svmlight_file.html
            save_args: Arguments passed on to ``dump_svmlight_file``.
                See the details in
                https://scikit-learn.org/stable/modules/generated/sklearn.datasets.dump_svmlight_file.html
            version: If specified, should be an instance of
                ``kedro.io.core.Version``. If its ``load`` attribute is
                None, the latest version will be loaded. If its ``save``
                attribute is None, save version will be autogenerated.
            credentials: Credentials required to get access to the underlying filesystem.
                E.g. for ``GCSFileSystem`` it should look like `{"token": None}`.
            fs_args: Extra arguments to pass into underlying filesystem class constructor
                (e.g. `{"project": "my-project"}` for ``GCSFileSystem``).
            metadata: Any arbitrary metadata.
                This is ignored by Kedro, but may be consumed by users or external plugins.
        """
        _fs_args = deepcopy(fs_args) or {}
        _fs_open_args_load = _fs_args.pop("open_args_load", {})
        _fs_open_args_save = _fs_args.pop("open_args_save", {})
        _credentials = deepcopy(credentials) or {}

        protocol, path = get_protocol_and_path(filepath, version)

        self._protocol = protocol
        if protocol == "file":
            _fs_args.setdefault("auto_mkdir", True)
        self._fs = fsspec.filesystem(self._protocol, **_credentials, **_fs_args)

        self.metadata = metadata

        super().__init__(
            filepath=PurePosixPath(path),
            version=version,
            exists_function=self._fs.exists,
            glob_function=self._fs.glob,
        )

        self._load_args = deepcopy(self.DEFAULT_LOAD_ARGS)
        if load_args is not None:
            self._load_args.update(load_args)
        self._save_args = deepcopy(self.DEFAULT_SAVE_ARGS)
        if save_args is not None:
            self._save_args.update(save_args)

        _fs_open_args_load.setdefault("mode", "rb")
        _fs_open_args_save.setdefault("mode", "wb")
        self._fs_open_args_load = _fs_open_args_load
        self._fs_open_args_save = _fs_open_args_save

    def _describe(self):
        return {
            "filepath": self._filepath,
            "protocol": self._protocol,
            "load_args": self._load_args,
            "save_args": self._save_args,
            "version": self._version,
        }

    def _load(self) -> _DO:
        load_path = get_filepath_str(self._get_load_path(), self._protocol)
        with self._fs.open(load_path, **self._fs_open_args_load) as fs_file:
            return load_svmlight_file(fs_file, **self._load_args)

    def _save(self, data: _DI) -> None:
        save_path = get_filepath_str(self._get_save_path(), self._protocol)
        with self._fs.open(save_path, **self._fs_open_args_save) as fs_file:
            dump_svmlight_file(data[0], data[1], fs_file, **self._save_args)

        self._invalidate_cache()

    def _exists(self) -> bool:
        try:
            load_path = get_filepath_str(self._get_load_path(), self._protocol)
        except DatasetError:
            return False

        return self._fs.exists(load_path)

    def _release(self) -> None:
        super()._release()
        self._invalidate_cache()

    def _invalidate_cache(self) -> None:
        """Invalidate underlying filesystem caches."""
        filepath = get_filepath_str(self._filepath, self._protocol)
        self._fs.invalidate_cache(filepath)


_DEPRECATED_CLASSES = {
    "SVMLightDataSet": SVMLightDataset,
}


def __getattr__(name):
    if name in _DEPRECATED_CLASSES:
        alias = _DEPRECATED_CLASSES[name]
        warnings.warn(
            f"{repr(name)} has been renamed to {repr(alias.__name__)}, "
            f"and the alias will be removed in Kedro-Datasets 2.0.0",
            KedroDeprecationWarning,
            stacklevel=2,
        )
        return alias
    raise AttributeError(f"module {repr(__name__)} has no attribute {repr(name)}")
