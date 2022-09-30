from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notice', '0002_alter_noticetemplate_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('enabled', models.BooleanField(verbose_name='enabled')),
                ('auto', models.BooleanField(verbose_name='auto subscription')),
                ('frequency', models.CharField(choices=[('dayly', 'dayly'), ('weekly', 'weekly'), ('monthly', 'monthly'), ('yearly', 'yearly')], max_length=50, verbose_name='frequency')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notice.noticetemplate', verbose_name='template')),
            ],
            options={
                'verbose_name': 'subscription',
                'verbose_name_plural': 'subscriptions',
                'db_table': 'notice_subscription',
            },
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user_id', models.UUIDField(editable=False)),
                ('enabled', models.BooleanField(verbose_name='enabled')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='subscription.subscription', verbose_name='subscription')),
            ],
            options={
                'verbose_name': 'user subscription',
                'verbose_name_plural': 'users subscriptions',
                'db_table': 'notice_user_subscription',
            },
        ),
        migrations.AddConstraint(
            model_name='usersubscription',
            constraint=models.UniqueConstraint(fields=('user_id', 'subscription'), name='user_subscription_idx'),
        ),
    ]
