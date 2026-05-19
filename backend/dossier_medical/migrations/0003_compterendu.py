from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dossier_medical', '0002_initial'),
        ('rendezvous', '0001_initial'),
        ('medecins', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompteRendu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observations', models.TextField(blank=True)),
                ('diagnostic', models.TextField(blank=True)),
                ('recommandations', models.TextField(blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('medecin', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='comptes_rendus',
                    to='medecins.medecin',
                )),
                ('rendezvous', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='compte_rendu',
                    to='rendezvous.rendezvous',
                )),
            ],
            options={
                'verbose_name': 'Compte-rendu',
                'verbose_name_plural': 'Comptes-rendus',
                'ordering': ['-date'],
            },
        ),
    ]
