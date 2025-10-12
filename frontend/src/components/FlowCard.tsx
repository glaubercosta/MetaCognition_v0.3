import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { GitBranch } from "lucide-react";
import { type Flow } from "@/lib/api";

interface FlowCardProps {
  flow: Flow;
  agentNames?: string;
}

export function FlowCard({ flow, agentNames }: FlowCardProps) {
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
          <Badge variant="outline" className="ml-2">
            {nodeCount} {nodeCount === 1 ? "node" : "nodes"}
          </Badge>
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
