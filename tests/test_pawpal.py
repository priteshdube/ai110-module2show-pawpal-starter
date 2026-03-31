import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task(name="Walk Max", duration=30, priority=5, frequency="daily")
    assert task.is_completed() is False
    task.mark_completed()
    assert task.is_completed() is True


def test_add_task_increases_pet_task_count():
    owner = Owner(name="Sarah", available_hours_per_day=4.0)
    pet = Pet(name="Max", species="dog", age=3)
    scheduler = Scheduler(owner, pet)

    task1 = Task(name="Walk Max", duration=30, priority=5)
    task2 = Task(name="Feed Max", duration=15, priority=4)

    assert len(scheduler.get_all_tasks()) == 0
    scheduler.add_task(task1)
    assert len(scheduler.get_all_tasks()) == 1
    scheduler.add_task(task2)
    assert len(scheduler.get_all_tasks()) == 2


def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Sarah", available_hours_per_day=4.0)
    scheduler = Scheduler(owner)

    task_morning = Task(name="Morning Walk", duration=30, priority=3, time="08:00")
    task_noon = Task(name="Noon Feed", duration=15, priority=4, time="12:30")
    task_evening = Task(name="Evening Walk", duration=30, priority=3, time="18:00")
    task_early = Task(name="Early Meds", duration=10, priority=5, time="07:15")

    # Add in non-chronological order
    scheduler.add_task(task_noon)
    scheduler.add_task(task_evening)
    scheduler.add_task(task_early)
    scheduler.add_task(task_morning)

    sorted_tasks = scheduler.sort_by_time()

    times = [t.time for t in sorted_tasks]
    assert times == sorted(times), f"Tasks not in chronological order: {times}"
    assert sorted_tasks[0].name == "Early Meds"
    assert sorted_tasks[-1].name == "Evening Walk"


def test_complete_daily_task_creates_next_day_task():
    owner = Owner(name="Sarah", available_hours_per_day=4.0)
    scheduler = Scheduler(owner)

    today = date(2026, 3, 31)
    task = Task(name="Feed Luna", duration=15, priority=4, frequency="daily", due_date=today)
    scheduler.add_task(task)

    next_task = scheduler.complete_task("Feed Luna")

    assert next_task is not None, "Expected a new task to be created for the next day"
    assert next_task.name == "Feed Luna"
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.is_completed() is False
    assert scheduler.get_task("Feed Luna") is next_task


def test_detect_conflicts_flags_overlapping_times():
    owner = Owner(name="Sarah", available_hours_per_day=4.0)
    scheduler = Scheduler(owner)

    # Both tasks start at 09:00 — direct duplicate time conflict
    task_a = Task(name="Walk Max", duration=30, priority=5, time="09:00")
    task_b = Task(name="Feed Max", duration=20, priority=4, time="09:00")
    scheduler.add_task(task_a)
    scheduler.add_task(task_b)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) > 0, "Expected at least one conflict for tasks at the same time"
    assert any("Walk Max" in w and "Feed Max" in w for w in conflicts)


def test_no_conflict_for_sequential_tasks():
    owner = Owner(name="Sarah", available_hours_per_day=4.0)
    scheduler = Scheduler(owner)

    # task_a ends at 09:30, task_b starts at 09:30 — no overlap
    task_a = Task(name="Morning Walk", duration=30, priority=5, time="09:00")
    task_b = Task(name="Morning Feed", duration=15, priority=4, time="09:30")
    scheduler.add_task(task_a)
    scheduler.add_task(task_b)

    conflicts = scheduler.detect_conflicts()

    assert conflicts == [], f"Expected no conflicts for back-to-back tasks, got: {conflicts}"
