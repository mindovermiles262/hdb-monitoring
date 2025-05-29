import requests
import os
import base64


class HarperDBOperations:
    def __init__(self, host="http://localhost:9925", username=None, password=None):
        self.host = host
        self.username = username or os.getenv("HDB_ADMIN_USERNAME", "HDB_ADMIN")
        self.password = password or os.getenv("HDB_ADMIN_PASSWORD", "password")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self._get_auth_token()}",
        }
        self.metrics = []

    def _get_auth_token(self):
        return base64.b64encode(f"{self.username}:{self.password}".encode()).decode()

    def validate_connection(self):
        try:
            response = requests.get(f"{self.host}/", headers=self.headers)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Connection validation failed: {str(e)}")
            return False

    def create_database(self, database_name):
        response = requests.post(
            f"{self.host}/",
            headers=self.headers,
            json={
                "operation": "create_database",
                "database": database_name,
            },
        )

        if response.status_code == 400 and "already exists" in response.text:
            print(f"Database {database_name} already exists")
            return response.json()
        elif response.status_code != 200:
            raise Exception(f"Database creation failed: {response.text}")
        return response.json()

    def create_table(self, db_name, table_name, hash_attribute="id"):
        response = requests.post(
            f"{self.host}/",
            headers=self.headers,
            json={
                "operation": "create_table",
                "database": db_name,
                "table": table_name,
                "primary_key": hash_attribute,
            },
        )
        if response.status_code == 400 and "already exists" in response.text:
            print(f"Table {table_name} already exists")
            return
        elif response.status_code != 200:
            raise Exception(f"Database creation failed: {response.text}")
        return response.json()

    def insert_records(self, schema_name, table_name, records):
        response = requests.post(
            f"{self.host}/",
            headers=self.headers,
            json={
                "operation": "insert",
                "schema": schema_name,
                "table": table_name,
                "records": records,
            },
        )

        if response.status_code == 400 and "already exists" in response.text:
            print("Records already exist")
            return
        elif response.status_code != 200:
            raise Exception(f"Database creation failed: {response.text}")
        return response.json()

    def update_records(self, db_name, table_name, records):
        # Do not need to look all of this up, but want to use the DB to get some metrics.
        for record in records:
            lookup_response = requests.post(
                f"{self.host}/",
                headers=self.headers,
                json={
                    "operation": "search_by_value",
                    "schema": db_name,
                    "table": table_name,
                    "search_attribute": "id",
                    "search_value": record["id"],
                    "get_attributes": ["id", "name", "primaryType"],
                },
            )
            print(f"Found {lookup_response.json()}")
            response = requests.post(
                f"{self.host}/",
                headers=self.headers,
                json={
                    "operation": "update",
                    "schema": db_name,
                    "table": table_name,
                    "records": [record],
                },
            )
            if response.status_code == 400 and "already exists" in response.text:
                print("Records already exist")
                return
            elif response.status_code != 200:
                raise Exception(f"Database creation failed: {response.text}")

    def validate_records(self, db_name, table_name, expected_records):
        # Again, looping to get some useful metrics
        for record in expected_records:
            db_response = requests.post(
                f"{self.host}/",
                headers=self.headers,
                json={
                    "operation": "search_by_value",
                    "schema": db_name,
                    "table": table_name,
                    "search_attribute": "id",
                    "search_value": record["id"],
                    "get_attributes": ["*"],
                },
            )
            actual_records = db_response.json()

            # Compare records
            for k, v in record.items():
                actual_value = actual_records[0][k]
                if actual_value != v:
                    print(f"Record {record['id']} is invalid")
                    return False
            print(f"Record {record['id']} is valid")
        return True
