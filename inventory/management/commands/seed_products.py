from decimal import Decimal
from datetime import date, timedelta
import random

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from inventory.models import Category, Product


OTC_PRODUCTS = [
    ("Panadol Extra", "Paracetamol", "20 tablets", "tablet"),
    ("Panadol Extra", "Paracetamol", "50 tablets", "tablet"),
    ("Brufen 400mg", "Ibuprofen", "100 tablets", "tablet"),
    ("Ibuprofen 200mg", "Ibuprofen", "50 tablets", "tablet"),
    ("Aspirin 300mg", "Acetylsalicylic Acid", "100 tablets", "tablet"),
    ("Aspirin Cardio 100mg", "Acetylsalicylic Acid", "30 tablets", "tablet"),
    ("Diclofenac 50mg", "Diclofenac Sodium", "100 tablets", "tablet"),
    ("Voltaren Gel 75g", "Diclofenac Diethylamine", "75g tube", "tube"),
    ("Paracetamol Syrup 100ml", "Paracetamol", "100ml bottle", "bottle"),
    ("Paracetamol Syrup 60ml", "Paracetamol", "60ml bottle", "bottle"),
    ("Ibuprofen Syrup 100ml", "Ibuprofen", "100ml bottle", "bottle"),
    ("Amoxicillin 500mg", "Amoxicillin", "21 capsules", "capsule"),
    ("Amoxicillin Suspension 100ml", "Amoxicillin", "100ml bottle", "bottle"),
    ("Augmentin 625mg", "Amoxicillin/Clavulanate", "14 tablets", "tablet"),
    ("Ciprofloxacin 500mg", "Ciprofloxacin", "20 tablets", "tablet"),
    ("Azithromycin 500mg", "Azithromycin", "3 tablets", "tablet"),
    ("Doxycycline 100mg", "Doxycycline", "20 capsules", "capsule"),
    ("Metronidazole 400mg", "Metronidazole", "100 tablets", "tablet"),
    ("Flagyl Syrup 100ml", "Metronidazole", "100ml bottle", "bottle"),
    ("Co-trimoxazole 480mg", "Trimethoprim/Sulfamethoxazole", "20 tablets", "tablet"),
    ("Ceftriaxone 1g Injection", "Ceftriaxone", "1 vial", "vial"),
    ("Omeprazole 20mg", "Omeprazole", "30 capsules", "capsule"),
    ("Losec 20mg", "Omeprazole", "14 capsules", "capsule"),
    ("Ranitidine 150mg", "Ranitidine", "50 tablets", "tablet"),
    ("Ranitidine Syrup 100ml", "Ranitidine", "100ml bottle", "bottle"),
    ("Pantoprazole 40mg", "Pantoprazole", "30 tablets", "tablet"),
    ("Esmoprazole 20mg", "Esomeprazole", "28 capsules", "capsule"),
    ("Antacid Suspension 200ml", "Aluminium/Magnesium Hydroxide", "200ml bottle", "bottle"),
    ("Gaviscon 500ml", "Alginic Acid", "500ml bottle", "bottle"),
    ("Loperamide 2mg", "Loperamide", "20 capsules", "capsule"),
    ("Imodium 2mg", "Loperamide", "6 capsules", "capsule"),
    ("ORS Sachets", "Oral Rehydration Salts", "20 sachets", "sachet"),
    ("ORS Sachets Orange", "Oral Rehydration Salts", "10 sachets", "sachet"),
    ("Buscopan 10mg", "Hyoscine Butylbromide", "20 tablets", "tablet"),
    ("Dulcolax 5mg", "Bisacodyl", "20 tablets", "tablet"),
    ("Lactulose Syrup 200ml", "Lactulose", "200ml bottle", "bottle"),
    ("Senokot 7.5mg", "Senna", "20 tablets", "tablet"),
    ("Cetirizine 10mg", "Cetirizine", "30 tablets", "tablet"),
    ("Loratadine 10mg", "Loratadine", "30 tablets", "tablet"),
    ("Claritin 10mg", "Loratadine", "10 tablets", "tablet"),
    ("Chlorpheniramine 4mg", "Chlorphenamine", "100 tablets", "tablet"),
    ("Piriton 4mg", "Chlorphenamine", "30 tablets", "tablet"),
    ("Diphenhydramine Syrup 100ml", "Diphenhydramine", "100ml bottle", "bottle"),
    ("Piriton Syrup 100ml", "Chlorphenamine", "100ml bottle", "bottle"),
    ("Cortimoxazol 200mg", "Promethazine", "30 tablets", "tablet"),
    ("Promethazine Syrup 100ml", "Promethazine", "100ml bottle", "bottle"),
    ("Fexofenadine 120mg", "Fexofenadine", "30 tablets", "tablet"),
    ("Desloratadine 5mg", "Desloratadine", "30 tablets", "tablet"),
    ("Bisolvon Syrup 100ml", "Bromhexine", "100ml bottle", "bottle"),
    ("Ambroxol Syrup 100ml", "Ambroxol", "100ml bottle", "bottle"),
    ("Dextromethorphan Syrup 100ml", "Dextromethorphan", "100ml bottle", "bottle"),
    ("Benylin Syrup 100ml", "Diphenhydramine", "100ml bottle", "bottle"),
    ("Robitussin Syrup 100ml", "Guaifenesin", "100ml bottle", "bottle"),
    ("Mucinex 600mg", "Guaifenesin", "20 tablets", "tablet"),
    ("Paracetamol 500mg", "Paracetamol", "100 tablets", "tablet"),
    ("Pharcon 500mg", "Paracetamol", "100 tablets", "tablet"),
    ("Calpol Syrup 100ml", "Paracetamol", "100ml bottle", "bottle"),
    ("Kofein Syrup 100ml", "Chlorphenamine/Paracetamol", "100ml bottle", "bottle"),
    ("Vitamin C 500mg", "Ascorbic Acid", "100 tablets", "tablet"),
    ("Vitamin C Effervescent", "Ascorbic Acid", "20 tablets", "tablet"),
    ("Multivitamin Tablets", "Multivitamin", "100 tablets", "tablet"),
    ("Vitamin B Complex", "Vitamin B Complex", "100 tablets", "tablet"),
    ("Vitamin D3 1000IU", "Cholecalciferol", "60 tablets", "tablet"),
    ("Vitamin E 400IU", "Tocopherol", "60 capsules", "capsule"),
    ("Vitamin B12 1000mcg", "Cyanocobalamin", "30 tablets", "tablet"),
    ("Vitamin A 10000IU", "Retinol", "100 capsules", "capsule"),
    ("Zinc Sulphate 20mg", "Zinc", "30 tablets", "tablet"),
    ("Iron Tablets 200mg", "Ferrous Sulphate", "100 tablets", "tablet"),
    ("Folic Acid 5mg", "Folic Acid", "100 tablets", "tablet"),
    ("Calcium 500mg", "Calcium Carbonate", "100 tablets", "tablet"),
    ("Omega-3 Fish Oil", "Omega-3 Fatty Acids", "60 capsules", "capsule"),
    ("Cod Liver Oil", "Vitamin A/D", "100 capsules", "capsule"),
    ("Hydrocortisone Cream 15g", "Hydrocortisone", "15g tube", "tube"),
    ("Miconazole Cream 20g", "Miconazole Nitrate", "20g tube", "tube"),
    ("Clotrimazole Cream 20g", "Clotrimazole", "20g tube", "tube"),
    ("Fucidin Ointment 15g", "Fusidic Acid", "15g tube", "tube"),
    ("Bacitracin Ointment 15g", "Bacitracin", "15g tube", "tube"),
    ("Mupirocin Ointment 15g", "Mupirocin", "15g tube", "tube"),
    ("Silver Sulfadiazine Cream 25g", "Silver Sulfadiazine", "25g tube", "tube"),
    ("Ichthammol Ointment 30g", "Ichthammol", "30g tube", "tube"),
    ("Calendula Cream 50g", "Calendula", "50g tube", "tube"),
    ("Savlon Antiseptic 200ml", "Chlorhexidine/Cetrimide", "200ml bottle", "bottle"),
    ("Dettol Antiseptic 200ml", "Chloroxylenol", "200ml bottle", "bottle"),
    ("Hydrogen Peroxide 100ml", "Hydrogen Peroxide", "100ml bottle", "bottle"),
    ("Iodine Solution 30ml", "Povidone Iodine", "30ml bottle", "bottle"),
    ("Betadine 10% 30ml", "Povidone Iodine", "30ml bottle", "bottle"),
    ("Saline Solution 500ml", "Sodium Chloride", "500ml bottle", "bottle"),
    ("Nasal Saline Spray", "Sodium Chloride", "50ml spray", "spray"),
    ("Sodium Chloride 0.9%", "Sodium Chloride", "500ml bottle", "bottle"),
    ("Oral Rehydration Salts 5", "ORS", "5 sachets", "sachet"),
    ("Activated Charcoal 250mg", "Charcoal", "30 capsules", "capsule"),
    ("Domperidone 10mg", "Domperidone", "30 tablets", "tablet"),
    ("Metoclopramide 10mg", "Metoclopramide", "50 tablets", "tablet"),
    ("Famotidine 20mg", "Famotidine", "30 tablets", "tablet"),
    ("Rennie Tablets", "Calcium Carbonate", "24 tablets", "tablet"),
    ("Gaviscon Extra 500ml", "Alginic Acid", "500ml bottle", "bottle"),
    ("Bismuth Subsalicylate 262mg", "Bismuth Subsalicylate", "48 tablets", "tablet"),
    ("Diphenoxylate 2.5mg", "Diphenoxylate", "20 tablets", "tablet"),
    ("Nux Vomica 200ml", "Homeopathic", "200ml bottle", "bottle"),
    ("Acetaminophen 650mg", "Paracetamol", "100 tablets", "tablet"),
    ("Tramadol 50mg", "Tramadol", "30 tablets", "tablet"),
]


