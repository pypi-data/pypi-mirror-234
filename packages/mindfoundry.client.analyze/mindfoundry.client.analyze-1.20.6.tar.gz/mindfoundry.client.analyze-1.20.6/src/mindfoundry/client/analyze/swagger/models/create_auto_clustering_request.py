from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.nlp_language import NlpLanguage
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateAutoClusteringRequest")

@attr.s(auto_attribs=True)
class CreateAutoClusteringRequest:
    """
    Attributes:
        name (str):
        data_set_id (int):
        minimum_clusters (int):
        maximum_clusters (int):
        description (Union[Unset, str]):
        excluded_columns (Union[Unset, List[str]]):
        nlp_language (Union[Unset, NlpLanguage]):  Default: NlpLanguage.AUTO_DETECT.
    """

    name: str
    data_set_id: int
    minimum_clusters: int
    maximum_clusters: int
    description: Union[Unset, str] = UNSET
    excluded_columns: Union[Unset, List[str]] = UNSET
    nlp_language: Union[Unset, NlpLanguage] = NlpLanguage.AUTO_DETECT
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        data_set_id = self.data_set_id
        minimum_clusters = self.minimum_clusters
        maximum_clusters = self.maximum_clusters
        description = self.description
        excluded_columns: Union[Unset, List[str]] = UNSET
        if not isinstance(self.excluded_columns, Unset):
            excluded_columns = self.excluded_columns




        nlp_language: Union[Unset, str] = UNSET
        if not isinstance(self.nlp_language, Unset):
            nlp_language = self.nlp_language.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "dataSetId": data_set_id,
            "minimumClusters": minimum_clusters,
            "maximumClusters": maximum_clusters,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if excluded_columns is not UNSET:
            field_dict["excludedColumns"] = excluded_columns
        if nlp_language is not UNSET:
            field_dict["nlpLanguage"] = nlp_language

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        data_set_id = d.pop("dataSetId")

        minimum_clusters = d.pop("minimumClusters")

        maximum_clusters = d.pop("maximumClusters")

        description = d.pop("description", UNSET)

        excluded_columns = cast(List[str], d.pop("excludedColumns", UNSET))


        _nlp_language = d.pop("nlpLanguage", UNSET)
        nlp_language: Union[Unset, NlpLanguage]
        if isinstance(_nlp_language,  Unset):
            nlp_language = UNSET
        else:
            nlp_language = NlpLanguage(_nlp_language)




        create_auto_clustering_request = cls(
            name=name,
            data_set_id=data_set_id,
            minimum_clusters=minimum_clusters,
            maximum_clusters=maximum_clusters,
            description=description,
            excluded_columns=excluded_columns,
            nlp_language=nlp_language,
        )

        create_auto_clustering_request.additional_properties = d
        return create_auto_clustering_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
