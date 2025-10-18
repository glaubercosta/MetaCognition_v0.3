const API_BASE_URL = "http://localhost:8000";

export interface Agent {
  id?: string;
  name: string;
  role: string;
  goal: string;
  backstory: string;
  tools?: string[];
  created_at?: string;
  updated_at?: string;
}

export interface Flow {
  id?: string;
  name: string;
  description?: string;
  graph_json?: {
    nodes: Array<{ id: string }>;
    edges: Array<{ from: string; to: string }>;
  };
  created_at?: string;
  updated_at?: string;
}

export interface Evaluation {
  id?: string;
  flow_id: string;
  score: number;
  feedback?: string;
  created_at?: string;
}

export interface OrchestrationRequest {
  flow_id: string;
  engine: "crewai" | "robotgreen" | "fake";
  inputs?: Record<string, any>;
}

export interface OrchestrationResult {
  flow_id: string;
  engine: string;
  // Backend may return either {plan, logs} or {result, duration_ms}
  plan?: any;
  logs?: string[];
  result?: any;
  duration_ms?: number;
}

// Health
export const checkHealth = async () => {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) throw new Error("API is not healthy");
  return response.json();
};

// Agents
export const getAgents = async (): Promise<Agent[]> => {
  const response = await fetch(`${API_BASE_URL}/agents`);
  if (!response.ok) throw new Error("Failed to fetch agents");
  return response.json();
};

export const getAgent = async (id: string): Promise<Agent> => {
  const response = await fetch(`${API_BASE_URL}/agents/${id}`);
  if (!response.ok) throw new Error("Failed to fetch agent");
  return response.json();
};

export const createAgent = async (agent: Omit<Agent, "id" | "created_at" | "updated_at">): Promise<Agent> => {
  const response = await fetch(`${API_BASE_URL}/agents`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(agent),
  });
  if (!response.ok) throw new Error("Failed to create agent");
  return response.json();
};

export const updateAgent = async (id: string, agent: Partial<Agent>): Promise<Agent> => {
  const response = await fetch(`${API_BASE_URL}/agents/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(agent),
  });
  if (!response.ok) throw new Error("Failed to update agent");
  return response.json();
};

export const deleteAgent = async (id: string): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/agents/${id}`, {
    method: "DELETE",
  });
  if (!response.ok) throw new Error("Failed to delete agent");
};

// Flows
export const getFlows = async (): Promise<Flow[]> => {
  const response = await fetch(`${API_BASE_URL}/flows`);
  if (!response.ok) throw new Error("Failed to fetch flows");
  return response.json();
};

export const getFlow = async (id: string): Promise<Flow> => {
  const response = await fetch(`${API_BASE_URL}/flows/${id}`);
  if (!response.ok) throw new Error("Failed to fetch flow");
  return response.json();
};

export const createFlow = async (flow: Omit<Flow, "id" | "created_at" | "updated_at">): Promise<Flow> => {
  const response = await fetch(`${API_BASE_URL}/flows`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(flow),
  });
  if (!response.ok) throw new Error("Failed to create flow");
  return response.json();
};

// Orchestration
export const runOrchestration = async (request: OrchestrationRequest): Promise<OrchestrationResult> => {
  const response = await fetch(`${API_BASE_URL}/orchestrate/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  if (!response.ok) throw new Error("Failed to run orchestration");
  return response.json();
};

// Evaluations
export const getEvaluations = async (): Promise<Evaluation[]> => {
  const response = await fetch(`${API_BASE_URL}/evaluations`);
  if (!response.ok) throw new Error("Failed to fetch evaluations");
  return response.json();
};

export const createEvaluation = async (
  evaluation: Omit<Evaluation, "id" | "created_at">
): Promise<Evaluation> => {
  const response = await fetch(`${API_BASE_URL}/evaluations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(evaluation),
  });
  if (!response.ok) throw new Error("Failed to create evaluation");
  return response.json();
};

// Import/Export
export const exportAgents = async (format: "json" | "yaml" = "json"): Promise<string> => {
  const response = await fetch(`${API_BASE_URL}/agents/export?format=${format}`);
  if (!response.ok) throw new Error("Failed to export agents");
  return response.text();
};

export const importAgents = async (data: string, format: "json" | "yaml" = "json"): Promise<any> => {
  const response = await fetch(`${API_BASE_URL}/agents/import?format=${format}`, {
    method: "POST",
    headers: { "Content-Type": format === "json" ? "application/json" : "text/plain" },
    body: data,
  });
  if (!response.ok) throw new Error("Failed to import agents");
  return response.json();
};

export const exportFlows = async (format: "json" | "yaml" = "json"): Promise<string> => {
  const response = await fetch(`${API_BASE_URL}/flows/export?format=${format}`);
  if (!response.ok) throw new Error("Failed to export flows");
  return response.text();
};

export const importFlows = async (data: string, format: "json" | "yaml" = "json"): Promise<any> => {
  const response = await fetch(`${API_BASE_URL}/flows/import?format=${format}`, {
    method: "POST",
    headers: { "Content-Type": format === "json" ? "application/json" : "text/plain" },
    body: data,
  });
  if (!response.ok) throw new Error("Failed to import flows");
  return response.json();
};
