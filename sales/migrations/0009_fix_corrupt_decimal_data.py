from django.db import migrations


def fix_corrupt_decimals(apps, schema_editor):
    """Replace empty-string values stored in DecimalFields with 0."""
    with schema_editor.connection.cursor() as cursor:
        tables_and_fields = {
            'sales_saleitem': ['unit_price', 'discount_percent', 'discount_amount', 'tax_amount', 'subtotal', 'original_price'],
            'sales_payment': ['amount'],
            'sales_salereturnitem': ['unit_price', 'subtotal'],
            'sales_creditrecord': ['credit_amount', 'amount_paid', 'remaining_balance'],
        }
        for table, fields in tables_and_fields.items():
            for field in fields:
                cursor.execute(
                    f"UPDATE {table} SET {field} = 0 WHERE {field} = ''"
                )


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_alter_creditrecord_credit_amount_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_corrupt_decimals, reverse),
    ]
