import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

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
