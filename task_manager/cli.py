import argparse


parser = argparse.ArgumentParser(
    prog="TextManagerParser",
    description="Parser for working with TextManager",
)
subparsers = parser.add_subparsers(
    dest="command",
    required=True,
)

# add parser
add_parser = subparsers.add_parser(
    "add",
    help="Add a new task",
)
add_parser.add_argument(
    "title",
    type=str,
    help="Task title",
)
add_parser.add_argument(
    "description",
    type=str,
    help="Task description",
)
add_parser.add_argument(
    "due_date",
    type=str,
    help="Task due date (DD-MM-YYYY)",
)

# update parser
update_parser = subparsers.add_parser(
    "update",
    help="Update task status",
)
update_parser.add_argument(
    "status",
    type=str,
    help="New task status",
)
update_parser.add_argument(
    "--task-id",
    type=int,
    help="Task ID",
)
update_parser.add_argument(
    "--title",
    type=str,
    help="Task title",
)

# list parser
list_parser = subparsers.add_parser(
    "list",
    help="Task list",
)

# delete parser
delete_parser = subparsers.add_parser(
    "delete",
    help="Delete task",
)
delete_parser.add_argument(
    "--task-id",
    type=int,
    help="Task ID",
)
delete_parser.add_argument(
    "--title",
    type=str,
    help="Task title",
)

def get_args():
    return parser.parse_args()
