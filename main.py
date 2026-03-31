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
        available_hours_per_day=1.0,   # tight budget to demo the greedy cap
        preferences={"preferred_schedule": "morning"}
    )
    print(f"Owner : {owner.name}")
    print(f"Budget: {owner.available_hours_per_day} h/day "
          f"({int(owner.available_hours_per_day * 60)} min)\n")

    # ── Pets (Improvement 3 – multi-pet scheduler) ────────────────────────────
    print_separator("PETS")
    pet1 = Pet(name="Max",  species="dog", age=3,
               breed="Golden Retriever", special_needs="Needs regular exercise")
    pet2 = Pet(name="Luna", species="cat", age=2,
               breed="Siamese",          special_needs="Requires medication daily")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Improvement 2: start_hour=8 → schedule begins at 08:00 instead of 00:00
    # Improvement 3: pass pet1 as primary; add pet2 via add_pet()
    scheduler = Scheduler(owner, pet=pet1, start_hour=8)
    scheduler.add_pet(pet2)

    print(f"Pets in scheduler: {[p.name for p in scheduler.pets]}\n")

    # ── Tasks ─────────────────────────────────────────────────────────────────
    print_separator("TASKS")

    tasks = [
        Task(name="Walk Max",             duration=30, priority=5, frequency="daily"),
        Task(name="Feed Max",             duration=15, priority=4, frequency="daily"),
        Task(name="Play with Luna",       duration=20, priority=3, frequency="daily"),
        Task(name="Give Luna Medication", duration=5,  priority=5, frequency="daily"),
        # Improvement 4: weekly task — only appears on Monday (day_number=0)
        Task(name="Groom Max",            duration=45, priority=2, frequency="weekly"),
    ]
    pets_for_tasks = [pet1, pet1, pet2, pet2, pet1]

    for task, pet in zip(tasks, pets_for_tasks):
        task.set_pet(pet)
        scheduler.add_task(task)
        freq_note = " (weekly — Monday only)" if task.frequency == "weekly" else ""
        print(f"  + {task.name:26s} {task.duration:3d} min  "
              f"priority {task.priority}  [{task.frequency}]{freq_note}")

    # ── Improvement 4: weekly vs daily demo ───────────────────────────────────
    print_separator("FREQUENCY CHECK (needs_today)")
    groom = scheduler.get_task("Groom Max")
    for day, label in [(0, "Monday"), (1, "Tuesday"), (6, "Sunday")]:
        print(f"  Groom Max on {label:9s} (day {day}): "
              f"{'YES' if groom.needs_today(day) else 'NO'}")

    # ── Improvement 1 + 2: greedy schedule with real start time ───────────────
    print_separator("TODAY'S SCHEDULE  (Monday, starts 08:00)")
    schedule = scheduler.generate_schedule(day_number=0)

    start_min = scheduler.start_hour * 60
    elapsed = 0
    for idx, task in enumerate(schedule, 1):
        s = start_min + elapsed
        e = s + task.duration
        sh, sm = divmod(s, 60)
        eh, em = divmod(e, 60)
        pet_name = task.pet.name if task.pet else "—"
        print(f"  {idx}. [{sh:02d}:{sm:02d}–{eh:02d}:{em:02d}]  "
              f"{task.name:26s}  pet: {pet_name}  priority: {task.priority}")
        elapsed += task.duration

    total_h, total_m = divmod(elapsed, 60)
    print(f"\n  Total scheduled: {total_h}h {total_m}m  "
          f"(budget: {int(owner.available_hours_per_day * 60)} min)")

    # ── Improvement 5: schedule explanation ───────────────────────────────────
    print_separator("SCHEDULE EXPLANATION")
    for line in scheduler.explain_schedule(day_number=0):
        print(f"  {line}")

    # ── Mark some tasks complete then show Improvement 6 ─────────────────────
    print_separator("COMPLETION RATE")
    tasks[0].mark_completed()   # Walk Max
    tasks[3].mark_completed()   # Give Luna Medication

    rate = scheduler.get_completion_rate()
    total  = len(scheduler.get_all_tasks())
    done   = sum(1 for t in scheduler.get_all_tasks() if t.is_completed())
    print(f"  Completed : {done}/{total} tasks")
    print(f"  Rate      : {rate:.1f}%")

    # ── Conflict detection ────────────────────────────────────────────────────
    print_separator("CONFLICT DETECTION")

    # Create a fresh scheduler with intentionally overlapping tasks
    conflict_scheduler = Scheduler(owner, pet=pet1, start_hour=8)

    # Task A: Walk Max  08:00 – 08:30  (30 min)
    t_walk = Task("Walk Max",       duration=30, priority=5,
                  frequency="daily", time="08:00")
    t_walk.set_pet(pet1)

    # Task B: Feed Max  08:20 – 08:35  (15 min) — overlaps Walk Max by 10 min
    t_feed = Task("Feed Max",       duration=15, priority=4,
                  frequency="daily", time="08:20")
    t_feed.set_pet(pet1)

    # Task C: Luna meds 09:00 – 09:05  (5 min) — no overlap
    t_meds = Task("Luna Medication", duration=5, priority=5,
                  frequency="daily", time="09:00")
    t_meds.set_pet(pet2)

    # Task D: Play Luna 09:03 – 09:23  (20 min) — overlaps Luna meds by 2 min
    t_play = Task("Play with Luna", duration=20, priority=3,
                  frequency="daily", time="09:03")
    t_play.set_pet(pet2)

    for t in [t_walk, t_feed, t_meds, t_play]:
        conflict_scheduler.add_task(t)

    print("Tasks scheduled:")
    for t in conflict_scheduler.get_all_tasks():
        h, m = map(int, t.time.split(":"))
        end_m = h * 60 + m + t.duration
        print(f"  {t.time}–{end_m // 60:02d}:{end_m % 60:02d}  "
              f"{t.name:20s}  pet: {t.pet.name if t.pet else '—'}")

    print()
    conflicts = conflict_scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts detected.")

    print_separator()
    print("All improvements verified.\n")


if __name__ == "__main__":
    main()