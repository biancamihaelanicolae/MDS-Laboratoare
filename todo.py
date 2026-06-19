import json
import os


DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todos.json")


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"next_id": 1, "tasks": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_task(data, description):
    tid = data["next_id"]
    data["tasks"][str(tid)] = {"description": description, "done": False}
    data["next_id"] += 1
    print(f"Added task #{tid}: {description}")
    save_data(data)


def list_tasks(data, status=None):
    if not data["tasks"]:
        print("No tasks.")
        return
    for tid_str in sorted(data["tasks"].keys(), key=int):
        t = data["tasks"][tid_str]
        if status == "pending" and t["done"]:
            continue
        if status == "done" and not t["done"]:
            continue
        mark = "[x]" if t["done"] else "[ ]"
        print(f"  {tid_str}. {mark} {t['description']}")


def mark_done(data, tid_str):
    if tid_str not in data["tasks"]:
        print(f"Task with ID {tid_str} not found.")
        return
    data["tasks"][tid_str]["done"] = True
    print(f"Task #{tid_str} marked as done.")
    save_data(data)


def delete_task(data, tid_str):
    if tid_str not in data["tasks"]:
        print(f"Task with ID {tid_str} not found.")
        return
    removed = data["tasks"].pop(tid_str)
    print(f"Deleted task #{tid_str}: {removed['description']}")
    save_data(data)


def clear_tasks(data):
    data["tasks"] = {}
    data["next_id"] = 1
    print("All tasks cleared.")
    save_data(data)


def show_help():
    print("Available commands:")
    print("  add <description>     Add a new task")
    print("  list [pending|done]   List tasks (optionally filtered)")
    print("  done <id>             Mark task as completed")
    print("  delete <id>           Delete a task")
    print("  clear                 Delete all tasks")
    print("  help                  Show this help")
    print("  exit                  Exit the application")


def main():
    data = load_data()
    print("TODO List Application. Type 'help' for commands.")
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            break
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "exit":
            break
        elif cmd == "help":
            show_help()
        elif cmd == "add":
            if not args:
                print("Usage: add <description>")
            else:
                add_task(data, " ".join(args))
        elif cmd == "list":
            status = args[0] if args else None
            if status and status not in ("pending", "done"):
                print("Usage: list [pending|done]")
            else:
                list_tasks(data, status)
        elif cmd == "done":
            if not args:
                print("Usage: done <id>")
            else:
                mark_done(data, args[0])
        elif cmd == "delete":
            if not args:
                print("Usage: delete <id>")
            else:
                delete_task(data, args[0])
        elif cmd == "clear":
            clear_tasks(data)
        else:
            print(f"Unknown command: {cmd}")
            print("Type 'help' for available commands.")


if __name__ == "__main__":
    main()
