from collections import OrderedDict

from rich.console import Console
from rich.table import Table, Column

from biolib.typing_utils import List, Any


class BioLibTable:
    def __init__(self, columns_to_row_map: OrderedDict, rows: List[Any], title):
        self.title = title
        self.rows = rows
        self.columns_to_row_map = columns_to_row_map
        self.table = self._create_table()

    def _create_table(self) -> Table:
        columns = [Column(header=header, **meta['params']) for header, meta in self.columns_to_row_map.items()]
        table = Table(*columns, title=self.title)
        for row in self.rows:
            table.add_row(
                *[str(row[column['key']]) for column in self.columns_to_row_map.values()]
            )
        return table

    def print_table(self):
        console = Console()
        console.print(self.table)
