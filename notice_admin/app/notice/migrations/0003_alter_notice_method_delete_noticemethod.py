from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0002_alter_noticetemplate_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='method',
            field=models.CharField(choices=[('email', 'Email'), ('push', 'Push'), ('sms', 'Sms')], max_length=50, verbose_name='method'),
        ),
        migrations.DeleteModel(
            name='NoticeMethod',
        ),
    ]
