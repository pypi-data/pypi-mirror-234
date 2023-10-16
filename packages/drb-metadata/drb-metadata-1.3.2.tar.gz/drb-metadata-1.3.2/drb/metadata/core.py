from __future__ import annotations
from types import ModuleType
from typing import Any, Dict, List, Tuple
from uuid import UUID

from drb.addons.addon import Addon
from drb.core.node import DrbNode
from drb.exceptions.core import DrbException
from drb.topics.dao import ManagerDao
from drb.topics.topic import DrbTopic
from drb.utils.plugins import get_entry_points
from drb.extractor import parse_extractor, Extractor
import os
import jsonschema
import yaml
import importlib
import logging
import drb.topics.resolver as resolver


_logger = logging.getLogger('DrbMetadata')
_schema = os.path.join(os.path.dirname(__file__), 'schema.yml')


def validate_md_cortex_file(path: str) -> None:
    """
    Checks the given metadata cortex file is valid.

    Parameters:
        path (str): metadata cortex file path

    Raises:
        DrbException: If the given cortex file is not valid
    """
    with open(_schema) as f:
        schema = yaml.safe_load(f)

    with open(path) as file:
        for data in yaml.safe_load_all(file):
            try:
                jsonschema.validate(data, schema)
            except jsonschema.ValidationError as ex:
                raise DrbException(
                    f'Invalid metadata cortex file: {path}') from ex


def _retrieve_cortex_file(module: ModuleType) -> str:
    """
    Retrieves the metadata cortex file from the given module.

    Parameters:
        module (ModuleType): target module where the cortex metadata file will
                             be search
    Returns:
        str - path to the cortex metadata file
    Raises:
        FileNotFound: If the metadata cortex file is not found
    """
    directory = os.path.dirname(module.__file__)
    path = os.path.join(directory, 'cortex.yml')
    if not os.path.exists(path):
        path = os.path.join(directory, 'cortex.yaml')

    if not os.path.exists(path):
        raise FileNotFoundError(f'File not found: {path}')

    return path


def _load_metadata(yaml_data: dict) -> Tuple[UUID, List[DrbMetadata]]:
    uuid = UUID(yaml_data['drbItemClass'])

    variables = {}
    yaml_vars = yaml_data.get('variables', None)
    if yaml_vars is not None:
        for var in yaml_vars:
            extractor = parse_extractor(var)
            variables[var['name']] = extractor

    metadata = []
    for md in yaml_data['metadata']:
        extractor = parse_extractor(md)
        metadata.append(DrbMetadata(md['name'], extractor, variables))
    return uuid, metadata


def _load_all_metadata() -> Dict[UUID, List[DrbMetadata]]:
    """
    Loads all metadata defined in the current Python environment
    """
    entry_point_group = 'drb.addon.metadata'
    metadata = {}

    for ep in get_entry_points(entry_point_group):
        try:
            module = importlib.import_module(ep.value)
        except ModuleNotFoundError as ex:
            _logger.warning(f'Invalid DRB Metadata entry-point {ep}: {ex.msg}')
            continue

        try:
            cortex = _retrieve_cortex_file(module)
            validate_md_cortex_file(cortex)
        except (FileNotFoundError, DrbException) as ex:
            _logger.warning(ex)
            continue

        with open(cortex) as file:
            for data in yaml.safe_load_all(file):
                uuid, mds = _load_metadata(data)
                metadata[uuid] = mds

    return metadata


def _get_parents_UUIDs(topic: DrbTopic):
    uuids = [topic.id]
    if topic.subClassOf is None:
        return uuids
    for parent in topic.subClassOf:
        uuids += _get_parents_UUIDs(ManagerDao().get_drb_topic(parent))
    return uuids


class DrbMetadata:
    def __init__(self, name: str, extractor: Extractor,
                 variables: dict = None):
        self._name = name
        self._extractor = extractor
        self._variables = variables if variables is not None else {}
        self._node = None

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, node):
        self._node = node

    @property
    def name(self) -> str:
        return self._name

    def extract(self, **kwargs) -> Any:
        variables = {}

        node = kwargs.get('node', self.node)

        if node is None:
            raise DrbException(
                'No source given to extract metadata'
            )

        for name, extractor in self._variables.items():
            variables[name] = extractor.extract(
                node,
                **variables)
        return self._extractor.extract(
            node,
            **variables)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DrbMetadata) and self._name == other._name


class MetadataAddon(Addon):
    __instance = None
    __metadata = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(MetadataAddon, cls).__new__(
                cls, *args, **kwargs)
        cls.__metadata = _load_all_metadata()
        return cls.__instance

    def _retrieve_metadata(self, ic: DrbTopic) -> Dict[str, DrbMetadata]:
        metadata = None

        # load metadata from super class
        if ic.subClassOf is not None:
            metadata = {}
            for parent_id in ic.subClassOf:
                parent = ManagerDao().get_drb_topic(parent_id)
                metadata.update(self._retrieve_metadata(
                    ManagerDao().get_drb_topic(parent.id)))

        if metadata is None:
            metadata = {}

        # add specific metadata of the given class (override if necessary)
        if ic.id in self.__metadata.keys():
            for md in self.__metadata[ic.id]:
                metadata[md.name] = md

        return metadata

    @classmethod
    def identifier(cls) -> str:
        return 'metadata'

    @classmethod
    def return_type(cls) -> type:
        return dict

    def apply(self, node: DrbNode, **kwargs) -> Any:
        topic = kwargs.get('topic') or resolver.resolve(node)[0]
        md = self._retrieve_metadata(topic)

        for key in md.keys():
            md[key].node = node

        return md

    def can_apply(self, source: DrbTopic) -> bool:
        uuids = _get_parents_UUIDs(source)
        for uuid in uuids:
            if uuid in self.__metadata.keys():
                return True
        return False
