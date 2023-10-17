# Developing Mongo Persist Handler
import pyarrow as pa

from ds_core.handlers.abstract_handlers import AbstractSourceHandler, AbstractPersistHandler
from ds_core.handlers.abstract_handlers import HandlerFactory, ConnectorContract
from ds_capability.components.commons import Commons


class DuckdbSourceHandler(AbstractSourceHandler):
    """ A mongoDB source handler"""

    def __init__(self, connector_contract: ConnectorContract):
        """ initialise the Handler passing the source_contract dictionary """
        # required module import
        self.duckdb = HandlerFactory.get_module('duckdb')
        super().__init__(connector_contract)

        self._file_state = 0
        self._changed_flag = True

    def supported_types(self) -> list:
        """ The source types supported with this module"""
        return ['duckdb']

    def load_canonical(self, **kwargs) -> pa.Table:
        """ returns the canonical dataset based on the source contract
            The canonical in this instance is a dictionary that has the headers as the key and then
            the ordered list of values for that header
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            raise ValueError("The PandasSource Connector Contract has not been set")


    def exists(self) -> bool:
        """ returns False """
        return False

    def has_changed(self) -> bool:
        """ returns False """
        return False

    def reset_changed(self, changed: bool = False):
        """ manual reset to say the file has been seen. This is automatically called if the file is loaded"""
        changed = changed if isinstance(changed, bool) else False
        self._changed_flag = changed


class DuckdbPersistHandler(DuckdbSourceHandler, AbstractPersistHandler):
    # a mongoDB persist handler

    def persist_canonical(self, canonical: pa.Table, **kwargs) -> bool:
        """ persists the canonical dataset
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            return False
        _uri = self.connector_contract.uri
        return self.backup_canonical(canonical=canonical, uri='', **kwargs)

    def backup_canonical(self, canonical: pa.Table, uri: str, **kwargs) -> bool:
        """  creates a backup of the canonical to an alternative table """
        return None

    def remove_canonical(self) -> bool:
        if not isinstance(self.connector_contract, ConnectorContract):
            return False
        return False
