import random
from faker import Faker
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tshirt_ecom.settings')
django.setup()
from products.models import Product, ProductVariant, ProductVariantImage
from django.core.files import File


def generate_product_data():
    sizes = ['S', 'M', 'L', 'XL']
    prices = [199, 299, 399, 699, 799]
    colors = [
        ("Red", "#FF0000"), ("Blue", "#0000FF"), ("Green", "#00FF00"),
        ("Black", "#000000"), ("White", "#FFFFFF"), ("Pink", "#FFC0CB"),
        ("Yellow", "#FFFF00"), ("Grey", "#808080"), ("Navy Blue", "#000080"),
        ("Lavender", "#E6E6FA")
    ]
    genders = ['Male', 'Female', 'Unisex']
    age_groups = ['Kids', 'Teens', 'Adults']

    product_names = [
        "Classic Boys T-Shirt", "Girls Floral Dress", "Teen Unisex Hoodie", "Adult Men's Formal Shirt",
        "Women's Casual Jeans", "Summer Shorts", "Denim Jacket", "Polo T-Shirt", "Track Pants", "Sweatshirt",
        "Sportswear Set", "Printed Kurti", "Winter Coat", "Rain Jacket", "Baby Romper",
        "Girls Skirt", "Boys Cargo Pants", "Graphic Tee", "Ankle Socks", "Woolen Sweater",
        "School Uniform", "Swimwear", "Yoga Pants", "Dungarees", "Party Dress", "Casual Top", "Sleeveless Tank",
        "Full Sleeve T-Shirt", "Jogger Pants", "Boys Blazer", "Girls Lehenga", "Boys Sherwani", "Capris", 
        "Harem Pants", "Shrug Jacket", "Dungaree Dress", "Tank Top", "Leggings", "Thermal Innerwear", 
        "Overcoat", "Zipper Hoodie", "Baby Sweater", "Rompers", "Culottes", "Crop Top"
    ]

    product_features = [
        "100% Cotton Fabric",
        "Breathable & Lightweight",
        "Soft and Comfortable Fit",
        "Durable Stitching",
        "Machine Washable",
        "Pre-shrunk Fabric to Reduce Shrinkage",
        "Eco-friendly Dyes",
        "Classic Crew Neck Design",
        "Wrinkle Resistant",
        "Tagless Label for Added Comfort"
    ]
    
    product_descriptions = [
        "Experience all-day comfort with this versatile t-shirt crafted from premium-quality fabric — perfect for daily wear or layering.",
        "A timeless essential for every wardrobe, this t-shirt blends soft fabric with a modern fit for unmatched comfort and style.",
        "Stay cool and stylish in this lightweight and breathable t-shirt designed for both casual and active lifestyles.",
        "Engineered with comfort and durability in mind, this t-shirt offers a smooth feel and long-lasting performance wash after wash.",
        "Crafted to suit every occasion, this t-shirt combines classic style with functional design — your go-to for effortless dressing."
    ]

    products_data = []

    for name in product_names:
        randomized_features = random.sample(product_features, k=random.randint(4, 7))
        product = {
            "product": {
                "name": name,
                "description": random.choice(product_descriptions),
                "tags": ", ".join(fake.words(nb=4)),
                "base_price": random.choice(prices),
                "features": "\n".join(randomized_features)
            },
            "variants": []
        }

        for _ in range(random.randint(3, 5)):
            color_name, color_code = random.choice(colors)
            price = random.choice(prices)

            discount_percentage = random.randint(5, 20)
            offer_price = price - int(price * (discount_percentage / 100))

            variant = {
                "size": random.choice(sizes),
                "color_name": color_name,
                "color_code": color_code,
                "gender": random.choice(genders),
                "age_group": random.choice(age_groups),
                "stock": random.randint(20, 100),
                "price": price,
                "offer_price": offer_price,
            }
            product["variants"].append(variant)

        products_data.append(product)

    return products_data

def add_product_data(data, img_file_paths):
    for entry in data:
        product_info = entry['product']
        variants = entry['variants']

        product = Product.objects.create(
            name=product_info['name'],
            description=product_info['description'],
            tags=product_info['tags'],
            base_price=product_info['base_price'],
            features=product_info['features']
        )
        for variant in variants:
            product_variant = ProductVariant.objects.create(
                product=product,
                size=variant['size'],
                color_name=variant['color_name'],
                color_code=variant['color_code'],
                gender=variant['gender'],
                age_group=variant['age_group'],
                stock=variant['stock'],
                price=variant['price'],
                offer_price=variant.get('offer_price')
            )

            img_paths = random.sample(img_file_paths, k=random.randint(3, 7))
            for img_path in img_paths:
                with open(img_path, 'rb') as img_file:
                    ProductVariantImage.objects.create(
                        variant=product_variant,
                        image=File(img_file, name=os.path.basename(img_path)),
                        alt_text=f"{product.name} - {variant['color_name']}"
                    )

if __name__ == '__main__':
    fake = Faker()
    img_dir = 'C:/Users/ajayv/Downloads/tshirt-imgs'
    img_files = os.listdir(img_dir)
    img_file_paths = [os.path.join(img_dir, file) for file in img_files]
    data = generate_product_data()
    add_product_data(data, img_file_paths)
