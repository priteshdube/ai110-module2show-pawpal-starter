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
        """
        Initialize an Owner.
        
        Args:
            name: Owner's name
            available_hours_per_day: Hours available per day for pet care (0-24)
            preferences: Dictionary of owner preferences (optional)
        """
        self._name = name
        self._available_hours_per_day = available_hours_per_day
        self._preferences = preferences if preferences else {}
    
    @property
    def name(self) -> str:
        """Get owner's name."""
        pass
    
    @property
    def available_hours_per_day(self) -> float:
        """Get available hours per day."""
        pass
    
    @property
    def preferences(self) -> dict:
        """Get owner preferences."""
        pass
    
    def get_available_time(self) -> float:
        """
        Get available hours per day for pet care.
        
        Returns:
            float: Available hours
        """
        pass
    
    def set_preferences(self, preferences: dict) -> None:
        """
        Set owner preferences.
        
        Args:
            preferences: Dictionary of preferences
        """
        pass


class Pet:
    """Represents a pet with its basic information."""
    
    def __init__(self, name: str, species: str, age: int, breed: str = "", special_needs: str = ""):
        """
        Initialize a Pet.
        
        Args:
            name: Pet's name
            species: Species (e.g., dog, cat)
            age: Age in years
            breed: Breed (optional)
            special_needs: Any special needs (optional)
        """
        self._name = name
        self._species = species
        self._age = age
        self._breed = breed
        self._special_needs = special_needs
    
    @property
    def name(self) -> str:
        """Get pet's name."""
        pass
    
    @property
    def species(self) -> str:
        """Get pet's species."""
        pass
    
    @property
    def age(self) -> int:
        """Get pet's age."""
        pass
    
    @property
    def breed(self) -> str:
        """Get pet's breed."""
        pass
    
    @property
    def special_needs(self) -> str:
        """Get pet's special needs."""
        pass
    
    def get_info(self) -> dict:
        """
        Get pet information.
        
        Returns:
            dict: Dictionary containing pet info
        """
        pass
    
    def update_info(self, info: dict) -> None:
        """
        Update pet information.
        
        Args:
            info: Dictionary of information to update
        """
        pass


class Task:
    """Represents a pet care task."""
    
    def __init__(self, name: str, duration: int, priority: int, frequency: str = "daily"):
        """
        Initialize a Task.
        
        Args:
            name: Task name (e.g., walk, feed, med)
            duration: Duration in minutes
            priority: Priority level (1-5, 5 being highest)
            frequency: How often (daily, weekly, etc.) - default: "daily"
        """
        self._name = name
        self._duration = duration
        self._priority = priority
        self._frequency = frequency
    
    @property
    def name(self) -> str:
        """Get task name."""
        pass
    
    @property
    def duration(self) -> int:
        """Get task duration in minutes."""
        pass
    
    @property
    def priority(self) -> int:
        """Get task priority level."""
        pass
    
    @property
    def frequency(self) -> str:
        """Get task frequency."""
        pass
    
    def is_high_priority(self) -> bool:
        """
        Check if task is high priority.
        
        Returns:
            bool: True if priority >= 4
        """
        pass
    
    def get_duration(self) -> int:
        """
        Get task duration in minutes.
        
        Returns:
            int: Duration in minutes
        """
        pass
    
    def needs_today(self) -> bool:
        """
        Check if task needs to be done today.
        
        Returns:
            bool: True if task is daily or needs today
        """
        pass


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
        """
        Initialize Scheduler.
        
        Args:
            owner: Owner instance
            pet: Pet instance
        """
        self._owner = owner
        self._pet = pet
        self._tasks = []
    
    @property
    def owner(self) -> Owner:
        """Get the owner."""
        pass
    
    @property
    def pet(self) -> Pet:
        """Get the pet."""
        pass
    
    @property
    def tasks(self) -> list:
        """Get list of tasks."""
        pass
    
    def add_task(self, task: Task) -> None:
        """
        Add a task to the scheduler.
        
        Args:
            task: Task instance to add
        """
        pass
    
    def remove_task(self, task_name: str) -> None:
        """
        Remove a task by name.
        
        Args:
            task_name: Name of task to remove
        """
        pass
    
    def get_task(self, task_name: str) -> Task:
        """
        Get a task by name.
        
        Args:
            task_name: Name of task to retrieve
        
        Returns:
            Task: The requested task, or None if not found
        """
        pass
    
    def get_all_tasks(self) -> list:
        """
        Get all tasks.
        
        Returns:
            list: List of all Task instances
        """
        pass
    
    def generate_schedule(self) -> list:
        """
        Generate a daily schedule.
        
        Returns:
            list: Ordered list of tasks for the day
        """
        pass
    
    def rank_tasks_by_priority(self) -> list:
        """
        Rank tasks by priority.
        
        Returns:
            list: Tasks sorted by priority (highest first)
        """
        pass
    
    def fit_tasks_in_time(self, tasks: list) -> bool:
        """
        Check if tasks fit within available time.
        
        Args:
            tasks: List of tasks to check
        
        Returns:
            bool: True if tasks fit within available hours, False otherwise
        """
        pass
    
    def calculate_total_duration(self, tasks: list) -> int:
        """
        Calculate total duration of tasks in minutes.
        
        Args:
            tasks: List of tasks
        
        Returns:
            int: Total duration in minutes
        """
        pass
    
    def is_schedule_feasible(self) -> bool:
        """
        Check if current schedule is feasible.
        
        Returns:
            bool: True if schedule fits within available time
        """
        pass
