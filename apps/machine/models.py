from django.db import models


class Machine(models.Model):
    name = models.CharField(max_length=255)
    machine_no = models.PositiveSmallIntegerField()
    status = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f'{self.machine_no}'

    class Meta:
        db_table = 'machine'


class MachineData(models.Model):
    machine_no = models.PositiveSmallIntegerField(db_index=True)
    machine_status = models.CharField(max_length=10)
    total_minutes = models.FloatField(default=5)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.machine_no}'

    class Meta:
        db_table = 'machine_data'
