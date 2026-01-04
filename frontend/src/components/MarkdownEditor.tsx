import "@uiw/react-md-editor/markdown-editor.css";
import "@uiw/react-markdown-preview/markdown.css";
import MDEditor from "@uiw/react-md-editor";
import { cn } from "@/lib/utils";

interface MarkdownEditorProps {
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
    className?: string;
    minHeight?: string;
}

export function MarkdownEditor({
    value,
    onChange,
    placeholder,
    className,
    minHeight = "200px",
}: MarkdownEditorProps) {
    return (
        <div className={cn("w-full", className)} data-color-mode="light">
            <MDEditor
                value={value}
                onChange={(val) => onChange(val || "")}
                preview="live"
                height={minHeight}
                textareaProps={{
                    placeholder: placeholder || "Enter markdown text...",
                }}
                previewOptions={{
                    rehypePlugins: [],
                }}
            />
        </div>
    );
}
