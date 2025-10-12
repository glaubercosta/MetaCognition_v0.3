import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Bot, Pencil, Trash2 } from "lucide-react";
import { type Agent } from "@/lib/api";

interface AgentCardProps {
  agent: Agent;
  onEdit?: (agent: Agent) => void;
  onDelete?: (id: string) => void;
}

export function AgentCard({ agent, onEdit, onDelete }: AgentCardProps) {
  return (
    <Card className="transition-all duration-200 hover:shadow-lg-custom group">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="rounded-full bg-primary/10 p-2">
              <Bot className="h-5 w-5 text-primary" aria-hidden="true" />
            </div>
            <div>
              <CardTitle className="text-lg">{agent.name}</CardTitle>
              <CardDescription className="text-sm mt-1">{agent.role}</CardDescription>
            </div>
          </div>
          {(onEdit || onDelete) && (
            <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              {onEdit && (
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onEdit(agent)}
                  aria-label={`Edit ${agent.name}`}
                >
                  <Pencil className="h-4 w-4" />
                </Button>
              )}
              {onDelete && (
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onDelete(agent.id!)}
                  aria-label={`Delete ${agent.name}`}
                >
                  <Trash2 className="h-4 w-4 text-destructive" />
                </Button>
              )}
            </div>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        <div>
          <p className="text-sm font-medium text-muted-foreground mb-1">Goal</p>
          <p className="text-sm text-foreground line-clamp-2">{agent.goal}</p>
        </div>
        {agent.tools && agent.tools.length > 0 && (
          <div>
            <p className="text-sm font-medium text-muted-foreground mb-2">Tools</p>
            <div className="flex flex-wrap gap-1">
              {agent.tools.slice(0, 3).map((tool, idx) => (
                <Badge key={idx} variant="secondary" className="text-xs">
                  {tool}
                </Badge>
              ))}
              {agent.tools.length > 3 && (
                <Badge variant="secondary" className="text-xs">
                  +{agent.tools.length - 3} more
                </Badge>
              )}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
