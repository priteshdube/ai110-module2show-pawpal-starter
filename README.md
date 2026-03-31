# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## 📸 Demo

<!-- Replace app_screenshot.png with your actual screenshot filename -->
![PawPal+ Streamlit App](app_screenshot.png)

---

## ✨ Features

| Feature | Description |
|---|---|
| **Chronological sorting** | `sort_by_time()` orders all tasks by their `HH:MM` start time using a lambda key, so the task list always reflects the real order of the day |
| **Conflict detection** | `detect_conflicts()` runs an O(n²) interval-overlap scan across all pending tasks and surfaces a plain-English warning for every pair that overlaps, without raising exceptions |
| **Daily recurrence** | `complete_task()` marks a task done, archives it to history, and auto-creates the next occurrence using `timedelta(days=1)` — so recurring care never falls off the schedule |
| **Weekly recurrence** | Same recurrence engine supports `"weekly"` frequency via `timedelta(weeks=1)`; weekly tasks only appear on Mondays via `needs_today(day_number)` |
| **Priority-based scheduling** | `generate_schedule()` fills the day greedily — highest priority first — and stops when the owner's time budget is exhausted, guaranteeing the plan always fits |
| **Schedule reasoning** | `explain_schedule()` returns a plain-English sentence for every task: chosen (priority + time remaining) or skipped (budget exceeded) |
| **Completion tracking** | `get_completion_rate()` returns the percentage of tasks finished, and completed tasks are archived to `_history` for audit |
| **Task filtering** | `filter_tasks(completed, pet_name)` returns tasks matching a completion status, a specific pet, or both combined |
| **Multi-pet support** | Multiple pets can be registered; tasks link to individual pets and are filtered or reported per pet |
| **Caching** | Priority-sort and total-duration results are cached and automatically invalidated whenever tasks change |

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

## Testing PawPal+

### Run the test suite

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Test | What it verifies |
|------|-----------------|
| `test_mark_complete_changes_status` | A task starts as incomplete and flips to completed after `mark_completed()` |
| `test_add_task_increases_pet_task_count` | Each `add_task()` call grows the scheduler's task list by one |
| `test_sort_by_time_returns_chronological_order` | `sort_by_time()` returns tasks in ascending `HH:MM` order regardless of insertion order |
| `test_complete_daily_task_creates_next_day_task` | Completing a `"daily"` task removes it, archives it, and auto-creates an identical task due the following day |
| `test_detect_conflicts_flags_overlapping_times` | `detect_conflicts()` returns at least one warning when two tasks share the same start time |
| `test_no_conflict_for_sequential_tasks` | Back-to-back tasks (one ends exactly when the next begins) produce no conflict warnings |

### Confidence Level

**4 / 5 stars**

The core scheduling behaviors — sorting, recurrence, and conflict detection — are fully covered and all 6 tests pass. One star is withheld because edge cases such as tasks that span midnight, tasks with no assigned time, and UI-layer integration with Streamlit remain untested.

---

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
