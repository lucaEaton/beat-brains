import React, { useState, useEffect, useRef } from "react";
import { Card, CardContent } from "./ui/card.tsx";
import { Button } from "./ui/button.tsx";

interface ChatMessage {
  content: string;
  sender: "user" | "bot";
}

export const FileUploader: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const API_URL = import.meta.env.VITE_API_URL || "/analyze";
  console.log("API_URL =", API_URL);

  const scrollRef = useRef<HTMLDivElement | null>(null);

  // auto scroll
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const selectedFile = event.target.files[0];
      setFile(selectedFile);
      setMessages([
        { sender: "user", content: `selected file: ${selectedFile.name}` },
        { sender: "bot", content: "ready to analyze. run [Analyze Track] to continue." },
      ]);
    } else {
      setFile(null);
      setMessages([]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", content: "no file detected. select an audio file first." },
      ]);
      return;
    }

    setLoading(true);
    setMessages((prev) => [
      ...prev,
      { sender: "bot", content: "analyzing track. stand by..." },
    ]);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.result) {
        setMessages((prev) => [
          ...prev.slice(0, -1),
          { sender: "bot", content: data.result },
        ]);
      } else {
        const errorContent =
          data.error || "an unknown error occurred during analysis.";
        setMessages((prev) => [
          ...prev.slice(0, -1),
          { sender: "bot", content: `error: ${errorContent}` },
        ]);
      }
    } catch (error) {
      console.error("Fetch error:", error);
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { sender: "bot", content: "network error. could not connect to server." },
      ]);
    } finally {
      setLoading(false);
      setFile(null);
    }
  };

  const renderMessage = (message: ChatMessage, index: number) => {
    const isBot = message.sender === "bot";

    const cardClasses = isBot
      ? "bg-black/80 border border-green-500/60"
      : "bg-emerald-950 border border-emerald-400/70";

    const title = isBot ? "beat-brains" : "user";

    return (
      <div
        key={index}
        className={`max-w-[95%] ${
          isBot ? "self-start" : "self-end"
        } my-1 text-xs sm:text-sm`}
      >
        <Card className={`shadow-md ${cardClasses}`}>
          <CardContent className="p-3">
            <p className="font-mono text-[0.7rem] mb-1 uppercase tracking-wide text-emerald-300/80">
              {title}
            </p>
            <p className="font-mono leading-snug whitespace-pre-wrap break-words">
              {message.content}
            </p>
          </CardContent>
        </Card>
      </div>
    );
  };

  return (
    <div className="flex flex-col gap-4 font-mono text-sm text-green-200">
      {/*status*/}
      <div className="mb-1 text-xs sm:text-sm text-green-400/80">
        <span className="text-emerald-300">&gt;</span>{" "}
        upload audio file and run analysis
        <span className="terminal-cursor" />
      </div>

      {/*chat window*/}
      <div
        ref={scrollRef}
        className="flex flex-col h-80 overflow-y-auto p-4 rounded-lg border border-green-500/40 bg-black/60 space-y-2 scrollbar-thin scrollbar-thumb-emerald-700/70 scrollbar-track-transparent"
      >
        {messages.length === 0 && !loading ? (
          <p className="text-center text-xs sm:text-sm text-green-500/70 italic mt-4">
            no logs yet. attach a track to begin.
          </p>
        ) : (
          messages.map(renderMessage)
        )}

        {loading && (
          <div className="self-start my-1 text-xs sm:text-sm">
            <Card className="shadow-md bg-black/80 border border-green-500/60">
              <CardContent className="p-3">
                <p className="font-mono text-[0.7rem] mb-1 uppercase tracking-wide text-emerald-300/80">
                  beat-brains
                </p>
                <p className="font-mono">
                  processing audio<span className="terminal-cursor" />
                </p>
              </CardContent>
            </Card>
          </div>
        )}
      </div>

      {/*input/button*/}
      <div className="flex flex-col gap-2">
        <input
          type="file"
          accept="audio/*"
          onChange={handleFileChange}
          disabled={loading}
          className="block w-full text-xs sm:text-sm
                     text-emerald-200 bg-black/80 border border-emerald-500/50 rounded-md
                     file:mr-4 file:py-2 file:px-4
                     file:rounded-md file:border-0
                     file:text-xs file:font-mono
                     file:bg-emerald-900/70 file:text-emerald-200
                     hover:file:bg-emerald-700/70
                     focus:outline-none focus:ring-1 focus:ring-emerald-400/80"
        />

        <Button
          onClick={handleUpload}
          disabled={loading || !file}
          className="w-full bg-emerald-500 hover:bg-emerald-400 text-black font-mono border border-emerald-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "Analyzing..." : "Analyze Track"}
        </Button>
      </div>
    </div>
  );
};
