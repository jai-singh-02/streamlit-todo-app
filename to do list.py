import streamlit as st

class ToDoList:
    def __init__(self):
         st.title("📝 TO-DO LIST APP ",anchor='centre')

         if "name" not in st.session_state:
             st.session_state.name=""

         if "date" not in st.session_state:
              st.session_state.date = None

         if "task" not in st.session_state:
             st.session_state.task = {}
         if  "form_submit" not in st.session_state:
             st.session_state.form_submit=False

         if not st.session_state.form_submit:
             self.user_info()
         else:
             self.menu()

    def user_info(self):
        with st.form("user form"):
            name=st.text_input("enter name")
            date=st.date_input("enter date",)
            if st.form_submit_button("👍 continue"):
                if name:
                    st.session_state.name = name.strip()
                    st.session_state.date = date
                    st.session_state.form_submit = True
                    st.rerun()
                else:
                    st.error("🔴 fill all the feilds")

    def menu(self):
        with st.sidebar:
            st.subheader(f"Hi {st.session_state.name}")
            st.markdown(st.session_state.date)
            if st.button("Change name/date"):
                if "name" not in st.session_state:
                    st.session_state.name = ""

                if "date" not in st.session_state:
                    st.session_state.date = None

                if "task" not in st.session_state:
                    st.session_state.task = {}
                if "form_submit" not in st.session_state:
                    st.session_state.form_submit = False
                st.rerun()
            choice=st.selectbox("**Features**",["👀 View Task","➕ Add Task","❌ Delete Task","✔️ Mark as done"])
        if choice == "👀 View Task":
            self.view_task()
        elif choice=="➕ Add Task":
            self.add_task()
        elif choice=="✔️ Mark as done":
            self.mark_as_done()
        else:
            self.del_task()

    def view_task(self):
        st.subheader(f"**📄 YOUR TASKS**")
        st.markdown("---")
        high_col,med_col,low_col=st.columns(3)
        with high_col:
            st.markdown("<h4>📍High priority tasks</h4>",unsafe_allow_html=True)
            if "high" in  st.session_state.task:
                arr_high = st.session_state.task["high"]
                for ind, t in enumerate(arr_high, start=1):
                    st.markdown(f"<h5>{ind}. {t}</h5>", unsafe_allow_html=True)

        with med_col:
            st.markdown("<h5>📍Medium priority tasks</h5>",unsafe_allow_html=True)
            if "medium" in st.session_state.task:
                arr_med = st.session_state.task["medium"]
                for ind, t in enumerate(arr_med, start=1):
                    st.markdown(f"<h5>{ind} . {t}</h5", unsafe_allow_html=True)

        with low_col:
            st.markdown("<h4>📍Low priority tasks</h4>",unsafe_allow_html=True)
            if "low" in st.session_state.task:
                arr_low = st.session_state.task["low"]
                for ind, t in enumerate(arr_low, start=1):
                    st.markdown(f"<h5>{ind} . {t}</h5", unsafe_allow_html=True)


    def add_task(self):
        st.subheader("➕ Add task")
        with st.form("add task"):
            task=st.text_input("enter task")
            priority=st.radio("Select priority",["low","high","medium"],index=2)
            if st.form_submit_button("➕ Add"):
                if task:
                        if priority in st.session_state.task:
                            if task not in st.session_state.task[priority]:
                                st.session_state.task[priority].append(task)
                                st.success("Task Added Successfully")
                            else:
                                st.error(f"{task} is already added in list")
                        else:
                            st.session_state.task[priority] = [task]
                            st.success("🟢 Task Added Successfully")
                else:
                    st.error("🔴Enter a task")

    def del_task(self):
        st.subheader("❌ Delete Tasks")
        st.markdown("---")
        if st.session_state.task:
            st.markdown("<h4>📋Current tasks :</h4>", unsafe_allow_html=True)
            for k, v in (st.session_state.task.items()):
                st.write(f"**{k} priority tasks = {v}**")

            st.markdown("---")
            options = [f"{k} : {v}" for k in st.session_state.task for v in st.session_state.task[k]]
            del_tasks = st.multiselect("Select tasks", options)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Delete selected tasks", type="primary"):
                    if del_tasks:
                        for i in del_tasks:
                            k, v = i.split(":")
                            k = k.strip()
                            v = v.strip()
                            st.session_state.task[k].remove(v)
                        st.success("🟢 Delete successfully")
                    else:
                        st.error("Choose tasks")

            with col2:
                if st.button("Clear all tasks", type="secondary"):
                    st.session_state.task.clear()
                    st.success("🟢Clear successfully")
                    st.rerun()
        else:
            st.markdown("<h3> No tasks to delete </h3>",unsafe_allow_html=True)


    def mark_as_done(self):
        st.subheader("✅Mark completed tasks")

        if st.session_state.task:
            # Initialize completed tasks in session state
            if "completed_tasks" not in st.session_state:
                st.session_state.completed_tasks = []

            tasks_to_remove = []

            if "high" in st.session_state.task and st.session_state.task["high"]:
                st.markdown("<h4>High priority tasks</h4>", unsafe_allow_html=True)
                for i, task in enumerate(st.session_state.task["high"]):
                    if st.checkbox(f"{task}"):
                        tasks_to_remove.append(("high", task))

            if "medium" in st.session_state.task and st.session_state.task["medium"]:
                st.markdown("<h4>Medium priority tasks</h4>", unsafe_allow_html=True)
                for i, task in enumerate(st.session_state.task["medium"]):
                    if st.checkbox(f"{task}"):
                        tasks_to_remove.append(("medium", task))

            if "low" in st.session_state.task and st.session_state.task["low"]:
                st.markdown("<h4>Low priority tasks</h4>", unsafe_allow_html=True)
                for i, task in enumerate(st.session_state.task["low"]):
                    if st.checkbox(f"{task}"):
                        tasks_to_remove.append(("low", task))

            # Process completed tasks
            if tasks_to_remove:
                if st.button("✅Mark Selected as Done", type="primary"):
                    for priority, task in tasks_to_remove:
                        if task in st.session_state.task[priority]:
                            st.session_state.task[priority].remove(task)
                            st.session_state.completed_tasks.append(f"[{priority.upper()}] {task}")
                            st.success(f" {task} marked as done!")

                    # Clean up empty priority lists
                    for priority in ["high", "medium", "low"]:
                        if priority in st.session_state.task and not st.session_state.task[priority]:
                            del st.session_state.task[priority]

                    st.rerun()

            # Show completed tasks
            if st.session_state.completed_tasks:
                st.markdown("---")
                st.markdown("<h4> Completed Tasks</h4>", unsafe_allow_html=True)
                for completed_task in st.session_state.completed_tasks:
                    st.markdown(f"~~{completed_task}~~")

        else:
            st.error("🔴NO tasks in list!")

ToDoList()





