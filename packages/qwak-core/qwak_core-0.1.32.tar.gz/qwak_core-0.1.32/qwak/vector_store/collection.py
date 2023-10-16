from dataclasses import dataclass
from typing import Dict, List, Optional, TypeVar, Union

from _qwak_proto.qwak.vectors.v1.vector_pb2 import (
    DoubleVector,
    Property,
    SearchResult as ProtoSearchResult,
    StoredVector,
)
from qwak.clients.vector_store.serving_client import VectorServingClient
from qwak.exceptions import QwakException
from qwak.vector_store.filters import Filter
from qwak.vector_store.inference_client import VectorStoreInferenceClient
from typeguard import typechecked

NaturalInput = TypeVar("T")
NaturalInputs = List[NaturalInput]
Vector = List[float]
Properties = Dict[str, Union[str, int, bool, float]]


@dataclass
class SearchResult:
    """
    A class used to represent the result of a vector similarity search operation.

     Attributes:
         properties (dict): The dictionary of properties to attach with the vectors
         id (str): The vector object unique identifier
         vector (Vector): The vector values
         distance (int): The distance metric indicating how similar the vector is to the search query.
             Smaller values indicate higher similarity.
    """

    properties: Properties
    id: Optional[str]
    vector: Optional[Vector]
    distance: Optional[float]


