"""
Seed the Tanzanian Essential Medicines List (EML) medicines as products
grouped by therapeutic category, then create completed purchase orders to
purchase stock for each medicine (mirroring the app's PO-completion logic:
stock increment + StockMovement records).
"""
import random
from decimal import Decimal
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from inventory.models import Category, Product, StockMovement
from purchases.models import PurchaseOrder, PurchaseOrderItem

# category name -> (icon, [medicine names])
EML_SECTIONS = [
    ("Anaesthetics & Medical Gases", "fa-bed", [
        "Halothane", "Isoflurane", "Nitrous oxide", "Oxygen", "Sevoflurane",
        "Atropine", "Calcium chloride", "Clonidine", "Dexmedetomidine",
        "Ephedrine injection", "Flumazenil", "Etomidate", "Glycopyrrolate",
        "Ketamine", "Labetalol", "Lipid emulsion", "Metaraminol", "Midazolam",
        "Noradrenaline", "Ondansetron", "Phenylephrine", "Propofol",
        "Sodium citrate", "Thiopental",
        "Bupivacaine", "Lidocaine", "Lidocaine in Dextrose",
        "Lidocaine + epinephrine (adrenaline)",
        "Atracurium", "Baclofen", "Neostigmine", "Pancuronium", "Rocuronium",
        "Sugammadex", "Suxamethonium", "Tizanidine",
    ]),
    ("Pain & Palliative Care", "fa-tablets", [
        "Acetylsalicylic acid", "Dexketoprofen", "Diclofenac", "Ketoprofen",
        "Ibuprofen", "Mefenamic Acid", "Meloxicam", "Paracetamol", "Piroxicam",
        "Sulfasalazine",
        "Fentanyl", "Methadone", "Morphine", "Naloxone", "Pethidine", "Tramadol",
        "Amitriptyline", "Haloperidol", "Hydrocortisone", "Hyoscine butyl bromide",
        "Loperamide", "Imipramine",
    ]),
    ("Anti-allergies & Anaphylaxis", "fa-allergies", [
        "Betahistine", "Bethametasone", "Cetirizine", "Chlorpheniramine",
        "Desloratadine", "Dexamethasone", "Epinephrine (Adrenaline)",
        "Loratadine", "Promethazine",
    ]),
    ("Antidotes & Poisonings", "fa-flask", [
        "Charcoal, activated", "Magnesium sulfate",
        "Acetylcysteine", "Atropine", "Calcium gluconate", "Deferoxamine",
        "D-penicillamine", "Dimercaprol",
        "Ethylenediaminetetra-acetic acid (EDTA)", "Flumazenil",
        "Pralidoxime", "Sodium bicarbonate 8.4%", "Sugammadex", "Succimer",
    ]),
    ("Anticonvulsants & Antiepileptics", "fa-brain", [
        "Carbamazepine", "Clonazepam", "Diazepam", "Lamotrigine",
        "Levetiracetam", "Lorazepam", "Magnesium sulfate", "Phenobarbital",
        "Phenytoin", "Pregabalin", "Sodium Valproate",
    ]),
    ("Anti-Infectives", "fa-bacteria", [
        "Albendazole", "Mebendazole", "Ivermectin", "Praziquantel",
        "Ampicillin", "Ampicillin + cloxacillin", "Amoxicillin",
        "Amoxicillin + Clavulanic acid", "Benzathine benzyl penicillin",
        "Benzyl Penicillin", "Cephalexin", "Cloxacillin", "Doxycycline",
        "Erythromycin", "Flucloxacillin + Amoxicillin", "Flucloxacillin",
        "Metronidazole", "Nitrofurantoin", "Phenoxymethylpenicillin",
        "Tetracycline", "Oxytetracycline",
        "Ampicillin + Sulbactam", "Azithromycin", "Clarithromycin",
        "Chloramphenicol", "Ceftriaxone", "Ceftriaxone + sulbactam",
        "Ciprofloxacin", "Gentamicin", "Piperacillin + tazobactam",
        "Sulfamethoxazole + trimethoprim", "Ceftazidime", "Cefixime", "Cefuroxime",
        "Amikacin", "Cefepime", "Clindamycin", "Colistin", "Dapsone",
        "Meropenem", "Vancomycin",
        "Clofazimine", "Dapsone", "Rifampicin",
        "Ethambutol", "Ethambutol + Isoniazid", "Ethionamide", "Isoniazid",
        "Pyrazinamide", "Rifampicin + Isoniazid",
        "Rifampicin + Isoniazid + Pyrazinamide + Ethambutol",
        "Cycloserine", "Bedaquiline", "Capreomycin", "Delamanid", "Kanamycin",
        "Levofloxacin", "Linezolid", "Moxifloxacin", "p-Amino salicylic acid (PAS)",
        "Amphotericin B", "Clotrimazole", "Fluconazole", "Flucytosine",
        "Griseofulvin", "Itraconazole", "Miconazole", "Nystatin", "Terbinafine",
        "Acyclovir", "Valganciclovir",
        "Abacavir (ABC)", "Lamivudine (3TC)", "Tenofovir disoproxil fumarate (TDF)",
        "Zidovudine (AZT)", "Efavirenz (EFV)", "Nevirapine (NVP)", "Atazanavir",
        "Atazanavir + Ritonavir", "Lopinavir + Ritonavir (LPV/r)", "Ritonavir",
        "Darunavir", "Raltegravir", "Abacavir / Lamivudine",
        "Tenofovir / Emtricitabine", "Tenofovir / Emtricitabine / Efavirenz",
        "Tenofovir / Lamivudine / Efavirenz",
        "Tenofovir / Lamivudine / Dolutegravir", "Zidovudine / Lamivudine",
        "Zidovudine / Lamivudine / Nevirapine", "Isoniazid", "Pyridoxine",
        "Sulfamethoxazole + trimethoprim",
        "Entecavir", "Tenofovir disoproxil fumarate (TDF)", "Ledipasvir",
        "Ribavirin", "Sofosbuvir",
        "Metronidazole", "Tinidazole", "Artemether / Lumefantrine (ALU)",
        "Artemether", "Artesunate", "Dihydroartemisinin + Piperaquine (DPQ)",
        "Primaquine", "Sulfadiazine", "Pyrimethamine",
        "Sulfadoxine + Pyrimethamine",
    ]),
    ("Antimigraine Medicines", "fa-head-side-virus", [
        "Acetylsalicylic acid", "Ibuprofen", "Ergotamine tartarate", "Propranolol",
    ]),
    ("Antineoplastics & Immunosuppressives", "fa-dna", [
        "5-Fluorouracil", "Abiraterone acetate", "Actinomycin D", "Alfuzosin",
        "Allopurinol", "Anastrozole", "Antithymocyte globulin (ATG)",
        "Azacitidine", "Azathioprine", "Basiliximab", "Bicalutamide",
        "Bleomycin", "Bortezomib", "Capecitabine", "Carboplatin",
        "Chlorambucil", "Cisplatin", "Cyclophosphamide", "Cyclosporine",
        "Dacarbazine", "Danazol", "Docetaxel", "Doxorubicin", "Dutasteride",
        "Etoposide", "Everolimus", "Febuxostat", "Filgrastim", "Finasteride",
        "Folinic acid", "Gemcitabine", "Goserelin", "Hydroxychloroquine",
        "Hydroxyurea", "Ifosfamide", "Imatinib", "Irinotecan", "Lenalidomide",
        "Leucovorin", "Mesna", "Methotrexate", "Mycophenolate Sodium",
        "Mycophenolate Mofetil", "Oxaliplatin", "Paclitaxel", "Rituximab",
        "Sirolimus", "Tacrolimus", "Tamsulosin", "Tamoxifen", "Temozolomide",
        "Thalidomide", "Trastuzumab", "Vinblastine", "Vincristine",
        "Zoledronic acid",
    ]),
    ("Hormones & Antihormones", "fa-staff-snake", [
        "Betamethasone", "Dexamethasone", "Hydrocortisone", "Methylprednisolone",
        "Metyrapone", "Prednisolone", "Triamcinolone",
        "Ethinyloestradiol", "Clomiphene",
        "Dydrogesterone", "Etonogestrel", "Levonorgestrel",
        "Medroxyprogesterone", "Norethisterone",
        "Testosterone",
        "Ethinyloestradiol + Norgestrel", "Ethinylestradiol + Levonorgestrel",
        "Ethinylestradiol + Desogestrel",
        "Carbimazole", "Potassium Iodide Solution", "Levothyroxine",
        "Iodized oil", "Propylthiouracil",
    ]),
    ("Antiparkinsonism", "fa-person-walking", [
        "Benzhexol", "Bromocriptine", "Cabergoline", "Levodopa / Carbidopa",
        "Selegiline",
    ]),
    ("Blood & Coagulation", "fa-droplet", [
        "Erythropoietin", "Ferrous", "Ferrous salts", "Folic acid",
        "Hydroxocobalamin (Vitamin B12)",
        "Desmopressin", "Etamsylate", "Low molecular Weight heparin",
        "Phytomenadione (Vit K1)", "Protamine sulfate", "Rivaroxaban",
        "Unfractionated Heparin Sodium", "Tranexamic acid", "Warfarin",
    ]),
    ("Blood Products & Plasma Substitutes", "fa-droplet", [
        "Fresh frozen plasma (FFP)", "Platelets", "Red blood cells", "Whole blood",
        "Anti-rabies immunoglobulin", "Anti-tetanus immunoglobulin",
        "Human Immunoglobulin G", "Eltrombopag", "Factor VIII concentrate",
        "Factor IX concentrate",
        "Albumin", "Polygeline",
    ]),
    ("Cardiovascular", "fa-heart-pulse", [
        "Bisoprolol", "Glyceryl trinitrate", "Isosorbide Dinitrate", "Labetalol",
        "Nifedipine", "Nitroglycerin", "Propranolol",
        "Adenosine", "Amiodarone", "Sotalol", "Verapamil",
        "Amlodipine", "Atenolol", "Candesartan", "Captopril", "Carvedilol",
        "Clonidine", "Diltiazem", "Doxazosin", "Enalapril", "Esmolol",
        "Hydralazine", "Irbesartan", "Lisinopril", "Losartan", "Nimodipine",
        "Methyldopa", "Metolazone", "Metoprolol", "Telmisartan",
        "Candesartan", "Dobutamine", "Dopamine", "Digoxin", "Ivabradine",
        "Furosemide", "Eplerenone", "Bendrofluazide", "Hydrochlorothiazide",
        "Mannitol", "Spironolactone", "Torsemide",
        "Acetylsalicylic acid", "Clopidogrel", "Prasugrel", "Ticagrelor",
        "Alteplase", "Streptokinase",
        "Atorvastatin", "Fenofibrate", "Rosuvastatin",
    ]),
    ("Dermatological", "fa-hand", [
        "Benzoic acid Compound (Whitfield's)", "Clotrimazole", "Miconazole",
        "Terbinafine",
        "Fusidic acid", "Gentian Violet", "Mupirocin", "Potassium permanganate",
        "Povidone iodine", "Silver Sulfadiazine",
        "Betamethasone", "Calamine", "Clobetasol propionate", "Fludrocortisone",
        "Hydrocortisone", "Mometasone furoate", "Triamcinolone",
        "All-trans-retinoic acid (ATRA)", "Benzoyl peroxide", "Coal tar",
        "Isotretinoin", "Podophyllin Solution", "Salicylic acid",
        "Silver nitrate pencil", "Tretinoin cream",
        "Benzyl benzoate Emulsion", "Lindane",
        "Sunscreen protecting factor (SPF 30+)",
    ]),
    ("Gastro-Intestinal", "fa-stomach", [
        "Antacid Mixture", "Bismuth Subgallate", "Esomeprazole", "Lansoprazole",
        "Magnesium trisilicate", "Mesalazine", "Octreotide", "Omeprazole",
        "Pantoprazole", "Terlipressin",
        "Cholestyramine", "Hyoscine butylbromide", "Infliximab", "Mebeverine",
        "Pancreatic Enzyme Supplement", "Ursodeoxycholic acid",
        "Domperidone", "Doxylamine", "Metoclopramide", "Promethazine",
        "Ondansetron",
        "Bisacodyl", "Lactulose", "L-Ornithine L-Aspartate",
        "Local anaesthetic + astringent and anti-inflammatory",
        "Loperamide", "Oral Rehydration Salts (ORS)", "Zinc",
    ]),
    ("Diabetes & Insulin", "fa-droplet", [
        "Empagliflozin", "Glibenclamide", "Gliclazide", "Glimepiride",
        "Glucagon", "Insulin", "Metformin", "Pioglitazone",
        "Phenoxybenzamine", "Sitagliptin",
    ]),
    ("Immunologicals & Vaccines", "fa-syringe", [
        "Anti D immunoglobulin", "Antirabies immune globulin",
        "Anti-venom immunoglobulin", "Diphtheria antitoxin",
        "Tetanus Immunoglobulin",
        "BCG Vaccine", "DPT-HepB-Hib Vaccine", "Hepatitis B Vaccine",
        "Human Papilloma Vaccine (HPV)", "Inactivated Polio Vaccine (IPV)",
        "Measles-Rubella Vaccine", "Oral Poliomyelitis Vaccine (OPV)",
        "Pneumococcal Conjugate Vaccine (PCV13)",
        "Pneumococcal polysaccharide vaccine (PPSV-23)", "Rota Vaccine",
        "Tetanus (toxoid) Vaccine",
        "Human Diploid Cell Rabies Freeze dried rabies vaccine",
        "Meningitis vaccine", "Yellow Fever Vaccine",
    ]),
    ("Ophthalmological", "fa-eye", [
        "Acyclovir ointment", "Ciprofloxacin", "Chloramphenicol",
        "Chlorhexidine", "Dexamethasone + Chloramphenicol",
        "Dexamethasone + Gentamicin", "Econazole", "Natamycin", "Ofloxacin",
        "Oxytetracycline", "Iodine",
        "Dexamethasone eye drops", "Hydroxypropylmethylcellulose",
        "Methylprednisolone acetate", "Prednisolone eye drops",
        "Oxymetazoline", "Sodium cromoglycate drops", "Triamcinolone Acetonide",
        "Amethocaine eye drops", "Tetracaine eye drops",
        "Acetazolamide", "Acetylcholine", "Betaxolol", "Brimonidine",
        "Dorzolamide", "Latanoprost", "Pilocarpine hydrochloride",
        "Prostamide bimatoprost", "Timolol",
        "Atropine", "Cyclopentolate", "Tropicamide",
        "Tropicamide with Cyclopentolate", "Tropicamide with Phenylephrine",
        "5-Fluorouracil", "Ganciclovir", "Mitomycin C", "Silicon Oil",
    ]),
    ("Oxytocics", "fa-person-pregnant", [
        "Ergometrine Injection", "Misoprostol", "Oxytocin Injection",
        "Dicyclomine", "Nifedipine", "Salbutamol Tablet",
    ]),
    ("Dialysis Solutions", "fa-filter", [
        "Iron Sucrose", "Intraperitoneal dialysis solution",
    ]),
    ("Psychotherapeutic", "fa-brain", [
        "Benzhexol", "Chlorpromazine", "Donepezil", "Fluphenazine",
        "Haloperidol", "Lorazepam", "Olanzapine", "Risperidone",
        "Zuclopenthixol",
        "Amitriptyline", "Citalopram", "Fluoxetine", "Imipramine",
        "Oxybutynin", "Carbamazepine", "Lamotrigine", "Sodium Valproate",
        "Diazepam",
        "Buprenorphine", "Methadone", "Naltrexone",
    ]),
    ("Respiratory", "fa-lungs", [
        "Budesonide inhaler", "Fluticasone propionate",
        "Ipratropium Bromide Aerosol", "Montelukast", "Salbutamol",
        "Salfolinl", "Tiotropium",
        "Cough syrup",
    ]),
    ("Solutions & Electrolytes", "fa-vial", [
        "Dextrose 5%", "Dextrose 10%", "Dextrose 25%", "Dextrose 50%",
        "Polystyrene sulfonate", "Sodium bicarbonate",
        "Sodium lactate compound (Ringer's solution)",
        "Sodium Chloride solution (0.9%)", "Sodium Chloride solution (3%)",
        "Sodium chloride + Dextrose", "Potassium chloride Solution",
        "Water for injection",
    ]),
    ("Vitamins & Minerals", "fa-pills", [
        "Ascorbic acid (Vitamin C)", "Calcium gluconate", "Calcium Carbonate",
        "Calcium with vitamins", "Calcium with amino acids",
        "Ergocalciferol (Vitamin D)", "Glucosamine + Chondroitin sulphate",
        "Iron with vitamins", "Iron with amino acid",
        "Nicotinamide (Vitamin B3)", "Potassium chloride",
        "Pyridoxine (Vitamin B6)", "Retinol (Vitamin A)",
        "Sodium Hyaluronate 1%", "Thiamine (Vitamin B1)",
        "Vitamin B complex", "Vitamin E",
    ]),
    ("Ear Nose & Throat", "fa-ear-listen", [
        "Betamethasone", "Boric acid", "Ciprofloxacin", "Clotrimazole",
        "Chloramphenicol", "Dexamethasone + Neomycin",
        "Lidocaine + Beclometasone + Clotrimazole + Chloramphenicol",
        "Chlorhexidine gluconate Solution", "Potassium permanganate Solution",
        "Ephedrine", "Normal saline", "Mometasone", "Xylometazoline",
    ]),
    ("Disinfectants & Antiseptics", "fa-spray-can", [
        "Chlorhexidine + Cetrimide", "Chloroxylenol", "Cresol saponated",
        "Formaldehyde", "Glutaraldehyde", "Hydrogen peroxide",
        "Methylated spirit", "Potassium permanganate", "Povidone-Iodine",
        "Sodium dichloroisocyanurate",
    ]),
    ("Miscellaneous", "fa-box-open", [
        "Sildenafil",
    ]),
]

