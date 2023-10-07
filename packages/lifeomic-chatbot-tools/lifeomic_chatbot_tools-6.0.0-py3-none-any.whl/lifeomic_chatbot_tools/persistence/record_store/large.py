import time
import typing as t

from lifeomic_chatbot_tools.aws.s3 import S3Client
from lifeomic_chatbot_tools.persistence.record_store.base import IRecord, IRecordStore
from lifeomic_chatbot_tools.persistence.record_store.dynamodb import DynamoDBRecordStore, KeyDict, TIDynamoDBRecord


TRecord = t.TypeVar("TRecord")


class ILargeRecord(IRecord, t.Protocol[TIDynamoDBRecord]):
    """
    Represents a database record whose payload is persisted in S3. This allows for very large records. The id
    and queryable attributes are stored in DynamoDB, but the payload is persisted in S3.
    """

    def get_attrs(self) -> TIDynamoDBRecord:
        """Gets this record's queryable attributes sub-record, which should have the same id as this record."""
        ...

    def get_body(self) -> bytes:
        """Gets the potentially large body of the record."""
        ...

    @classmethod
    def attrs_id_to_body_id(cls, attrs_id: KeyDict) -> str:
        """Converts the DynamoDB attributes id to the format used for storing the record body under in S3."""
        ...

    @classmethod
    def body_id_to_attrs_id(cls, body_id: str) -> KeyDict:
        """Converts the S3-formatted record id to the DynamoDB style used for storing the record attributes."""
        ...

    @classmethod
    def reconstitute(cls, attrs: TIDynamoDBRecord, body: bytes) -> "ILargeRecord":
        """Reconstitutes a record from its separated attributes and body."""
        ...


TILargeRecord = t.TypeVar("TILargeRecord", bound=ILargeRecord)


class ConsistencyError(Exception):
    """Raised when a data consistency error occurs in a LargeRecordStore operation."""

    pass


class LargeRecordStore(t.Generic[TILargeRecord, TIDynamoDBRecord], IRecordStore[str, TILargeRecord]):
    """
    A record store, backed by DynamoDB and S3, which supports very large records. The queryable attributes are stored
    in a pointer object in DynamoDB, and the actual record body is stored in a linked S3 object.
    """

    def __init__(
        self,
        bucket_name: str,
        record_class: t.Type[TILargeRecord],
        attrs_store: DynamoDBRecordStore[TIDynamoDBRecord],
        wait_between_retries=0.5,
        max_retries=4,
    ):
        self._record_class = record_class
        self._attrs_store = attrs_store
        self._s3 = S3Client()
        self._bucket = bucket_name
        self._retry_wait = wait_between_retries
        self._n_retries = max_retries

    def save(self, record: TILargeRecord):
        """Persist a potentially large record, saving its queryable attributes in DynamoDB, and its body to S3."""
        # Save the queryable attributes.
        self._attrs_store.save(record.get_attrs())
        # Save the potentially large payload.
        self._s3.client.put_object(Bucket=self._bucket, Body=record.get_body(), Key=record.get_id())

    def get(self, id_: str) -> t.Optional[TILargeRecord]:
        """Gets the components of a record, reconstitutes it, then returns the record."""
        attrs_id = self._record_class.body_id_to_attrs_id(id_)
        attrs, body = None, None
        body = self._s3.get_object(self._bucket, id_)
        if body is not None:
            # Since `body` exists, we expect `attrs` to exist as well. Therefore we do a `get` for the attrs with a
            # retry. The retry is needed because S3 has strong consistency while DynamoDB only has eventual consistency.
            attrs = self._get_attrs_with_retry(attrs_id)
        else:
            # Try to get the `attrs` anyways, just to catch a potential consistency issue.
            attrs = self._attrs_store.get(attrs_id)
        if attrs is None and body is None:
            return None
        if attrs is not None and body is not None:
            return t.cast(TILargeRecord, self._record_class.reconstitute(attrs, body))
        raise ConsistencyError(
            f"during get, attrs ({attrs_id}) exists == {attrs is not None} "
            f"while body ({id_}) exists == {body is not None}"
        )

    def delete(self, id_: str) -> bool:
        """
        Deletes all components of a record. Returns `True` if the function completes without raising any exceptions.
        The case where a component does not exist at the time of deletion is not treated as an error
        because the component can be considered already deleted.
        """
        attrs_id = self._record_class.body_id_to_attrs_id(id_)
        self._attrs_store.delete(attrs_id)
        self._s3.delete_object(self._bucket, id_)
        return True

    def get_all(self, *conditions: t.Tuple[str, str, t.Any], **where_equals) -> t.Iterable[TILargeRecord]:
        """Get all chunks satisfying the condition, then de-chunk into single records."""
        for attrs in self._attrs_store.get_all(*conditions, **where_equals):
            attrs_id = attrs.get_id()
            body_id = self._record_class.attrs_id_to_body_id(attrs_id)
            body = self._s3.get_object(self._bucket, body_id)
            if body is None:
                raise ConsistencyError(
                    f"during get_all, attrs ({attrs_id}) exists == True while body ({body_id}) exists == False"
                )
            yield t.cast(TILargeRecord, self._record_class.reconstitute(attrs, body))

    def delete_all(self, *conditions: t.Tuple[str, str, t.Any], **where_equals) -> int:
        n_deleted = 0
        for attrs in self._attrs_store.get_all(*conditions, **where_equals):
            n_deleted += int(self.delete(self._record_class.attrs_id_to_body_id(attrs.get_id())))
        return n_deleted

    def _get_attrs_with_retry(self, id_: KeyDict):
        attrs = None
        for _ in range(self._n_retries + 1):
            attrs = self._attrs_store.get(id_)
            if attrs is not None:
                break
            time.sleep(self._retry_wait)
        return attrs
