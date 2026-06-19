import json
import os
from openai import OpenAI


OLLAMA_BASE = "http://localhost:11434/v1"
MODEL = "mistral"
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todos_agent.json")

client = OpenAI(base_url=OLLAMA_BASE, api_key="ollama")


def load():
    if not os.path.exists(DATA_FILE):
        return {"next_id": 1, "tasks": {}}
    with open(DATA_FILE) as f:
        return json.load(f)


def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_task(description):
    data = load()
    tid = data["next_id"]
    data["tasks"][str(tid)] = {"description": description, "done": False}
    data["next_id"] += 1
    save(data)
    return f"Added task #{tid}: {description}"


def list_tasks(status=None):
    data = load()
    if not data["tasks"]:
        return "No tasks."
    lines = []
    for tid in sorted(data["tasks"].keys(), key=int):
        t = data["tasks"][tid]
        if status == "pending" and t["done"]:
            continue
        if status == "done" and not t["done"]:
            continue
        mark = "[x]" if t["done"] else "[ ]"
        lines.append(f"  {tid}. {mark} {t['description']}")
    return "\n".join(lines) if lines else "No matching tasks."


def mark_done(tid):
    data = load()
    if tid not in data["tasks"]:
        return f"Task #{tid} not found."
    data["tasks"][tid]["done"] = True
    save(data)
    return f"Task #{tid} marked as done."


def delete_task(tid):
    data = load()
    if tid not in data["tasks"]:
        return f"Task #{tid} not found."
    desc = data["tasks"].pop(tid)["description"]
    save(data)
    return f"Deleted task #{tid}: {desc}"


def clear_tasks():
    data = load()
    data["tasks"] = {}
    data["next_id"] = 1
    save(data)
    return "All tasks cleared."


def todo_tools():
    return [
        {"type": "function", "function": {
            "name": "add_task", "description": "Add a new task.",
            "parameters": {"type": "object", "properties": {"description": {"type": "string"}}, "required": ["description"]},
        }},
        {"type": "function", "function": {
            "name": "list_tasks", "description": "List all tasks or filter by status (pending/done).",
            "parameters": {"type": "object", "properties": {"status": {"type": "string", "enum": ["pending", "done"]}}, "required": []},
        }},
        {"type": "function", "function": {
            "name": "mark_done", "description": "Mark a task as completed by ID.",
            "parameters": {"type": "object", "properties": {"tid": {"type": "string"}}, "required": ["tid"]},
        }},
        {"type": "function", "function": {
            "name": "delete_task", "description": "Delete a task by ID.",
            "parameters": {"type": "object", "properties": {"tid": {"type": "string"}}, "required": ["tid"]},
        }},
        {"type": "function", "function": {
            "name": "clear_tasks", "description": "Delete all tasks.",
            "parameters": {"type": "object", "properties": {}},
        }},
    ]


def handle_tool_call(tc):
    name = tc.function.name
    args = json.loads(tc.function.arguments) if tc.function.arguments else {}
    funcs = {
        "add_task": lambda: add_task(args["description"]),
        "list_tasks": lambda: list_tasks(args.get("status")),
        "mark_done": lambda: mark_done(args["tid"]),
        "delete_task": lambda: delete_task(args["tid"]),
        "clear_tasks": clear_tasks,
    }
    return funcs.get(name, lambda: f"Unknown tool: {name}")()


def chat_loop():
    print("TODO Agent (type 'exit' to quit)")
    print("Examples:")
    print('  "Add a task for buying groceries"')
    print('  "List all tasks"')
    print('  "Mark task 1 as done"')
    print('  "Delete task 2"')
    print('  "Show pending tasks"')
    print()

    messages = [{"role": "system", "content": "You are a TODO assistant. You MUST use the provided tools to manage tasks. Do NOT describe what tools to use — ALWAYS call them directly. When asked to add/list/mark/delete tasks, call the appropriate function immediately."}]
    tools = todo_tools()

    while True:
        try:
            user = input("> ").strip()
        except EOFError:
            break
        if not user:
            continue
        if user.lower() == "exit":
            break

        messages.append({"role": "user", "content": user})

        r = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
        msg = r.choices[0].message

        if msg.tool_calls:
            messages.append(msg)
            for tc in msg.tool_calls:
                result = handle_tool_call(tc)
                print(f"  >> {result}")
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
            r = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
            print(f"  {r.choices[0].message.content}")
        else:
            print(f"  {msg.content}")


if __name__ == "__main__":
    chat_loop()
