# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

The scheduler goes beyond a simple sorted list with several algorithmic improvements:

- **Greedy time-cap** — `generate_schedule()` fills the day highest-priority first and stops when the owner's time budget is exhausted, guaranteeing the returned schedule always fits.
- **Real start times** — the `Scheduler` accepts a `start_hour` so slots display as `08:00`, `08:30`, etc. instead of `00:00`.
- **Multi-pet support** — multiple pets can be registered with one scheduler; tasks are linked to individual pets and filtered or reported per pet.
- **Weekly frequency** — `needs_today(day_number)` supports `"daily"` and `"weekly"` tasks; weekly tasks only appear on Mondays.
- **Schedule explanation** — `explain_schedule()` returns a plain-English reason for every task: whether it was chosen (priority + time remaining) or skipped (not enough budget).
- **Completion rate** — `get_completion_rate()` returns the percentage of tasks finished so far.
- **Sort by time** — `sort_by_time()` orders any task list chronologically using a lambda key on `"HH:MM"` strings.
- **Filter tasks** — `filter_tasks(completed, pet_name)` returns tasks matching a completion status, a specific pet, or both combined.
- **Recurring tasks** — `complete_task()` marks a task done, archives it to history, and auto-creates the next occurrence using `timedelta` (`+1 day` for daily, `+7 days` for weekly).
- **Conflict detection** — `detect_conflicts()` scans all task pairs for overlapping time intervals and returns warning strings without ever raising an exception.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
