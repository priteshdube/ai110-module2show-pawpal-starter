"""
PawPal+ - Pet Care Scheduler
Class stubs for the core scheduling system
"""

from datetime import date, timedelta


class Owner:
    """
    Represents a pet owner with their schedule and preferences.

    Attributes:
        name (str): Owner's name
        available_hours_per_day (float): Hours available per day for pet care
        preferences (dict): Dictionary of owner preferences
    """

    def __init__(self, name: str, available_hours_per_day: float, preferences: dict = None):
        """Initialize an Owner with name, available hours, and optional preferences."""
        self._name = name
        self._available_hours_per_day = available_hours_per_day
        self._preferences = preferences if preferences else {}
        self._pets = {}  # Dictionary for O(1) pet lookup by name

    @property
    def name(self) -> str:
        """Get owner's name."""
        return self._name

    @property
    def available_hours_per_day(self) -> float:
        """Get available hours per day."""
        return self._available_hours_per_day

    @property
    def preferences(self) -> dict:
        """Get owner preferences."""
        return self._preferences

    def get_available_time(self) -> float:
        """Return the number of hours per day the owner has available for pet care."""
        return self._available_hours_per_day

    def set_preferences(self, preferences: dict) -> None:
        """Replace the owner's preferences with the given dictionary."""
        self._preferences = preferences

    def add_pet(self, pet: 'Pet') -> None:
        """Add a pet to the owner's collection and set this owner on the pet."""
        self._pets[pet.name] = pet
        pet.set_owner(self)

    def remove_pet(self, pet_name: str) -> None:
        """Remove the pet with the given name from the owner's collection."""
        if pet_name in self._pets:
            del self._pets[pet_name]

    def get_pet(self, pet_name: str) -> 'Pet':
        """Return the pet with the given name, or None if not found."""
        return self._pets.get(pet_name, None)

    def get_all_pets(self) -> list:
        """Return a list of all pets belonging to this owner."""
        return list(self._pets.values())


class Pet:
    """Represents a pet with its basic information."""

    def __init__(self, name: str, species: str, age: int, breed: str = "", special_needs: str = ""):
        """Initialize a Pet with name, species, age, and optional breed and special needs."""
        self._name = name
        self._species = species
        self._age = age
        self._breed = breed
        self._special_needs = special_needs
        self._owner = None

    @property
    def name(self) -> str:
        """Get pet's name."""
        return self._name

    @property
    def species(self) -> str:
        """Get pet's species."""
        return self._species

    @property
    def age(self) -> int:
        """Get pet's age."""
        return self._age

    @property
    def breed(self) -> str:
        """Get pet's breed."""
        return self._breed

    @property
    def special_needs(self) -> str:
        """Get pet's special needs."""
        return self._special_needs

    def get_info(self) -> dict:
        """Return a dictionary of the pet's name, species, age, breed, and special needs."""
        return {
            "name": self._name,
            "species": self._species,
            "age": self._age,
            "breed": self._breed,
            "special_needs": self._special_needs
        }

    def update_info(self, info: dict) -> None:
        """Update pet attributes from a dictionary, ignoring keys not present in the dict."""
        if "name" in info:
            self._name = info["name"]
        if "species" in info:
            self._species = info["species"]
        if "age" in info:
            self._age = info["age"]
        if "breed" in info:
            self._breed = info["breed"]
        if "special_needs" in info:
            self._special_needs = info["special_needs"]

    @property
    def owner(self) -> 'Owner':
        """Get the pet's owner."""
        return self._owner

    def set_owner(self, owner: 'Owner') -> None:
        """Set the owner associated with this pet."""
        self._owner = owner


