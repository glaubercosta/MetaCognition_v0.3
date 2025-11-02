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

export interface ValidationResult {
  ok: boolean;
  errors: string[];
  message?: string;
}

export interface ImportSummary<T> {
  created: T[];
  count: number;
}

export interface ConvertAgentMarkdownResponse {
  ok: boolean;
  agent?: Record<string, unknown>;
  errors: string[];
  message?: string;
}

const isJsonFormat = (format: "json" | "yaml"): boolean => format === "json";

const buildPayload = (data: string, format: "json" | "yaml") => {
  if (isJsonFormat(format)) {
    try {
      const parsed = JSON.parse(data);
      return { body: JSON.stringify(parsed), contentType: "application/json" };
    } catch (error) {
      throw new Error("Invalid JSON payload. Please fix the syntax before continuing.");
    }
  }
  return { body: data, contentType: "text/plain" };
};

const parseErrorResponse = async (response: Response): Promise<Error> => {
  const text = await response.text();
  try {
    const payload = JSON.parse(text);
    const detail = payload.detail ?? payload.message ?? text;
    if (typeof detail === "string") {
      return new Error(detail);
    }
    if (Array.isArray(detail)) {
      return new Error(detail.map((item) => (item.msg ? item.msg : JSON.stringify(item))).join("; "));
    }
    if (detail && typeof detail === "object") {
      const message = detail.message ?? response.statusText;
      const errors = Array.isArray(detail.errors) && detail.errors.length > 0 ? `: ${detail.errors.join("; ")}` : "";
      return new Error(`${message}${errors}`);
    }
    return new Error(JSON.stringify(detail));
  } catch {
    return new Error(text || response.statusText);
  }
};

export interface OrchestrationRequest {
  flow_id: string;
  engine: "crewai" | "robotgreen" | "fake";
  inputs?: Record<string, unknown>;
}

export interface OrchestrationResult {
  flow_id: string;
  engine: string;
  // Backend may return either {plan, logs} or {result, duration_ms}
  plan?: unknown;
  logs?: string[];
  result?: unknown;
  duration_ms?: number;
  request_id?: string;
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
  const payload = (await response.json()) as Agent[];
  return payload;
};

export const getAgent = async (id: string): Promise<Agent> => {
  const response = await fetch(`${API_BASE_URL}/agents/${id}`);
  if (!response.ok) throw new Error("Failed to fetch agent");
  const payload = (await response.json()) as Agent;
  return payload;
};

export const createAgent = async (agent: Omit<Agent, "id" | "created_at" | "updated_at">): Promise<Agent> => {
  const response = await fetch(`${API_BASE_URL}/agents`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(agent),
  });
  if (!response.ok) throw new Error("Failed to create agent");
  const payload = (await response.json()) as Agent;
  return payload;
};

