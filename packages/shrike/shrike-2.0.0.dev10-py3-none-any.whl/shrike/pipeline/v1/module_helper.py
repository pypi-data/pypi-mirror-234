# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
Pipeline helper class to create pipelines loading modules from a flexible manifest.
"""
from abc import abstractmethod, ABC
import logging
from packaging.specifiers import SpecifierSet
from packaging.version import Version, InvalidVersion

from azure.ml.component import Component
from azure.ml.component._core._component_definition import ComponentDefinition

from shrike.pipeline.v1.aml_connect import current_workspace
from shrike.pipeline.module_helper_base import AMLModuleLoaderBase

log = logging.getLogger(__name__)


class AMLModuleLoader(AMLModuleLoaderBase):
    def load_local_module_helper(self, module_spec_path):
        return Component.from_yaml(yaml_file=module_spec_path)

    def solve_module_version_and_load(
        self, module_name, module_version, module_cache_key, registry=None
    ):
        """Loads module class if exists

        Args:
            module_name (str): name of the module to load
            module_version (str): version of the module to load
            module_cache_key (str): cache key of the module after loading
            registy (str): registry name if loading from a registry
        """
        module_version = self.solve_module_version(
            module_name,
            module_version,
            workspace=current_workspace() if registry is None else None,
            registry=registry,
        )

        loaded_module_class = Component.load(
            current_workspace(),
            name=module_name,
            version=module_version,
            registry=registry,
        )

        self.put_in_cache(module_cache_key, loaded_module_class)
        return loaded_module_class

    def solve_module_version(
        self, module_name, module_version, workspace=None, registry=None
    ):
        if module_version is None:
            return module_version

        try:
            module_version_PEP440 = Version(module_version)
            if str(module_version_PEP440) != module_version:
                log.warning(
                    "We suggest adopting PEP440 versioning for your component {module_name}!"
                )

        except InvalidVersion as e:
            log.info(f"{module_version} is a version constraint. Try to solve it...")

            spec = SpecifierSet(module_version)
            if registry:
                components = ComponentDefinition.list(
                    registry_name=registry, name=module_name
                )
            elif workspace:
                components = ComponentDefinition.list(
                    workspace=workspace, name=module_name
                )

            versions = []
            for component in components:
                version = component.version
                version_PEP440 = Version(version)
                if str(version_PEP440) != version:
                    log.warning(
                        f"Version {version} does not follow PEP440 versioning, skipping ..."
                    )
                else:
                    versions.append(version_PEP440)

            compatible_versions = list(spec.filter(versions))
            if compatible_versions:
                module_version = max(compatible_versions)
                log.info(f"Solved version for {module_name} is {module_version}.")

            else:
                raise ValueError(
                    f"No version exists for the constraint {module_version}. Existing versions: {versions}"
                )

        return str(module_version)
