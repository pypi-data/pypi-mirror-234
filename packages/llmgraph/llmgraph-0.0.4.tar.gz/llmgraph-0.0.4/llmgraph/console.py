import typer

typer_app = typer.Typer()


@typer_app.command()
def run(
    entity_type: str,
    entity_wikipedia: str,
    entity_root: str = None,
    levels: int = 2,
    max_sum_total_tokens: int = 200000,
    output_folder: str = "./_output/",
):
    print(f"Hello from llmgraph! {entity_type=}, {entity_wikipedia=}")