CONTROLLED = {
    "fentanyl", "methadone", "morphine", "pethidine", "ketamine", "thiopental",
    "midazolam", "buprenorphine", "tramadol", "diazepam", "lorazepam",
    "phenobarbital", "nitrous oxide", "suxamethonium", "ergotamine tartarate",
    "morphine sulphate",
}

OTC = {
    "paracetamol", "ibuprofen", "acetylsalicylic acid", "mefenamic acid",
    "cetirizine", "loratadine", "chlorpheniramine", "desloratadine",
    "betahistine", "calamine", "sunscreen protecting factor (spf 30+)",
    "oral rehydration salts (ors)", "zinc", "ascorbic acid (vitamin c)",
    "vitamin b complex", "vitamin e", "retinol (vitamin a)",
    "thiamine (vitamin b1)", "pyridoxine (vitamin b6)",
    "nicotinamide (vitamin b3)", "cough syrup", "clotrimazole", "miconazole",
    "terbinafine", "benzoyl peroxide", "salicylic acid", "tretinoin cream",
    "coal tar", "benzoic acid compound (whitfield's)", "povidone iodine",
    "hydrogen peroxide", "methylated spirit", "boric acid", "chlorhexidine",
    "lactulose", "bisacodyl", "loperamide", "potassium chloride",
    "calcium carbonate", "ferrous salts", "folic acid",
}

