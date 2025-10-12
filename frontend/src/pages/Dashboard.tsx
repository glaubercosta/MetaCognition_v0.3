import { useQuery } from "@tanstack/react-query";
import { getAgents, getFlows } from "@/lib/api";
import { Bot, GitBranch, TrendingUp, Zap } from "lucide-react";
import { StatCard } from "@/components/StatCard";
import { AgentCard } from "@/components/AgentCard";
import { FlowCard } from "@/components/FlowCard";
import { PageHeader } from "@/components/PageHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function Dashboard() {
  const { data: agents } = useQuery({
    queryKey: ["agents"],
    queryFn: getAgents,
  });

  const { data: flows } = useQuery({
    queryKey: ["flows"],
    queryFn: getFlows,
  });

  const totalNodes = flows?.reduce((sum, flow) => sum + (flow.graph_json?.nodes?.length || 0), 0) || 0;
  const avgNodes = flows && flows.length > 0 ? (totalNodes / flows.length).toFixed(1) : "0";

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Dashboard" 
        description="Overview of your AI orchestration platform"
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Agents"
          value={agents?.length || 0}
          icon={Bot}
        />
        <StatCard
          title="Total Flows"
          value={flows?.length || 0}
          icon={GitBranch}
        />
        <StatCard
          title="Total Nodes"
          value={totalNodes}
          icon={Zap}
        />
        <StatCard
          title="Avg Nodes/Flow"
          value={avgNodes}
          icon={TrendingUp}
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Recent Agents</CardTitle>
            <CardDescription>Latest configured AI agents</CardDescription>
          </CardHeader>
          <CardContent>
            {agents && agents.length > 0 ? (
              <div className="space-y-3">
                {agents.slice(0, 3).map((agent) => (
                  <AgentCard key={agent.id} agent={agent} />
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                No agents found. Create your first agent to get started.
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Flows</CardTitle>
            <CardDescription>Latest orchestration flows</CardDescription>
          </CardHeader>
          <CardContent>
            {flows && flows.length > 0 ? (
              <div className="space-y-3">
                {flows.slice(0, 3).map((flow) => (
                  <FlowCard key={flow.id} flow={flow} />
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                No flows found. Create your first flow to get started.
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
