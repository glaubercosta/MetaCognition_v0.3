import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getAgents, createAgent, updateAgent, deleteAgent, type Agent } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { PageHeader } from "@/components/PageHeader";
import { EmptyState } from "@/components/EmptyState";
import { AgentCard } from "@/components/AgentCard";
import { MarkdownEditor } from "@/components/MarkdownEditor";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Plus, Pencil, Trash2, Bot } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function Agents() {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [open, setOpen] = useState(false);
  const [editingAgent, setEditingAgent] = useState<Agent | null>(null);
  const [formData, setFormData] = useState({
    name: "",
    role: "",
    goal: "",
    backstory: "",
    tools: "",
    input_artifacts: "",
    output_artifacts: "",
  });

  const { data: agents, isLoading } = useQuery({
    queryKey: ["agents"],
    queryFn: getAgents,
  });

  const createMutation = useMutation({
    mutationFn: createAgent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["agents"] });
      toast({ title: "Agent created successfully" });
      setOpen(false);
      resetForm();
    },
    onError: () => {
      toast({ title: "Failed to create agent", variant: "destructive" });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Agent> }) => updateAgent(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["agents"] });
      toast({ title: "Agent updated successfully" });
      setOpen(false);
      resetForm();
    },
    onError: () => {
      toast({ title: "Failed to update agent", variant: "destructive" });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteAgent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["agents"] });
      toast({ title: "Agent deleted successfully" });
    },
    onError: () => {
      toast({ title: "Failed to delete agent", variant: "destructive" });
    },
  });

  const resetForm = () => {
    setFormData({ name: "", role: "", goal: "", backstory: "", tools: "", input_artifacts: "", output_artifacts: "" });
    setEditingAgent(null);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Parse JSON fields
    let inputArtifacts = null;
    let outputArtifacts = null;

    try {
      if (formData.input_artifacts.trim()) {
        inputArtifacts = JSON.parse(formData.input_artifacts);
      }
    } catch (e) {
      toast({ title: "Invalid Input Artifacts JSON", variant: "destructive" });
      return;
    }

    try {
      if (formData.output_artifacts.trim()) {
        outputArtifacts = JSON.parse(formData.output_artifacts);
      }
    } catch (e) {
      toast({ title: "Invalid Output Artifacts JSON", variant: "destructive" });
      return;
    }

    const agentData = {
      name: formData.name,
      role: formData.role,
      goal: formData.goal,
      backstory: formData.backstory,
      tools: formData.tools ? formData.tools.split(",").map((t) => t.trim()) : [],
      input_artifacts: inputArtifacts,
      output_artifacts: outputArtifacts,
    };

    if (editingAgent) {
      updateMutation.mutate({ id: editingAgent.id!, data: agentData });
    } else {
      createMutation.mutate(agentData);
    }
  };

  const handleEdit = (agent: Agent) => {
    setEditingAgent(agent);
    setFormData({
      name: agent.name,
      role: agent.role,
      goal: agent.goal,
      backstory: agent.backstory,
      tools: agent.tools?.join(", ") || "",
      input_artifacts: agent.input_artifacts ? JSON.stringify(agent.input_artifacts, null, 2) : "",
      output_artifacts: agent.output_artifacts ? JSON.stringify(agent.output_artifacts, null, 2) : "",
    });
    setOpen(true);
  };

  const handleDelete = (id: string) => {
    if (confirm("Are you sure you want to delete this agent?")) {
      deleteMutation.mutate(id);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Agents"
        description="Manage your AI agents"
        action={
          <Dialog open={open} onOpenChange={(isOpen) => {
            setOpen(isOpen);
            if (!isOpen) resetForm();
          }}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Create Agent
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>{editingAgent ? "Edit Agent" : "Create New Agent"}</DialogTitle>
                <DialogDescription>
                  Configure your AI agent with role, goals, and capabilities
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="name">Name</Label>
                    <Input
                      id="name"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      required
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="role">Role</Label>
                    <Input
                      id="role"
                      value={formData.role}
                      onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                      required
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="goal">Goal</Label>
                    <MarkdownEditor
                      value={formData.goal}
                      onChange={(val) => setFormData({ ...formData, goal: val })}
                      placeholder="Define the agent's primary objective..."
                      minHeight="min-h-[100px]"
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="backstory">Backstory</Label>
                    <MarkdownEditor
                      value={formData.backstory}
                      onChange={(val) => setFormData({ ...formData, backstory: val })}
                      placeholder="Describe the agent's background and personality..."
                      minHeight="min-h-[150px]"
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="tools">Tools (comma separated)</Label>
                    <Input
                      id="tools"
                      value={formData.tools}
                      onChange={(e) => setFormData({ ...formData, tools: e.target.value })}
                      placeholder="tool1, tool2, tool3"
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="input_artifacts">Input Artifacts (JSON - Optional)</Label>
                    <Textarea
                      id="input_artifacts"
                      value={formData.input_artifacts || ""}
                      onChange={(e) => setFormData({ ...formData, input_artifacts: e.target.value })}
                      placeholder='{"key": "value"}'
                      className="font-mono text-sm min-h-[80px]"
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="output_artifacts">Output Artifacts (JSON - Optional)</Label>
                    <Textarea
                      id="output_artifacts"
                      value={formData.output_artifacts || ""}
                      onChange={(e) => setFormData({ ...formData, output_artifacts: e.target.value })}
                      placeholder='{"key": "value"}'
                      className="font-mono text-sm min-h-[80px]"
                    />
                  </div>
                </div>
                <DialogFooter>
                  <Button type="submit" disabled={createMutation.isPending || updateMutation.isPending}>
                    {editingAgent ? "Update Agent" : "Create Agent"}
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        }
      />

      {isLoading ? (
        <div className="text-center py-12 text-muted-foreground" role="status" aria-live="polite">
          Loading agents...
        </div>
      ) : agents && agents.length > 0 ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {agents.map((agent) => (
            <AgentCard
              key={agent.id}
              agent={agent}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          ))}
        </div>
      ) : (
        <EmptyState
          icon={Bot}
          title="No agents found"
          description="Create your first AI agent to get started with orchestration."
          actionLabel="Create Agent"
          onAction={() => setOpen(true)}
        />
      )}
    </div>
  );
}
