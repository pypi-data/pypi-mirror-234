# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
V1 Pipeline helper class to create pipelines loading modules from a flexible manifest.
"""
from __future__ import annotations
import argparse
from abc import ABC
import os
import json
import logging
import uuid
from typing import Callable, Optional
from toposort import toposort_flatten
import yaml
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from toposort import toposort_flatten, CircularDependencyError
from dataclasses import dataclass, fields, asdict
from functools import lru_cache, wraps
from itertools import groupby

try:
    import hydra
    from hydra.core.hydra_config import HydraConfig
    from omegaconf import DictConfig, OmegaConf, MISSING
    from flatten_dict import flatten

    import azureml
    from azureml.core import Datastore
    from azureml.core import Dataset
    from azureml.pipeline.core import PipelineRun
    from azure.ml.component.component import Component, Input, Output
    from azure.ml.component.pipeline import Pipeline
    from azure.ml.component._pipeline_parameters import PipelineParameter
    from azureml.exceptions._azureml_exception import UserErrorException
except ImportError as error:
    raise ImportError(
        f"{error.msg}. Please install using `pip install shrike[pipeline]`."
    )

from shrike import __version__
from shrike.pipeline.pipeline_helper_base import AMLPipelineHelperBase
from shrike.pipeline.v1.aml_connect import azureml_connect, current_workspace
from shrike.pipeline.v1.module_helper import AMLModuleLoader
from shrike.pipeline.pipeline_config import (
    HDI_DEFAULT_CONF,
    pipeline_compute_config,
    uw_compute_config,
)

log = logging.getLogger(__name__)


class AMLPipelineHelper(AMLPipelineHelperBase, ABC):
    def __init__(self, config, module_loader=None):
        """Constructs the pipeline helper.

        Args:
            config (DictConfig): config for this object
            module_loader (AMLModuleLoader): which module loader to (re)use
        """
        if module_loader is None:
            log.info(
                f"Creating instance of AMLModuleLoader for {self.__class__.__name__}"
            )
            module_loader = AMLModuleLoader(config)
        super(AMLPipelineHelper, self).__init__(
            config=config, module_loader=module_loader
        )

    def _get_job_status(self, job):
        return job.get_status()

    def _wait_for_job_completion(self, job):
        return job.wait_for_completion(show_output=True)

    ##################################
    ### USER FACING HELPER METHODS ###
    ##################################
    @lru_cache()
    def component_load(self, component_key) -> Callable[..., "Component"]:
        """Loads one component from the manifest"""
        component_func = self.module_loader.load_module(
            component_key, self.required_modules()
        )

        @wraps(component_func)
        def wrapper(*args, **kwargs):
            component_step = component_func(*args, **kwargs)
            if not self.unified_workspace:
                # In unified workspace, we don't know which location/environment to use
                # so we will not call apply_smart_runsettings by default
                log.info(
                    f"Now try applying the smart runsettting as component post load operation after component initialize: "
                )
                self.apply_smart_runsettings(component_step)
                log.info(f"Successfully applied the smart runsettting. ")
            return component_step

        return wrapper

    @lru_cache()
    def module_load(self, module_key):
        """Loads one module from the manifest"""
        module_func = self.module_loader.load_module(
            module_key, self.required_modules()
        )

        @wraps(module_func)
        def wrapper(*args, **kwargs):
            module_step = module_func(*args, **kwargs)
            if not self.unified_workspace:
                log.info(
                    f"Now try applying the smart runsettting as component post load operation after component initialize: "
                )
                self.apply_smart_runsettings(module_step)
                log.info(f"Successfully applied the smart runsettting. ")
            return module_step

        return wrapper

    @lru_cache()
    def dataset_load(
        self,
        name,
        version="latest",
        datastore=None,
        path_on_datastore=None,
        description=None,
    ):
        """Loads a dataset by either id or name. If the workspace does not contain this dataset and path is given, create the dataset.

        Args:
            name (str): name or uuid of dataset to load
            version (str): if loading by name, used to specify version (default "latest")
            datastore (str): datastore for registering the dataset as <name>
            path_on_datastore (str): path for registering the dataset as <name>
            description (str): description of dataset to register
        """
        try:
            return self._dataset_load_by_name_or_id(name, version)
        except UserErrorException:
            log.info(
                f"Dataset {name} not found. Try registering from {path_on_datastore} on {datastore}..."
            )
            dataset = Dataset.File.from_files(
                path=[(Datastore(self.workspace(), datastore), path_on_datastore)],
                validate=False,
            )
            dataset = dataset.register(
                workspace=self.workspace(),
                name=name,
                description=description,
                create_new_version=True,
            )
            return dataset

    @lru_cache()
    def workspace(self):
        """Gets the current workspace"""
        return current_workspace()

    def connect(self):
        """Connect to the AML workspace using internal config"""
        # Only call azureml_connect if there is not an already a pre-existing workspace
        try:
            return self.workspace()
        except:
            return azureml_connect(
                aml_subscription_id=self.config.aml.subscription_id,
                aml_resource_group=self.config.aml.resource_group,
                aml_workspace_name=self.config.aml.workspace_name,
                aml_auth=self.config.aml.auth,
                aml_tenant=self.config.aml.tenant,
                aml_force=self.config.aml.force,
            )  # NOTE: this also stores aml workspace in internal global variable

    ################
    ### MAIN/RUN ###
    ################
    def apply_recommended_runsettings(
        self,
        module_name,
        module_instance,
        gpu=False,  # can't autodetect that
        hdi="auto",
        windows="auto",
        parallel="auto",
        mpi="auto",
        scope="auto",
        datatransfer="auto",
        sweep="auto",
        synapse="auto",
        location=None,
        environment=None,
        **custom_runtime_arguments,
    ):
        """Applies regular settings for a given module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            gpu (bool): is the module using GPU?
            hdi (bool): is the module using HDI/Spark?
            windows (bool): is the module using Windows compute?
            parallel (bool): is the module using ParallelRunStep?
            mpi (bool): is the module using Mpi?
            scope (bool): is the component using scope?
            datatransfer (bool): is the component using datatransfer?
            sweep (bool): is the component using sweep?
            synapse (bool): is the component using Synapse?
            location (str): location of the silo to use in unified workspace setting
            environment (str): environment of the silo to use in unified workspace setting
            custom_runtime_arguments (dict): any additional custom args
        """
        # Verifies if module_name corresponds to module_instance
        self._check_module_runsettings_consistency(module_name, module_instance)

        # Skips if this is a PipelineComponent
        if str(module_instance.type) == "PipelineComponent":
            log.info(f"Component {module_name} detected as PipelineComponent.")
            return

        if environment:
            assert environment.lower() in [
                "cloverport",
                "msit",
                "mdp",
                "dnd",
            ]  # TODO: what else allowed?

        # Auto detects runsettings
        if hdi == "auto":
            hdi = str(module_instance.type) == "HDInsightComponent"
            if hdi:
                log.info(f"Module {module_name} detected as HDI: {hdi}")

        if parallel == "auto":
            parallel = str(module_instance.type) == "ParallelComponent"
            if parallel:
                log.info(f"Module {module_name} detected as PARALLEL: {parallel}")

        if mpi == "auto":
            mpi = str(module_instance.type) == "DistributedComponent"
            if mpi:
                log.info(f"Module {module_name} detected as MPI: {mpi}")

        if scope == "auto":
            scope = str(module_instance.type) == "ScopeComponent"
            if scope:
                log.info(f"Module {module_name} detected as SCOPE: {scope}")

        if sweep == "auto":
            sweep = str(module_instance.type) == "SweepComponent"
            if sweep:
                log.info(f"Module {module_name} detected as SweepComponent: {sweep}")

        if synapse == "auto":
            synapse = str(module_instance.type) in ["SparkComponent", "spark"]
            if synapse:
                log.info(f"Module {module_name} detected as spark (Synapse): {synapse}")

        if windows == "auto":
            if (
                str(module_instance.type) == "HDInsightComponent"
                or str(module_instance.type) == "ScopeComponent"
                or str(module_instance.type) == "DataTransferComponent"
                or str(module_instance.type) == "SweepComponent"
                or str(module_instance.type) == "SparkComponent"
            ):
                # HDI/scope/datatransfer/sweep modules might not have that environment object
                windows = False
            else:
                windows = (
                    module_instance._definition.environment.os.lower() == "windows"
                )
                if windows:
                    log.info(f"Module {module_name} detected as WINDOWS: {windows}")

        if datatransfer == "auto":
            datatransfer = str(module_instance.type) == "DataTransferComponent"
            if datatransfer:
                log.info(
                    f"Module {module_name} detected as DATATRANSFER: {datatransfer}"
                )

        if parallel:
            self._apply_parallel_runsettings(
                module_name,
                module_instance,
                windows=windows,
                gpu=gpu,
                location=location,
                environment=environment,
                **custom_runtime_arguments,
            )
            return

        if sweep:
            self._apply_sweep_runsettings(
                module_name,
                module_instance,
                windows=windows,
                gpu=gpu,
                location=location,
                environment=environment,
                **custom_runtime_arguments,
            )
            return

        if windows:
            self._apply_windows_runsettings(
                module_name,
                module_instance,
                mpi=mpi,
                location=location,
                environment=environment,
                **custom_runtime_arguments,
            )
            return

        if hdi:
            self._apply_hdi_runsettings(
                module_name,
                module_instance,
                location=location,
                environment=environment,
                **custom_runtime_arguments,
            )
            return

        if scope:
            self._apply_scope_runsettings(
                module_name,
                module_instance,
                location=location,
                environment=environment,
                **custom_runtime_arguments,
            )
            return

        if datatransfer:
            self._apply_datatransfer_runsettings(
                module_name,
                module_instance,
                location=location,
                environment=environment,
                **custom_runtime_arguments,
            )
            return

        if synapse:
            self._apply_synapse_runsettings(
                module_name,
                module_instance,
                location=location,
                environment=environment,
                **custom_runtime_arguments,
            )
            return

        self._apply_linux_runsettings(
            module_name,
            module_instance,
            mpi=mpi,
            gpu=gpu,
            location=location,
            environment=environment,
            **custom_runtime_arguments,
        )

    def apply_smart_runsettings(
        self,
        component_instance,
        gpu=False,  # can't autodetect that
        hdi="auto",
        windows="auto",
        parallel="auto",
        mpi="auto",
        scope="auto",
        datatransfer="auto",
        sweep="auto",
        synapse="auto",
        location=None,
        environment=None,
        **custom_runtime_arguments,
    ):
        """Applies regular settings for a given component.

        Args:
            component_instance (Component): the AML component we need to add settings to
            gpu (bool): is the component using GPU?
            hdi (bool): is the component using HDI?
            windows (bool): is the component using Windows compute?
            parallel (bool): is the component using ParallelRunStep?
            mpi (bool): is the component using Mpi?
            scope (bool): is the component using scope?
            datatransfer (bool): is the component using datatransfer?
            sweep (bool): is the component using sweep?
            synapse (bool): is the component using Synapse?
            location (str): location of the silo to use in unified workspace setting
            environment (str): environment of the silo to use in unified workspace setting
            custom_runtime_arguments (dict): any additional custom args
        """
        # infer component_name
        component_name = self._get_component_name_from_instance(component_instance)
        self.apply_recommended_runsettings(
            component_name,
            component_instance,
            gpu,
            hdi,
            windows,
            parallel,
            mpi,
            scope,
            datatransfer,
            sweep,
            synapse,
            location,
            environment,
            **custom_runtime_arguments,
        )

    def _get_pipeline_run(self, run_id, experiment):
        return PipelineRun(experiment, self.config.run.pipeline_run_id)

    def _get_run_url(self, pipeline_run):
        return pipeline_run.get_portal_url()

    def _dataset_load_by_name_or_id(self, name, version):
        """Loads a dataset by either id or name.

        Args:
            name (str): name or uuid of dataset to load
            version (str): if loading by name, used to specify version (default "latest")

        NOTE: in AzureML SDK there are 2 different methods for loading dataset
        one for id, one for name. This method just wraps them up in one."""
        # test if given name is a uuid
        try:
            parsed_uuid = uuid.UUID(name)
            log.info(f"Getting a dataset handle [id={name}]...")
            return Dataset.get_by_id(self.workspace(), id=name)
        except ValueError:
            log.info(f"Getting a dataset handle [name={name} version={version}]...")
            return Dataset.get_by_name(self.workspace(), name=name, version=version)

    def _set_all_inputs_to(self, module_instance, input_mode):
        """Sets all module inputs to a given intput mode"""
        input_names = [
            a
            for a in dir(module_instance.inputs)
            if isinstance(getattr(module_instance.inputs, a), Input)
        ]
        for input_key in input_names:
            input_instance = getattr(module_instance.inputs, input_key)
            input_instance.configure(mode=input_mode)
            log.info(f"Configured input {input_key} to use mode {input_mode}")

    def _set_all_outputs_to(
        self, module_instance, output_mode, compliant=True, datastore_name=None
    ):
        """Sets all module outputs to a given output mode"""
        output_names = [
            a
            for a in dir(module_instance.outputs)
            if isinstance(getattr(module_instance.outputs, a), Output)
        ]
        if not datastore_name:
            datastore_name = self._get_datastore_name(module_instance, compliant)
        for output_key in output_names:
            output_instance = getattr(module_instance.outputs, output_key)
            if output_mode:
                output_instance.configure(output_mode=output_mode)
            output_instance.configure(datastore=datastore_name)
            log.info(
                f"Configured output {output_key} to use mode {output_mode} and datastore {datastore_name}"
            )

    @lru_cache()
    def _get_uw_configs(self, assets, key_func):
        assets_dict = {}
        for key, group in groupby(assets, key_func):
            for x in group:
                pass
            assets_dict[key] = x["name"]  # list(x["name"] for x in group)
        return assets_dict

    @lru_cache()
    def _get_uw_datastores(self, location: str, environment: str, dc: bool):
        environment = environment.lower()
        if environment == "cloverport":
            # no DC concept for eyes-on workspace
            key_func = lambda x: (x["location"].lower(), x["environment"].lower())
            return self._get_uw_configs(self.config.uw_config.datastores, key_func)[
                location, environment
            ]
        else:
            key_func = lambda x: (
                x["location"].lower(),
                x["environment"].lower(),
                x["DC"],
            )
            return self._get_uw_configs(self.config.uw_config.datastores, key_func)[
                location, environment, dc
            ]

    @lru_cache()
    def _get_uw_computes(
        self,
        location: str,
        environment: str,
        type: str,
        os: str = None,
        gpu: bool = None,
        dc: bool = None,
    ):
        location = location.lower()
        environment = environment.lower()
        type = type.lower()
        if type == "datafactory":
            key_func = lambda x: (
                x["location"].lower(),
                x["environment"].lower(),
                x["type"].lower(),
            )
        elif environment == "cloverport":
            key_func = lambda x: (
                x["location"].lower(),
                x["environment"].lower(),
                x["type"].lower(),
                x["os"].lower(),
                x["gpu"],
            )
        else:
            key_func = lambda x: (
                x["location"].lower(),
                x["environment"].lower(),
                x["type"].lower(),
                x["os"].lower(),
                x["gpu"],
                x["DC"],
            )
        uw_computes = self._get_uw_configs(self.config.uw_config.computes, key_func)
        if type == "datafactory":
            return uw_computes[location, environment, type]
        elif environment == "cloverport":
            return uw_computes[location, environment, type, os.lower(), gpu]
        else:
            return uw_computes[location, environment, type, os.lower(), gpu, dc]

    def _apply_windows_runsettings(
        self,
        module_name,
        module_instance,
        mpi=False,
        target=None,
        node_count=None,
        process_count_per_node=None,
        input_mode=None,
        output_mode=None,
        datastore_name=None,
        location=None,
        environment=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a windows module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            mpi (bool): is job mpi ?
            target (str): force target compute over hydra conf
            node_count (int): force node_count over hydra conf
            process_count_per_node (int): force process_count_per_node over hydra conf
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            datastore_name (str): output datastore. This will override the datastore based on silo
            location (str): location of the silo to use in unified workspace setting
            environment (str): environment of the silo to use in unified workspace setting
            custom_runtime_arguments (dict): any additional custom args
        """
        if self.unified_workspace:
            target = target or self._get_uw_computes(
                location,
                environment,
                "amlcompute",
                "windows",
                False,
                self.module_loader.is_local(module_name),
            )
            datastore_name = self._get_uw_datastores(
                location, environment, self.module_loader.is_local(module_name)
            )  # TODO: how does hdi/spark dc work?
        else:
            if self.module_loader.is_local(module_name):
                target = (
                    target
                    if target is not None
                    else self.config.compute.windows_cpu_dc_target
                )
            else:
                target = (
                    target
                    if target is not None
                    else self.config.compute.windows_cpu_prod_target
                )

        log.info(
            f"Using windows compute target {target} to run {module_name} from pipeline class {self.__class__.__name__}"
        )
        if custom_runtime_arguments:
            log.info(f"Adding custom runtime arguments {custom_runtime_arguments}")

        module_instance.runsettings.configure(target=target, **custom_runtime_arguments)
        if mpi:
            node_count = node_count if node_count is not None else 1
            process_count_per_node = (
                process_count_per_node if process_count_per_node is not None else 1
            )
            log.info(
                f"Using mpi with node_count={node_count} process_count_per_node={process_count_per_node}"
            )
            module_instance.runsettings.resource_layout.configure(
                node_count=node_count,
                process_count_per_node=process_count_per_node,
            )

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        else:
            self._set_all_inputs_to(
                module_instance,
                self.config.compute.windows_input_mode,  # TODO: verify if this works in uw
            )

        if output_mode:
            self._set_all_outputs_to(
                module_instance, output_mode, datastore_name=datastore_name
            )
        else:
            self._set_all_outputs_to(
                module_instance,
                self.config.compute.windows_output_mode,
                datastore_name=datastore_name,
            )

    def _apply_hdi_runsettings(
        self,
        module_name,
        module_instance,
        target=None,
        driver_cores=None,
        driver_memory=None,
        executor_memory=None,
        executor_cores=None,
        number_executors=None,
        conf=None,
        input_mode=None,
        output_mode=None,
        datastore_name=None,
        location=None,
        environment=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a HDI module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            target (str): force target compute over hydra conf
            driver_cores (int): force driver_cores over hydra conf
            driver_memory (str): force driver_memory over hydra conf
            executor_memory (int): force executor_memory over hydra conf
            executor_cores (int): force executor_cores over hydra conf
            number_executors (int): force number_executors over hydra conf
            conf (str): force conf over hydra conf
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            datastore_name (str): output datastore. This will override the datastore based on silo
            location (str): location of the silo to use in unified workspace setting
            environment (str): environment of the silo to use in unified workspace setting
            custom_runtime_arguments (dict): any additional custom args
        """
        merged_conf = json.loads(HDI_DEFAULT_CONF)
        if self.unified_workspace:
            target = target or self._get_uw_computes(
                location,
                environment,
                "hdinsight",
                "linux",
                False,
                self.module_loader.is_local(module_name),
            )
            datastore_name = datastore_name or self._get_uw_datastores(
                location, environment, self.module_loader.is_local(module_name)
            )  # TODO: how does hdi/spark dc work?
        else:
            if self.module_loader.is_local(module_name):
                target = (
                    target if target is not None else self.config.compute.hdi_dc_target
                )
                if not self.config.compute.hdi_dc_target:
                    raise Exception(
                        f"Your HDI component {module_name} is using local version. Please specify hdi_dc_target"
                    )
            else:
                target = (
                    target
                    if target is not None
                    else self.config.compute.hdi_prod_target
                )
        log.info(
            f"Using HDI compute target {target} to run {module_name} from pipeline class {self.__class__.__name__}"
        )
        if custom_runtime_arguments:
            log.info(f"Adding custom runtime arguments {custom_runtime_arguments}")

        merged_conf = json.loads(HDI_DEFAULT_CONF)
        new_conf = (
            self.config.compute.hdi_conf if "hdi_conf" in self.config.compute else None
        )
        if conf is not None:
            new_conf = conf
        if new_conf is not None:
            if isinstance(new_conf, str):
                new_conf = json.loads(new_conf)
            elif isinstance(new_conf, DictConfig):
                new_conf = flatten(dict(new_conf), reducer="dot")
            else:
                raise ValueError(
                    "computed.hdi_conf is not a valid json string or a single tested configuration."
                )
            merged_conf.update(new_conf)

        module_instance.runsettings.configure(target=target)

        module_instance.runsettings.hdinsight.configure(
            driver_memory=driver_memory
            if driver_memory is not None
            else self.config.compute.hdi_driver_memory,
            driver_cores=driver_cores
            if driver_cores is not None
            else self.config.compute.hdi_driver_cores,
            executor_memory=executor_memory
            if executor_memory is not None
            else self.config.compute.hdi_executor_memory,
            executor_cores=executor_cores
            if executor_cores is not None
            else self.config.compute.hdi_executor_cores,
            number_executors=number_executors
            if number_executors is not None
            else self.config.compute.hdi_number_executors,
            conf=merged_conf,
            **custom_runtime_arguments,
        )

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        self._set_all_outputs_to(
            module_instance, output_mode, datastore_name=datastore_name
        )

    def _apply_synapse_runsettings(
        self,
        module_name,
        module_instance,
        target=None,
        driver_cores=None,
        driver_memory=None,
        executor_memory=None,
        executor_cores=None,
        number_executors=None,
        conf=None,
        input_mode=None,
        output_mode=None,
        datastore_name=None,
        location=None,
        environment=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a Synapse component. Shrike will not set default runsettings except for spark_identity.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            target (str): force target compute over hydra conf
            driver_cores (int): force driver_cores over hydra conf
            driver_memory (str): force driver_memory over hydra conf
            executor_memory (int): force executor_memory over hydra conf
            executor_cores (int): force executor_cores over hydra conf
            number_executors (int): force number_executors over hydra conf
            conf (str): force conf over hydra conf
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            datastore_name (str): output datastore. This will override the datastore based on silo
            location (str): location of the silo to use in unified workspace setting
            environment (str): environment of the silo to use in unified workspace setting
            custom_runtime_arguments (dict): any additional custom args
        """

        if self.unified_workspace:
            target = target or self._get_uw_computes(
                location,
                environment,
                "synapse",
                "linux",
                False,
                self.module_loader.is_local(module_name),
            )
            datastore_name = datastore_name or self._get_uw_datastores(
                location, environment, self.module_loader.is_local(module_name)
            )  # TODO: how does hdi/spark dc work?
        else:
            if self.module_loader.is_local(module_name):
                target = (
                    target
                    if target is not None
                    else self.config.compute.synapse_dc_target
                )
            else:
                target = (
                    target
                    if target is not None
                    else self.config.compute.synapse_prod_target
                )
        log.info(
            f"Using Synapse compute target {target} to run {module_name} from pipeline class {self.__class__.__name__}"
        )
        if custom_runtime_arguments:
            log.info(f"Adding custom runtime arguments {custom_runtime_arguments}")

        new_conf = (
            self.config.compute.synapse_conf
            if "synapse_conf" in self.config.compute
            else None
        )
        if conf is not None:
            new_conf = conf
        if new_conf is not None:
            if isinstance(new_conf, str):
                new_conf = json.loads(new_conf)
            elif isinstance(new_conf, DictConfig) or isinstance(new_conf, dict):
                new_conf = flatten(dict(new_conf), reducer="dot")
            else:
                raise TypeError(
                    f"compute.synapse_conf of type {type(new_conf)} is not a valid json string or a single tested configuration."
                )
            if self.module_loader.is_local(module_name):
                # https://msdata.visualstudio.com/Vienna/_workitems/edit/1918995
                new_conf = json.dumps(new_conf)

            module_instance.runsettings.spark.configure(
                conf=new_conf,
            )

        module_instance.runsettings.configure(target=target)
        module_instance.runsettings.spark_identity.configure(type="managed")

        if "synapse_driver_memory" in self.config.compute:
            driver_memory = driver_memory or self.config.compute.synapse_driver_memory
        if driver_memory:
            module_instance.runsettings.spark.configure(driver_memory=driver_memory)
        if "synapse_driver_cores" in self.config.compute:
            driver_cores = driver_cores or self.config.compute.synapse_driver_cores
        if driver_cores:
            module_instance.runsettings.spark.configure(driver_cores=driver_cores)
        if "synapse_executor_memory" in self.config.compute:
            executor_memory = (
                executor_memory or self.config.compute.synapse_executor_memory
            )
        if executor_memory:
            module_instance.runsettings.spark.configure(executor_memory=executor_memory)
        if "synapse_number_executors" in self.config.compute:
            number_executors = (
                number_executors or self.config.compute.synapse_number_executors
            )
        if number_executors:
            module_instance.runsettings.spark.configure(
                number_executors=number_executors
            )
        if "synapse_executor_cores" in self.config.compute:
            executor_cores = (
                executor_cores or self.config.compute.synapse_executor_cores
            )
        if executor_cores:
            module_instance.runsettings.spark.configure(executor_cores=executor_cores)
        module_instance.runsettings.spark.configure(
            **custom_runtime_arguments,
        )
        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        self._set_all_outputs_to(
            module_instance, output_mode, datastore_name=datastore_name
        )

    def _apply_parallel_runsettings(
        self,
        module_name,
        module_instance,
        windows=False,
        gpu=False,
        target=None,
        node_count=None,
        process_count_per_node=None,
        mini_batch_size=None,
        run_invocation_timeout=None,
        run_max_try=None,
        error_threshold=None,
        input_mode=None,
        output_mode=None,
        datastore_name=None,
        location=None,
        environment=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a ParallelRunStep linux module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            windows (bool): is the module using Windows compute?
            gpu (bool): is the module using GPU compute?
            target (str): force target compute over hydra conf
            node_count (int): force node_count over hydra conf
            process_count_per_node (int): force process_count_per_node over hydra conf
            mini_batch_size (int): force mini_batch_size over hydra conf
            run_invocation_timeout (int): force run_invocation_timeout over hydra conf
            run_max_try (int): force run_max_try over hydra conf
            error_threshold (int): The number of file failures for the input FileDataset that should be ignored during processing.
                If the error count goes above this value, then the job will be aborted.
                Error threshold is for the entire input and not for individual mini-batches sent to run() method.
                The range is [-1, int.max]. -1 indicates ignoring all failures during processing.
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            datastore_name (str): output datastore. This will override the datastore based on silo
            location (str): location of the silo to use in unified workspace setting
            environment (str): environment of the silo to use in unified workspace setting
            custom_runtime_arguments (dict): any additional custom args
        """
        if self.unified_workspace:
            if windows and gpu:
                raise ValueError(
                    "A GPU compute target with Windows OS is not available yet!"
                )
            target = target or self._get_uw_computes(
                location,
                environment,
                "amlcompute",
                "windows" if windows else "linux",
                gpu,
                self.module_loader.is_local(module_name),
            )
            datastore_name = datastore_name or self._get_uw_datastores(
                location, environment, self.module_loader.is_local(module_name)
            )  # TODO: how does hdi/spark dc work?
        else:
            if self.module_loader.is_local(module_name):
                if windows:
                    if gpu:
                        raise ValueError(
                            "A GPU compute target with Windows OS is not available yet!"
                        )
                    else:
                        _target = self.config.compute.windows_cpu_dc_target
                else:
                    if gpu:
                        _target = self.config.compute.linux_gpu_dc_target
                    else:
                        _target = self.config.compute.linux_cpu_dc_target
            else:
                if windows:
                    if gpu:
                        raise ValueError(
                            "A GPU compute target with Windows OS is not available yet!"
                        )
                    else:
                        _target = self.config.compute.windows_cpu_prod_target
                else:
                    if gpu:
                        _target = self.config.compute.linux_gpu_prod_target
                    else:
                        _target = self.config.compute.linux_cpu_prod_target

            target = target if target is not None else _target

        log.info(
            f"Using parallelrunstep compute target {target} to run {module_name} from pipeline class {self.__class__.__name__}"
        )
        if custom_runtime_arguments:
            log.info(f"Adding custom runtime arguments {custom_runtime_arguments}")

        module_instance.runsettings.configure(target=target)

        module_instance.runsettings.parallel.configure(
            node_count=node_count
            if node_count is not None
            else self.config.compute.parallel_node_count,
            process_count_per_node=process_count_per_node
            if process_count_per_node is not None
            else (
                self.config.compute.parallel_process_count_per_node
                if "parallel_process_count_per_node" in self.config.compute
                else None
            ),
            mini_batch_size=str(
                mini_batch_size
                if mini_batch_size is not None
                else self.config.compute.parallel_mini_batch_size
            ),
            run_invocation_timeout=run_invocation_timeout
            if run_invocation_timeout is not None
            else self.config.compute.parallel_run_invocation_timeout,
            run_max_try=run_max_try
            if run_max_try is not None
            else self.config.compute.parallel_run_max_try,
            error_threshold=error_threshold
            if error_threshold is not None
            else self.config.compute.parallel_error_threshold,
            **custom_runtime_arguments,
        )

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        self._set_all_outputs_to(
            module_instance, output_mode, datastore_name=datastore_name
        )

    def _apply_linux_runsettings(
        self,
        module_name,
        module_instance,
        mpi=False,
        gpu=False,
        target=None,
        node_count=None,
        process_count_per_node=None,
        input_mode=None,
        output_mode=None,
        datastore_name=None,
        location=None,
        environment=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for linux module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            mpi (bool): is the job mpi?
            gpu (bool): is the job using GPU?
            target (str): force target compute over hydra conf
            node_count (int): force node_count over hydra conf
            process_count_per_node (int): force process_count_per_node over hydra conf
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            datastore_name (str): output datastore. This will override the datastore based on silo
            location (str): location of the silo to use in unified workspace setting
            environment (str): environment of the silo to use in unified workspace setting
            custom_runtime_arguments (dict): any additional custom args
        """
        if self.unified_workspace:
            target = target or self._get_uw_computes(
                location,
                environment,
                "amlcompute",
                "linux",
                gpu,
                self.module_loader.is_local(module_name),
            )
            datastore_name = datastore_name or self._get_uw_datastores(
                location, environment, self.module_loader.is_local(module_name)
            )  # TODO: how does hdi/spark dc work?
        else:
            if self.module_loader.is_local(module_name) and gpu:
                target = (
                    target
                    if target is not None
                    else self.config.compute.linux_gpu_dc_target
                )
            elif not self.module_loader.is_local(module_name) and gpu:
                target = (
                    target
                    if target is not None
                    else self.config.compute.linux_gpu_prod_target
                )
            elif self.module_loader.is_local(module_name) and not gpu:
                target = (
                    target
                    if target is not None
                    else self.config.compute.linux_cpu_dc_target
                )
            elif not self.module_loader.is_local(module_name) and not gpu:
                target = (
                    target
                    if target is not None
                    else self.config.compute.linux_cpu_prod_target
                )
        processor = "GPU" if gpu else "CPU"
        source = "local" if self.module_loader.is_local(module_name) else "registered"
        log.info(
            f"Using target {target} for {source} {processor} module {module_name} from pipeline class {self.__class__.__name__}"
        )

        if custom_runtime_arguments:
            log.info(f"Adding custom runtime arguments {custom_runtime_arguments}")

        module_instance.runsettings.configure(target=target, **custom_runtime_arguments)

        if mpi:
            node_count = node_count if node_count is not None else 1
            process_count_per_node = (
                process_count_per_node if process_count_per_node is not None else 1
            )
            log.info(
                f"Using mpi with node_count={node_count} process_count_per_node={process_count_per_node}"
            )
            module_instance.runsettings.resource_layout.configure(
                node_count=node_count,
                process_count_per_node=process_count_per_node,
            )

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        else:
            self._set_all_inputs_to(
                module_instance, self.config.compute.linux_input_mode
            )
        if output_mode:
            self._set_all_outputs_to(
                module_instance, output_mode, datastore_name=datastore_name
            )
        else:
            self._set_all_outputs_to(
                module_instance,
                self.config.compute.linux_output_mode,
                datastore_name=datastore_name,
            )

    def _apply_scope_runsettings(
        self,
        module_name,
        module_instance,
        input_mode=None,
        output_mode=None,
        scope_param=None,
        custom_job_name_suffix=None,
        adla_account_name=None,
        priority=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a scope module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            scope_param (str): Parameters to pass to scope e.g. Nebula parameters, VC allocation parameters etc.
            custom_job_name_suffix (str): Optional parameter defining custom string to append to job name
            adla_account_name (str): The name of the Cosmos-migrated Azure Data Lake Analytics account to submit scope job
            priority (int): Scope job priority. Default is 1000.
            custom_runtime_arguments (dict): any additional custom args
        """
        log.info(
            f"Using scope compute target to run {module_name} from pipeline class {self.__class__.__name__}"
        )
        if custom_runtime_arguments:
            log.info(f"Adding custom runtime arguments {custom_runtime_arguments}")

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        self._set_all_outputs_to(module_instance, output_mode, compliant=False)

        module_instance.runsettings.scope.configure(
            adla_account_name=adla_account_name,
            scope_param=scope_param,
            custom_job_name_suffix=custom_job_name_suffix,
            priority=priority,
        )

    def _apply_datatransfer_runsettings(
        self,
        module_name,
        module_instance,
        compliant=True,
        target=None,
        input_mode=None,
        output_mode=None,
        datastore_name=None,
        location=None,
        environment=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a HDI module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            compliant (bool): destination datastore, `compliant_datastore` if True, else `noncompliant_datastore`
            target (str): force target compute over hydra conf
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            datastore_name (str): output datastore. This will override the datastore based on silo
            location (str): location of the silo to use in unified workspace setting
            environment (str): environment of the silo to use in unified workspace setting
            custom_runtime_arguments (dict): any additional custom args
        """
        if custom_runtime_arguments:
            log.info(f"Adding custom runtime arguments {custom_runtime_arguments}")

        if self.unified_workspace:
            target = target or self._get_uw_computes(
                location, environment, "datafactory"
            )
            if compliant:
                datastore_name = datastore_name or self._get_uw_datastores(
                    location, environment, False
                )
            else:
                datastore_name = (
                    datastore_name or self.config.compute.noncompliant_datastore
                )
            self._set_all_outputs_to(
                module_instance, output_mode, datastore_name=datastore_name
            )
        else:
            target = target or self.config.compute.datatransfer_target
            self._set_all_outputs_to(
                module_instance, output_mode, compliant, datastore_name
            )
        log.info(
            f"Using datatransfer compute target {target} to run {module_name} from pipeline class {self.__class__.__name__}"
        )
        module_instance.runsettings.configure(target=target)

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)

    def _apply_sweep_runsettings(
        self,
        module_name,
        module_instance,
        windows=False,
        gpu=False,
        target=None,
        input_mode=None,
        output_mode=None,
        node_count=None,
        process_count_per_node=None,
        algorithm=None,
        primary_metric=None,
        goal=None,
        policy_type=None,
        evaluation_interval=None,
        delay_evaluation=None,
        slack_factor=None,
        slack_amount=None,
        truncation_percentage=None,
        max_total_trials=None,
        max_concurrent_trials=None,
        timeout_minutes=None,
        datastore_name=None,
        location=None,
        environment=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a sweep component.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            target (str): force target compute over hydra conf
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf

            # For below sweep specific parameters configurations, see below doc link for more info:
            # https://componentsdk.azurewebsites.net/components/sweep_component.html#set-runsettings
            algorithm (str): sweep sampling method
            primary_metric (str): the primary metric of the hyperparameter tuning to optimize
            goal (str): whether the primary metric will be maximize or minimize when evaluating the trials
            policy_type (str): sweep early termination policy type
            evaluation_interval (int): frequency of applying the policy
            delay_evaluation (int): delays the first policy evaluation for a specified number of intervals
            slack_factor (float): the slack allowed with respect to the best performing training run, as a ratio
            slack_amount (float): the slack allowed with respect to the best performing training run, as an absolute ampunt. You should only specify either slack_factor or slack_amount, but not both.
            truncation_percentage (int): the percentage of lowest performing runs to terminate at each evaluation interval. An integer value between 1 and 99.
            max_total_trials (int): maximum number of trial runs. Must be an integer between 1 and 1000.
            max_concurrent_trials (int): maximum number of runs that can run concurrently. If not specified, all runs launch in parallel. If specified, must be an integer between 1 and 100.
            timeout_minutes (int): maximum duration, in minutes, of the hyperparameter tuning experiment. Runs after this duration are canceled.

            datastore_name (str): output datastore
            location (str): location of the silo to use in unified workspace setting
            environment (str): environment of the silo to use in unified workspace setting

            custom_runtime_arguments (dict): any additional custom args
        """
        if self.unified_workspace:
            target = target or self._get_uw_computes(
                location,
                environment,
                "amlcompute",
                "windows" if windows else "linux",
                gpu,
                self.module_loader.is_local(module_name),
            )
            datastore_name = datastore_name or self._get_uw_datastores(
                location, environment, self.module_loader.is_local(module_name)
            )  # TODO: how does hdi/spark dc work?
        else:
            if target is not None:
                target = target
            elif self.module_loader.is_local(module_name):
                if windows:
                    if gpu:
                        raise ValueError(
                            "A GPU compute target with Windows OS is not available yet!"
                        )
                    else:
                        target = self.config.compute.windows_cpu_dc_target
                else:
                    if gpu:
                        target = self.config.compute.linux_gpu_dc_target
                    else:
                        target = self.config.compute.linux_cpu_dc_target
            else:
                if windows:
                    if gpu:
                        raise ValueError(
                            "A GPU compute target with Windows OS is not available yet!"
                        )
                    else:
                        target = self.config.compute.windows_cpu_prod_target
                else:
                    if gpu:
                        target = self.config.compute.linux_gpu_prod_target
                    else:
                        target = self.config.compute.linux_cpu_prod_target
        log.info(
            f"Using target {target} to run sweep component {module_name} from pipeline class {self.__class__.__name__}"
        )
        if custom_runtime_arguments:
            log.info(f"Adding custom runtime arguments {custom_runtime_arguments}")

        module_instance.runsettings.configure(target=target, **custom_runtime_arguments)

        if node_count:
            log.info(
                f"Setting node_count={node_count} and process_count_per_node={process_count_per_node} as run settings for sweep component {module_name} from pipeline class {self.__class__.__name__}"
            )
            module_instance.runsettings.resource_layout.configure(
                node_count=node_count, process_count_per_node=process_count_per_node
            )

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        self._set_all_outputs_to(
            module_instance, output_mode, datastore_name=datastore_name
        )

        if algorithm:
            module_instance.runsettings.sweep.algorithm = algorithm
        if primary_metric:
            module_instance.runsettings.sweep.objective.configure(
                primary_metric=primary_metric
            )
        if goal:
            module_instance.runsettings.sweep.objective.configure(goal=goal)
        if policy_type:
            module_instance.runsettings.sweep.early_termination.configure(
                policy_type=policy_type
            )
        if evaluation_interval:
            module_instance.runsettings.sweep.early_termination.configure(
                evaluation_interval=evaluation_interval
            )
        if delay_evaluation:
            module_instance.runsettings.sweep.early_termination.configure(
                delay_evaluation=delay_evaluation
            )
        if slack_factor:
            module_instance.runsettings.sweep.early_termination.configure(
                slack_factor=slack_factor
            )
        if slack_amount:
            module_instance.runsettings.sweep.early_termination.configure(
                slack_amount=slack_amount
            )
        if truncation_percentage:
            module_instance.runsettings.sweep.early_termination.configure(
                truncation_percentage=truncation_percentage
            )
        if max_total_trials:
            module_instance.runsettings.sweep.limits.configure(
                max_total_trials=max_total_trials
            )
        if max_concurrent_trials:
            module_instance.runsettings.sweep.limits.configure(
                max_concurrent_trials=max_concurrent_trials
            )
        if timeout_minutes:
            module_instance.runsettings.sweep.limits.configure(
                timeout_minutes=timeout_minutes
            )

    def _get_component_name_helper(self, component_instance):
        return component_instance.name

    def _update_dc_configs(self, pipeline: Pipeline, debug: bool = False) -> Pipeline:
        # collect the known DC targets
        dc_datastore = None
        if not self.unified_workspace:
            # workaround for missing "throw_on_missing" in currently used omegaconf
            compute_config_as_dict = yaml.safe_load(
                OmegaConf.to_yaml(self.config.compute)
            )
            dc_targets: Set[str] = {
                target
                for key, target in compute_config_as_dict.items()
                if key.endswith("_dc_target") and target and target != str(MISSING)
            }
            dc_datastore = self.config.compute.dc_datastore
        else:
            log.warn(
                """
                Updating for DC is not fully supported for multi-region pipelines 
                in the unified workspace mode and is subject to error. 
                Strongly recommend to skip this by setting `run.skip_update_dc`. 
                If you need to test on DC, please try `module_loader.use_local='!<data_transfer>'`
                """
            )
            dc_targets: Set[str] = {
                target["name"]
                for target in self.config.uw_config.computes
                if target["DC"]
            }
        if not dc_targets:
            # This is kind of pointless because if one local component exists
            # then one of the `apply_*` methods wil fail if no dc target is not
            # specified. And if no local component exists, then there is no
            # point in outputting this. But let's do it anyway:
            log.info("The compute config does not contain any DC targets.")
            return pipeline

        log.info("Overriding compute target if upstream steps use DC...")

        # build and parse the dependency graph
        dependency_graph = _DependencyGraph.from_pipeline(
            pipeline=pipeline, debug=debug
        )

        should_use_dc = dependency_graph.determine_dc_nodes(dc_targets=dc_targets)

        log.info(f"Need to configure the following for DC: {sorted(should_use_dc)}")

        # prepare a mapping from known prod targets to (their corresponding
        # key in the shrike config and) the corresponding DC target
        target_map: Dict[str, Tuple[str, Optional[str]]] = {}
        if self.unified_workspace:
            for prod_target_info in self.config.uw_config.computes:
                if (
                    prod_target_info.DC
                    or prod_target_info.type.lower() == "datafactory"
                ):
                    continue
                prod_target = prod_target_info.name
                dc_target = self._get_uw_computes(
                    prod_target_info.location,
                    prod_target_info.environment,
                    prod_target_info.type,
                    prod_target_info.os,
                    prod_target_info.gpu,
                    True,
                )
                target_map[prod_target] = [prod_target, dc_target]
        else:
            for prod_target in [
                "hdi_prod_target",
                "linux_cpu_prod_target",
                "linux_gpu_prod_target",
                "windows_cpu_prod_target",
                "synapse_prod_target",
            ]:
                if prod_target not in self.config.compute:
                    continue
                target_map[self.config.compute[prod_target]] = [
                    prod_target,
                    self.config.compute.get(
                        prod_target.replace("_prod_", "_dc_"), None
                    ),
                ]

        # move to DC!
        for node_id in should_use_dc:
            node = dependency_graph.nodes[node_id]

            if isinstance(node, Output):

                if node._owner.type == "ScopeComponent":
                    # output datastore has to be cosmos (ADLSg1), while dc_datastore is ADLSg2
                    continue
                if self.unified_workspace:
                    dc_datastore = None
                    prod_datastore = node._datastore
                    for datastore in self.config.uw_config.datastores:
                        if datastore.name == prod_datastore:
                            dc_datastore = self._get_uw_datastores(
                                datastore.location,
                                datastore.environment,
                                True,
                            )
                            break
                if dc_datastore:
                    node.configure(
                        datastore=dc_datastore,
                        output_mode=None,
                    )
                    log.info(f"Configured {node_id} to use datastore {dc_datastore}.")

            elif not hasattr(node.runsettings, "target"):
                # e.g. scope component doesn't need to configure compute target
                log.info(f"Node {node.name} does not have `target`.")
                continue
            elif not isinstance(node.runsettings.target, str):
                log.warn(
                    f"The compute target of node {node.name} is a PipelineParameter. Shrike will not update even if this or the upstream steps use DC. Please update manually."
                )
                continue
            elif node.runsettings.target in dc_targets:
                # nothing to do here
                pass

            elif node.runsettings.target not in target_map:
                log.error(
                    f"Node {node} is using an unknown target: "
                    f"{node.runsettings.target}. "
                    f"Please move this to DC manually, or re-run "
                    f"this after adding the target to the compute config."
                )

            else:
                prod_target_key, dc_target = target_map[node.runsettings.target]
                if dc_target is None:
                    log.error(
                        f"No corresponding DC target is defined for "
                        f"prod target {prod_target_key}. "
                        f"Please move this to DC manually, or re-run "
                        f"this after adding the DC target to the compute config."
                    )
                    continue

                node.runsettings.configure(target=dc_target)
                log.info(
                    f"Updating compute target for {node_id} to {node.runsettings.target}"
                )
        return pipeline

    ################
    ### MAIN/RUN ###
    ################

    def connect(self):
        """Connect to the AML workspace using internal config"""
        # Only call azureml_connect if there is not an already a pre-existing workspace
        try:
            return self.workspace()
        except:
            return azureml_connect(
                aml_subscription_id=self.config.aml.subscription_id,
                aml_resource_group=self.config.aml.resource_group,
                aml_workspace_name=self.config.aml.workspace_name,
                aml_auth=self.config.aml.auth,
                aml_tenant=self.config.aml.tenant,
                aml_force=self.config.aml.force,
            )  # NOTE: this also stores aml workspace in internal global variable

    def _build_pipeline(self) -> Pipeline:
        log.info(f"Building Pipeline [{self.__class__.__name__}]...")
        pipeline_function = self.build(self.config)

        log.info("Creating Pipeline Instance...")
        pipeline = self.pipeline_instance(pipeline_function, self.config)

        if not self.config.run.skip_update_dc and self.is_eyesoff():
            log.info("Overriding compute target if upstream steps use DC...")
            pipeline = self._update_dc_configs(pipeline)

        if not self.config.run.skip_validation:
            log.info("Validating...")
            pipeline.validate(workspace=self.workspace())

        if self.config.run.export:
            log.info(f"Exporting to {self.config.run.export}...")
            with open(self.config.run.export, "w") as export_file:
                export_file.write(pipeline._get_graph_json(workspace=self.workspace()))
        return pipeline

    def _submit_pipeline(self, pipeline: Pipeline) -> Optional[PipelineRun]:
        """Publish and submit the given pipeline.

        Args:
            pipeline: pipeline to be submitted
        """
        if self.config.run.publish:
            self._publish_to_endpoint(pipeline)

        if self.config.run.submit:
            pipeline_tags = self._parse_pipeline_tags()
            pipeline_tags.update({"shrike": __version__})
            pipeline_tags.update(self.repository_info)
            pipeline_tags.update(self._validate_tags(self.extra_tags()))
            log.info(f"Submitting Experiment... [tags={pipeline_tags}]")

            # pipeline_run is of the class "azure.ml.component.run", which
            # is different from "azureml.pipeline.core.PipelineRun"
            pipeline_run = pipeline.submit(
                workspace=self.workspace(),
                experiment_name=self.config.run.experiment_name,
                description=self.config.run.experiment_description,
                display_name=self.config.run.display_name,
                tags=pipeline_tags,
                default_compute_target=None
                if self.unified_workspace
                else self.config.compute.default_compute_target,
                regenerate_outputs=self.config.run.regenerate_outputs,
                continue_on_step_failure=self.config.run.continue_on_failure,
                skip_validation=self.config.run.skip_validation,
            )

            # Forece pipeline_run to be of the class "azureml.pipeline.core.PipelineRun"
            pipeline_run = PipelineRun(
                experiment=pipeline_run._experiment,
                run_id=pipeline_run._id,
            )
            return pipeline_run

        else:
            log.info(
                "Exiting now, if you want to submit please override run.submit=True"
            )
            self.__class__.BUILT_PIPELINE = (
                pipeline  # return so we can have some unit tests done
            )
            return

    @classmethod
    def main(cls):
        """Pipeline helper main function, parses arguments and run pipeline."""
        config_dict = cls._default_config()

        @hydra.main(config_name="default")
        def hydra_run(cfg: DictConfig):
            # merge cli config with default config
            cfg = OmegaConf.merge(config_dict, cfg)

            arg_parser = argparse.ArgumentParser()
            arg_parser.add_argument("--config-dir")
            args, _ = arg_parser.parse_known_args()
            cfg.run.config_dir = os.path.join(
                HydraConfig.get().runtime.cwd, args.config_dir
            )

            log.info("*** CONFIGURATION ***")
            log.info(OmegaConf.to_yaml(cfg))

            # create class instance
            main_instance = cls(cfg)

            # run
            main_instance.run()

        hydra_run()

        return cls.BUILT_PIPELINE  # return so we can have some unit tests done


class _DependencyGraph:
    NodeType = Union[Component, Output]

    graph: Dict[str, List[str]] = {}
    nodes: Dict[str, NodeType] = {}
    debug: bool = False

    def map_to_id(self, item: Union[Pipeline, Component, Output]) -> Optional[str]:
        """Maps the given item to an id."""
        # Reminder: class-wise, pipelines are also components
        extra = f"{item.comment}, " if self.debug and hasattr(item, "comment") else ""
        if isinstance(item, Pipeline):
            return f"pipeline `{item.display_name.replace(' ', '-')}` ({extra}{item._instance_id})"
        if isinstance(item, Component):
            return f"component `{item.display_name.replace(' ', '-')}` ({extra}{item._instance_id})"
        if isinstance(item, Output):
            return f"output `{item.port_name}` of {self.map_to_id(item._owner)}"
        raise ValueError(
            f"Please report this. Could not map {item} to dependency graph id."
        )

    def add_edge(
        self,
        from_node: NodeType,
        to_node: NodeType,
    ) -> None:
        """Add an edge from a dependent node its dependency."""
        for node in [from_node, to_node]:
            if not isinstance(node, (Component, Output)):
                raise ValueError(
                    f"Please report this. "
                    f"Expected a valid node type but was given {node} as node."
                )
            node_id = self.map_to_id(node)
            known_node = self.nodes.get(node_id)
            if known_node is not None and node is not known_node:
                raise ValueError("Report this. Two different nodes with same id.")
            self.nodes[node_id] = node

        ids = [self.map_to_id(node) for node in [from_node, to_node]]
        if ids[0] == ids[1]:
            return
        to_nodes = self.graph.setdefault(ids[0], [])
        if ids[1] not in to_nodes:  # yeah it's a list but short
            to_nodes.append(ids[1])
        self.assert_acyclic()
        log.debug(f"Add edge {ids})")

    def topsorted_ids(self) -> List[str]:
        return toposort_flatten(self.graph)

    def assert_acyclic(self) -> None:
        try:
            self.topsorted_ids()
        except CircularDependencyError as e:
            raise ValueError(
                "Error while constructing dependency graph for DC management."
            ) from e

    @classmethod
    def from_pipeline(cls, pipeline: Pipeline, debug: bool) -> _DependencyGraph:
        graph = _DependencyGraph()
        graph.debug = debug

        def resolve(node: Any) -> Optional[_DependencyGraph.NodeType]:
            if isinstance(node, Output) or isinstance(node, Component):
                return node
            if isinstance(node, Input):
                input_dset = node._dset
                if input_dset is None:
                    return None
                return resolve(input_dset)
            if isinstance(node, PipelineParameter):
                default_value = node.default_value
                if default_value is None or default_value is node:
                    # can't resolve this
                    return None
                return resolve(default_value)
            return None

        for subpipeline in pipeline._expand_pipeline_to_pipelines():
            # For DC, we only need to adapt `Output` and `Component`
            # components. The `Output`s of pipelines do not coincide
            # with the `Output`s of components, hence we have to
            # insert those into our dependency graph:
            for output_name, output in subpipeline.outputs.items():
                linked_output = subpipeline._outputs_mapping[output_name]
                graph.add_edge(output, linked_output)
            # However, it seems we can skip the pipeline inputs.

        for component in pipeline._expand_pipeline_nodes():
            for output in component.outputs.values():
                graph.add_edge(output, component)
            for input_ in component.inputs.values():
                corresponding_node = resolve(input_)
                if corresponding_node is not None:
                    graph.add_edge(component, corresponding_node)
        return graph

    def determine_dc_nodes(self, dc_targets: List[str]) -> Set[str]:
        """Determine which downstream components/outputs should be configured for DC.

        Args:
            dc_targets: known DC targets (used to determine which nodes
               are already configured for DC)
        Returns:
            list of node ids for all nodes that should be configured for
            dc (or have already been configured for dc)
        """
        should_use_dc: Set[str] = set()
        for node_id in self.topsorted_ids():

            # use dc, if upstream used dc
            for dependency in self.graph.get(node_id, []):
                if dependency in should_use_dc:
                    should_use_dc.add(node_id)
                    continue

            item = self.nodes[node_id]

            if not isinstance(item, Component):
                # If users choose to move an output to iso datastore out of
                # nowhere, we ignore this. We're only caring about cases where
                # the (`apply_*` method caused the) run settings of components
                # to be configured for DC - and fix downstream components.
                continue

            if not hasattr(item.runsettings, "target") or not isinstance(
                item.runsettings.target, str
            ):
                # e.g. Scope components do not configure compute targets
                # e.g. if `target` is a PipelineParameter, it returns None
                # and no need to update
                continue

            if item.runsettings.target in dc_targets:
                should_use_dc.add(node_id)

        return should_use_dc
