from django.db import migrations

def update_testadmin_role(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('accounts', 'UserProfile')

    try:
        user = User.objects.get(username='testadmin2')
        UserProfile.objects.filter(user=user).update(role='ADMIN')
    except User.DoesNotExist:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_update_testowner_role'),
    ]

    operations = [
        migrations.RunPython(
            update_testadmin_role,
            migrations.RunPython.noop
        ),
    ]