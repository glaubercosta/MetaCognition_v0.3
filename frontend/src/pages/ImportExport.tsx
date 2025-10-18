import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { exportAgents, importAgents, exportFlows, importFlows, importAgentsFile, importFlowsFile } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Download, Upload, FileJson, FileCode } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { PageHeader } from "@/components/PageHeader";

export default function ImportExport() {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [format, setFormat] = useState<"json" | "yaml">("json");
  const [importData, setImportData] = useState("");
  const [exportedData, setExportedData] = useState("");
  const [agentsFile, setAgentsFile] = useState<File | null>(null);
  const [flowsFile, setFlowsFile] = useState<File | null>(null);

  const exportAgentsMutation = useMutation({
    mutationFn: () => exportAgents(format),
    onSuccess: (data) => {
      setExportedData(data);
      toast({ title: "Agents exported successfully" });
    },
    onError: () => {
      toast({ title: "Failed to export agents", variant: "destructive" });
    },
  });

  const importAgentsMutation = useMutation({
    mutationFn: () => importAgents(importData, format),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["agents"] });
      toast({ title: "Agents imported successfully" });
      setImportData("");
    },
    onError: () => {
      toast({ title: "Failed to import agents", variant: "destructive" });
    },
  });

  const exportFlowsMutation = useMutation({
    mutationFn: () => exportFlows(format),
    onSuccess: (data) => {
      setExportedData(data);
      toast({ title: "Flows exported successfully" });
    },
    onError: () => {
      toast({ title: "Failed to export flows", variant: "destructive" });
    },
  });

  const importFlowsMutation = useMutation({
    mutationFn: () => importFlows(importData, format),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["flows"] });
      toast({ title: "Flows imported successfully" });
      setImportData("");
    },
    onError: () => {
      toast({ title: "Failed to import flows", variant: "destructive" });
    },
  });

  const downloadFile = (content: string, filename: string) => {
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Import / Export" 
        description="Import and export agents and flows"
      />

      <div className="flex items-center gap-4">
        <Label>Format:</Label>
        <Select value={format} onValueChange={(value) => setFormat(value as "json" | "yaml")}>
          <SelectTrigger className="w-[180px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="json">
              <div className="flex items-center gap-2">
                <FileJson className="h-4 w-4" />
                JSON
              </div>
            </SelectItem>
            <SelectItem value="yaml">
              <div className="flex items-center gap-2">
                <FileCode className="h-4 w-4" />
                YAML
              </div>
            </SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Tabs defaultValue="agents" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="agents">Agents</TabsTrigger>
          <TabsTrigger value="flows">Flows</TabsTrigger>
        </TabsList>

        <TabsContent value="agents" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Export Agents</CardTitle>
                <CardDescription>Download all agents as {format.toUpperCase()}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Button
                  onClick={() => exportAgentsMutation.mutate()}
                  disabled={exportAgentsMutation.isPending}
                  className="w-full"
                >
                  <Download className="mr-2 h-4 w-4" />
                  Export Agents
                </Button>
                {exportedData && (
                  <>
                    <Textarea
                      value={exportedData}
                      readOnly
                      className="font-mono text-sm"
                      rows={10}
                    />
                    <Button
                      variant="outline"
                      onClick={() => downloadFile(exportedData, `agents.${format}`)}
                      className="w-full"
                    >
                      <Download className="mr-2 h-4 w-4" />
                      Download File
                    </Button>
                  </>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Import Agents</CardTitle>
                <CardDescription>Upload agents from {format.toUpperCase()}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="agents-file">Upload file</Label>
                  <input id="agents-file" type="file" accept={format === 'json' ? '.json' : '.yaml,.yml'} onChange={(e)=> setAgentsFile(e.target.files?.[0] || null)} />
                  <Button variant="outline" className="w-full" disabled={!agentsFile}
                    onClick={async ()=>{
                      if(!agentsFile) return;
                      await importAgentsFile(agentsFile, format);
                      setAgentsFile(null);
                      queryClient.invalidateQueries({ queryKey: ["agents"] });
                      toast({ title: "Agents imported successfully (file)" });
                    }}>
                    <Upload className="mr-2 h-4 w-4" /> Import Agents (File)
                  </Button>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="import-agents">Paste {format.toUpperCase()} data</Label>
                  <Textarea
                    id="import-agents"
                    value={importData}
                    onChange={(e) => setImportData(e.target.value)}
                    placeholder={`Paste your ${format.toUpperCase()} data here...`}
                    className="font-mono text-sm"
                    rows={10}
                  />
                </div>
                <Button
                  onClick={() => importAgentsMutation.mutate()}
                  disabled={importAgentsMutation.isPending || !importData}
                  className="w-full"
                >
                  <Upload className="mr-2 h-4 w-4" />
                  Import Agents
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="flows" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Export Flows</CardTitle>
                <CardDescription>Download all flows as {format.toUpperCase()}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Button
                  onClick={() => exportFlowsMutation.mutate()}
                  disabled={exportFlowsMutation.isPending}
                  className="w-full"
                >
                  <Download className="mr-2 h-4 w-4" />
                  Export Flows
                </Button>
                {exportedData && (
                  <>
                    <Textarea
                      value={exportedData}
                      readOnly
                      className="font-mono text-sm"
                      rows={10}
                    />
                    <Button
                      variant="outline"
                      onClick={() => downloadFile(exportedData, `flows.${format}`)}
                      className="w-full"
                    >
                      <Download className="mr-2 h-4 w-4" />
                      Download File
                    </Button>
                  </>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Import Flows</CardTitle>
                <CardDescription>Upload flows from {format.toUpperCase()}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="flows-file">Upload file</Label>
                  <input id="flows-file" type="file" accept={format === 'json' ? '.json' : '.yaml,.yml'} onChange={(e)=> setFlowsFile(e.target.files?.[0] || null)} />
                  <Button variant="outline" className="w-full" disabled={!flowsFile}
                    onClick={async ()=>{
                      if(!flowsFile) return;
                      await importFlowsFile(flowsFile, format);
                      setFlowsFile(null);
                      queryClient.invalidateQueries({ queryKey: ["flows"] });
                      toast({ title: "Flows imported successfully (file)" });
                    }}>
                    <Upload className="mr-2 h-4 w-4" /> Import Flows (File)
                  </Button>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="import-flows">Paste {format.toUpperCase()} data</Label>
                  <Textarea
                    id="import-flows"
                    value={importData}
                    onChange={(e) => setImportData(e.target.value)}
                    placeholder={`Paste your ${format.toUpperCase()} data here...`}
                    className="font-mono text-sm"
                    rows={10}
                  />
                </div>
                <Button
                  onClick={() => importFlowsMutation.mutate()}
                  disabled={importFlowsMutation.isPending || !importData}
                  className="w-full"
                >
                  <Upload className="mr-2 h-4 w-4" />
                  Import Flows
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