class Command(BaseCommand):
    help = "Seed 100 OTC medicine products into the inventory"

    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(
            name="Over-the-Counter Medicine",
            defaults={
                "slug": "otc-medicine",
                "description": "Over-the-counter medicines available without a prescription",
                "icon": "fas fa-pills",
            },
        )

        random.seed(42)
        today = date.today()
        created = 0
        for index, (name, generic, pack, unit) in enumerate(OTC_PRODUCTS):
            if index >= 100:
                break
            if Product.objects.filter(name=name, pack_size=pack).exists():
                self.stdout.write(self.style.WARNING(f"Skipping existing: {name}"))
                continue

            sku = f"OTC{index + 1:03d}"
            if Product.objects.filter(sku=sku).exists():
                sku = f"OTC{index + 1:03d}U{random.randint(10, 99)}"

            expiry = today + timedelta(days=random.randint(180, 900))
            stock = random.randint(20, 500)
            purchase = Decimal(random.randint(200, 2000)) + Decimal(random.randint(0, 99)) / 100
            markup = Decimal(random.choice(["1.25", "1.30", "1.35", "1.40"]))

            Product.objects.create(
                name=name,
                generic_name=generic,
                sku=sku,
                barcode=f"6{random.randint(10**11, 10**12 - 1)}",
                category=category,
                product_type="medicine",
                batch_number=f"B{index + 1:04d}",
                manufacturing_date=today - timedelta(days=random.randint(30, 200)),
                expiry_date=expiry,
                pack_size=pack,
                purchase_price=purchase,
                selling_price=(purchase * markup).quantize(Decimal("0.01")),
                wholesale_price=(purchase * Decimal("1.15")).quantize(Decimal("0.01")),
                discount_percent=Decimal(random.choice(["0", "0", "5", "10"])),
                vat_percent=Decimal("18"),
                reorder_level=random.randint(5, 25),
                reorder_quantity=random.randint(50, 200),
                current_stock=stock,
                minimum_stock=10,
                maximum_stock=10000,
                unit=unit,
                prescription_required="none",
                is_controlled=False,
                description=f"{name} ({pack}) - {generic} for over-the-counter use",
                ingredients=generic,
                dosage=random.choice(
                    ["Take as directed", "1 tablet 3 times daily after meals", "2 tablets twice daily", "5ml 3 times daily"]
                ),
                storage_conditions="Store below 25°C, protect from light and moisture",
                is_active=True,
                is_featured=index % 10 == 0,
                is_prescription=False,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} OTC products in category '{category.name}'"))
