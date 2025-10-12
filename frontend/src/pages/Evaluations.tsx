import { useQuery } from "@tanstack/react-query";
import { getEvaluations, getFlows } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { BarChart3, Clock } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { PageHeader } from "@/components/PageHeader";
import { EmptyState } from "@/components/EmptyState";

export default function Evaluations() {
  const { data: evaluations, isLoading } = useQuery({
    queryKey: ["evaluations"],
    queryFn: getEvaluations,
  });

  const { data: flows } = useQuery({
    queryKey: ["flows"],
    queryFn: getFlows,
  });

  const getFlowName = (flowId: string) => {
    const flow = flows?.find((f) => f.id === flowId);
    return flow?.name || `Flow #${flowId}`;
  };

  const getScoreBadge = (score: number) => {
    if (score >= 80) return <Badge className="bg-success">Excellent</Badge>;
    if (score >= 60) return <Badge className="bg-primary">Good</Badge>;
    if (score >= 40) return <Badge variant="secondary">Fair</Badge>;
    return <Badge variant="destructive">Poor</Badge>;
  };

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Evaluations" 
        description="View orchestration evaluations"
      />

      <Card>
        <CardHeader>
          <CardTitle>All Evaluations</CardTitle>
          <CardDescription>Performance metrics for flow executions</CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="text-center py-8 text-muted-foreground">Loading evaluations...</div>
          ) : evaluations && evaluations.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Flow</TableHead>
                  <TableHead>Score</TableHead>
                  <TableHead>Rating</TableHead>
                  <TableHead>Feedback</TableHead>
                  <TableHead>Date</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {evaluations.map((evaluation) => (
                  <TableRow key={evaluation.id}>
                    <TableCell className="font-medium">
                      <div className="flex items-center gap-2">
                        <BarChart3 className="h-4 w-4 text-primary" />
                        {getFlowName(evaluation.flow_id)}
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className="text-lg font-semibold">{evaluation.score}</span>
                      <span className="text-muted-foreground">/100</span>
                    </TableCell>
                    <TableCell>{getScoreBadge(evaluation.score)}</TableCell>
                    <TableCell className="max-w-xs truncate">
                      {evaluation.feedback || "-"}
                    </TableCell>
                    <TableCell>
                      {evaluation.created_at
                        ? new Date(evaluation.created_at).toLocaleDateString()
                        : "-"}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <EmptyState
              icon={Clock}
              title="No evaluations found"
              description="Run an orchestration flow to generate evaluations."
            />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
