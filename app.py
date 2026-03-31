import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ── Session-state initialisation ──────────────────────────────────────────────
# Only create these objects once; Streamlit reruns on every interaction.
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
        # Keep the scheduler's primary pet set to the first pet added
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
st.subheader("Tasks")

priority_map = {"low": 1, "medium": 3, "high": 5}

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    new_task = Task(
        name=task_title,
        duration=int(duration),
        priority=priority_map[priority_label],
        frequency="daily",
    )
    # Associate the task with the first pet if one exists
    if pets:
        new_task.set_pet(pets[0])
    st.session_state.scheduler.add_task(new_task)
    st.success(f"Added task '{task_title}' ({duration} min, priority {priority_label}).")

all_tasks = st.session_state.scheduler.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table([
        {
            "Task": t.name,
            "Duration (min)": t.duration,
            "Priority": t.priority,
            "Pet": t.pet.name if t.pet else "—",
            "Done": t.is_completed(),
        }
        for t in all_tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate Schedule ─────────────────────────────────────────────────────────
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    schedule = st.session_state.scheduler.generate_schedule()
    if not schedule:
        st.warning("No pending daily tasks to schedule.")
    else:
        feasible = st.session_state.scheduler.is_schedule_feasible()
        if feasible:
            st.success("Schedule is feasible — all tasks fit within available time.")
        else:
            st.error("Schedule exceeds available time — consider removing lower-priority tasks.")

        time_elapsed = 0
        for idx, task in enumerate(schedule, 1):
            start_h, start_m = divmod(time_elapsed, 60)
            end_h, end_m = divmod(time_elapsed + task.duration, 60)
            pet_label = task.pet.name if task.pet else "—"
            st.markdown(
                f"**{idx}. [{start_h:02d}:{start_m:02d} – {end_h:02d}:{end_m:02d}]  {task.name}**  "
                f"| Pet: {pet_label} | {task.duration} min | Priority: {task.priority}/5"
            )
            time_elapsed += task.duration

        total_h, total_m = divmod(time_elapsed, 60)
        st.markdown(f"---\n**Total time:** {total_h}h {total_m}m")
