import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.sso_configuration_authentication_flow import SsoConfigurationAuthenticationFlow
from ..types import UNSET, Unset

T = TypeVar("T", bound="SsoConfiguration")


@attr.s(auto_attribs=True)
class SsoConfiguration:
    """
    Attributes:
        domain (str):
        authentication_flow (SsoConfigurationAuthenticationFlow):
        enabled (bool):
        organization_id (Union[Unset, str]):
        default_role_id (Union[Unset, str]):
        default_team_id (Union[Unset, str]):
        default_account_id (Union[Unset, None, str]):
        client_id (Union[Unset, None, str]):
        issuer (Union[Unset, None, str]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    domain: str
    authentication_flow: SsoConfigurationAuthenticationFlow
    enabled: bool
    organization_id: Union[Unset, str] = UNSET
    default_role_id: Union[Unset, str] = UNSET
    default_team_id: Union[Unset, str] = UNSET
    default_account_id: Union[Unset, None, str] = UNSET
    client_id: Union[Unset, None, str] = UNSET
    issuer: Union[Unset, None, str] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        domain = self.domain
        authentication_flow = self.authentication_flow.value

        enabled = self.enabled
        organization_id = self.organization_id
        default_role_id = self.default_role_id
        default_team_id = self.default_team_id
        default_account_id = self.default_account_id
        client_id = self.client_id
        issuer = self.issuer
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "domain": domain,
                "authenticationFlow": authentication_flow,
                "enabled": enabled,
            }
        )
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if default_role_id is not UNSET:
            field_dict["defaultRoleId"] = default_role_id
        if default_team_id is not UNSET:
            field_dict["defaultTeamId"] = default_team_id
        if default_account_id is not UNSET:
            field_dict["defaultAccountId"] = default_account_id
        if client_id is not UNSET:
            field_dict["clientId"] = client_id
        if issuer is not UNSET:
            field_dict["issuer"] = issuer
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        domain = d.pop("domain")

        authentication_flow = SsoConfigurationAuthenticationFlow(d.pop("authenticationFlow"))

        enabled = d.pop("enabled")

        organization_id = d.pop("organizationId", UNSET)

        default_role_id = d.pop("defaultRoleId", UNSET)

        default_team_id = d.pop("defaultTeamId", UNSET)

        default_account_id = d.pop("defaultAccountId", UNSET)

        client_id = d.pop("clientId", UNSET)

        issuer = d.pop("issuer", UNSET)

        id = d.pop("id", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        sso_configuration = cls(
            domain=domain,
            authentication_flow=authentication_flow,
            enabled=enabled,
            organization_id=organization_id,
            default_role_id=default_role_id,
            default_team_id=default_team_id,
            default_account_id=default_account_id,
            client_id=client_id,
            issuer=issuer,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

        sso_configuration.additional_properties = d
        return sso_configuration

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