class Task:
    """Represents a pet care task."""

    def __init__(self, name: str, duration: int, priority: int,
                 frequency: str = "daily", time: str = "00:00",
                 due_date: date = None):
        """Initialize a Task with name, duration, priority, frequency, start time, and due date."""
        self._name = name
        self._duration = duration
        self._priority = priority
        self._frequency = frequency
        self._time = time           # scheduled start time in "HH:MM" format
        self._due_date = due_date if due_date is not None else date.today()
        self._pet = None
        self._completed = False

    @property
    def name(self) -> str:
        """Get task name."""
        return self._name

    @property
    def duration(self) -> int:
        """Get task duration in minutes."""
        return self._duration

    @property
    def priority(self) -> int:
        """Get task priority level."""
        return self._priority

    @property
    def frequency(self) -> str:
        """Get task frequency."""
        return self._frequency

    @property
    def time(self) -> str:
        """Get the scheduled start time as a string in 'HH:MM' format."""
        return self._time

    def set_time(self, time: str) -> None:
        """Set the scheduled start time; value must be in 'HH:MM' format."""
        self._time = time

    def is_high_priority(self) -> bool:
        """Return True if the task's priority is 4 or higher."""
        return self._priority >= 4

    def get_duration(self) -> int:
        """Return the task duration in minutes."""
        return self._duration

    def needs_today(self, day_number: int = 0) -> bool:
        """Return True if the task should run today.

        day_number: 0 = Monday ... 6 = Sunday.
        'daily' tasks always return True.
        'weekly' tasks return True only on Monday (day_number == 0).
        """
        freq = self._frequency.lower()
        if freq == "daily":
            return True
        if freq == "weekly":
            return day_number == 0
        return False

    @property
    def pet(self) -> 'Pet':
        """Get the pet associated with this task."""
        return self._pet

    def set_pet(self, pet: 'Pet') -> None:
        """Associate the given pet with this task."""
        self._pet = pet

    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self._completed = True

    def is_completed(self) -> bool:
        """Return True if the task has been marked as completed."""
        return self._completed

    @property
    def due_date(self) -> date:
        """Return the date this task is due."""
        return self._due_date


