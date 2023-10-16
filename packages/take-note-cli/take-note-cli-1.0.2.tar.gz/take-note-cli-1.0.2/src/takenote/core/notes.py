from datetime import date
import sys
from takenote.utils.paths import (
    generate_note_folder,
    generate_note_path,
    generate_template_path,
)
from takenote.utils.dates import (
    get_monday,
    get_time_delta_from_options,
    format_header_date,
)
from takenote.utils.args import process_args
from subprocess import call


def create_file(note_file, template, folder_path, week: date):
    if not template:
        note_file.touch()
    else:
        text = ""
        template_path = generate_template_path(folder_path, template)
        with open(template_path, "r") as template_file:
            text = template_file.read().replace("HEADER_DATE", format_header_date(week))

        note_file.write_text(text)


def check_for_file(week: date, folder_path):
    folder = generate_note_folder(week, folder_path)

    if not folder.exists():
        print(f"Creating folder: {folder}")
        folder.mkdir(parents=True)

    note_path = folder.joinpath(generate_note_path(week))

    return note_path, note_path.exists()


def open_file(week: date, folder_path, editor, workspace=None, template=None):
    note_file, file_exists = check_for_file(week, folder_path)

    if not file_exists:
        print(f"Creating file: {note_file}")
        create_file(note_file, template, folder_path, week)

    args = [editor, note_file]
    if workspace:
        args.append(folder_path.joinpath(workspace))

    call(args)
    return note_file


def main(argv):
    options, parser = process_args(argv)
    print(options)

    try:
        delta = get_time_delta_from_options(options)
    except ValueError:
        parser.print_help()
        sys.exit()

    monday = get_monday(date.today()) + delta
    open_file(
        monday, options.notesFolder, options.editor, options.workspace, options.template
    )