export const updateAgent = async (id: string, agent: Partial<Agent>): Promise<Agent> => {
  const response = await fetch(`${API_BASE_URL}/agents/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(agent),
  });
  if (!response.ok) throw new Error("Failed to update agent");
  const payload = (await response.json()) as Agent;
  return payload;
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
  const payload = (await response.json()) as Flow[];
  return payload;
};

export const getFlow = async (id: string): Promise<Flow> => {
  const response = await fetch(`${API_BASE_URL}/flows/${id}`);
  if (!response.ok) throw new Error("Failed to fetch flow");
  const payload = (await response.json()) as Flow;
  return payload;
};

export const createFlow = async (flow: Omit<Flow, "id" | "created_at" | "updated_at">): Promise<Flow> => {
  const response = await fetch(`${API_BASE_URL}/flows`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(flow),
  });
  if (!response.ok) throw new Error("Failed to create flow");
  const payload = (await response.json()) as Flow;
  return payload;
};

// Orchestration
export const runOrchestration = async (request: OrchestrationRequest): Promise<OrchestrationResult> => {
  const response = await fetch(`${API_BASE_URL}/orchestrate/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  if (!response.ok) throw new Error("Failed to run orchestration");
  const payload = (await response.json()) as OrchestrationResult;
  return payload;
};

// Evaluations
export const getEvaluations = async (): Promise<Evaluation[]> => {
  const response = await fetch(`${API_BASE_URL}/evaluations`);
  if (!response.ok) throw new Error("Failed to fetch evaluations");
  const payload = (await response.json()) as Evaluation[];
  return payload;
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
  const payload = (await response.json()) as Evaluation;
  return payload;
};

// Import/Export
export const exportAgents = async (format: "json" | "yaml" = "json"): Promise<string> => {
  const response = await fetch(`${API_BASE_URL}/agents/export?format=${format}`);
  if (!response.ok) throw new Error("Failed to export agents");
  return response.text();
};

export const importAgents = async (
  data: string,
  format: "json" | "yaml" = "json"
): Promise<ImportSummary<Record<string, unknown>>> => {
  const { body, contentType } = buildPayload(data, format);
  const response = await fetch(`${API_BASE_URL}/agents/import?format=${format}`, {
    method: "POST",
    headers: { "Content-Type": contentType },
    body,
  });
  if (!response.ok) throw await parseErrorResponse(response);
  const payload = (await response.json()) as ImportSummary<Record<string, unknown>>;
  return payload;
};

export const exportFlows = async (format: "json" | "yaml" = "json"): Promise<string> => {
  const response = await fetch(`${API_BASE_URL}/flows/export?format=${format}`);
  if (!response.ok) throw new Error("Failed to export flows");
  return response.text();
};

export const importFlows = async (
  data: string,
  format: "json" | "yaml" = "json"
): Promise<ImportSummary<Record<string, unknown>>> => {
  const { body, contentType } = buildPayload(data, format);
  const response = await fetch(`${API_BASE_URL}/flows/import?format=${format}`, {
    method: "POST",
    headers: { "Content-Type": contentType },
    body,
  });
  if (!response.ok) throw await parseErrorResponse(response);
  const payload = (await response.json()) as ImportSummary<Record<string, unknown>>;
  return payload;
};

export const importAgentsFile = async (
  file: File,
  fileFormat: "json" | "yaml"
): Promise<ImportSummary<Record<string, unknown>>> => {
  const form = new FormData();
  form.append("file", file);
  form.append("file_format", fileFormat);
  const response = await fetch(`${API_BASE_URL}/agents/import`, {
    method: "POST",
    body: form,
  });
  if (!response.ok) throw await parseErrorResponse(response);
  const payload = (await response.json()) as ImportSummary<Record<string, unknown>>;
  return payload;
};

export const importFlowsFile = async (
  file: File,
  fileFormat: "json" | "yaml"
): Promise<ImportSummary<Record<string, unknown>>> => {
  const form = new FormData();
  form.append("file", file);
  form.append("file_format", fileFormat);
  const response = await fetch(`${API_BASE_URL}/flows/import`, {
    method: "POST",
    body: form,
  });
  if (!response.ok) throw await parseErrorResponse(response);
  const payload = (await response.json()) as ImportSummary<Record<string, unknown>>;
  return payload;
};

export const validateAgentPayload = async (data: string, format: "json" | "yaml"): Promise<ValidationResult> => {
  const { body, contentType } = buildPayload(data, format);
  const response = await fetch(`${API_BASE_URL}/agents/validate?format=${format}`, {
    method: "POST",
    headers: { "Content-Type": contentType },
    body,
  });
  if (!response.ok) throw await parseErrorResponse(response);
  const payload = (await response.json()) as ValidationResult;
  return payload;
};

export const validateFlowPayload = async (data: string, format: "json" | "yaml"): Promise<ValidationResult> => {
  const { body, contentType } = buildPayload(data, format);
  const response = await fetch(`${API_BASE_URL}/flows/validate?format=${format}`, {
    method: "POST",
    headers: { "Content-Type": contentType },
    body,
  });
  if (!response.ok) throw await parseErrorResponse(response);
  const payload = (await response.json()) as ValidationResult;
  return payload;
};

export const convertAgentMarkdown = async (markdown: string): Promise<ConvertAgentMarkdownResponse> => {
  const response = await fetch(`${API_BASE_URL}/convert/agent-md`, {
    method: "POST",
    headers: { "Content-Type": "text/markdown" },
    body: markdown,
  });
  if (!response.ok) throw await parseErrorResponse(response);
  const payload = (await response.json()) as ConvertAgentMarkdownResponse;
  return payload;
};
