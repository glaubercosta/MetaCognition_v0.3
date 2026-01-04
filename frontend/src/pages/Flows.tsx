import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getFlows, getAgents, createFlow, updateFlow, deleteFlow, type Flow } from "@/lib/api";
import { Button } from "@/components/ui/button";
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
import { Plus, GitBranch } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { Checkbox } from "@/components/ui/checkbox";
import { PageHeader } from "@/components/PageHeader";
import { EmptyState } from "@/components/EmptyState";
import { FlowCard } from "@/components/FlowCard";

export default function Flows() {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [open, setOpen] = useState(false);
  const [editingFlow, setEditingFlow] = useState<Flow | null>(null);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    graph_json: {
      nodes: [] as Array<{ id: string }>,
      edges: [] as Array<{ from: string; to: string }>,
    },
  });

  const { data: flows, isLoading: flowsLoading } = useQuery({
    queryKey: ["flows"],
    queryFn: getFlows,
  });

  const { data: agents } = useQuery({
    queryKey: ["agents"],
    queryFn: getAgents,
  });

  const createMutation = useMutation({
    mutationFn: createFlow,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["flows"] });
      toast({ title: "Flow created successfully" });
      setOpen(false);
      resetForm();
    },
    onError: () => {
      toast({ title: "Failed to create flow", variant: "destructive" });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Flow> }) => updateFlow(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["flows"] });
      toast({ title: "Flow updated successfully" });
      setOpen(false);
      resetForm();
    },
    onError: () => {
      toast({ title: "Failed to update flow", variant: "destructive" });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteFlow,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["flows"] });
      toast({ title: "Flow deleted successfully" });
    },
    onError: () => {
      toast({ title: "Failed to delete flow", variant: "destructive" });
    },
  });

  const resetForm = () => {
    setFormData({
      name: "",
      description: "",
      graph_json: { nodes: [], edges: [] }
    });
    setEditingFlow(null);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editingFlow) {
      updateMutation.mutate({ id: editingFlow.id!, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleEdit = (flow: Flow) => {
    setEditingFlow(flow);
    setFormData({
      name: flow.name,
      description: flow.description || "",
      graph_json: flow.graph_json || { nodes: [], edges: [] },
    });
    setOpen(true);
  };

  const handleDelete = (id: string) => {
    if (confirm("Are you sure you want to delete this flow?")) {
      deleteMutation.mutate(id);
    }
  };

  const toggleAgent = (agentId: string) => {
    const nodeExists = formData.graph_json.nodes.some(n => n.id === agentId);
    setFormData((prev) => ({
      ...prev,
      graph_json: {
        ...prev.graph_json,
        nodes: nodeExists
          ? prev.graph_json.nodes.filter((n) => n.id !== agentId)
          : [...prev.graph_json.nodes, { id: agentId }],
      },
    }));
  };

  const getAgentNames = (nodes?: Array<{ id: string }>) => {
    if (!agents || !nodes || nodes.length === 0) return "";
    return agents
      .filter((a) => nodes.some(n => n.id === a.id))
      .map((a) => a.name)
      .join(", ");
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Flows"
        description="Manage orchestration flows"
        action={
          <Dialog
            open={open}
            onOpenChange={(isOpen) => {
              setOpen(isOpen);
              if (!isOpen) resetForm();
            }}
          >
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Create Flow
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>{editingFlow ? "Edit Flow" : "Create New Flow"}</DialogTitle>
                <DialogDescription>
                  Configure an orchestration flow with multiple agents
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="name">Flow Name</Label>
                    <Input
                      id="name"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      required
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="description">Description</Label>
                    <Textarea
                      id="description"
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label>Select Agents</Label>
                    {agents && agents.length > 0 ? (
                      <div className="space-y-2 border border-border rounded-lg p-4 max-h-60 overflow-y-auto">
                        {agents.map((agent) => (
                          <div key={agent.id} className="flex items-center space-x-2">
                            <Checkbox
                              id={`agent-${agent.id}`}
                              checked={formData.graph_json.nodes.some(n => n.id === agent.id)}
                              onCheckedChange={() => toggleAgent(agent.id!)}
                            />
                            <label
                              htmlFor={`agent-${agent.id}`}
                              className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                            >
                              {agent.name} - {agent.role}
                            </label>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-muted-foreground">
                        No agents available. Create agents first.
                      </p>
                    )}
                  </div>
                </div>
                <DialogFooter>
                  <Button type="submit" disabled={createMutation.isPending || updateMutation.isPending || formData.graph_json.nodes.length === 0}>
                    {editingFlow ? "Update Flow" : "Create Flow"}
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        }
      />

      {flowsLoading ? (
        <div className="text-center py-12 text-muted-foreground" role="status" aria-live="polite">
          Loading flows...
        </div>
      ) : flows && flows.length > 0 ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {flows.map((flow) => (
            <FlowCard
              key={flow.id}
              flow={flow}
              agentNames={getAgentNames(flow.graph_json?.nodes)}
              onEdit={() => handleEdit(flow)}
              onDelete={() => handleDelete(flow.id!)}
            />
          ))}
        </div>
      ) : (
        <EmptyState
          icon={GitBranch}
          title="No flows found"
          description="Create your first orchestration flow to connect multiple agents."
          actionLabel="Create Flow"
          onAction={() => setOpen(true)}
        />
      )}
    </div>
  );
}
