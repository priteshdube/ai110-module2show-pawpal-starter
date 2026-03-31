import streamlit as st
from datetime import time as dt_time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ── Session-state initialisation ──────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_hours_per_day=4.0)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(
        owner=st.session_state.owner, pet=None
    )

# ── Owner section ─────────────────────────────────────────────────────────────
st.subheader("Owner")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)

# ── Add a Pet ─────────────────────────────────────────────────────────────────
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    existing_names = [p.name for p in st.session_state.owner.get_all_pets()]
    if pet_name in existing_names:
        st.warning(f"A pet named '{pet_name}' is already added.")
    else:
        new_pet = Pet(name=pet_name, species=species, age=0)
        st.session_state.owner.add_pet(new_pet)
        if st.session_state.scheduler.pet is None:
            st.session_state.scheduler = Scheduler(
                owner=st.session_state.owner, pet=new_pet
            )
        st.success(f"Added pet '{pet_name}' ({species}) to {st.session_state.owner.name}.")

pets = st.session_state.owner.get_all_pets()
if pets:
    st.write("Current pets:", ", ".join(p.name for p in pets))

st.divider()

# ── Add a Task ────────────────────────────────────────────────────────────────
st.subheader("Add a Task")

priority_map = {"low": 1, "medium": 3, "high": 5}

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col4, col5 = st.columns(2)
with col4:
    task_time = st.time_input("Start time", value=dt_time(8, 0))
with col5:
    frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

if st.button("Add task"):
    time_str = task_time.strftime("%H:%M")
    new_task = Task(
        name=task_title,
        duration=int(duration),
        priority=priority_map[priority_label],
        frequency=frequency,
        time=time_str,
    )
    if pets:
        new_task.set_pet(pets[0])
    st.session_state.scheduler.add_task(new_task)
    st.success(f"Added '{task_title}' at {time_str} ({duration} min, {priority_label} priority).")

st.divider()

# ── Task List — sorted chronologically ────────────────────────────────────────
st.subheader("Task List")

scheduler = st.session_state.scheduler
all_tasks = scheduler.get_all_tasks()

if all_tasks:
    # Pending tasks sorted by start time
    pending = scheduler.filter_tasks(completed=False)
    completed = scheduler.filter_tasks(completed=True)

    if pending:
        st.markdown("**Pending tasks** *(sorted by start time)*")
        sorted_pending = scheduler.sort_by_time(pending)
        st.table([
            {
                "Start": t.time,
                "Task": t.name,
                "Duration": f"{t.duration} min",
                "Priority": "⭐" * t.priority,
                "Frequency": t.frequency.capitalize(),
                "Pet": t.pet.name if t.pet else "—",
            }
            for t in sorted_pending
        ])
    else:
        st.info("All tasks are completed.")

    if completed:
        with st.expander(f"Completed tasks ({len(completed)})"):
            st.table([
                {
                    "Task": t.name,
                    "Duration": f"{t.duration} min",
                    "Pet": t.pet.name if t.pet else "—",
                }
                for t in completed
            ])

    # ── Conflict Detection ────────────────────────────────────────────────────
    conflicts = scheduler.detect_conflicts(pending)
    if conflicts:
        st.markdown("---")
        st.markdown("### ⚠️ Schedule Conflicts Detected")
        st.caption(
            "Two or more tasks overlap in time. "
            "Adjust a task's start time or shorten its duration to resolve."
        )
        for warning in conflicts:
            # Parse the warning to highlight task names for readability
            st.warning(warning)
        st.markdown(
            "> **Tip for pet owners:** Conflicting tasks can't both start on time. "
            "Consider whether one can wait — for example, medication is usually higher "
            "priority than a grooming session."
        )
    else:
        if pending:
            st.success("No time conflicts — your schedule looks clear!")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Complete a Task ───────────────────────────────────────────────────────────
st.subheader("Mark Task Complete")

pending_names = [t.name for t in scheduler.filter_tasks(completed=False)]
if pending_names:
    task_to_complete = st.selectbox("Select a task to complete", pending_names)
    if st.button("Mark complete"):
        next_task = scheduler.complete_task(task_to_complete)
        if next_task is not None:
            st.success(
                f"'{task_to_complete}' marked done! "
                f"Next occurrence scheduled for **{next_task.due_date}**."
            )
        else:
            st.success(f"'{task_to_complete}' marked done (one-off task — no recurrence).")
else:
    st.info("No pending tasks to complete.")

st.divider()

# ── Generate Schedule ─────────────────────────────────────────────────────────
st.subheader("Daily Schedule")

if st.button("Generate schedule"):
    schedule = scheduler.generate_schedule()
    explanations = scheduler.explain_schedule()

    if not schedule:
        st.warning("No pending daily tasks to schedule.")
    else:
        feasible = scheduler.is_schedule_feasible()
        avail = scheduler.owner.available_hours_per_day
        if feasible:
            st.success(f"All pending tasks fit within your {avail}h daily budget.")
        else:
            st.error(
                f"Tasks exceed your {avail}h daily budget — "
                "lower-priority tasks have been dropped from the schedule below."
            )

        # Schedule timeline
        st.markdown("**Today's plan:**")
        start_hour = scheduler.start_hour
        time_elapsed = 0
        for idx, task in enumerate(schedule, 1):
            total_start = start_hour * 60 + time_elapsed
            total_end = total_start + task.duration
            s_h, s_m = divmod(total_start, 60)
            e_h, e_m = divmod(total_end, 60)
            pet_label = task.pet.name if task.pet else "—"
            priority_stars = "⭐" * task.priority
            st.markdown(
                f"**{idx}. {s_h:02d}:{s_m:02d} – {e_h:02d}:{e_m:02d}** &nbsp; "
                f"{task.name} &nbsp;|&nbsp; {pet_label} &nbsp;|&nbsp; "
                f"{task.duration} min &nbsp;|&nbsp; {priority_stars}"
            )
            time_elapsed += task.duration

        total_h, total_m = divmod(time_elapsed, 60)
        st.markdown(f"**Total scheduled time:** {total_h}h {total_m}m")

        # Reasoning expander
        if explanations:
            with st.expander("Why was each task chosen or skipped?"):
                for line in explanations:
                    if "chosen" in line:
                        st.success(line)
                    else:
                        st.warning(line)
