from db.driver_registry import create_drivers_table, add_driver

# Create the table if it doesn't exist
create_drivers_table()

# Seed sample drivers
add_driver("Ayesha", "Toyota Camry", "TX-4821", "555-1234", "ayesha@fleet.com")
add_driver("Malik", "Honda Accord", "TX-9988", "555-5678", "malik@fleet.com")
add_driver("Jorge", "Chevy Malibu", "TX-3344", "555-8765", "jorge@fleet.com")
add_driver("Fatima", "Nissan Altima", "TX-1122", "555-4321", "fatima@fleet.com")

print("✅ Driver table seeded successfully.")