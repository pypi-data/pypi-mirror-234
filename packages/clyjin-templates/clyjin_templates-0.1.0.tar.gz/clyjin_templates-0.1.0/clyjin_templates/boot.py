from pathlib import Path

from clyjin.base import PluginInitializeData

from clyjin_templates.template.group_service import TemplateGroupService
from clyjin_templates.utils.service import Service
from clyjin_templates.utils.servicehub import ServiceHub


class Boot:
    _SERVICE_CLASSES: list[type[Service]] = [
        TemplateGroupService,
    ]

    def __init__(self, data: PluginInitializeData) -> None:
        self._data: PluginInitializeData = data
        self._groups_dir = Path(
            self._data.called_plugin_common_sysdir,
            "templategroups",
        )


    async def start(self) -> None:
        services: list[Service] = []
        service: Service

        for ServiceClass in self._SERVICE_CLASSES:
            if ServiceClass is TemplateGroupService:
                service = TemplateGroupService(
                    root_dir=self._data.root_dir,
                    groups_dir=self._groups_dir,
                )
            else:
                service = ServiceClass()
            services.append(service)

        ServiceHub(services)
