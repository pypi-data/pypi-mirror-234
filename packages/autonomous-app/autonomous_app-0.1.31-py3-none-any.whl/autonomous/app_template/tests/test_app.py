import sys

from app.models.model import Model

from autonomous import log


class ChildModel(Model):
    pass


class TestApp:
    def test_model(self):
        m = Model(name="test")
        m.save()
        log(m.pk)
        assert m.pk

    def test_child_model(self):
        m = ChildModel(name="test")
        m.save()
        assert m.table().name == "ChildModel"
        assert m.table().table.name == "ChildModel"
