from django.db import migrations


def update_testowner_role(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('accounts', 'UserProfile')

    try:
        user = User.objects.get(username='testowner')
        UserProfile.objects.filter(user=user).update(role='OWNER')
    except User.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            update_testowner_role,
            migrations.RunPython.noop
        ),
    ]