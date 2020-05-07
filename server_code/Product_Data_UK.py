import anvil.stripe
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
products =  """Children's Items | Board Games / Puzzles
Children's Items | Exercise Books
Children's Items | Paper, lined
Children's Items | Paper, plain
Children's Items | Pencils
Children's Items | Pens
Children's Items | Story Books
Children's Items | Study Guides / Revision Aids /  Flash Cards
Children's Items | Toys
Drinks | Carbonated | Citrus Flavours
Drinks | Carbonated | Coca Cola / Pepsi
Drinks | Carbonated | Energy / Sports
Drinks | Carbonated | Ginger Beer / Ale
Drinks | Coffee | Coffee Beans
Drinks | Coffee | Filter Coffee
Drinks | Coffee | Instant Coffee
Drinks | Fruit Juice | Apple Juice
Drinks | Fruit Juice | Orange Juice
Drinks | Fruit Juice | Other Flavours
Drinks | Milk | Coconut / Soya etc.
Drinks | Milk | Flavoured Milk
Drinks | Tea | Herbal / Fruit Tea
Drinks | Tea | Tea Bags
Drinks | Water | Mineral Water (sparkling)
Drinks | Water | Mineral Water (still)
Essentials | Antidiarrhea
Essentials | Antihistamine
Essentials | Antiseptic Cream / Spray
Essentials | Aspirin
Essentials | Batteries
Essentials | Bread
Essentials | Butter / Margarine
Essentials | Candles
Essentials | Cold / Flu / Sinus Remedies
Essentials | Facemask
Essentials | Hand Sanitiser
Essentials | Ibuprofen
Essentials | Matches
Essentials | Milk
Essentials | Paracetamol
Essentials | Thermometer
Essentials | Throat Lozenges
Essentials | Toilet Paper
Food | Baby Food & Drink | Baby Food, 10 months and over
Food | Baby Food & Drink | Baby Food, 12 months and over
Food | Baby Food & Drink | Baby Food, 4 months and over
Food | Baby Food & Drink | Baby Food, 7 Months and over
Food | Baby Food & Drink | Baby Food, Desserts
Food | Baby Food & Drink | Baby Formula – Growing up
Food | Baby Food & Drink | Baby Formula, First milk
Food | Baby Food & Drink | Baby Formula, Follow on
Food | Baking | Baking Powder
Food | Baking | Bicarbonate Of Soda
Food | Baking | Corn Flour
Food | Baking | Lemon / Lime Juice
Food | Baking | Plain Flour
Food | Baking | Self-raising Flour
Food | Baking | Strong Bread Flour
Food | Baking | Sugar
Food | Baking | Yeast
Food | Condiments | Brown Sauce
Food | Condiments | Hot Sauce
Food | Condiments | Ketchup
Food | Condiments | Mayonnaise
Food | Condiments | Mustard
Food | Condiments | Soy Sauce
Food | Condiments | Vinegar
Food | Cooking Sauces | Bolognese
Food | Cooking Sauces | Chilli Con Carne
Food | Cooking Sauces | Curry
Food | Cooking Sauces | Pesto
Food | Cooking Sauces | Sweet and Sour
Food | Dairy | Cheese, Other
Food | Dairy | Cheese, Slices
Food | Dairy | Cream
Food | Dairy | Hard Cheese e.g. Cheddar
Food | Dairy | Ice-Cream
Food | Dairy | Soft Cheese
Food | Dairy | Yogurt (Flavoured)
Food | Dairy | Yogurt (Plain)
Food | Fruits | Apples
Food | Fruits | Avocados
Food | Fruits | Bananas
Food | Fruits | Blueberries
Food | Fruits | Cherries
Food | Fruits | Grapefruits
Food | Fruits | Grapes
Food | Fruits | Kiwis
Food | Fruits | Lemon/Limes
Food | Fruits | Melons
Food | Fruits | Nectarines
Food | Fruits | Oranges
Food | Fruits | Peaches
Food | Fruits | Pears
Food | Fruits | Plums
Food | Fruits | Raspberries
Food | Fruits | Strawberries
Food | Meats | Bacon
Food | Meats | Beef, Diced
Food | Meats | Beef, Halal
Food | Meats | Beef, Joint
Food | Meats | Beef, Kosher
Food | Meats | Beef, Minced
Food | Meats | Beef, Steak
Food | Meats | Chicken, Breast
Food | Meats | Chicken, Diced
Food | Meats | Chicken, Halal
Food | Meats | Chicken, Kosher
Food | Meats | Chicken, Thighs
Food | Meats | Chicken, Wings
Food | Meats | Frankfurter Sausages
Food | Meats | Ham
Food | Meats | Lamb, Chops
Food | Meats | Lamb, Diced
Food | Meats | Lamb, Halal
Food | Meats | Lamb, Joint
Food | Meats | Lamb, Kosher
Food | Meats | Lamb, Minced
Food | Meats | Pork Sausages
Food | Meats | Pork, Chops
Food | Meats | Pork, Diced
Food | Meats | Pork, Joint
Food | Ready Meals | Chinese
Food | Ready Meals | Chinese, Vegetarian 
Food | Ready Meals | Indian
Food | Ready Meals | Indian, Vegetarian
Food | Ready Meals | Meat / Fish and Pasta e.g. Spaghetti Bolognese
Food | Ready Meals | Meat / Fish and Rice e.g. Chilli Con Carne
Food | Ready Meals | Meat / Fish Soup
Food | Ready Meals | Meat Pizza
Food | Ready Meals | Rice and Vegetables
Food | Ready Meals | Thai
Food | Ready Meals | Thai, Vegetarian
Food | Ready Meals | Vegetable Soup
Food | Ready Meals | Vegetarian Pasta
Food | Ready Meals | Vegetarian Pizza
Food | Sandwich Spreads | Chocolate / Hazlenut Spread
Food | Sandwich Spreads | Jam / Marmalade
Food | Sandwich Spreads | Marmite / Vegemite
Food | Sandwich Spreads | Peanut Butter
Food | Seafood | Cod
Food | Seafood | Fish Fingers / Fish Cakes
Food | Seafood | Haddock
Food | Seafood | Mackerel
Food | Seafood | Plaice
Food | Seafood | Seabass
Food | Seafood | Shrimp / Prawns
Food | Seafood | Tuna
Food | Snacks | Biscuits
Food | Snacks | Cakes
Food | Snacks | Cereal / Energy Bars
Food | Snacks | Chocolate / Confectionery
Food | Snacks | Crisps, Meat Flavoured
Food | Snacks | Crisps, Vegetarian Flavoured
Food | Snacks | Fruit / Nuts
Food | Staples | Bagels
Food | Staples | Baked Beans
Food | Staples | Breakfast Cereal
Food | Staples | Gluten Free Bread
Food | Staples | Gravy/Stock/Bouillon
Food | Staples | Herbs
Food | Staples | Oats
Food | Staples | Olive/Sunflower/Vegetable Oil
Food | Staples | Pasta
Food | Staples | Pepper
Food | Staples | Pitta Bread
Food | Staples | Rice
Food | Staples | Salt
Food | Staples | Spices
Food | Staples | Tortilla Wraps
Food | Vegetables | Asparagus
Food | Vegetables | Aubergine
Food | Vegetables | Broccoli
Food | Vegetables | Carrots
Food | Vegetables | Cauliflower
Food | Vegetables | Celery
Food | Vegetables | Courgette
Food | Vegetables | Cucumbers
Food | Vegetables | Lettuce / Greens
Food | Vegetables | Mixed Veg
Food | Vegetables | Mushrooms
Food | Vegetables | Onions
Food | Vegetables | Peas
Food | Vegetables | Peppers
Food | Vegetables | Potatoes
Food | Vegetables | Spinach
Food | Vegetables | Squash
Food | Vegetables | Sweetcorn
Food | Vegetables | Tomatoes
Healthcare | Antiperspirant / Deodorant
Healthcare | Baby Lotion / Oil
Healthcare | Baby Pull-ups
Healthcare | Baby Wipes
Healthcare | Bandages / Dressings
Healthcare | Cotton Buds
Healthcare | Cotton Wool
Healthcare | Dental Floss
Healthcare | Indigestion / Antacid
Healthcare | Latex Gloves
Healthcare | Lip Balm
Healthcare | Moisturiser
Healthcare | Mouthwash
Healthcare | Nappies / 11kg to 22kg
Healthcare | Nappies / 13+ kg
Healthcare | Nappies / 2kg to 5kg
Healthcare | Nappies / 4kg to 9kg
Healthcare | Nappies / 7kg to 16kg
Healthcare | Nappy Bags
Healthcare | Plasters
Healthcare | Razor Blades
Healthcare | Shampoo / Conditioner
Healthcare | Shaving Foam / Gel
Healthcare | Soap / Shower Gel
Healthcare | Tampons / Sanitary Towels
Healthcare | Toothpaste
Healthcare | Vitamins / Supplements
Household Items | Air Freshener
Household Items | Aluminium Foil
Household Items | Baking Paper
Household Items | Bathroom Cleaner
Household Items | Bleach
Household Items | Dishwasher Soap / tablets
Household Items | Disinfectant
Household Items | Fabric Softner
Household Items | Garbage Bags
Household Items | Glass Cleaner
Household Items | Kitchen Cleaner
Household Items | Mop Heads / Vacuum Bags
Household Items | Napkins
Household Items | Paper Towels
Household Items | Plastic Wrap
Household Items | Sandwich / Freezer Bags
Household Items | Sponges / Scrubbers
Household Items | Toilet Cleaner
Household Items | Washing Powder / Liquid
Household Items | Washing Up liquid
Pet Care | Cat Food 
Pet Care | Cat Litter
Pet Care | Cat Treats
Pet Care | Dog Food
Pet Care | Dog Poo Bags
Pet Care | Dog Treats"""