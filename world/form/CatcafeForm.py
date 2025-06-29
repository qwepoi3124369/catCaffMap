from django import forms
from world.models import catCoffee

class CatcafeForm(forms.ModelForm):
    class Meta:
        model = catCoffee
        fields = ['name','address', 'type', 'location', 'rate','comments']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px;'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px;'}),
            'type': forms.Select(
                choices=[
                    ('混合', '混合'),
                    ('短毛貓', '短毛貓'),
                    ('長毛貓', '長毛貓'),
                    ('波斯貓', '波斯貓'),
                    ('英國短毛貓', '英國短毛貓'),
                    ('美國短毛貓', '美國短毛貓'),
                    ('緬因貓', '緬因貓'),
                    ('俄羅斯藍貓', '俄羅斯藍貓'),
                    ('蘇格蘭折耳貓', '蘇格蘭折耳貓'),
                    ('布偶貓', '布偶貓'),
                    ('孟加拉貓', '孟加拉貓'),
                    ('加菲貓', '加菲貓'),
                    ('暹羅貓', '暹羅貓'),
                    ('埃及貓', '埃及貓'),
                    ('土耳其安哥拉貓', '土耳其安哥拉貓'),
                    ('挪威森林貓', '挪威森林貓'),
                    ('喜馬拉雅貓', '喜馬拉雅貓'),
                    ('狸花貓', '狸花貓'),
                    ('曼赤肯貓', '曼赤肯貓'),
                    ('無毛貓', '無毛貓'),
                    ('米克斯', '米克斯'),

                ],

            attrs={'class': 'form-control', 'style': 'width: 600px;'}
            ),
            'rate': forms.NumberInput(attrs={'id':'rate','class': 'form-control', 'style': 'width: 600px;display:none', 'min': '0'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 600px;'}),
        }
