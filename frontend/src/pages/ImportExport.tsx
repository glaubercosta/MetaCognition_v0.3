import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
  exportAgents,
  exportFlows,
  importAgents,
  importAgentsFile,
  importFlows,
  importFlowsFile,
  validateAgentPayload,
  validateFlowPayload,
  convertAgentMarkdown,
} from "@/lib/api";
import { PageHeader } from "@/components/PageHeader";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  Download,
  Upload,
  FileJson,
  FileCode,
  ShieldAlert,
  Sparkles,
  FileText,
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

type SupportedFormat = "json" | "yaml";

interface ValidationState {
  errors: string[];
  message?: string;
  lastCheckedAt?: number;
}

const DEFAULT_MARKDOWN_SAMPLE = `---
name: Example Agent
role: Helpful assistant
---
You are responsible for summarizing the provided context into bullet points.
`;

const formatLabel: Record<SupportedFormat, string> = {
  json: "JSON",
  yaml: "YAML",
};

const iconByFormat: Record<SupportedFormat, JSX.Element> = {
  json: <FileJson className="h-4 w-4" />,
  yaml: <FileCode className="h-4 w-4" />,
};

export default function ImportExport() {
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const [format, setFormat] = useState<SupportedFormat>("json");
  const [agentsData, setAgentsData] = useState("");
  const [flowsData, setFlowsData] = useState("");
  const [agentsFile, setAgentsFile] = useState<File | null>(null);
  const [flowsFile, setFlowsFile] = useState<File | null>(null);
  const [exportedAgents, setExportedAgents] = useState("");
  const [exportedFlows, setExportedFlows] = useState("");
  const [agentValidation, setAgentValidation] = useState<ValidationState>({ errors: [] });
  const [flowValidation, setFlowValidation] = useState<ValidationState>({ errors: [] });
  const [markdownSource, setMarkdownSource] = useState(DEFAULT_MARKDOWN_SAMPLE);
  const [markdownResult, setMarkdownResult] = useState("");
  const [markdownErrors, setMarkdownErrors] = useState<string[]>([]);

  const downloadFile = (content: string, filename: string) => {
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const exportAgentsMutation = useMutation({
    mutationFn: () => exportAgents(format),
    onSuccess: (data: string) => {
      setExportedAgents(data);
      toast({ title: "Agents exported successfully" });
    },
    onError: (error: Error) => {
      toast({ title: "Failed to export agents", description: error.message, variant: "destructive" });
    },
  });

  const exportFlowsMutation = useMutation({
    mutationFn: () => exportFlows(format),
    onSuccess: (data: string) => {
      setExportedFlows(data);
      toast({ title: "Flows exported successfully" });
    },
    onError: (error: Error) => {
      toast({ title: "Failed to export flows", description: error.message, variant: "destructive" });
    },
  });

  const validateAgents = async () => {
    if (!agentsData.trim()) {
      throw new Error("Provide agent data before validating.");
    }
    const result = await validateAgentPayload(agentsData, format);
    setAgentValidation({ errors: result.errors, message: result.message, lastCheckedAt: Date.now() });
    return result.ok;
  };

  const validateFlows = async () => {
    if (!flowsData.trim()) {
      throw new Error("Provide flow data before validating.");
    }
    const result = await validateFlowPayload(flowsData, format);
    setFlowValidation({ errors: result.errors, message: result.message, lastCheckedAt: Date.now() });
    return result.ok;
  };

  const validateAgentsMutation = useMutation({
    mutationFn: validateAgents,
    onSuccess: (ok) => {
      if (ok) {
        toast({ title: "Agent payload looks good!" });
      } else {
        toast({
          title: "Agent payload has issues",
          description: "Review the errors highlighted below.",
          variant: "destructive",
        });
      }
    },
    onError: (error: Error) => {
      toast({ title: "Validation failed", description: error.message, variant: "destructive" });
    },
  });

  const validateFlowsMutation = useMutation({
    mutationFn: validateFlows,
    onSuccess: (ok) => {
      if (ok) {
        toast({ title: "Flow payload looks good!" });
      } else {
        toast({
          title: "Flow payload has issues",
          description: "Review the errors highlighted below.",
          variant: "destructive",
        });
      }
    },
    onError: (error: Error) => {
      toast({ title: "Validation failed", description: error.message, variant: "destructive" });
    },
  });

  const importAgentsMutation = useMutation({
    mutationFn: async () => {
      const ok = await validateAgents();
      if (!ok) {
        throw new Error("Agent payload failed validation.");
      }
      return importAgents(agentsData, format);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["agents"] });
      toast({ title: "Agents imported successfully" });
      setAgentsData("");
      setAgentValidation({ errors: [] });
    },
    onError: (error: Error) => {
      toast({ title: "Failed to import agents", description: error.message, variant: "destructive" });
    },
  });

  const importFlowsMutation = useMutation({
    mutationFn: async () => {
      const ok = await validateFlows();
      if (!ok) {
        throw new Error("Flow payload failed validation.");
      }
      return importFlows(flowsData, format);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["flows"] });
      toast({ title: "Flows imported successfully" });
      setFlowsData("");
      setFlowValidation({ errors: [] });
    },
    onError: (error: Error) => {
      toast({ title: "Failed to import flows", description: error.message, variant: "destructive" });
    },
  });

  const importAgentsFileMutation = useMutation({
    mutationFn: () => {
      if (!agentsFile) throw new Error("Select a file before importing.");
      return importAgentsFile(agentsFile, format);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["agents"] });
      toast({ title: "Agents imported successfully (file)" });
      setAgentsFile(null);
    },
    onError: (error: Error) => {
      toast({ title: "File import failed", description: error.message, variant: "destructive" });
    },
  });

  const importFlowsFileMutation = useMutation({
    mutationFn: () => {
      if (!flowsFile) throw new Error("Select a file before importing.");
      return importFlowsFile(flowsFile, format);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["flows"] });
      toast({ title: "Flows imported successfully (file)" });
      setFlowsFile(null);
    },
    onError: (error: Error) => {
      toast({ title: "File import failed", description: error.message, variant: "destructive" });
    },
  });

  const convertMarkdownMutation = useMutation({
    mutationFn: () => {
      if (!markdownSource.trim()) {
        throw new Error("Provide markdown content to convert.");
      }
      return convertAgentMarkdown(markdownSource);
    },
    onSuccess: (result) => {
      if (result.ok) {
        setMarkdownResult(JSON.stringify(result.agent, null, 2));
        setMarkdownErrors([]);
        toast({ title: "Markdown converted successfully" });
      } else {
        setMarkdownResult("");
        setMarkdownErrors(result.errors);
        toast({
          title: "Conversion returned validation errors",
          description: "Review the issues listed below.",
          variant: "destructive",
        });
      }
    },
    onError: (error: Error) => {
      toast({ title: "Conversion failed", description: error.message, variant: "destructive" });
    },
  });

  const renderValidationAlert = (state: ValidationState, entity: "Agent" | "Flow") => {
    if (!state.errors.length) {
      return null;
    }
    return (
      <Alert variant="destructive">
        <ShieldAlert className="h-4 w-4" />
        <AlertTitle>{entity} validation issues</AlertTitle>
        <AlertDescription>
          <ul className="list-disc pl-4 text-sm">
            {state.errors.map((error, index) => (
              <li key={`${entity}-error-${index}`}>{error}</li>
            ))}
          </ul>
        </AlertDescription>
      </Alert>
    );
  };

  const renderMarkdownAlert = () => {
    if (!markdownErrors.length) return null;
    return (
      <Alert variant="destructive">
        <ShieldAlert className="h-4 w-4" />
        <AlertTitle>Markdown conversion errors</AlertTitle>
        <AlertDescription>
          <ul className="list-disc pl-4 text-sm">
            {markdownErrors.map((error, index) => (
              <li key={`markdown-error-${index}`}>{error}</li>
            ))}
          </ul>
        </AlertDescription>
      </Alert>
    );
  };

  return (
    <div className="space-y-6">
      <PageHeader title="Import / Export" description="Validate, import and export agents and flows" />

      <div className="flex flex-wrap items-center gap-4">
        <Label>Format:</Label>
        <Select
          value={format}
          onValueChange={(value) => {
            setFormat(value as SupportedFormat);
            setAgentValidation({ errors: [] });
            setFlowValidation({ errors: [] });
          }}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {(Object.keys(formatLabel) as SupportedFormat[]).map((value) => (
              <SelectItem key={value} value={value}>
                <div className="flex items-center gap-2">
                  {iconByFormat[value]}
                  {formatLabel[value]}
                </div>
              </SelectItem>
            ))}
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
                <CardDescription>Download a {formatLabel[format]} snapshot</CardDescription>
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
                {exportedAgents && (
                  <>
                    <Textarea
                      value={exportedAgents}
                      readOnly
                      className="font-mono text-sm"
                      rows={12}
                    />
                    <Button
                      variant="outline"
                      onClick={() => downloadFile(exportedAgents, `agents.${format}`)}
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
                <CardDescription>Validate and load agents from {formatLabel[format]}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="agents-file">Upload file</Label>
                  <input
                    id="agents-file"
                    type="file"
                    accept={format === "json" ? ".json" : ".yaml,.yml"}
                    onChange={(event) => setAgentsFile(event.target.files?.[0] ?? null)}
                  />
                  <Button
                    variant="outline"
                    className="w-full"
                    disabled={!agentsFile || importAgentsFileMutation.isPending}
                    onClick={() => importAgentsFileMutation.mutate()}
                  >
                    <Upload className="mr-2 h-4 w-4" />
                    Import Agents (File)
                  </Button>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="import-agents">Paste {formatLabel[format]} data</Label>
                  <Textarea
                    id="import-agents"
                    value={agentsData}
                    onChange={(event) => setAgentsData(event.target.value)}
                    placeholder={`Paste your ${formatLabel[format]} agents payload here...`}
                    className="font-mono text-sm"
                    rows={10}
                  />
                </div>

                {renderValidationAlert(agentValidation, "Agent")}

                <div className="flex flex-wrap gap-2">
                  <Button
                    variant="secondary"
                    onClick={() => validateAgentsMutation.mutate()}
                    disabled={validateAgentsMutation.isPending || !agentsData.trim()}
                  >
                    <Sparkles className="mr-2 h-4 w-4" />
                    Validate Agents
                  </Button>
                  <Button
                    onClick={() => importAgentsMutation.mutate()}
                    disabled={importAgentsMutation.isPending || !agentsData.trim()}
                    className="flex-1"
                  >
                    <Upload className="mr-2 h-4 w-4" />
                    Import Agents
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="flows" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Export Flows</CardTitle>
                <CardDescription>Download a {formatLabel[format]} snapshot</CardDescription>
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
                {exportedFlows && (
                  <>
                    <Textarea
                      value={exportedFlows}
                      readOnly
                      className="font-mono text-sm"
                      rows={12}
                    />
                    <Button
                      variant="outline"
                      onClick={() => downloadFile(exportedFlows, `flows.${format}`)}
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
                <CardDescription>Validate and load flows from {formatLabel[format]}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="flows-file">Upload file</Label>
                  <input
                    id="flows-file"
                    type="file"
                    accept={format === "json" ? ".json" : ".yaml,.yml"}
                    onChange={(event) => setFlowsFile(event.target.files?.[0] ?? null)}
                  />
                  <Button
                    variant="outline"
                    className="w-full"
                    disabled={!flowsFile || importFlowsFileMutation.isPending}
                    onClick={() => importFlowsFileMutation.mutate()}
                  >
                    <Upload className="mr-2 h-4 w-4" />
                    Import Flows (File)
                  </Button>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="import-flows">Paste {formatLabel[format]} data</Label>
                  <Textarea
                    id="import-flows"
                    value={flowsData}
                    onChange={(event) => setFlowsData(event.target.value)}
                    placeholder={`Paste your ${formatLabel[format]} flows payload here...`}
                    className="font-mono text-sm"
                    rows={10}
                  />
                </div>

                {renderValidationAlert(flowValidation, "Flow")}

                <div className="flex flex-wrap gap-2">
                  <Button
                    variant="secondary"
                    onClick={() => validateFlowsMutation.mutate()}
                    disabled={validateFlowsMutation.isPending || !flowsData.trim()}
                  >
                    <Sparkles className="mr-2 h-4 w-4" />
                    Validate Flows
                  </Button>
                  <Button
                    onClick={() => importFlowsMutation.mutate()}
                    disabled={importFlowsMutation.isPending || !flowsData.trim()}
                    className="flex-1"
                  >
                    <Upload className="mr-2 h-4 w-4" />
                    Import Flows
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Convert Agent Markdown
          </CardTitle>
          <CardDescription>
            Paste a Markdown file with YAML front-matter and convert it to a valid agent payload.
          </CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="markdown-source">Markdown</Label>
            <Textarea
              id="markdown-source"
              value={markdownSource}
              onChange={(event) => setMarkdownSource(event.target.value)}
              className="font-mono text-sm"
              rows={14}
            />
            <div className="flex flex-wrap gap-2">
              <Button
                onClick={() => convertMarkdownMutation.mutate()}
                disabled={convertMarkdownMutation.isPending}
              >
                <Sparkles className="mr-2 h-4 w-4" />
                Convert to JSON
              </Button>
              <Button
                variant="ghost"
                onClick={() => {
                  setMarkdownSource(DEFAULT_MARKDOWN_SAMPLE);
                  setMarkdownResult("");
                  setMarkdownErrors([]);
                }}
              >
                Reset sample
              </Button>
            </div>
            {renderMarkdownAlert()}
          </div>

          <div className="space-y-2">
            <Label htmlFor="markdown-result">Generated JSON</Label>
            <Textarea
              id="markdown-result"
              value={markdownResult}
              readOnly
              placeholder="Run the conversion to preview the generated agent payload..."
              className="font-mono text-sm"
              rows={14}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
