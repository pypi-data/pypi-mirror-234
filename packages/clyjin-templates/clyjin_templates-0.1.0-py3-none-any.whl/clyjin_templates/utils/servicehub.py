import typing

from antievil import NotFoundError

from clyjin_templates.utils.service import Service, ServiceType
from clyjin_templates.utils.singleton import Singleton


class ServiceHub(Singleton):
    """
    Stores all services.
    """
    def __init__(
        self,
        services: list[Service],
    ) -> None:
        super().__init__()

        self._service_by_class: dict[type[Service], Service] = {}

        self._save_services(services)

    def get(self, ServiceClass: type[ServiceType]) -> ServiceType:
        try:
            return typing.cast(
                ServiceType,
                self._service_by_class[ServiceClass],
            )
        except KeyError as error:
            raise NotFoundError(
                title="service class",
                value=ServiceClass,
            ) from error

    def _save_services(self, services: list[Service]) -> None:
        for service in services:
            self._service_by_class[type(service)] = service
