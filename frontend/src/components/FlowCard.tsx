import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { GitBranch, Pencil, Trash2 } from "lucide-react";
import { type Flow } from "@/lib/api";

interface FlowCardProps {
  flow: Flow;
  agentNames?: string;
  onEdit?: () => void;
  onDelete?: () => void;
}

export function FlowCard({ flow, agentNames, onEdit, onDelete }: FlowCardProps) {
  const nodeCount = flow.graph_json?.nodes?.length || 0;

  return (
    <Card className="transition-all duration-200 hover:shadow-lg-custom">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="rounded-full bg-accent/10 p-2">
              <GitBranch className="h-5 w-5 text-accent" aria-hidden="true" />
            </div>
            <div>
              <CardTitle className="text-lg">{flow.name}</CardTitle>
              <CardDescription className="text-sm mt-1">
                {flow.description || "No description"}
              </CardDescription>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline">
              {nodeCount} {nodeCount === 1 ? "node" : "nodes"}
            </Badge>
            {onEdit && (
              <Button variant="ghost" size="icon" onClick={onEdit} title="Edit flow">
                <Pencil className="h-4 w-4" />
              </Button>
            )}
            {onDelete && (
              <Button variant="ghost" size="icon" onClick={onDelete} title="Delete flow">
                <Trash2 className="h-4 w-4" />
              </Button>
            )}
          </div>
        </div>
      </CardHeader>
      {agentNames && (
        <CardContent>
          <div>
            <p className="text-sm font-medium text-muted-foreground mb-1">Agents</p>
            <p className="text-sm text-foreground">{agentNames}</p>
          </div>
        </CardContent>
      )}
    </Card>
  );
}
