"""
PawPal+ - Pet Care Scheduler
Class stubs for the core scheduling system
"""


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
        self._owner = None  # Reference to Owner instance (missing relationship)

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

    def __init__(self, name: str, duration: int, priority: int, frequency: str = "daily"):
        """Initialize a Task with name, duration in minutes, priority level, and frequency."""
        self._name = name
        self._duration = duration
        self._priority = priority
        self._frequency = frequency
        self._pet = None  # Reference to Pet instance (missing relationship)
        self._completed = False  # Track completion status for filtering

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

    def is_high_priority(self) -> bool:
        """Return True if the task's priority is 4 or higher."""
        return self._priority >= 4

    def get_duration(self) -> int:
        """Return the task duration in minutes."""
        return self._duration

    def needs_today(self) -> bool:
        """Return True if the task frequency is 'daily'."""
        return self._frequency.lower() == "daily"

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


class Scheduler:
    """
    Main scheduling engine for PawPal+.
    Generates daily schedules based on owner, pet, and tasks.

    Attributes:
        owner (Owner): The pet owner instance
        pet (Pet): The pet instance
        tasks (list): List of Task instances
    """

    def __init__(self, owner: Owner, pet: Pet):
        """Initialize the Scheduler with an owner and primary pet."""
        self._owner = owner
        self._pet = pet
        self._tasks = {}  # Dictionary for O(1) task lookup by name (bottleneck fix)
        self._task_list = []  # Sorted list for scheduling (cache)
        self._total_duration_cache = None  # Cache for total duration (bottleneck fix)
        self._sorted_by_priority_cache = None  # Cache for priority-sorted tasks (bottleneck fix)

    @property
    def owner(self) -> Owner:
        """Get the owner."""
        return self._owner

    @property
    def pet(self) -> Pet:
        """Get the pet."""
        return self._pet

    @property
    def tasks(self) -> list:
        """Get list of tasks."""
        return list(self._tasks.values())

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

    def generate_schedule(self) -> list:
        """Return pending daily tasks sorted by priority (highest first)."""
        # Get pending tasks that need to be done today
        pending_tasks = self.get_pending_tasks()
        daily_tasks = [t for t in pending_tasks if t.needs_today()]

        # Rank by priority and return
        ranked = sorted(daily_tasks, key=lambda t: (-t.priority, t.name))
        return ranked

    def rank_tasks_by_priority(self) -> list:
        """Return all tasks sorted by priority descending, using a cache when available."""
        # Use cached result if available
        if self._sorted_by_priority_cache is not None:
            return self._sorted_by_priority_cache

        # Sort tasks by priority (descending) and then by name (ascending)
        sorted_tasks = sorted(
            self.get_all_tasks(),
            key=lambda t: (-t.priority, t.name)
        )

        # Cache the result
        self._sorted_by_priority_cache = sorted_tasks
        return sorted_tasks

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
        pending_tasks = self.get_pending_tasks()
        return self.fit_tasks_in_time(pending_tasks)

    def get_pending_tasks(self) -> list:
        """Return all tasks that have not yet been marked as completed."""
        return [task for task in self.get_all_tasks() if not task.is_completed()]

    def invalidate_cache(self) -> None:
        """Clear cached duration and priority-sort results after tasks change."""
        self._total_duration_cache = None
        self._sorted_by_priority_cache = None

    def get_preference_value(self, preference_key: str, default=None):
        """Return the owner preference for the given key, or default if not set."""
        return self._owner.preferences.get(preference_key, default)
