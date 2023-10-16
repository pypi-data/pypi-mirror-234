def create_status(start_dt, finish_dt, success):
    if (start_dt and finish_dt and start_dt > finish_dt) \
            or (start_dt and finish_dt is None):
        return "in_progress"

    if success is False:
        return "failure"

    if success is True:
        return "success"


def create_msg(status, task_name):
    if status == "failure":
        return f"{task_name} failed."
