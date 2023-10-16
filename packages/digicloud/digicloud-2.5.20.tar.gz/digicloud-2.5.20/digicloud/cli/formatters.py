from cliff.formatters import base
from rich import box
from rich.console import Console
from rich.table import Table, Column


class RichFormatter(base.ListFormatter, base.SingleFormatter):
    def add_argument_group(self, parser):
        pass

    def emit_list(self, column_names, data, stdout, parsed_args):
        table = Table(
            *[Column(c, overflow='fold') for c in column_names],
            width=int(parsed_args.max_width) or None,
        )
        for row in data:
            table.add_row(*[str(cell) for cell in row])
        Console(emoji=False, markup=False).print(table)

    def emit_one(self, column_names, data, stdout, parsed_args):
        table = Table(
            Column("Key", overflow='fold'),
            Column("Value", overflow='fold'),
            show_header=False,
            box=box.SQUARE,
        )
        for key, value in list(zip(column_names, data)):
            table.add_row(key, str(value))
        Console(emoji=False, markup=False).print(table)
