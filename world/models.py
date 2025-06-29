from django.contrib.gis.db import models as gis_models
from django.db import models




class Announcement(models.Model):
    name = models.CharField(max_length=50)  # 公告名稱
    content = models.TextField()  # 公告內容
    created_at = models.DateTimeField(auto_now_add=True)  # 發布時間
    owner = models.CharField(max_length=50)  # 發佈人
    def __str__(self):
        return self.name

class catCoffee(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.


    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    rate = models.PositiveIntegerField()
    comments= models.CharField(max_length=100)
    location=gis_models.PointField(srid=3826)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="catCoffee"

class kaohsiung(models.Model):
    gid = models.AutoField(primary_key=True)
    townid = models.CharField(max_length=8, blank=True, null=True)
    towncode = models.CharField(max_length=12, blank=True, null=True)
    countyname = models.CharField(max_length=12, blank=True, null=True)
    townname = models.CharField(max_length=12, blank=True, null=True)
    geom = gis_models.GeometryField(blank=True, null=True)

    class Meta:
        db_table = 'kaohsiung'  # 請替換成實際的資料表名稱