HIGH_VALUE = {
    "vaccine", "immunoglobulin", "globulin", "factor viii", "factor ix",
    "albumin", "antithymocyte", "rituximab", "trastuzumab", "imatinib",
    "bortezomib", "lenalidomide", "amphotericin", "meropenem", "colistin",
    "vancomycin", "insulin", "erythropoietin", "filgrastim", "sofosbuvir",
    "ledipasvir", "bedaquiline", "delamanid", "thalidomide", "everolimus",
    "sirolimus", "tacrolimus", "mycophenolate", "infliximab", "basiliximab",
    "darunavir", "ritonavir", "atezanavir", "econazole", "natamycin",
    "mitomycin", "octreotide", "terlipressin", "ertapenem", "dabigatran",
}

SUPPLIERS = [
    "Rapid Africa Pharmaceuticals Ltd",
    "Zanif Pharma Distributors",
    "Medical Express (T) Ltd",
    "Geita Medical Supplies",
    "Swiss Pharma Tanzania",
    "MMI (Tanzania) Limited",
    "Shelys Pharmaceuticals",
    "Universal Corp Ltd",
]


def _pack_size(name, index):
    lower = name.lower()
    if any(k in lower for k in ("solution", "saline", "dextrose", "water for",
                                 "dialysis", "ringer", "spirit")):
        return "1000ml bottle", "bottle"
    if any(k in lower for k in ("syrup", "suspension", "drops", "emulsion",
                                "mixture", "mouthwash", "gargle")):
        return "100ml bottle", "bottle"
    if any(k in lower for k in ("ointment", "cream", "gel", "paste", "lotion")):
        return "30g tube", "tube"
    if any(k in lower for k in ("inhaler", "aerosol", "spray")):
        return "inhaler", "inhaler"
    if any(k in lower for k in ("vaccine", "injection", "vial", "concentrate",
                                "globulin", "antitoxin", "immunoglobulin",
                                "plasma", "cells", "platelets", "blood",
                                "ampoule", "infusion")):
        return "1 vial", "vial"
    if any(k in lower for k in ("tablet", "tablets")):
        return "100 tablets", "tablet"
    if "capsule" in lower:
        return "100 capsules", "capsule"
    if index % 3 == 0:
        return "100 tablets", "tablet"
    if index % 3 == 1:
        return "30 capsules", "capsule"
    return "50 tablets", "tablet"


