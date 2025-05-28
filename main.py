from records import initial_records
from updates import secondary_types
from HarperDBOperations import HarperDBOperations


def main():
    # Initialize HarperDB operations
    harper = HarperDBOperations()

    # Validate connection
    if not harper.validate_connection():
        print("Failed to connect to HarperDB")
        return

    # Create schema and table
    table_name = "pokemon"
    db_name = "pokemon"

    harper.create_database(db_name)
    harper.create_table(db_name, table_name)

    # Sample data
    records = initial_records

    # Insert records
    harper.insert_records(db_name, table_name, records)

    # Update records
    updated_records = secondary_types
    harper.update_records(db_name, table_name, updated_records)

    # Validate records
    expected_records = [
        # Validate no secondary types on Pokemon that do not have them
        {"id": 1, "name": "Bulbasaur", "primaryType": "Grass"},
        {"id": 2, "name": "Ivysaur", "primaryType": "Grass"},
        {"id": 3, "name": "Venusaur", "primaryType": "Grass"},
        {"id": 6, "name": "Charizard", "primaryType": "Fire"},
        {"id": 12, "name": "Butterfree", "primaryType": "Bug"},
        # Validate secondary types on Pokemon that DO have them
        {"id": 1018, "name": "Archaludon", "primaryType": "Steel"},
        {"id": 1019, "name": "Hydrapple", "primaryType": "Grass"},
        {"id": 1020, "name": "Gouging Fire", "primaryType": "Fire"},
        {"id": 1021, "name": "Raging Bolt", "primaryType": "Electric"},
        {"id": 1022, "name": "Iron Boulder", "primaryType": "Rock"},
        {"id": 1023, "name": "Iron Crown", "primaryType": "Steel"},
        {"id": 1025, "name": "Pecharunt", "primaryType": "Poison"},
    ]

    validation_result = harper.validate_records(db_name, table_name, expected_records)
    print(f"Validation result: {'Success' if validation_result else 'Failed'}")


if __name__ == "__main__":
    main()
