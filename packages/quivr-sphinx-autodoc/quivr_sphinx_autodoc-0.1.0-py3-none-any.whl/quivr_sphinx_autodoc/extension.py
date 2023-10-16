from typing import Any, Iterator, Optional

import quivr as qv
import quivr.attributes
from sphinx.ext.autodoc import AttributeDocumenter, ClassDocumenter, ObjectMember
from sphinx.pycode import ModuleAnalyzer

from quivr_sphinx_autodoc.__version__ import version


def table_columns(table_class: type[qv.Table]) -> Iterator[qv.Column]:
    for col in table_class.schema:
        yield (getattr(table_class, col.name))


class QuivrTableDocumenter(ClassDocumenter):
    objtype = "qvtable"
    directivetype = ClassDocumenter.objtype
    priority = 10 + ClassDocumenter.priority

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        try:
            if issubclass(member, qv.Table):
                return True
        except TypeError:
            pass
        return False

    def get_object_members(self, want_all: bool) -> tuple[bool, list[ObjectMember]]:
        check_module, members = super().get_object_members(want_all)

        # Add schema to members
        pa_schema = self.object.schema
        schema_member = ObjectMember("schema", pa_schema, docstring="Pyarrow table schema", skipped=False)
        members = [schema_member, *members]

        return check_module, members

    def filter_members(
        self,
        members: list[ObjectMember],
        want_all: bool,
    ) -> list[tuple[str, Any, bool]]:
        # Filter out columns and attributes
        filtered_members = super().filter_members(members, want_all)
        column_names = {col.name for col in table_columns(self.object)}
        attr_names = set(self.object._quivr_attributes.keys())

        filtered_members = [
            member for member in filtered_members if member[0] not in column_names and member[0] not in attr_names
        ]
        return filtered_members


class QuivrSchemaDocumenter(AttributeDocumenter):
    objtype = "qvschema"
    directivetype = AttributeDocumenter.objtype
    priority = 10 + AttributeDocumenter.priority

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        try:
            if isinstance(parent, QuivrTableDocumenter):
                if membername == "schema":
                    return True
        except TypeError:
            pass
        return False

    def add_content(self, more_content: Optional[list[str]]) -> None:
        super().add_content(more_content)
        self.add_schema_table()

    def should_suppress_value_header(self) -> bool:
        return True

    def add_schema_table(self):
        # Add table directive
        self.add_line(".. list-table:: Schema", self.get_sourcename())
        self.add_line("  :widths: 30 30 40", self.get_sourcename())
        self.add_line("  :header-rows: 1", self.get_sourcename())
        self.add_line("", self.get_sourcename())

        # Add table header
        self.add_line("  * - Column", self.get_sourcename())
        self.add_line("    - Type", self.get_sourcename())
        self.add_line("    - Doc", self.get_sourcename())

        # Add row for each column in the table
        for column in table_columns(self.parent):
            self.add_schema_table_row(column)

        # If the table has scalar attributes, add them
        if len(self.parent._quivr_attributes) > 0:
            self.add_line("", self.get_sourcename())
            self.add_attributes_list()

    def add_schema_table_row(self, column: qv.Column):
        self.add_line(f"  * - {column.name}", self.get_sourcename())
        self.add_line(f"    - {self._type_string(column)}", self.get_sourcename())
        coldoc = self.get_column_doc(column)
        if coldoc is not None:
            self.add_line(f"    - {coldoc[0]}", self.get_sourcename())
            for line in coldoc[1:]:
                self.add_line(f"      {line}", self.get_sourcename())
        else:
            self.add_line("    - ", self.get_sourcename())

    def get_column_doc(self, column: qv.Column) -> Optional[list[str]]:
        self.analyzer = ModuleAnalyzer.for_module(self.real_modname)
        docs = self.analyzer.find_attr_docs()

        objpath = (self.parent.__name__, column.name)
        if objpath in docs:
            return docs[objpath]
        return None

    def add_attributes_list(self):
        # Add table directive
        self.add_line(".. list-table:: Scalar Attributes", self.get_sourcename())
        self.add_line("  :widths: 30 70", self.get_sourcename())
        self.add_line("  :header-rows: 1", self.get_sourcename())
        self.add_line("", self.get_sourcename())

        # Add table header
        self.add_line("  * - Attribute", self.get_sourcename())
        self.add_line("    - Type", self.get_sourcename())

        # Add row for each attribute in the table
        for attr in self.parent._quivr_attributes.values():
            self.add_attributes_list_row(attr)

    def add_attributes_list_row(self, attr: quivr.attributes.Attribute):
        self.add_line(f"  * - {attr.name}", self.get_sourcename())
        self.add_line(f"    - {self._attr_type_string(attr)}", self.get_sourcename())

    def _type_string(self, col: qv.Column) -> str:
        if isinstance(col, qv.SubTableColumn):
            return f":obj:`{col.table_type.__name__}`"
        elif isinstance(col, qv.Float64Column):
            return "float64"
        elif isinstance(col, qv.Float32Column):
            return "float32"
        return str(col.dtype)

    def _attr_type_string(self, attr: quivr.attributes.Attribute) -> str:
        if isinstance(attr, qv.StringAttribute):
            return "str"
        elif isinstance(attr, qv.IntAttribute):
            return "int"
        elif isinstance(attr, qv.FloatAttribute):
            return "float"
        return str(attr._type)


def setup(app):
    app.setup_extension("sphinx.ext.autodoc")  # Require autodoc extension
    app.add_autodocumenter(QuivrSchemaDocumenter)
    app.add_autodocumenter(QuivrTableDocumenter)

    return {
        "version": version,
        "parallel_read_safe": True,
    }