class Command(BaseCommand):
    help = "Seed Tanzanian EML medicines as products and create purchase orders for them."

    def handle(self, *args, **options):
        random.seed(20260731)
        from django.contrib.auth import get_user_model

        User = get_user_model()
        created_by = User.objects.filter(is_superuser=True).first()

        today = timezone.localdate()
        created_products = 0
        existing_products = 0
        products_to_purchase = []  # (product, category_name)

        for cat_name, icon, meds in EML_SECTIONS:
            category, _ = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name), 'icon': icon,
                          'description': f'Tanzania Essential Medicines List - {cat_name}'},
            )
            for index, med_name in enumerate(meds):
                product = Product.objects.filter(name=med_name).first()
                if product:
                    existing_products += 1
                else:
                    price = self._price(med_name, index)
                    selling = (price * Decimal(random.choice(["1.30", "1.35", "1.40"]))).quantize(Decimal("0.01"))
                    pack, unit = _pack_size(med_name, index)
                    rx = self._prescription(med_name)
                    product = Product.objects.create(
                        name=med_name,
                        generic_name=med_name,
                        category=category,
                        product_type="medicine",
                        pack_size=pack,
                        purchase_price=price,
                        selling_price=selling,
                        wholesale_price=(price * Decimal("1.15")).quantize(Decimal("0.01")),
                        discount_percent=Decimal("0"),
                        vat_percent=Decimal("18"),
                        reorder_level=random.randint(5, 25),
                        reorder_quantity=random.randint(50, 200),
                        current_stock=0,
                        minimum_stock=10,
                        maximum_stock=999999999,
                        unit=unit,
                        prescription_required=rx,
                        is_controlled=rx == "controlled",
                        batch_number=f"EML{index + 1:04d}",
                        expiry_date=today + timedelta(days=random.randint(360, 900)),
                        manufacturing_date=today - timedelta(days=random.randint(30, 120)),
                        description=f"Tanzania EML: {med_name} ({cat_name})",
                        ingredients=med_name,
                        storage_conditions="Store below 25°C, protect from light and moisture",
                        is_active=True,
                        is_prescription=rx in ("prescription", "controlled"),
                    )
                    created_products += 1
                products_to_purchase.append((product, cat_name))

        self.stdout.write(self.style.SUCCESS(
            f"Products ready: {created_products} created, {existing_products} already existed, "
            f"{len(products_to_purchase)} to purchase."
        ))

        # Create purchase orders for the medicines (8 POs covering all of them)
        po_count = 8
        chunk_size = max(1, -(-len(products_to_purchase) // po_count))
        order_date = timezone.now().replace(hour=11, minute=0, second=0, microsecond=0)

        for chunk_index in range(po_count):
            chunk = products_to_purchase[chunk_index * chunk_size:(chunk_index + 1) * chunk_size]
            if not chunk:
                continue
            po = PurchaseOrder.objects.create(
                supplier_name=SUPPLIERS[chunk_index % len(SUPPLIERS)],
                order_date=order_date - timedelta(days=chunk_index),
                notes=f"EML restock batch {chunk_index + 1}",
                status="completed",
                created_by=created_by,
            )
            subtotal = Decimal("0")
            item_count = 0
            for product, _cat in chunk:
                qty = random.randint(50, 400)
                unit_price = (product.purchase_price or Decimal("0")).quantize(Decimal("0.01"))
                selling_price = (product.selling_price or unit_price * Decimal("1.3")).quantize(Decimal("0.01"))
                PurchaseOrderItem.objects.create(
                    purchase_order=po,
                    product=product,
                    quantity=qty,
                    unit_price=unit_price,
                    markup_percent=Decimal("30"),
                    selling_price=selling_price,
                    batch_number=f"PO{chunk_index + 1}B{qty:03d}",
                    expiry_date=product.expiry_date,
                    subtotal=(unit_price * qty).quantize(Decimal("0.01")),
                )
                subtotal += unit_price * qty

                previous_stock = product.current_stock
                product.current_stock += qty
                product.save(update_fields=["current_stock"])
                StockMovement.objects.create(
                    product=product,
                    movement_type="purchase",
                    quantity=qty,
                    previous_quantity=previous_stock,
                    new_quantity=product.current_stock,
                    unit_price=unit_price,
                    total_amount=unit_price * qty,
                    reference_type="PurchaseOrder",
                    reference_id=str(po.id),
                    created_by=created_by,
                    notes=f"PO {po.po_number} | EML restock batch {chunk_index + 1}",
                )
                item_count += 1

            po.subtotal = subtotal.quantize(Decimal("0.01"))
            po.total_amount = po.subtotal
            po.save(update_fields=["subtotal", "total_amount"])
            self.stdout.write(self.style.SUCCESS(
                f"  {po.po_number}: {item_count} items, TZS {po.total_amount:,.2f}"
            ))

        self.stdout.write(self.style.SUCCESS(
            f"Done. {PurchaseOrder.objects.filter(status='completed').count()} completed purchase orders total."
        ))

    def _price(self, name, index):
        lower = name.lower()
        if any(k in lower for k in HIGH_VALUE):
            return Decimal(random.randint(25000, 250000))
        if any(k in lower for k in ("injection", "infusion", "vial", "ampoule",
                                    "concentrate", "solution", "saline",
                                    "dextrose", "ringer", "water for")):
            return Decimal(random.randint(2000, 25000))
        return Decimal(random.randint(800, 15000))

    def _prescription(self, name):
        lower = name.lower().strip()
        if lower in CONTROLLED or any(c in lower for c in CONTROLLED):
            return "controlled"
        if lower in OTC:
            return "none"
        return "prescription"
