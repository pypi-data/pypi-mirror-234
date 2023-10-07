import sys
import typer
from datetime import datetime
from tqdm import tqdm
from time import sleep
from loguru import logger
from .library import engine, env, log, consts

typer_app = typer.Typer()


@typer_app.command()
def main(
    entity_type: str,
    entity_wikipedia: str,
    entity_root: str = None,
    levels: int = 2,
    max_sum_total_tokens: int = 200000,
    output_folder: str = "./_output/",
) -> None:
    if "/wiki/" in entity_type:
        raise Exception(f"You appear to have the 'entity_type' and 'entity_wikipedia' arguments mixed up.")

    custom_entity_root = True
    if "/wiki/" not in entity_wikipedia:
        raise Exception(f"{entity_wikipedia} doesn't look like a valid wikipedia url.")
    if not entity_root:
        wiki_loc = entity_wikipedia.rfind("/wiki/")
        entity_root = entity_wikipedia[wiki_loc:].replace("/wiki/", "").replace("_", " ")  # TODO: review
        custom_entity_root = False

    logger.info(f"Running with {entity_type=}, {entity_wikipedia=}, {entity_root=}, {custom_entity_root=}, {levels=}")
    if levels > 4:
        logger.warning(f"Running with {levels=} - this will take many LLM calls, watch your costs if using a paid API!")
        user_input = input(
            f"Running with {levels=} - this will take many LLM calls, watch your costs if using a paid API! Press Y to continue..."
        )
        if user_input.lower() != "y":
            sys.exit("User did not press Y.")
    start = datetime.now()
    engine.create_company_graph(entity_type, entity_root, entity_wikipedia, levels, max_sum_total_tokens, output_folder)
    took = datetime.now() - start
    logger.info(f"Done, took {took.total_seconds()}s")


if __name__ == "__main__":
    log.configure()
    typer_app()