class Collection:
    """
    The Collection class is a Python class that provides functionalities for handling operations on vectors within a
    specific collection in a vector store. This class should be used after a collection has been created or fetched
    using `VectorStoreClient`.

    The Collection class allows you to:
        * **Search for Similar Vectors**: This helps in finding vectors that are most similar to a given query vector.
        * **Upsert Vectors**: This operation allows you to insert new vectors into the collection or update existing
            vectors if they already exist.
        * **Delete Vectors by ID**: This operation deletes vectors based on their unique identifiers
    """

    id: str
    name: str
    metric: str
    dimension: int
    description: Optional[str]
    vectorizer: Optional[str]

    _vector_serving_client: VectorServingClient
    _type_to_proto_property_mapping: Dict[str, TypeVar] = {
        str: "string_val",
        bool: "bool_val",
        int: "int_val",
        float: "double_val",
    }

    _proto_property_to_type_mapping = {
        v: k for k, v in _type_to_proto_property_mapping.items()
    }

    def __init__(
        self,
        id: str,
        name: str,
        metric: str,
        dimension: int,
        vector_serving_client: VectorServingClient,
        description: Optional[str] = None,
        vectorizer: Optional[str] = None,
    ):
        """
        Initializes a `Collection` client object to interact with Qwak's vector serving service. Should not be created
        directly - created or fetched using the `VectorStoreClient` object.
        """
        self.id = id
        self.name = name
        self.description = description
        self.metric = metric
        self.dimension = dimension
        self.vectorizer = vectorizer
        self._vector_serving_client = vector_serving_client
        self._realtime_inference_client = None

        if vectorizer:
            self._realtime_inference_client = VectorStoreInferenceClient(
                model_id=self.vectorizer.lower().replace(" ", "_").replace("-", "_")
            )

    @typechecked
    def search(
        self,
        output_properties: List[str],
        vector: Optional[Vector] = None,
        natural_input: Optional[NaturalInput] = None,
        top_results: int = 1,
        include_id: bool = True,
        include_vector: bool = False,
        include_distance: bool = False,
        filter: Optional[Filter] = None,
    ) -> List[SearchResult]:
        """
        Searches for vectors in the collection that are most similar to a given query vector.
        Vector similarity is a measure of the closeness or similarity between two vectors. In the context of machine
        learning, vectors often represent points in a high-dimensional space, and the concept of similarity between
        vectors can be crucial for many tasks such as clustering, classification, and nearest-neighbor searches.

        Parameters:
            output_properties (list): A list of property fields to include in the results.
            vector (list): The vector to get the most similar vectors to according to the distance metric
            natural_input (any): Natural inputs (text, image) which should be embedded by the collection and, and
              according to the resulting embedding - get the most similar vectors
            top_results (int): The number of relevant results to return
            include_id (list): Whether to include the vector ID's in the result set
            include_vector (list): Whether to include the vector values themselves in the result set
            include_distance (list): Whether to include the distance calculations to the result set
            filter (Filter): Pre-filtering search results

        Returns:
            List[SearchResult]: A list of SearchResult object, which is used as a container for the search results

        Raises:
            QwakException: If you don't provide either vectors or natural_inputs
            QwakException: If you provide both vectors and natural_inputs
        """
        if bool(vector) and bool(natural_input):
            raise QwakException(
                "Only one of `vectors` or `natural` inputs should be defined and not empty."
            )

        if natural_input:
            vector = self._transform_natural_input_to_vectors(
                natural_input=natural_input
            )
        proto_filter = filter._to_proto() if filter else None

        return [
            self._to_search_result(
                result,
                include_id=include_id,
                include_distance=include_distance,
                include_vector=include_vector,
            )
            for result in self._vector_serving_client.search(
                collection_name=self.name,
                vector=vector,
                properties=output_properties,
                top_results=top_results,
                include_id=include_id,
                include_vector=include_vector,
                include_distance=include_distance,
                filters=proto_filter,
            )
        ]

    @typechecked
    def upsert(
        self,
        ids: List[str],
        properties: List[Properties],
        vectors: Optional[List[Vector]] = None,
        natural_inputs: Optional[NaturalInputs] = None,
    ) -> None:
        """
        Inserts new vectors into the collection or updates existing vectors. Notice that this method will overwrite
        existing vectors with the same IDs.

        Parameters:
            ids (str): A list of vector ids to be added
            vectors (list): The list of vectors to add. This attribute or `natural_inputs` must be set
            natural_inputs (list): Natural inputs (text, image) which should be embedded by the collection and added
              to the store. This attribute or `vectors` must be set
            properties (dict): A dictionary of properties to attach with the vectors

        Raises:
            QwakException: If you don't provide either vectors or natural_inputs
            QwakException: If you provide both vectors and natural_inputs
        """

        if bool(vectors) and bool(natural_inputs):
            raise QwakException(
                "`vectors` or `natural` inputs should be defined and not empty. But not both"
            )

        if natural_inputs:
            vectors = self._transform_natural_input_list_to_vectors(
                natural_inputs=natural_inputs
            )

        if (len(vectors) != len(ids)) or (len(properties) != len(ids)):
            raise QwakException(
                "Non matching lengths for input list (vectors / natural inputs), ID's, and properties list. "
                "Make sure all 3 fields are aligned in length"
            )

        for zipped_vectors_chunks in self._divide_chunks(
            list(zip(ids, vectors, properties)), 100
        ):
            self._vector_serving_client.upsert_vectors(
                collection_name=self.name,
                vectors=[
                    StoredVector(
                        id=vector_object[0],
                        vector=DoubleVector(element=vector_object[1]),
                        properties=[
                            self._build_property(key, value)
                            for (key, value) in vector_object[2].items()
                        ],
                    )
                    for vector_object in zipped_vectors_chunks
                ],
            )

    @typechecked
    def delete(self, vector_ids: List[str]) -> int:
        """
        Deletes vectors from the collection based on their IDs.

        Parameters:
            vector_ids (list): A list of vector IDs to delete.

        Returns:
            int: Number of actual vectors deleted from the collection
        """
        return sum(
            self._vector_serving_client.delete_vectors(
                collection_name=self.name, vector_ids=ids_chunk
            )
            for ids_chunk in self._divide_chunks(vector_ids, 100)
        )

    def _to_search_result(
        self,
        search_result: ProtoSearchResult,
        include_id: bool,
        include_vector: bool,
        include_distance: bool,
    ) -> SearchResult:
        return SearchResult(
            id=search_result.id if include_id else None,
            vector=[e for e in search_result.vector.element]
            if include_vector
            else None,
            distance=search_result.distance if include_distance else None,
            properties={
                prop.name: self._extract_value_with_type(prop)
                for prop in search_result.properties
            },
        )

    @staticmethod
    def _divide_chunks(list_to_break, chunk_size):
        for i in range(0, len(list_to_break), chunk_size):
            yield list_to_break[i : i + chunk_size]

    def _build_property(self, key: str, value: Union[str, int, bool, float]):
        type_val = self._type_to_proto_property_mapping.get(type(value), None)
        if not type_val:
            raise QwakException(
                f"Cannot upsert vector with property value type {type(value)}. "
                f"Supported types are: {list(self._type_to_proto_property_mapping.keys())}"
            )

        property_args = {"name": key, type_val: value}
        return Property(**property_args)

    def _extract_value_with_type(self, prop: Property):
        type_caster = self._proto_property_to_type_mapping.get(
            prop.WhichOneof("value_type"), None
        )
        if not type_caster:
            raise QwakException(
                f"Cannot deserialize property with type {type(type_caster)}. This means an invalid property type"
                f" was registered to the platform. Please delete and add the vector object again."
            )

        return type_caster(getattr(prop, prop.WhichOneof("value_type")))

    def _transform_natural_input_to_vectors(
        self, natural_input: NaturalInput
    ) -> Vector:
        if not self.vectorizer:
            raise QwakException(
                "Unable to search by natural input because the collection does not have a Vectorizer defined."
            )
        feature_vector = [
            {
                "input": natural_input,
            }
        ]
        try:
            result_list = self._realtime_inference_client.predict(feature_vector)
        except Exception as e:
            raise QwakException(
                f"Vectorizer {self.vectorizer} failed to transform input {feature_vector} to vectors. Error is: {str(e)}"
            )
        try:
            vector = result_list[0]["embeddings"]
        except Exception:
            raise QwakException(
                f"Vectorizer {self.vectorizer} must return a dataframe containing an `embeddings` column"
            )
        if not vector:
            raise QwakException(
                f"Vectorizer {self.vectorizer} did not return embeddings for the given natural input. Unable to continue with the query."
            )
        return vector

    def _transform_natural_input_list_to_vectors(
        self, natural_inputs: NaturalInputs
    ) -> List[Vector]:
        return [
            self._transform_natural_input_to_vectors(natural_input=natural_input)
            for natural_input in natural_inputs
        ]
