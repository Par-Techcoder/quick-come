# Generated by Django 5.1.3 on 2025-03-10 04:29

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('profile_photo_url', models.URLField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=10)),
                ('gender', models.IntegerField(blank=True, choices=[(1, 'MALE'), (2, 'FEMALE'), (3, 'OTHER')], null=True)),
                ('roles', models.IntegerField(blank=True, choices=[(1, 'ADMIN'), (2, 'END_USER'), (3, 'SUPER_ADMIN')], db_default=2, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(blank=True, max_length=128, null=True)),
                ('is_staff', models.BooleanField(blank=True, db_default=False)),
                ('is_superuser', models.BooleanField(blank=True, db_default=False)),
            ],
            options={
                'db_table': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_created=True)),
                ('vehicle_type', models.IntegerField(choices=[(1, 'BIKE'), (2, 'CAR'), (3, 'BOTH')])),
                ('current_location', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_user_bookings_created_users_id', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_user_bookings_users_id', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_user_bookings_updated_users_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bookings',
            },
        ),
        migrations.CreateModel(
            name='Garage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_created=True)),
                ('garage_name', models.CharField(max_length=50)),
                ('garage_image', models.URLField(blank=True, null=True)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=10)),
                ('vehicle_type', models.IntegerField(choices=[(1, 'BIKE'), (2, 'CAR'), (3, 'BOTH')])),
                ('garage_ac', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_user_garage_create_users_id', to=settings.AUTH_USER_MODEL)),
                ('garage_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_user_garage_users_id', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_user_garage_update_users_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'garages',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_created=True)),
                ('type', models.IntegerField(blank=True, choices=[(1, 'CASH'), (2, 'CARD'), (3, 'ONLINE')], null=True)),
                ('bank_ac', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pay_status', models.IntegerField(choices=[(1, 'PENDING'), (2, 'COMPLETE'), (3, 'FAILED')])),
                ('paid_at', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_booking_payments_bookings_id', to='qcome.booking')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_user_payments_users_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'payments',
            },
        ),
        migrations.CreateModel(
            name='ServiceCatalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_created=True)),
                ('service_name', models.CharField(max_length=200)),
                ('service_image', models.URLField(blank=True, null=True)),
                ('spare_part', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_user_service_created_users_id', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_user_service_updated_users_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'services',
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qcome.servicecatalog'),
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_created=True)),
                ('experience', models.CharField(blank=True, max_length=15, null=True)),
                ('expertise', models.TextField(max_length=100)),
                ('is_verified', models.BooleanField(blank=True, default=False)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('garage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_garage_worker_garages_id', to='qcome.garage')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_user_worker_users_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'workers',
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_created=True)),
                ('final_work_image', models.URLField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'PENDING'), (2, 'IN_PROGRESS'), (3, 'COMPLETED'), (4, 'CANCELLED')], null=True)),
                ('work_photo_url', models.URLField(blank=True, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_bookig_work_bookings_id', to='qcome.booking')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_user_work_users_id', to=settings.AUTH_USER_MODEL)),
                ('work_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_worker_work_workers_id', to='qcome.worker')),
            ],
            options={
                'db_table': 'works',
            },
        ),
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.UniqueConstraint(condition=models.Q(('is_active', True)), fields=('customer',), name='unique_active_booking_per_user'),
        ),
    ]
