from lumipy.test.unit.lumiflex_tests.utils import SqlTestCase
from lumipy.lumiflex._metadata import ParamMeta
from lumipy.lumiflex._metadata import DType
from pydantic import ValidationError


class TestParamMeta(SqlTestCase):

    def test_parameter_metadata_ctor(self):
        field_name, table_name = 'Param1', 'My.Test.Table'
        meta = ParamMeta(field_name=field_name, table_name=table_name, dtype=DType.Text)
        self.assertEqual(field_name, meta.field_name)
        self.assertEqual(table_name, meta.table_name)
        self.assertEqual(DType.Text, meta.dtype)

    def test_parameter_metadata_ctor_defaults(self):
        field_name, table_name = 'Param1', 'My.Test.Table'
        meta = ParamMeta(field_name=field_name, table_name=table_name, dtype=DType.Text)
        self.assertEqual(field_name, meta.field_name)
        self.assertEqual(table_name, meta.table_name)
        self.assertEqual(DType.Text, meta.dtype)

    def test_parameter_metadata_extras_error(self):
        field_name, table_name = 'Param1', 'My.Test.Table'
        self.assertErrorsWithMessage(
            lambda: ParamMeta(field_name=field_name, table_name=table_name, dtype=DType.Text, bad_field=True),
            ValidationError,
            "1 validation error for ParamMeta\nbad_field\n  extra fields not permitted (type=value_error.extra)"
        )

    def test_parameter_metadata_frozen(self):
        field_name, table_name = 'Param1', 'My.Test.Table'
        meta = ParamMeta(field_name=field_name, table_name=table_name, dtype=DType.Text)

        def action():
            meta.dtype = DType.Date

        self.assertErrorsWithMessage(
            action,
            TypeError,
            '"ParamMeta" is immutable and does not support item assignment',
        )

    def test_parameter_metadata_python_name(self):
        field_name, table_name = 'MyParam1', 'My.Test.Table'
        meta = ParamMeta(field_name=field_name, table_name=table_name, dtype=DType.Text)
        self.assertEqual('my_param1', meta.python_name())
