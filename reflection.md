# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design. 
- What classes did you include, and what responsibilities did you assign to each?

The PawPal system includes four core classes:

Owner - Manages owner information and availability

    Stores name, available hours per day, and preferences
    Responsible for tracking how much time the owner has for pet care

Pet - Represents a single pet with its characteristics

    Stores name, species, age, breed, and special needs
    Responsibility is to maintain pet profile data

Task - Represents individual care tasks (walk, feed, medication, etc.)

    Stores task name, duration (minutes), priority level (1-5), and frequency (daily, weekly, etc.)
    Responsible for determining if task is high priority and if it's needed today

Scheduler - The main coordination engine

    Links together an Owner, Pet, and list of Tasks
    Responsible for generating feasible daily schedules, ranking tasks by priority, and checking if all tasks fit within available time

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---
Yes, the design changed during implementation to address missing relationships and performance issues:

1. Owner → Multiple Pets (One-to-Many)

Previously, there was only one to one relationship between owner and pet but now there is one to many relationship as one owner can own many pets. 


## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?


The scheduler considers three constraints: available time (owner's daily hour budget), task priority (1–5 scale), and frequency (daily vs. weekly). Priority was treated as most important because a pet's medication or walk can't be skipped the way grooming can — so high-priority tasks are always scheduled first, and lower-priority tasks are dropped when time runs out via the greedy cap.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?


The greedy time-cap sorts by priority and fills the schedule top-down until the budget is exhausted. This can leave short low-priority tasks unscheduled even when they would physically fit after rearranging. For example, a 5-minute task might get dropped because a 30-minute high-priority task ahead of it consumed the last available slot. This is reasonable here because pet care priorities are genuine (medication matters more than play), and the simplicity of the greedy approach means the schedule is predictable and explainable to the owner — which explain_schedule() surfaces directly.

---



## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI tools for almost all the tasks. If I did not understand the syntax or any part of code, I was using at as Insctructor. I used it mainly for the coding part. 

- What kinds of prompts or questions were most helpful?
The prompts conatainng clear breakdown of tasks were most helpful. 


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I mostly accepted the AI suggestion but was reviewing them thoroughly. I evaluted them by reading the code and understanding the logic myself before pasting them. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
Sorting correctness — tasks return in chronological HH:MM order regardless of insertion order
Daily recurrence — completing a daily task auto-creates the next occurrence due the following day
Conflict detection — overlapping time slots are flagged with a warning
Task completion status — mark_completed() flips the task state correctly
Task count — add_task() grows the scheduler's list as expected
No false conflicts — back-to-back tasks (one ends exactly when the next starts) produce zero warnings

- Why were these tests important?
These three behaviors — sorting, recurrence, and conflict detection — are the core of the scheduling engine. If sorting is wrong, the owner sees tasks out of order. If recurrence breaks, daily care silently disappears after the first completion. If conflict detection misfires, two tasks get scheduled at the same time with no warning, which is the exact problem the feature exists to prevent.

**b. Confidence**

- How confident are you that your scheduler works correctly?
4/5 — all six tests pass and the happy paths for the main algorithms are covered. The core logic is reliable for normal daily use.

- What edge cases would you test next if you had more time?
I would test
-- a task with duration = 0 or a very long task that exceeds the daily budget. 
-- genereat_schedule() when avaliable_hours_per_day = 0 .
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I was satisfied with how the guidances to proceed on this project were clearly provided and broken down into managebl steps.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteration, I would chanage the UI and make its frontend more robust.
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned how AI can be like a partner or teammate while working on any project. 
