from django.db import migrations

def reset_ratings(apps, schema_editor):
    UserProfile = apps.get_model('authentication', 'UserProfile')
    UserProfile.objects.all().update(rating=0)

class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0002_alter_userprofile_rating'),
    ]

    operations = [
        migrations.RunPython(reset_ratings),
    ]