class Scheduler:
    """
    Main scheduling engine for PawPal+.
    Generates daily schedules based on owner, pets, and tasks.

    Attributes:
        owner (Owner): The pet owner instance
        pets (list): All pets managed by this scheduler
        start_hour (int): Hour of day the schedule begins (0–23)
    """

    def __init__(self, owner: Owner, pet: 'Pet' = None, start_hour: int = 8):
        """Initialize the Scheduler with an owner, optional primary pet, and start hour."""
        self._owner = owner
        # Improvement 3: store all pets in a list instead of a single reference
        self._pets = [pet] if pet is not None else []
        # Improvement 2: real start time instead of always 00:00
        self._start_hour = start_hour
        self._tasks = {}
        self._history = []          # completed Task instances are archived here
        self._total_duration_cache = None
        self._sorted_by_priority_cache = None

    @property
    def owner(self) -> Owner:
        """Get the owner."""
        return self._owner

    @property
    def pet(self) -> 'Pet':
        """Return the primary (first) pet, or None if no pets have been added."""
        return self._pets[0] if self._pets else None

    @property
    def pets(self) -> list:
        """Return all pets tracked by this scheduler."""
        return list(self._pets)

    @property
    def start_hour(self) -> int:
        """Return the hour of day the schedule starts."""
        return self._start_hour

    @property
    def tasks(self) -> list:
        """Get list of tasks."""
        return list(self._tasks.values())

    def add_pet(self, pet: 'Pet') -> None:
        """Add a pet to the scheduler if it is not already present."""
        if pet not in self._pets:
            self._pets.append(pet)

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler and invalidate cached results."""
        self._tasks[task.name] = task
        self.invalidate_cache()

    def remove_task(self, task_name: str) -> None:
        """Remove the task with the given name and invalidate cached results."""
        if task_name in self._tasks:
            del self._tasks[task_name]
            self.invalidate_cache()

    def get_task(self, task_name: str) -> Task:
        """Return the task with the given name, or None if not found."""
        return self._tasks.get(task_name, None)

    def get_all_tasks(self) -> list:
        """Return a list of all tasks currently in the scheduler."""
        return list(self._tasks.values())

    def generate_schedule(self, day_number: int = 0) -> list:
        """Return a feasible, priority-ordered list of tasks for today.

        Improvement 1 — greedy time-cap: tasks are added highest-priority first
        and the loop stops once the remaining budget is exhausted, so the
        returned schedule always fits within the owner's available hours.

        Improvement 4 — weekly frequency: day_number (0=Mon … 6=Sun) is
        forwarded to needs_today() so weekly tasks only appear on Mondays.
        """
        pending = self.get_pending_tasks()
        todays = [t for t in pending if t.needs_today(day_number)]
        ranked = sorted(todays, key=lambda t: (-t.priority, t.name))

        available = int(self._owner.available_hours_per_day * 60)
        schedule, used = [], 0
        for task in ranked:
            if used + task.duration <= available:
                schedule.append(task)
                used += task.duration
        return schedule

    def explain_schedule(self, day_number: int = 0) -> list:
        """Return a human-readable explanation for every task: chosen or skipped and why.

        Improvement 5 — schedule reasoning: each entry states whether the task
        was included or dropped, its priority, and how much time was left.
        """
        pending = self.get_pending_tasks()
        todays = [t for t in pending if t.needs_today(day_number)]
        ranked = sorted(todays, key=lambda t: (-t.priority, t.name))

        available = int(self._owner.available_hours_per_day * 60)
        used, lines = 0, []
        for task in ranked:
            remaining = available - used
            if used + task.duration <= available:
                lines.append(
                    f"{task.name} — chosen "
                    f"(priority {task.priority}, fits in remaining {remaining} min)"
                )
                used += task.duration
            else:
                lines.append(
                    f"{task.name} — skipped "
                    f"(only {remaining} min left, needs {task.duration} min)"
                )
        return lines

    def get_completion_rate(self) -> float:
        """Return the percentage of all tasks that have been marked completed.

        Improvement 6 — completion tracking: 0.0 if no tasks exist.
        """
        all_tasks = self.get_all_tasks()
        if not all_tasks:
            return 0.0
        completed = sum(1 for t in all_tasks if t.is_completed())
        return completed / len(all_tasks) * 100

    def rank_tasks_by_priority(self) -> list:
        """Return all tasks sorted by priority descending, using a cache when available."""
        if self._sorted_by_priority_cache is not None:
            return self._sorted_by_priority_cache
        sorted_tasks = sorted(
            self.get_all_tasks(),
            key=lambda t: (-t.priority, t.name)
        )
        self._sorted_by_priority_cache = sorted_tasks
        return sorted_tasks

    def sort_by_time(self, tasks: list = None) -> list:
        """Return tasks sorted by their 'HH:MM' start time using a lambda key.

        Splits each time string on ':' and converts hours and minutes to
        integers so that '09:05' sorts before '09:30' and '08:00' sorts
        before '10:00'.  Passing no argument sorts all tasks in the scheduler.
        """
        source = tasks if tasks is not None else self.get_all_tasks()
        return sorted(source, key=lambda t: (int(t.time.split(":")[0]),
                                             int(t.time.split(":")[1])))

    def fit_tasks_in_time(self, tasks: list) -> bool:
        """Return True if the total duration of the given tasks fits within the owner's available time."""
        total_minutes = self.calculate_total_duration(tasks)
        available_minutes = int(self._owner.available_hours_per_day * 60)
        return total_minutes <= available_minutes

    def calculate_total_duration(self, tasks: list) -> int:
        """Return the sum of durations (in minutes) for all tasks in the given list."""
        return sum(task.duration for task in tasks)

    def is_schedule_feasible(self) -> bool:
        """Return True if all pending tasks fit within the owner's available daily time."""
        return self.fit_tasks_in_time(self.get_pending_tasks())

    def complete_task(self, task_name: str) -> 'Task':
        """Mark a task complete and automatically schedule the next occurrence.

        How timedelta works:
            timedelta(days=1)  shifts a date forward by exactly one day.
            timedelta(weeks=1) shifts a date forward by exactly seven days.
            Adding a timedelta to a date object returns a new date object,
            so the original due_date is never mutated.

        Recurrence rules:
            'daily'  → next due_date = current due_date + timedelta(days=1)
            'weekly' → next due_date = current due_date + timedelta(weeks=1)
            other    → task is completed with no new occurrence created.

        Returns:
            The newly created Task for the next occurrence, or None if the
            task is non-recurring or was not found.
        """
        task = self._tasks.get(task_name)
        if task is None:
            return None

        # Mark complete and move to history
        task.mark_completed()
        self._history.append(task)
        del self._tasks[task_name]
        self.invalidate_cache()

        # Determine next due date using timedelta
        freq = task.frequency.lower()
        if freq == "daily":
            next_due = task.due_date + timedelta(days=1)
        elif freq == "weekly":
            next_due = task.due_date + timedelta(weeks=1)
        else:
            return None     # one-off task — no recurrence

        # Create a fresh Task instance for the next occurrence
        next_task = Task(
            name=task.name,
            duration=task.duration,
            priority=task.priority,
            frequency=task.frequency,
            time=task.time,
            due_date=next_due,
        )
        if task.pet is not None:
            next_task.set_pet(task.pet)

        self.add_task(next_task)
        return next_task

    def get_history(self) -> list:
        """Return all tasks that have been completed, in the order they were finished."""
        return list(self._history)

    def get_pending_tasks(self) -> list:
        """Return all tasks that have not yet been marked as completed."""
        return [task for task in self.get_all_tasks() if not task.is_completed()]

    @staticmethod
    def _to_minutes(time_str: str) -> int:
        """Convert a 'HH:MM' string to a total-minutes integer."""
        h, m = time_str.split(":")
        return int(h) * 60 + int(m)

    def detect_conflicts(self, tasks: list = None) -> list:
        """Return a list of warning strings for every pair of tasks whose time slots overlap.

        Conflict rule: two tasks conflict when their intervals overlap, i.e.
            start_a < end_b  AND  start_b < end_a
        where start = time converted to minutes, end = start + duration.

        This is a lightweight O(n²) scan that collects all warnings and
        returns them as strings — it never raises an exception.

        Args:
            tasks: list of Task objects to check. Defaults to all scheduler tasks.

        Returns:
            List of warning strings (empty list = no conflicts).
        """
        source = tasks if tasks is not None else self.get_all_tasks()

        # Pre-compute (start, end) once per task so the nested loop does no parsing
        intervals = [
            (t, self._to_minutes(t.time), self._to_minutes(t.time) + t.duration)
            for t in source
        ]

        warnings = []
        for i, (a, a_start, a_end) in enumerate(intervals):
            for b, b_start, b_end in intervals[i + 1:]:
                if a_start < b_end and b_start < a_end:
                    a_pet = a.pet.name if a.pet else "no pet"
                    b_pet = b.pet.name if b.pet else "no pet"
                    warnings.append(
                        f"WARNING: '{a.name}' ({a_pet}, {a.time}–"
                        f"{a_end // 60:02d}:{a_end % 60:02d}) conflicts with "
                        f"'{b.name}' ({b_pet}, {b.time}–"
                        f"{b_end // 60:02d}:{b_end % 60:02d})"
                    )

        return warnings

    def filter_tasks(self, completed: bool = None, pet_name: str = None) -> list:
        """Return tasks filtered by completion status, pet name, or both.

        Args:
            completed: If True, return only completed tasks.
                       If False, return only pending tasks.
                       If None, completion status is not filtered.
            pet_name:  If provided, return only tasks whose pet matches this name.
                       If None, pet name is not filtered.

        Examples:
            filter_tasks(completed=False)              # all pending tasks
            filter_tasks(completed=True)               # all completed tasks
            filter_tasks(pet_name="Max")               # all tasks for Max
            filter_tasks(completed=False, pet_name="Luna")  # pending tasks for Luna
        """
        results = self.get_all_tasks()

        if completed is not None:
            results = [t for t in results if t.is_completed() == completed]

        if pet_name is not None:
            results = [t for t in results
                       if t.pet is not None and t.pet.name == pet_name]

        return results

    def invalidate_cache(self) -> None:
        """Clear cached duration and priority-sort results after tasks change."""
        self._total_duration_cache = None
        self._sorted_by_priority_cache = None

    def get_preference_value(self, preference_key: str, default=None):
        """Return the owner preference for the given key, or default if not set."""
        return self._owner.preferences.get(preference_key, default)
