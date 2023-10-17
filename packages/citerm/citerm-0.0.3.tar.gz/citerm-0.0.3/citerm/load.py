import asyncio

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.reactive import var
from textual.widgets import DataTable, LoadingIndicator


class TableApp(App):
    CSS = """
    Grid {
        grid-size: 2;
    }

    DataTable {
        border: round $primary;
    }
    """

    load_count: var[int] = var(0)
    fully_loaded: var[bool] = var(False)

    def compose(self) -> ComposeResult:
        yield LoadingIndicator()
        with Grid():
            yield DataTable(id="table-one")
            yield DataTable(id="table-two")
            yield DataTable(id="table-three")
            yield DataTable(id="table-four")

    def on_mount(self) -> None:
        self.query_one(LoadingIndicator).display = True
        self.query_one(Grid).display = False

        self.load_table_one_data()
        self.load_table_two_data()
        self.load_table_three_data()
        self.load_table_four_data()

    def compute_fully_loaded(self) -> bool:
        return self.load_count == 4

    def watch_fully_loaded(self, fully_loaded: bool) -> None:
        if fully_loaded:
            self.query_one(LoadingIndicator).display = False
            self.query_one(Grid).display = True

    @work
    async def load_table_one_data(self) -> None:
        await asyncio.sleep(1)  # Simulate time to load the data
        data: list[tuple] = [
            ("TableOne C1", "TableOne C2"),
            ("TableOne R1 C1", "TableOne R1 C2"),
            ("TableOne R2 C1", "TableOne R2 C2"),
            ("TableOne R3 C1", "TableOne R3 C2"),
        ]
        table = self.query_one("#table-one", DataTable)
        table.border_title = "Table One"
        rows = iter(data)
        table.add_columns(*next(rows))
        table.add_rows(rows)

        self.load_count += 1

    @work
    async def load_table_two_data(self) -> None:
        await asyncio.sleep(2)  # Simulate time to load the data
        data: list[tuple] = [
            ("TableTwo C1", "TableTwo C2"),
            ("TableTwo R1 C1", "TableTwo R1 C2"),
            ("TableTwo R2 C1", "TableTwo R2 C2"),
            ("TableTwo R3 C1", "TableTwo R3 C2"),
        ]
        table = self.query_one("#table-two", DataTable)
        table.border_title = "Table Two"
        rows = iter(data)
        table.add_columns(*next(rows))
        table.add_rows(rows)

        self.load_count += 1

    @work
    async def load_table_three_data(self) -> None:
        await asyncio.sleep(3)  # Simulate time to load the data
        data: list[tuple] = [
            ("TableThree C1", "TableThree C2"),
            ("TableThree R1 C1", "TableThree R1 C2"),
            ("TableThree R2 C1", "TableThree R2 C2"),
            ("TableThree R3 C1", "TableThree R3 C2"),
        ]
        table = self.query_one("#table-three", DataTable)
        table.border_title = "Table Three"
        rows = iter(data)
        table.add_columns(*next(rows))
        table.add_rows(rows)

        self.load_count += 1

    @work
    async def load_table_four_data(self) -> None:
        await asyncio.sleep(4)  # Simulate time to load the data
        data: list[tuple] = [
            ("TableFour C1", "TableFour C2"),
            ("TableFour R1 C1", "TableFour R1 C2"),
            ("TableFour R2 C1", "TableFour R2 C2"),
            ("TableFour R3 C1", "TableFour R3 C2"),
        ]
        table = self.query_one("#table-four", DataTable)
        table.border_title = "Table Four"
        rows = iter(data)
        table.add_columns(*next(rows))
        table.add_rows(rows)

        self.load_count += 1


app = TableApp()
if __name__ == "__main__":
    app.run()
