from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticetemplate',
            name='content',
            field=models.TextField(help_text='Jinja template format', verbose_name='content'),
        ),
    ]
