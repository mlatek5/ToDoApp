import streamlit as st
from transformers import pipeline

# zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# categories
categories = ["Work", "Personal", "Chores", "Errands", "Fitness", "School"]

# start session
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

if "completed" not in st.session_state:
    st.session_state["completed"] = []

st.title("Smart To-Do List App 📝")
st.write("Input your tasks below, and the app will categorize them and allow you to check them off!")

# input
new_task = st.text_input("Add a new task:", "")
if st.button("Add Task"):
    if new_task.strip():
        result = classifier(new_task, categories)
        category = result["labels"][0]  
        st.session_state["tasks"].append({"task": new_task, "category": category, "completed": False})
        st.success(f"Task added and categorized as **{category}**!")
    else:
        st.warning("Please enter a valid task.")


# show tasks
st.subheader("Your To-Do List")
if st.session_state["tasks"]:
    for i, task in enumerate(st.session_state["tasks"]):
        completed = st.checkbox(f"[{task['category']}] {task['task']}", value=task["completed"], key=i)
        st.session_state["tasks"][i]["completed"] = completed
else:
    st.write("No tasks yet. Add some above!")

# progress bar
st.subheader("Progress")
total_tasks = len(st.session_state["tasks"])
completed_tasks = sum(task["completed"] for task in st.session_state["tasks"])
if total_tasks > 0:
    progress = completed_tasks / total_tasks
    st.progress(progress)
    st.write(f"{completed_tasks}/{total_tasks} tasks completed!")
else:
    st.write("No tasks to track progress.")

if st.button("Clear All Tasks"):
    st.session_state["tasks"] = []
    st.session_state["completed"] = []
    st.success("All tasks cleared!")

#python3 -m streamlit run app_todo.py
