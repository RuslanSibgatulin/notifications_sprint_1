from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NoticeMethod',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Method',
                'verbose_name_plural': 'Methods',
                'db_table': 'notice_method',
            },
        ),
        migrations.CreateModel(
            name='NoticeTemplate',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('content', models.TextField(verbose_name='content')),
            ],
            options={
                'verbose_name': 'Template',
                'verbose_name_plural': 'Templates',
                'db_table': 'notice_template',
            },
        ),
        migrations.CreateModel(
            name='NoticeTrigger',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Trigger',
                'verbose_name_plural': 'Triggers',
                'db_table': 'notice_trigger',
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('enabled', models.BooleanField(verbose_name='enabled')),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notice.noticemethod', verbose_name='method')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notice.noticetemplate', verbose_name='template')),
                ('trigger', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notice.noticetrigger', verbose_name='trigger')),
            ],
            options={
                'verbose_name': 'Notice',
                'verbose_name_plural': 'Notices',
                'db_table': 'notice',
            },
        ),
        migrations.RunSQL(
            sql="""
            INSERT INTO notice_trigger VALUES (gen_random_uuid(), 'registred');
            INSERT INTO notice_trigger VALUES (gen_random_uuid(), 'views');
            """,
            reverse_sql=""
        ),
    ]
