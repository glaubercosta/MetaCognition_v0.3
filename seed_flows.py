import sys
sys.path.insert(0, '/app')

from app.services.agents_service import list_agents
from app.services.flows_service import create_flow
from app.models import FlowCreate

# Get all agents
agents = list_agents()
agent_map = {agent.name: agent.id for agent in agents}

print("Available agents:")
for name, id in agent_map.items():
    print(f"  - {name}: {id}")

# Define flows
flows = [
    {
        "name": "CI/CD Pipeline",
        "description": "Automated continuous integration and deployment pipeline with quality gates",
        "graph_json": {
            "nodes": [
                {"id": agent_map["Backend Developer"], "type": "agent", "label": "Backend Developer"},
                {"id": agent_map["QA Engineer"], "type": "agent", "label": "QA Engineer"},
                {"id": agent_map["Code Reviewer"], "type": "agent", "label": "Code Reviewer"},
                {"id": agent_map["DevOps Engineer"], "type": "agent", "label": "DevOps Engineer"}
            ],
            "edges": [
                {"from": agent_map["Backend Developer"], "to": agent_map["Code Reviewer"], "label": "code_review"},
                {"from": agent_map["Code Reviewer"], "to": agent_map["QA Engineer"], "label": "approved"},
                {"from": agent_map["QA Engineer"], "to": agent_map["DevOps Engineer"], "label": "tests_passed"}
            ]
        }
    },
    {
        "name": "Feature Development Flow",
        "description": "End-to-end feature development from backend to frontend with testing",
        "graph_json": {
            "nodes": [
                {"id": agent_map["Backend Developer"], "type": "agent", "label": "Backend Developer"},
                {"id": agent_map["API Designer"], "type": "agent", "label": "API Designer"},
                {"id": agent_map["Frontend Developer"], "type": "agent", "label": "Frontend Developer"},
                {"id": agent_map["QA Engineer"], "type": "agent", "label": "QA Engineer"}
            ],
            "edges": [
                {"from": agent_map["API Designer"], "to": agent_map["Backend Developer"], "label": "api_spec"},
                {"from": agent_map["Backend Developer"], "to": agent_map["Frontend Developer"], "label": "api_ready"},
                {"from": agent_map["Frontend Developer"], "to": agent_map["QA Engineer"], "label": "feature_complete"}
            ]
        }
    },
    {
        "name": "Security Review Process",
        "description": "Comprehensive security review workflow for new features",
        "graph_json": {
            "nodes": [
                {"id": agent_map["Backend Developer"], "type": "agent", "label": "Backend Developer"},
                {"id": agent_map["Security Engineer"], "type": "agent", "label": "Security Engineer"},
                {"id": agent_map["Code Reviewer"], "type": "agent", "label": "Code Reviewer"},
                {"id": agent_map["DevOps Engineer"], "type": "agent", "label": "DevOps Engineer"}
            ],
            "edges": [
                {"from": agent_map["Backend Developer"], "to": agent_map["Security Engineer"], "label": "security_scan"},
                {"from": agent_map["Security Engineer"], "to": agent_map["Code Reviewer"], "label": "vulnerabilities_fixed"},
                {"from": agent_map["Code Reviewer"], "to": agent_map["DevOps Engineer"], "label": "approved_for_deploy"}
            ]
        }
    },
    {
        "name": "Database Migration Flow",
        "description": "Safe database schema changes with review and deployment",
        "graph_json": {
            "nodes": [
                {"id": agent_map["Database Architect"], "type": "agent", "label": "Database Architect"},
                {"id": agent_map["Backend Developer"], "type": "agent", "label": "Backend Developer"},
                {"id": agent_map["Code Reviewer"], "type": "agent", "label": "Code Reviewer"},
                {"id": agent_map["DevOps Engineer"], "type": "agent", "label": "DevOps Engineer"}
            ],
            "edges": [
                {"from": agent_map["Database Architect"], "to": agent_map["Backend Developer"], "label": "migration_scripts"},
                {"from": agent_map["Backend Developer"], "to": agent_map["Code Reviewer"], "label": "code_updated"},
                {"from": agent_map["Code Reviewer"], "to": agent_map["DevOps Engineer"], "label": "ready_to_migrate"}
            ]
        }
    },
    {
        "name": "Full Stack Development",
        "description": "Complete development cycle from API design to deployment",
        "graph_json": {
            "nodes": [
                {"id": agent_map["API Designer"], "type": "agent", "label": "API Designer"},
                {"id": agent_map["Database Architect"], "type": "agent", "label": "Database Architect"},
                {"id": agent_map["Backend Developer"], "type": "agent", "label": "Backend Developer"},
                {"id": agent_map["Frontend Developer"], "type": "agent", "label": "Frontend Developer"},
                {"id": agent_map["QA Engineer"], "type": "agent", "label": "QA Engineer"},
                {"id": agent_map["Security Engineer"], "type": "agent", "label": "Security Engineer"},
                {"id": agent_map["DevOps Engineer"], "type": "agent", "label": "DevOps Engineer"}
            ],
            "edges": [
                {"from": agent_map["API Designer"], "to": agent_map["Database Architect"], "label": "data_requirements"},
                {"from": agent_map["Database Architect"], "to": agent_map["Backend Developer"], "label": "schema_ready"},
                {"from": agent_map["Backend Developer"], "to": agent_map["Frontend Developer"], "label": "api_implemented"},
                {"from": agent_map["Frontend Developer"], "to": agent_map["QA Engineer"], "label": "ui_complete"},
                {"from": agent_map["QA Engineer"], "to": agent_map["Security Engineer"], "label": "tests_passed"},
                {"from": agent_map["Security Engineer"], "to": agent_map["DevOps Engineer"], "label": "security_approved"}
            ]
        }
    }
]

print("\nCreating flows...")
for flow_data in flows:
    try:
        flow = create_flow(FlowCreate(**flow_data))
        print(f"✓ Created: {flow.name} ({len(flow_data['graph_json']['nodes'])} nodes, {len(flow_data['graph_json']['edges'])} edges)")
    except Exception as e:
        print(f"✗ Failed to create {flow_data['name']}: {e}")

print("\nDone! All flows created successfully.")
