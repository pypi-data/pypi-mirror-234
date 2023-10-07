# Generated by Django 2.2.27 on 2022-02-22 08:55

from django.db import migrations, models
import django.db.models.deletion
import djangocms_attributes_field.fields
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cms", "0022_auto_20180620_1551"),
    ]

    operations = [
        migrations.CreateModel(
            name="JetcodeConfig",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Name")),
                (
                    "options",
                    djangocms_attributes_field.fields.AttributesField(
                        blank=True, default=dict, verbose_name="Options"
                    ),
                ),
            ],
            options={
                "verbose_name": "Configuration",
                "verbose_name_plural": "Configurations",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Jetcode",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="djangocms_dag_jetcode_jetcode",
                        serialize=False,
                        to="cms.CMSPlugin",
                    ),
                ),
                (
                    "jetcode_type",
                    models.CharField(
                        choices=[
                            ("product", "Product"),
                            ("productselector", "Product selector"),
                            ("package", "Package"),
                        ],
                        max_length=20,
                        verbose_name="Type",
                    ),
                ),
                ("jetcode_id", models.IntegerField(verbose_name="Identifier")),
                (
                    "styles",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[],
                        max_length=100,
                        null=True,
                        verbose_name="Styles",
                    ),
                ),
                (
                    "configuration",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="djangocms_dag_jetcode.JetcodeConfig",
                        verbose_name="Configuration",
                    ),
                ),
            ],
            options={
                "verbose_name": "Jetcode",
                "verbose_name_plural": "Jetcodes",
            },
            bases=("cms.cmsplugin",),
        ),
    ]
