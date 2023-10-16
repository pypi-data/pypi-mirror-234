from dataclasses import dataclass
from typing import Any, Dict, List

from pydantic.utils import deep_update

from kelvin.sdk.lib.configs.general_configs import GeneralConfigs
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import ApplicationFlavour
from kelvin.sdk.lib.models.apps.ksdk_app_setup import Directory, File
from kelvin.sdk.lib.models.factories.project.project import ProjectBase, ProjectFileTree
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.types import FileType
from kelvin.sdk.lib.schema.schema_manager import generate_base_schema_template
from kelvin.sdk.lib.utils.general_utils import dict_to_yaml


class ProjectDockerDefaultFileTree(ProjectFileTree):
    @staticmethod
    def get_tree_dict(app_root: KPath, **kwargs: Any) -> Dict:
        return {FileType.ROOT.value: {"file_type": FileType.CONFIGURATION, "directory": app_root}}

    def fundamental_dirs(self) -> List[Directory]:
        return [self.root]

    def optional_dirs(self) -> List[Directory]:
        return []


@dataclass
class KelvinV2Project(ProjectBase):
    flavour_registry = {
        ApplicationFlavour.default: ProjectDockerDefaultFileTree,
        ApplicationFlavour.template: ProjectDockerDefaultFileTree,
    }

    def get_template_parameters(self) -> Dict:
        app_name = self.creation_parameters.app_name
        app_description = self.creation_parameters.app_description
        dir_path = self.creation_parameters.app_dir
        app_config_file = GeneralConfigs.default_app_config_file
        app_root_dir_path: KPath = KPath(dir_path) / app_name

        return {
            "app_root": app_root_dir_path,
            "app_name": app_name,
            "app_description": app_description,
            "app_version": GeneralConfigs.default_app_version,
            "app_config_file": app_config_file,
            "title": app_name.title(),
        }

    def _build_app_config_file(self, app_config_file_path: KPath) -> File:
        app_configuration = generate_base_schema_template(project_creation_parameters_object=self.creation_parameters)

        if self.creation_parameters.app_flavour == ApplicationFlavour.default:
            app_configuration = deep_update(
                app_configuration,
                {
                    "app": {
                        "kelvin": {
                            "assets": [{"name": "<asset_name>"}],
                            "outputs": [{"data_type": "number", "name": "<output_name>"}],
                        }
                    },
                    "system": {"environment_vars": [{"name": "KELVIN_GW_MODE", "value": "SOCKETS"}]},
                },
            )
        elif self.creation_parameters.app_flavour == ApplicationFlavour.template:
            app_configuration = deep_update(
                app_configuration,
                {
                    "app": {
                        "kelvin": {
                            "assets": [
                                {
                                    "name": "asset1",
                                    "parameters": {
                                        "param-number": {"value": 7.5},
                                        "param-string": {"value": "goodbye"},
                                    },
                                }
                            ],
                            "inputs": [
                                {
                                    "name": "input-number",
                                    "data_type": "number",
                                    "sources": [{"names": ["input-number-datastream"]}],
                                }
                            ],
                            "outputs": [
                                {
                                    "name": "output-number",
                                    "data_type": "number",
                                    "targets": [{"names": ["output-number-datastream"]}],
                                },
                                {
                                    "name": "output-random-number",
                                    "data_type": "number",
                                    "targets": [{"names": ["output-random-number-datastream"]}],
                                },
                                {
                                    "name": "output-random-boolean",
                                    "data_type": "boolean",
                                    "targets": [{"names": ["output-random-boolean-datastream"]}],
                                },
                                {
                                    "name": "output-random-string",
                                    "data_type": "string",
                                    "targets": [{"names": ["output-random-string-datastream"]}],
                                },
                                {
                                    "name": "output-cc-number",
                                    "data_type": "number",
                                    "control_change": True,
                                    "targets": [{"names": ["output-cc-number-datastream"]}],
                                },
                            ],
                            "parameters": [
                                {"name": "param-number", "data_type": "number", "default": {"value": 3.5}},
                                {"name": "param-string", "data_type": "string", "default": {"value": "hello world"}},
                            ],
                            "configuration": {"foo": {"bar": "hello world"}},
                        }
                    },
                    "system": {"environment_vars": [{"name": "KELVIN_GW_MODE", "value": "SOCKETS"}]},
                },
            )

        app_configuration_yaml: str = dict_to_yaml(content=app_configuration)
        file = File(file=app_config_file_path, content=app_configuration_yaml)

        return file

    def _build_file_tree(self) -> ProjectFileTree:
        # 1 - Configuration files, app dir and files
        parameters: dict = self.get_template_parameters()
        app_config_file = parameters.get("app_config_file", "")
        app_root_dir_path = parameters.get("app_root", "")

        project_file_tree_class = self.get_flavour_class()
        parameters.update(**project_file_tree_class.get_extra_template_parameters())

        # directory file tree required for a docker project
        project_type = self.creation_parameters.app_type
        kelvin_app_flavour = self.creation_parameters.app_flavour

        file_tree: ProjectFileTree = project_file_tree_class.from_tree(
            app_root=app_root_dir_path,
            template_parameters=parameters,
            project_type=project_type,
            kelvin_app_flavour=kelvin_app_flavour,
        )

        # append app config file
        app_config_file_path: KPath = app_root_dir_path / app_config_file
        file = self._build_app_config_file(app_config_file_path=app_config_file_path)
        file_tree.root.files.append(file)

        return file_tree
