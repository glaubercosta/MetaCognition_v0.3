import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_flow_crud():
    print("Testing Flow CRUD...")
    
    # 1. Create Flow
    print("\n1. Creating Flow...")
    flow_data = {
        "name": "Test Flow",
        "description": "A test flow",
        "graph_json": {"nodes": [], "edges": []}
    }
    try:
        res = requests.post(f"{BASE_URL}/flows", json=flow_data)
        res.raise_for_status()
        flow = res.json()
        flow_id = flow["id"]
        print(f"✓ Created flow: {flow_id}")
    except Exception as e:
        print(f"✗ Failed to create flow: {e}")
        return

    # 2. Update Flow
    print("\n2. Updating Flow...")
    update_data = {
        "name": "Updated Test Flow",
        "description": "Updated description",
        "graph_json": {"nodes": [{"id": "test"}], "edges": []}
    }
    try:
        res = requests.put(f"{BASE_URL}/flows/{flow_id}", json=update_data)
        res.raise_for_status()
        updated_flow = res.json()
        if updated_flow["name"] == "Updated Test Flow":
            print(f"✓ Updated flow: {updated_flow['name']}")
        else:
            print(f"✗ Update mismatch: {updated_flow['name']}")
    except Exception as e:
        print(f"✗ Failed to update flow: {e}")
        print(res.text)

    # 3. Delete Flow
    print("\n3. Deleting Flow...")
    try:
        res = requests.delete(f"{BASE_URL}/flows/{flow_id}")
        res.raise_for_status()
        print("✓ Deleted flow")
    except Exception as e:
        print(f"✗ Failed to delete flow: {e}")

    # 4. Verify Deletion
    print("\n4. Verifying Deletion...")
    res = requests.get(f"{BASE_URL}/flows/{flow_id}")
    if res.status_code == 404:
        print("✓ Flow correctly not found")
    else:
        print(f"✗ Flow still exists or error: {res.status_code}")

if __name__ == "__main__":
    test_flow_crud()
