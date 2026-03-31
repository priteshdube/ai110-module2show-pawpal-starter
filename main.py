"""
PawPal+ Test Script
Tests the scheduling system with sample Owner, Pets, and Tasks.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def print_separator(title: str = ""):
    """Print a formatted separator line."""
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}\n")
    else:
        print(f"\n{'-' * 60}\n")


def print_pet_info(pet: Pet):
    """Print formatted pet information."""
    info = pet.get_info()
    print(f"  🐾 {pet.name}")
    print(f"     Species: {info['species']}, Age: {info['age']} years")
    if info['breed']:
        print(f"     Breed: {info['breed']}")
    if info['special_needs']:
        print(f"     Special Needs: {info['special_needs']}")
    print()


def print_task_info(task: Task):
    """Print formatted task information."""
    priority_indicator = "⭐" * task.priority
    status = "✓ DONE" if task.is_completed() else "⏳ PENDING"
    print(f"  [{status}] {task.name} ({task.duration} mins)")
    print(f"      Priority: {priority_indicator} ({task.priority}/5)")
    print(f"      Frequency: {task.frequency}")
    print()


def main():
    """Main test function."""
    
    print_separator("PAWPAL+ PET CARE SCHEDULER - TEST RUN")
    
    # ===== CREATE OWNER =====
    print("Creating Owner...")
    owner = Owner(
        name="Sarah",
        available_hours_per_day=4.0,
        preferences={"preferred_schedule": "morning", "pet_friendly": True}
    )
    print(f"✓ Owner: {owner.name}")
    print(f"✓ Available Time: {owner.available_hours_per_day} hours/day")
    print(f"✓ Preferences: {owner.preferences}\n")
    
    # ===== CREATE PETS =====
    print_separator("CREATING PETS")
    
    pet1 = Pet(
        name="Max",
        species="dog",
        age=3,
        breed="Golden Retriever",
        special_needs="Needs regular exercise"
    )
    print(f"✓ Created Pet 1:")
    print_pet_info(pet1)
    
    pet2 = Pet(
        name="Luna",
        species="cat",
        age=2,
        breed="Siamese",
        special_needs="Requires medication daily"
    )
    print(f"✓ Created Pet 2:")
    print_pet_info(pet2)
    
    # Add pets to owner
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    print(f"✓ Added {len(owner.get_all_pets())} pets to owner\n")
    
    # ===== CREATE TASKS =====
    print_separator("CREATING TASKS")
    
    # Task 1: Walk Max (high priority, daily)
    task1 = Task(
        name="Walk Max",
        duration=30,
        priority=5,
        frequency="daily"
    )
    task1.set_pet(pet1)
    print(f"✓ Created Task 1:")
    print_task_info(task1)
    
    # Task 2: Feed Max (high priority, daily)
    task2 = Task(
        name="Feed Max",
        duration=15,
        priority=4,
        frequency="daily"
    )
    task2.set_pet(pet1)
    print(f"✓ Created Task 2:")
    print_task_info(task2)
    
    # Task 3: Play with Luna (medium priority, daily)
    task3 = Task(
        name="Play with Luna",
        duration=20,
        priority=3,
        frequency="daily"
    )
    task3.set_pet(pet2)
    print(f"✓ Created Task 3:")
    print_task_info(task3)
    
    # Task 4: Give Luna medication (high priority, daily)
    task4 = Task(
        name="Give Luna Medication",
        duration=5,
        priority=5,
        frequency="daily"
    )
    task4.set_pet(pet2)
    print(f"✓ Created Task 4:")
    print_task_info(task4)
    
    # ===== CREATE SCHEDULER =====
    print_separator("SETTING UP SCHEDULER")
    
    scheduler = Scheduler(owner, pet1)
    
    # Add tasks to scheduler
    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_task(task3)
    scheduler.add_task(task4)
    
    print(f"✓ Scheduler created with {len(scheduler.get_all_tasks())} tasks")
    print(f"✓ Owner: {scheduler.owner.name}")
    print(f"✓ Primary Pet: {scheduler.pet.name}\n")
    
    # ===== CHECK FEASIBILITY =====
    print_separator("SCHEDULE FEASIBILITY CHECK")
    
    total_duration = scheduler.calculate_total_duration(scheduler.get_all_tasks())
    available_minutes = int(owner.available_hours_per_day * 60)
    
    print(f"Total Task Duration: {total_duration} minutes")
    print(f"Available Time: {available_minutes} minutes")
    print(f"Feasible: {'✓ YES' if scheduler.is_schedule_feasible() else '✗ NO'}")
    
    if scheduler.is_schedule_feasible():
        print(f"Extra Time Available: {available_minutes - total_duration} minutes\n")
    else:
        print(f"Over Budget By: {total_duration - available_minutes} minutes\n")
    
    # ===== GENERATE AND PRINT SCHEDULE =====
    print_separator("TODAY'S SCHEDULE")
    
    schedule = scheduler.generate_schedule()
    
    if schedule:
        print(f"Schedule for {owner.name} - {owner.available_hours_per_day} hours available\n")
        
        time_elapsed = 0
        for idx, task in enumerate(schedule, 1):
            start_time_mins = time_elapsed
            end_time_mins = time_elapsed + task.duration
            
            start_hour = start_time_mins // 60
            start_min = start_time_mins % 60
            end_hour = end_time_mins // 60
            end_min = end_time_mins % 60
            
            pet_name = task.pet.name if task.pet else "Unknown"
            priority_indicator = "⭐" * task.priority
            
            print(f"{idx}. [{start_hour:02d}:{start_min:02d} - {end_hour:02d}:{end_min:02d}] {task.name}")
            print(f"   Pet: {pet_name} | Duration: {task.duration} min | Priority: {priority_indicator}")
            print()
            
            time_elapsed += task.duration
        
        print("-" * 60)
        print(f"Total Time: {time_elapsed} minutes ({time_elapsed // 60}h {time_elapsed % 60}m)")
    else:
        print("No tasks scheduled for today.")
    
    # ===== MARK SOME TASKS AS COMPLETED =====
    print_separator("MARKING TASKS AS COMPLETED")
    
    task1.mark_completed()
    task3.mark_completed()
    
    print(f"✓ Marked '{task1.name}' as completed")
    print(f"✓ Marked '{task3.name}' as completed\n")
    
    pending = scheduler.get_pending_tasks()
    print(f"Pending Tasks Remaining: {len(pending)}")
    for task in pending:
        print(f"  - {task.name} ({task.duration} mins)")
    
    # ===== DISPLAY SUMMARY =====
    print_separator("SUMMARY")
    
    print(f"Owner: {owner.name}")
    print(f"Pets: {', '.join([pet.name for pet in owner.get_all_pets()])}")
    print(f"Total Tasks: {len(scheduler.get_all_tasks())}")
    print(f"Completed Tasks: {len(scheduler.get_all_tasks()) - len(pending)}")
    print(f"Pending Tasks: {len(pending)}")
    print(f"Schedule Feasible: {'✓ YES' if scheduler.is_schedule_feasible() else '✗ NO'}")
    
    print_separator()
    print("✓ Test completed successfully!\n")


if __name__ == "__main__":
    main()
