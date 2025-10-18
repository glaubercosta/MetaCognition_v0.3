import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { getFlows, runOrchestration, type OrchestrationRequest } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { PlayCircle, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { Textarea } from "@/components/ui/textarea";
import { PageHeader } from "@/components/PageHeader";

export default function Orchestration() {
  const { toast } = useToast();
  const [selectedFlow, setSelectedFlow] = useState<string>("");
  const [selectedEngine, setSelectedEngine] = useState<"crewai" | "robotgreen" | "fake">("crewai");
  const [inputs, setInputs] = useState("{}");
  const [result, setResult] = useState<any>(null);

  const { data: flows } = useQuery({
    queryKey: ["flows"],
    queryFn: getFlows,
  });

  const runMutation = useMutation({
    mutationFn: (request: OrchestrationRequest) => runOrchestration(request),
    onSuccess: (data) => {
      setResult(data);
      toast({ title: "Orchestration completed successfully" });
    },
    onError: (error: Error) => {
      toast({ 
        title: "Orchestration failed", 
        description: error.message,
        variant: "destructive" 
      });
    },
  });

  const handleRun = () => {
    if (!selectedFlow) {
      toast({ title: "Please select a flow", variant: "destructive" });
      return;
    }

    let parsedInputs = {};
    try {
      parsedInputs = JSON.parse(inputs);
    } catch {
      toast({ title: "Invalid JSON in inputs", variant: "destructive" });
      return;
    }

    runMutation.mutate({
      flow_id: selectedFlow,
      engine: selectedEngine,
      inputs: parsedInputs,
    });
  };

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Orchestration" 
        description="Execute AI agent flows"
      />

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Configure Execution</CardTitle>
            <CardDescription>Select flow and engine to run orchestration</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="flow">Flow</Label>
              <Select
                value={selectedFlow}
                onValueChange={(value) => setSelectedFlow(value)}
              >
                <SelectTrigger id="flow">
                  <SelectValue placeholder="Select a flow" />
                </SelectTrigger>
                <SelectContent>
                  {flows?.map((flow) => (
                    <SelectItem key={flow.id} value={flow.id!}>
                      {flow.name} ({flow.graph_json?.nodes?.length || 0} nodes)
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="engine">Engine</Label>
              <Select
                value={selectedEngine}
                onValueChange={(value) => setSelectedEngine(value as "crewai" | "robotgreen" | "fake")}
              >
                <SelectTrigger id="engine">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="crewai">CrewAI</SelectItem>
                  <SelectItem value="robotgreen">RobotGreenAI</SelectItem>
                  <SelectItem value="fake">Fake</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="inputs">Inputs (JSON)</Label>
              <Textarea
                id="inputs"
                value={inputs}
                onChange={(e) => setInputs(e.target.value)}
                placeholder='{"key": "value"}'
                className="font-mono text-sm"
                rows={5}
              />
            </div>

            <Button 
              onClick={handleRun} 
              disabled={runMutation.isPending || !selectedFlow}
              className="w-full"
            >
              {runMutation.isPending ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Running...
                </>
              ) : (
                <>
                  <PlayCircle className="mr-2 h-4 w-4" />
                  Run Orchestration
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Execution Result</CardTitle>
            <CardDescription>Output from the orchestration engine</CardDescription>
          </CardHeader>
          <CardContent>
            {runMutation.isPending ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : result ? (
              <div className="space-y-4">
                <div>
                  <Label className="text-xs text-muted-foreground">Duration</Label>
                  <p className="text-lg font-semibold">{result.duration_ms ?? "-"}ms</p>
                </div>
                <div>
                  <Label className="text-xs text-muted-foreground">Engine</Label>
                  <p className="text-lg font-semibold">{result.engine}</p>
                </div>
                <div>
                  <Label className="text-xs text-muted-foreground">Result</Label>
                  <pre className="mt-2 rounded-lg bg-muted p-4 text-sm overflow-x-auto">
                    {JSON.stringify(result.plan ?? result.result ?? result, null, 2)}
                  </pre>
                </div>
                {result.logs && (
                  <div>
                    <Label className="text-xs text-muted-foreground">Logs</Label>
                    <pre className="mt-2 rounded-lg bg-muted p-4 text-sm overflow-x-auto">
                      {JSON.stringify(result.logs, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center justify-center py-12 text-muted-foreground">
                No execution results yet
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
