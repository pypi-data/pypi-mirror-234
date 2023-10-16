import time

import pytest
from tasks import errormocktask, longmocktask, mocktask, parametermocktask

from autonomous import log
from autonomous.tasks import AutoTasks


class TestAutoTasks:
    def test_autotask_connection(self):
        tasks = AutoTasks()
        tasks.clear()
        assert tasks._connection.ping()
        assert tasks.queue
        assert tasks.queue.job_ids == []

    def test_autotask_add(self):
        tasks = AutoTasks()
        tasks.clear()
        job = tasks.task(mocktask)
        assert job.id

    def test_autotask_get(self):
        tasks = AutoTasks()
        tasks.clear()
        job = tasks.task(mocktask)
        log(job.id)
        result = tasks.get_task(job.id)
        assert result

    def test_autotask_status(self):
        tasks = AutoTasks()
        tasks.clear()
        job = tasks.task(mocktask)
        result = job.status
        assert result

    def test_autotask_param(app):
        at = AutoTasks()
        task = at.task(parametermocktask, 1, 2, "hello", key="value")
        assert at.get_task(task.id)
        assert at.get_task(task.id)
        while task.status == "running":
            time.sleep(1)
            log(task.status)

    def test_autotask_result(app):
        at = AutoTasks()
        task = at.task(parametermocktask, 1, 2, "hello", key="value")
        assert at.get_task(task.id)
        while task.status in ["running", "queued"]:
            time.sleep(1)
            log(task.status)
        log(task.status)
        log(task.result)
        log(task.return_value)
        assert task.return_value == 3

    def test_autotask_long(app):
        at = AutoTasks()
        task = at.task(longmocktask)
        time.sleep(2)
        assert at.get_task(task.id)
        while task.status in ["running", "queued", "started"]:
            time.sleep(1)
        assert task.status == "finished"
        assert task.return_value == "success"

    def test_autotask_all(self):
        tasks = AutoTasks()
        tasks.clear()
        (tasks.task(mocktask, 5, i) for i in range(3))
        for t in tasks.get_tasks():
            assert t.return_value or t.status == "running"

    def test_error_task(app):
        at = AutoTasks()
        task = at.task(errormocktask)
        time.sleep(2)
        assert task.status == "failed"
        assert task.return_value == None
