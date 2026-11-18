"""本地资料交接检查。"""
import csv
from pathlib import Path
import shutil
import tempfile
import unittest

from inspect_inputs import load_tables


DATA = Path(__file__).parent / "data"


class InputTests(unittest.TestCase):
    def test_import_keeps_source_rows(self):
        tables = load_tables(DATA)
        self.assertEqual({name: len(rows) for name, rows in tables.items()}, {'menu_runs': 7, 'serving_split': 8, 'waste_weighs': 10, 'nutrition': 2, 'recipes': 4, 'purchases': 5, 'next_service': 3})

    def test_bad_row_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "data"
            shutil.copytree(DATA, target)
            with (target / ('menu_runs' + ".csv")).open("a", encoding="utf-8") as stream:
                stream.write("多余的一列\n")
            with self.assertRaisesRegex(ValueError, "字段数量不符"):
                load_tables(target)

    def test_reference_is_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "data"
            shutil.copytree(DATA, target)
            records = load_tables(target)
            name, field = ['serving_split', 'batch']
            headers = list(records[name][0])
            row = dict(records[name][0], **{field: "不存在的编号"})
            with (target / (name + ".csv")).open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=headers)
                writer.writeheader()
                writer.writerow(row)
            with self.assertRaisesRegex(ValueError, "不在"):
                load_tables(target)
