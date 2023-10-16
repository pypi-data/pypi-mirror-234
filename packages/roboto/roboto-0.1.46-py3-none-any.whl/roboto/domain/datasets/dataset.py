import collections.abc
import dataclasses
import pathlib
from typing import Any, Callable, Optional

import pathspec

from ...auth import Permissions
from ...query import QuerySpecification
from ...serde import (
    git_paths_match,
    pydantic_jsonable_dict,
)
from ...updates import (
    MetadataChangeset,
    StrSequence,
    UpdateCondition,
)
from ..files import (
    File,
    FileDelegate,
    FileTag,
    S3Credentials,
)
from ..files.progress import (
    TqdmProgressMonitorFactory,
)
from .delegate import (
    Credentials,
    DatasetDelegate,
    StorageLocation,
)
from .record import Administrator, DatasetRecord


@dataclasses.dataclass
class FileUploadInfo:
    bucket: str
    key: str
    transaction_id: str


class Dataset:
    __dataset_delegate: DatasetDelegate
    __file_delegate: FileDelegate
    __record: DatasetRecord
    __temp_credentials: Optional[Credentials] = None

    @classmethod
    def create(
        cls,
        dataset_delegate: DatasetDelegate,
        file_delegate: FileDelegate,
        administrator: Administrator = Administrator.Roboto,
        storage_location: StorageLocation = StorageLocation.S3,
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        tags: Optional[list[str]] = None,
        description: Optional[str] = None,
    ) -> "Dataset":
        record = dataset_delegate.create_dataset(
            administrator,
            metadata,
            storage_location,
            tags,
            org_id,
            created_by,
            description,
        )
        return cls(record, dataset_delegate, file_delegate)

    @classmethod
    def from_id(
        cls,
        dataset_id: str,
        dataset_delegate: DatasetDelegate,
        file_delegate: FileDelegate,
        org_id: Optional[str] = None,
    ) -> "Dataset":
        record = dataset_delegate.get_dataset_by_primary_key(dataset_id, org_id)
        return cls(record, dataset_delegate, file_delegate)

    @classmethod
    def query(
        cls,
        query: QuerySpecification,
        dataset_delegate: DatasetDelegate,
        file_delegate: FileDelegate,
        org_id: Optional[str] = None,
    ) -> collections.abc.Generator["Dataset", None, None]:
        known = set(DatasetRecord.__fields__.keys())
        actual = set()
        for field in query.fields():
            # Support dot notation for nested fields
            # E.g., "metadata.SoftwareVersion"
            if "." in field:
                actual.add(field.split(".")[0])
            else:
                actual.add(field)
        unknown = actual - known
        if unknown:
            plural = len(unknown) > 1
            msg = (
                "are not known attributes of Dataset"
                if plural
                else "is not a known attribute of Dataset"
            )
            raise ValueError(f"{unknown} {msg}. Known attributes: {known}")

        paginated_results = dataset_delegate.query_datasets(query, org_id=org_id)
        while True:
            for record in paginated_results.items:
                yield cls(record, dataset_delegate, file_delegate)
            if paginated_results.next_token:
                query.after = paginated_results.next_token
                paginated_results = dataset_delegate.query_datasets(
                    query, org_id=org_id
                )
            else:
                break

    def __init__(
        self,
        record: DatasetRecord,
        dataset_delegate: DatasetDelegate,
        file_delegate: FileDelegate,
    ) -> None:
        self.__dataset_delegate = dataset_delegate
        self.__file_delegate = file_delegate
        self.__record = record

    @property
    def dataset_id(self) -> str:
        return self.__record.dataset_id

    @property
    def metadata(self) -> dict[str, Any]:
        return self.__record.metadata.copy()

    @property
    def record(self) -> DatasetRecord:
        return self.__record

    @property
    def tags(self) -> list[str]:
        return self.__record.tags.copy()

    def complete_upload(self, upload_id: str) -> None:
        """
        Marks an upload as 'completed', which allows the Roboto Platform to evaluate triggers for automatic action on
        incoming data. This also aides reporting on partial upload failure cases.

        This API is called implicitly by the `upload_file` and `upload_directory` operations, and should only be
        used explicitly in power-user scenarios.

        Args:
            upload_id: An ID for a particular upload transaction which is granted by RobotoService when upload
                credentials are requested.

        Returns:
            None
        """
        self.__dataset_delegate.complete_upload(
            dataset_id=self.__record.dataset_id,
            upload_id=upload_id,
            org_id=self.__record.org_id,
        )

    def delete_dataset(self) -> None:
        self.__dataset_delegate.delete_dataset(self.__record)

    def delete_files(
        self,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
    ) -> None:
        """
        Delete files associated with this dataset.

        `include_patterns` and `exclude_patterns` are lists of gitignore-style patterns.
        See https://git-scm.com/docs/gitignore.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> dataset.delete_files(
            ...    include_patterns=["**/*.png"],
            ...    exclude_patterns=["**/back_camera/**"]
            ... )

        """
        for file in self.list_files(include_patterns, exclude_patterns):
            file.delete()

    def download_files(
        self,
        out_path: pathlib.Path,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
    ) -> None:
        """
        Download files associated with this dataset to the given directory.
        If `out_path` does not exist, it will be created.

        `include_patterns` and `exclude_patterns` are lists of gitignore-style patterns.
        See https://git-scm.com/docs/gitignore.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> dataset.download_files(
            ...     pathlib.Path("/tmp/tmp.nV1gdW5WHV"),
            ...     include_patterns=["**/*.g4"],
            ...     exclude_patterns=["**/test/**"]
            ... )
        """
        if (
            self.__record.storage_location != StorageLocation.S3
            or self.__record.administrator != Administrator.Roboto
        ):
            raise NotImplementedError(
                "Only S3-backed storage administered by Roboto is supported at this time."
            )

        if not out_path.is_dir():
            out_path.mkdir(parents=True)

        def _credential_provider():
            return self.get_temporary_credentials(
                Permissions.ReadOnly
            ).to_s3_credentials()

        for file in self.list_files(include_patterns, exclude_patterns):
            local_path = out_path / file.relative_path
            file.download(
                local_path,
                _credential_provider,
                progress_monitor_factory=TqdmProgressMonitorFactory(concurrency=1),
            )

    def get_temporary_credentials(
        self,
        permissions: Permissions = Permissions.ReadOnly,
        caller: Optional[str] = None,  # A Roboto user_id
        force_refresh: bool = False,
        transaction_id: Optional[str] = None,
    ) -> Credentials:
        if (
            force_refresh
            or permissions == Permissions.ReadWrite
            or self.__temp_credentials is None
            or self.__temp_credentials.is_expired()
        ):
            self.__temp_credentials = self.__dataset_delegate.get_temporary_credentials(
                self.__record, permissions, caller, transaction_id
            )
        return self.__temp_credentials

    def list_files(
        self,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
    ) -> collections.abc.Generator[File, None, None]:
        """
        List files associated with this dataset.

        `include_patterns` and `exclude_patterns` are lists of gitignore-style patterns.
        See https://git-scm.com/docs/gitignore.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> for file in dataset.list_files(
            ...     include_patterns=["**/*.g4"],
            ...     exclude_patterns=["**/test/**"]
            ... ):
            ...     print(file.relative_path)
        """

        paginated_results = self.__dataset_delegate.list_files(
            self.__record.dataset_id, self.__record.org_id
        )
        while True:
            for record in paginated_results.items:
                file = File(record, self.__file_delegate)
                if not git_paths_match(
                    include_patterns=include_patterns,
                    exclude_patterns=exclude_patterns,
                    file=file.relative_path,
                ):
                    continue

                yield file
            if paginated_results.next_token:
                paginated_results = self.__dataset_delegate.list_files(
                    self.__record.dataset_id,
                    self.__record.org_id,
                    paginated_results.next_token,
                )
            else:
                break

    def put_metadata(
        self,
        metadata: dict[str, Any],
        updated_by: Optional[str] = None,  # A Roboto user_id
    ) -> None:
        """
        Set each `key`: `value` in this dict as dataset metadata if it doesn't exist, else overwrite the existing value.
        Keys must be strings. Dot notation is supported for nested keys.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> dataset.put_metadata({
            ...     "foo": "bar",
            ...     "baz.qux": 101,
            ... })

        """
        self.update(
            metadata_changeset=MetadataChangeset(put_fields=metadata),
            updated_by=updated_by,
        )

    def put_tags(
        self,
        tags: StrSequence,
        updated_by: Optional[str] = None,  # A Roboto user_id
    ) -> None:
        """Add each tag in this sequence if it doesn't exist"""
        self.update(
            metadata_changeset=MetadataChangeset(put_tags=tags),
            updated_by=updated_by,
        )

    def refresh(self) -> None:
        """Refresh the underlying dataset record with the latest server state."""
        self.__record = self.__dataset_delegate.get_dataset_by_primary_key(
            self.__record.dataset_id, self.__record.org_id
        )

    def remove_metadata(
        self,
        metadata: StrSequence,
        updated_by: Optional[str] = None,  # A Roboto user_id
    ) -> None:
        """
        Remove each key in this sequence from dataset metadata if it exists.
        Keys must be strings. Dot notation is supported for nested keys.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> dataset.remove_metadata(["foo", "baz.qux"])
        """
        self.update(
            metadata_changeset=MetadataChangeset(remove_fields=metadata),
            updated_by=updated_by,
        )

    def remove_tags(
        self,
        tags: StrSequence,
        updated_by: Optional[str] = None,  # A Roboto user_id
    ) -> None:
        """Remove each tag in this sequence if it exists"""
        self.update(
            metadata_changeset=MetadataChangeset(remove_tags=tags),
            updated_by=updated_by,
        )

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    def upload_directory(
        self,
        directory_path: pathlib.Path,
        exclude_patterns: Optional[list[str]] = None,
    ) -> None:
        """
        Upload everything, recursively, in directory, ignoring files that match any of the ignore patterns.

        `exclude_patterns` is a list of gitignore-style patterns.
        See https://git-scm.com/docs/gitignore#_pattern_format.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> dataset.upload_directory(
            ...     pathlib.Path("/path/to/directory"),
            ...     exclude_patterns=[
            ...         "__pycache__/",
            ...         "*.pyc",
            ...         "node_modules/",
            ...         "**/*.log",
            ...     ],
            ... )
        """
        if not directory_path.is_dir():
            raise ValueError(f"{directory_path} is not a directory")

        exclude_spec: Optional[pathspec.PathSpec] = None
        if exclude_patterns is not None:
            exclude_spec = pathspec.GitIgnoreSpec.from_lines(
                exclude_patterns,
            )

        credentials = self.get_temporary_credentials(Permissions.ReadWrite)

        def _credential_provider():
            return self.get_temporary_credentials(
                Permissions.ReadWrite,
                force_refresh=True,
                transaction_id=credentials.upload_id,
            ).to_s3_credentials()

        def _upload_directory(directory_path: pathlib.Path, key_prefix: str) -> None:
            for path in directory_path.iterdir():
                if path.is_dir():
                    _upload_directory(path, f"{key_prefix}/{path.name}")
                else:
                    if exclude_spec is not None and exclude_spec.match_file(path):
                        continue
                    self.__upload_file(
                        path,
                        f"{key_prefix}/{path.name}",
                        credentials,
                        _credential_provider,
                    )

        _upload_directory(directory_path, "")

        # Eventually we should error on credentials.upload_id is None, but we'll handle it gracefully
        # for backwards compatible rollout
        if credentials.upload_id is not None:
            self.complete_upload(upload_id=credentials.upload_id)

    def upload_file(
        self,
        local_file_path: pathlib.Path,
        key: str,
        credentials: Optional[Credentials] = None,
        credential_provider: Optional[Callable[[], S3Credentials]] = None,
    ) -> FileUploadInfo:
        """
        Uploads a file to the dataset's storage location.
        """
        upload_info = self.__upload_file(
            local_file_path, key, credentials, credential_provider
        )

        self.complete_upload(upload_info.transaction_id)

        return upload_info

    def update(
        self,
        metadata_changeset: Optional[MetadataChangeset] = None,
        conditions: Optional[list[UpdateCondition]] = None,
        description: Optional[str] = None,
        updated_by: Optional[str] = None,  # A Roboto user_id
    ) -> None:
        updated = self.__dataset_delegate.update(
            self.__record,
            metadata_changeset=metadata_changeset,
            conditions=conditions,
            description=description,
            updated_by=updated_by,
        )
        self.__record = updated

    def __upload_file(
        self,
        local_file_path: pathlib.Path,
        key: str,
        credentials: Optional[Credentials] = None,
        credential_provider: Optional[Callable[[], S3Credentials]] = None,
    ) -> FileUploadInfo:
        """
        Uploads a file to the dataset's storage location. Does not mark the upload as complete.
        """
        if not local_file_path.is_file():
            raise ValueError(f"{local_file_path} is not a file")

        if (
            self.__record.storage_location != StorageLocation.S3
            or self.__record.administrator != Administrator.Roboto
        ):
            raise NotImplementedError(
                "Only S3-backed storage administered by Roboto is supported at this time."
            )

        credentials = (
            credentials
            if credentials is not None
            else self.get_temporary_credentials(Permissions.ReadWrite)
        )

        upload_id = credentials.upload_id
        if upload_id is None:
            raise ValueError("Cannot upload a file without a valid upload_id")

        if credential_provider is None:

            def _credential_provider():
                return self.get_temporary_credentials(
                    Permissions.ReadWrite, transaction_id=upload_id
                ).to_s3_credentials()

            credential_provider = _credential_provider

        key = f"{credentials.required_prefix}/{key.lstrip('/')}"
        self.__file_delegate.upload_file(
            local_file_path,
            credentials.bucket,
            key,
            credential_provider,
            tags={
                FileTag.DatasetId: self.__record.dataset_id,
                FileTag.OrgId: self.__record.org_id,
                FileTag.CommonPrefix: credentials.required_prefix,
                FileTag.UploadId: upload_id,
            },
            progress_monitor_factory=TqdmProgressMonitorFactory(concurrency=1),
        )

        return FileUploadInfo(
            bucket=credentials.bucket,
            key=key,
            transaction_id=upload_id,
        )
