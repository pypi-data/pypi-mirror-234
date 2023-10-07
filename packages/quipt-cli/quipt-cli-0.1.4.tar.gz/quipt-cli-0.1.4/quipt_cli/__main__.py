import os
import sys
from typing import cast
from uuid import UUID
import click

from rich import print as rprint
from platformdirs import user_data_dir

from .parser import Database, convert_handle_error
from .server_sync import ErrorReason, OperationalError, QuiptApp, ScriptContext
from .serialisation import ItemType, Deserializer, Trigger

APP_NAME = "quipt-cli"
AUTHOR_NAME = "Stausee1337"
DATA_DIR = user_data_dir(APP_NAME, AUTHOR_NAME)

@click.group()
def cli():
    pass

@cli.command(help="Compare and Stage different versions of the same script file")
@click.option("-D", "--database", default=None, help="Path to a quipt-cli database directory")
@click.argument("filename", type=click.Path(exists=True))
def diff(database, filename):
    database_location = database or DATA_DIR
    convert_handle_error(filename, database_location)

@cli.command(help="Push changes upstream to the Quipt server")
@click.option("-D", "--database", default=None, help="Path to a quipt-cli database directory")
@click.argument("play_name")
def push(database, play_name):
    database_location = database or DATA_DIR
    if (database := Database.open(database_location, play_name)) is None:
        print(f"Failed to find Version Database for {play_name}", file=sys.stderr)
        print(f"Maybe you've stored it at a different location", file=sys.stderr)
        return
    database = cast(Database, database)

    history = database.history
    rprint(f"Version history of [italic green]{database.script_id}[/] for [yellow]{play_name}[/]")

    unpushed_versions = []
    for version in reversed(history):
        if version["pushed"]:
            break
        unpushed_versions.append(version)

    changes: list[tuple[str, str]] = []
    for version in reversed(unpushed_versions):
        rprint(f"  Changes at Version {version['version']:03d}")
        for change in version["changes"]:
            changes.append((change, version["filename"]))
            rprint(f"    {change}")

    if database.serialized_file is None:
        print("Invalid: Empty History")
        return

    if len(unpushed_versions) == 0:
        print("No changes; Nothing to push")
        rprint("[yellow]exiting...[/]")
        return

    try:
        connection: QuiptApp = QuiptApp.login(DATA_DIR)
    except OperationalError as ex:
        if ex.reason == ErrorReason.UserCanceledOperation:
            print("Pushing canceled at login")
        return

    if unpushed_versions[-1]["version"] == 0:
        try:
            connection.create_script(database.serialized_file, database.script_id, play_name)
            rprint(f"Created Script for [italic green]{database.script_id}[/]")
        except OperationalError:
            rprint(f"Application exited with error")
            connection.close()
            return
    else:
        changes = simplify_changes(changes)
        try:
            with connection.alternate_script(database.script_id) as context:
                process_changes(context, database.database_path, changes)
            rprint(f"Pushed Changes Script for [italic green]{database.script_id}[/]")
        except OperationalError:
            rprint(f"Application exited with error")
            connection.close()
            return

    database.write_pushed()
    connection.close()

@cli.command(help="Forget a database for the play entierly; removing it from the system")
@click.argument("play_name")
def forget(play_name):
    if (database := Database.open(DATA_DIR, play_name)) is None:
        print(f"Failed to find Version Database for {play_name}", file=sys.stderr)
        print(f"Maybe you've stored it at a different location", file=sys.stderr)
        return
    database.remove()

@cli.command(help="Restore a specific past version of the script from the database")
@click.option("-D", "--database", default=None, help="Path to a quipt-cli database directory")
@click.argument("play_name")
@click.argument("version", type=click.types.INT)
def restore(database, play_name, version: int):
    database_location = database or DATA_DIR
    if (database := Database.open(database_location, play_name)) is None:
        print(f"Failed to find Version Database for {play_name}", file=sys.stderr)
        print(f"Maybe you've stored it at a different location", file=sys.stderr)
        return
    
    if (state := database.restore_to_version(version)) is None:
        return
    if (out_file_path := database.write_out()) is not None:
        state.save(out_file_path)
        rprint(f"Staged changes [italic green]{database.script_id}[/] for [yellow]{play_name}[/]")

def simplify_changes(changes: list[tuple[str, str]]) -> list[tuple[str, str]]:
    trigger_events: dict[str, tuple[str, str]] = {}
    division_events: dict[str, tuple[str, str]] = {}

    new_changes: list[tuple[str, str]]= []

    for idx, (ochange, file) in enumerate(changes):
        noappend = False
        change = ochange.split()
        match change:
            case ["Deleted", "Trigger", trigger_uuid]:
                if (idx := trigger_events.get(trigger_uuid, None)) is not None:
                    noappend = idx[0].startswith("Inserted")
                    new_changes.remove(idx)
            case ["Deleted", "Division", div_name]:
                if (idx := division_events.get(div_name, None)) is not None:
                    noappend = idx[0].startswith("Inserted")
                    new_changes.remove(idx)
            case ["Inserted", "Trigger", trigger_uuid, "after", prev]:
                trigger_events[trigger_uuid] = (ochange, file)
            case ["Inserted", "Division", div_name, "after", prev]:
                division_events[div_name] = (ochange, file)
            case ["Changed", "Trigger", trigger_uuid]:
                if (idx := trigger_events.get(trigger_uuid, None)) is not None:
                    ochange = idx[0]
                    new_changes.remove(idx)
                trigger_events[trigger_uuid] = (ochange, file)
        if not noappend:
            new_changes.append((ochange, file))

    return new_changes

def process_changes(context: ScriptContext, db_path: str, changes: list[tuple[str, str]]): 
    for change_tpl in changes:
        change, file = change_tpl
        change = change.split()
        match change:
            case ["Deleted", "Trigger", trigger_uuid]:
                context.delete_trigger(UUID(trigger_uuid))
            case ["Deleted", "Division", div_name]:
                context.delete_division(div_name.replace('\x1b', ' '))
            case ["Inserted", "Trigger", trigger_uuid, "after", prev]:
                new_trigger = lookup_trigger(db_path, file, trigger_uuid)
                context.insert_trigger(prev, new_trigger)
            case ["Inserted", "Division", div_name, "after", prev]:
                context.insert_division(prev, div_name.replace('\x1b', ' '))
            case ["Changed", "Trigger", trigger_uuid]:
                new_trigger = lookup_trigger(db_path, file, trigger_uuid)
                context.change_trigger(new_trigger)
            case ["Changed", "Division", "from", old_div_name, "to", new_div_name]:
                context.change_division(old_div_name.replace('\x1b', ' '), new_div_name.replace('\x1b', ' '))

def lookup_trigger(db_path: str, version_file: str, trigger_uuid: str) -> Trigger:
    uuid = UUID(trigger_uuid)
    uuid_bytes = uuid.bytes

    version_path = os.path.join(db_path, version_file)
    deser = Deserializer()
    file = deser.load(version_path)
    for item in file.overview_talbe:
        if item.item_type == ItemType.TRIGGER and item.item.uuid == uuid_bytes:
            return item.item

    assert False, "Something weird about your local files"

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    cli()

