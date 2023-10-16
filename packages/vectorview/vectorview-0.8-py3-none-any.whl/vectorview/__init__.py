import requests
from typing import List, Tuple, Dict, Any, Union, Optional

class Vectorview:
    """
    A class to interact with the Vectorview backend.
    
    Attributes
    ----------
    key : str
        Authentication key to interact with the endpoint.
    project_id : str
        Leave empty if you are not given one. Identifier for the project interacting with the endpoint. Default is "default".
    verbose : bool
        Flag to toggle printing of debug information. Default is False.
    """

    def __init__(self, key: str, project_id: str = "default", verbose: bool = False):
        """
        Initializes the Vectorview instance.
        """
        self.key = key
        self.project_id = project_id
        self.verbose = verbose

    def _convert_to_string(self, o: Any) -> Any:
        """
        Convert all values in an object to strings.

        Parameters
        ----------
        o : Any
            The object whose nested items are to be converted to strings.

        Returns
        -------
        Any
            The object with all nested items converted to strings.
        """
        if isinstance(o, list):
            return [self._convert_to_string(item) for item in o]
        if isinstance(o, dict):
            return {k: self._convert_to_string(v) for k, v in o.items()}
        return str(o)

    def event(self, query: str, docs_with_score: List[Tuple[Union[str, Any], float]], query_metadata: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Logs an event to Vectorview, with payload containing query, documents, and metadata.

        Parameters
        ----------
        query : str
            A string representing the query to be sent in the event.
        docs_with_score : List[Tuple[Union[str, langchain.schema.Document], float]]
            A list of tuples, each containing a document and a corresponding score. 
            The document can be a string or a langchain Document (or any other object with `page_content` and `metadata` attributes).
        query_metadata : Dict[str, Any], optional
            Additional metadata related to the query. Default is an empty dictionary.

        Returns
        -------
        requests.Response
            The HTTP response returned after sending the event.
        """
        if query_metadata is None:
            query_metadata = {}

        documents = []
        for doc, score in docs_with_score:
            # Check if doc is a string
            if isinstance(doc, str):
                text_content = doc
                metadata_content = {}
            # Otherwise, assume it's an object with expected attributes
            else:
                text_content = doc.page_content
                metadata_content = doc.metadata

            documents.append({
                "text": text_content,
                "distance": score,
                "metadata": metadata_content
            })

        payload = {
            'sender': 'py',
            'vv_key': self.key,
            'project_id': self.project_id,
            'query': query,
            'documents': documents,
            'metadata': query_metadata
        }
        payload = self._convert_to_string(payload)

        if self.verbose:
            print("Payload", payload)

        response = requests.post('https://europe-west1-miko-17c4e.cloudfunctions.net/event', json=payload)
        
        if self.verbose:
            print("Response", response)

        return response

