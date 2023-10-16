# Vectorview API

`Vectorview` is a Python class designed to interact with the [Vectorview](https://www.vectorview.ai/) backend.

## Methods

### `__init__(key, project_id='default', verbose=False)`

Creates an instance of the `Vectorview` class.

#### Parameters

- `key: str` - Authentication key to interact with the endpoint.
- `project_id: str` - (Optional, leave blank if not given one) Identifier for the project interacting with the endpoint. Default is "default".
- `verbose: bool` - (Optional) Flag to toggle printing of debug information. Default is False.

### `event(query, docs_with_score, query_metadata=None) -> requests.Response`

Logs an event to Vectorview, with payload containing query, documents, and metadata.

#### Parameters

- `query: str` - A string representing the query.
- `docs_with_score: List[Tuple[Union[str, Any], float]]` - A list of tuples, each containing a document and a corresponding score. The document can be a string or a [langchain Document](https://docs.langchain.com/docs/components/schema/document) (or any other object with `page_content` and `metadata` attributes).
- `query_metadata: Dict[str, Any], optional` - (Optional) Additional metadata related to the query. Default is an empty dictionary.

#### Returns

- `requests.Response` - The HTTP response returned after sending the event.

