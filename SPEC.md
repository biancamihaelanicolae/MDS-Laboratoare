# TODO List Application - Specification

## Overview
A command-line TODO list application with an interactive REPL (Read-Eval-Print Loop). Users can manage tasks through simple text commands.

## Commands

### `add <description>`
Add a new task with the given description. The task is assigned a unique numeric ID and is marked as pending.
- Example: `add Buy groceries`

### `list [status]`
List all tasks. Optionally filter by status.
- `list` — show all tasks
- `list pending` — show only pending tasks
- `list done` — show only completed tasks

Each task is displayed as:
```
[ID] [status] description
```
where status is `[ ]` for pending and `[x]` for done.

### `done <id>`
Mark the task with the given ID as completed.
- Example: `done 1`

### `delete <id>`
Remove the task with the given ID from the list.
- Example: `delete 1`

### `clear`
Remove all tasks.

### `help`
Show available commands with brief descriptions.

### `exit`
Exit the application.

## Data Persistence
Tasks are stored in a `todos.json` file in the same directory as the application. The data is loaded on startup and saved after every modification.

## Error Handling
- If a user provides a non-existent ID for `done` or `delete`, print an error message: `Task with ID X not found.`
- If a user provides invalid arguments, print a usage hint.

## Implementation Details
- Use Python standard library only (no external dependencies).
- The REPL loop should display a prompt like `> ` and read user input.
- Task IDs are auto-incremented integers starting from 1.
- Deleted task IDs are not reused.
- The `todos.json` file format is a JSON object with two keys:
  - `next_id`: the next ID to assign
  - `tasks`: a dictionary mapping ID -> { "description": str, "done": bool }
