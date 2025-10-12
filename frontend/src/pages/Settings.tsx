import { useQuery } from "@tanstack/react-query";
import { checkHealth } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Activity, CheckCircle2, XCircle, Server } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PageHeader } from "@/components/PageHeader";

export default function Settings() {
  const { data: health, isLoading, refetch } = useQuery({
    queryKey: ["health"],
    queryFn: checkHealth,
    refetchInterval: 10000,
  });

  const isHealthy = health?.status === "ok";

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Settings" 
        description="Configure your orchestration platform"
      />

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            API Health Status
          </CardTitle>
          <CardDescription>Monitor the status of your FastAPI backend</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between rounded-lg border border-border p-4">
            <div className="flex items-center gap-3">
              <Server className="h-8 w-8 text-muted-foreground" />
              <div>
                <p className="font-semibold">MetaCognition API</p>
                <p className="text-sm text-muted-foreground">http://localhost:8000</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {isLoading ? (
                <Badge variant="secondary">Checking...</Badge>
              ) : isHealthy ? (
                <>
                  <CheckCircle2 className="h-5 w-5 text-success" />
                  <Badge className="bg-success">Healthy</Badge>
                </>
              ) : (
                <>
                  <XCircle className="h-5 w-5 text-destructive" />
                  <Badge variant="destructive">Down</Badge>
                </>
              )}
            </div>
          </div>

          <Button onClick={() => refetch()} variant="outline" className="w-full">
            Refresh Status
          </Button>

          {health && (
            <div className="rounded-lg bg-muted p-4">
              <p className="text-sm font-mono">{JSON.stringify(health, null, 2)}</p>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>System Information</CardTitle>
          <CardDescription>Details about your MetaCognition setup</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex justify-between items-center py-2 border-b border-border">
            <span className="text-sm font-medium">Version</span>
            <span className="text-sm text-muted-foreground">v0.3</span>
          </div>
          <div className="flex justify-between items-center py-2 border-b border-border">
            <span className="text-sm font-medium">Backend</span>
            <span className="text-sm text-muted-foreground">FastAPI + Python 3.11</span>
          </div>
          <div className="flex justify-between items-center py-2 border-b border-border">
            <span className="text-sm font-medium">Database</span>
            <span className="text-sm text-muted-foreground">SQLite</span>
          </div>
          <div className="flex justify-between items-center py-2 border-b border-border">
            <span className="text-sm font-medium">Engines</span>
            <span className="text-sm text-muted-foreground">CrewAI, RobotGreenAI</span>
          </div>
          <div className="flex justify-between items-center py-2">
            <span className="text-sm font-medium">Testing</span>
            <span className="text-sm text-muted-foreground">PyTest (TDD)</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
