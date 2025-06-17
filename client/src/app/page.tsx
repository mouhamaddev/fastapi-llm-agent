"use client";
import { useState, useRef, useEffect } from "react";

type SummaryLength = "short" | "medium" | "long";

const ALLOWED_EXTENSIONS = [".pdf", ".docx", ".jpg", ".jpeg", ".png"];

export default function Home() {
  const [summaryLength, setSummaryLength] = useState<SummaryLength>("medium");
  const [fileName, setFileName] = useState<string | null>(null);
  const [fullSummary, setFullSummary] = useState("");
  const [displayedText, setDisplayedText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [containerHeight, setContainerHeight] = useState(0);
  const leftSectionRef = useRef<HTMLDivElement>(null);

  const [message, setMessage] = useState<{ type: "warning" | "success"; text: string } | null>(null);

  useEffect(() => {
    if (!fullSummary) {
      setDisplayedText("");
      setIsTyping(false);
      return;
    }

    setDisplayedText("");
    setIsTyping(true);

    let index = 0;
    let accumulated = "";

    const interval = setInterval(() => {
      if (index < fullSummary.length) {
        accumulated += fullSummary.charAt(index);
        setDisplayedText(accumulated);
        index++;
      } else {
        clearInterval(interval);
        setIsTyping(false);
      }
    }, 20);

    return () => clearInterval(interval);
  }, [fullSummary]);

  useEffect(() => {
    function updateHeight() {
      if (leftSectionRef.current) {
        setContainerHeight(leftSectionRef.current.offsetHeight);
      }
    }
    updateHeight();
    window.addEventListener("resize", updateHeight);
    return () => window.removeEventListener("resize", updateHeight);
  }, []);

  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => setMessage(null), 4000);
      return () => clearTimeout(timer);
    }
  }, [message]);

  function validateFileExtension(fileName: string) {
    const ext = fileName.slice(fileName.lastIndexOf(".")).toLowerCase();
    return ALLOWED_EXTENSIONS.includes(ext);
  }

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      if (!validateFileExtension(file.name)) {
        setMessage({ type: "warning", text: "Unsupported file type. Please upload pdf, docx, jpg, jpeg, or png." });
        setFileName(null);
        setDisplayedText("");
        setIsUploading(false);
        return;
      }

      setFileName(file.name);
      setDisplayedText("");
      setIsUploading(true);

      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/documents/upload/?summary_length=${summaryLength}`,
          {
            method: "POST",
            headers: {
              accept: "application/json",
            },
            body: formData,
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Upload failed");
        }

        const data = await response.json();
        setFullSummary(data.summary || "");
        setDisplayedText("");
        setMessage({ type: "success", text: "Summary generated successfully!" });
        setIsUploading(false);
      } catch (err: any) {
        setMessage({ type: "warning", text: "Something went wrong :(" });
        setDisplayedText("");
        setIsUploading(false);
      }
    } else {
      setFileName(null);
      setDisplayedText("");
      setIsUploading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8">
      <h1 className="text-4xl font-bold mb-4 text-gray-900">
        FastAPI Microservice
      </h1>
      <p className="text-gray-600 mb-8 max-w-3xl text-center">
        Upload a document or paste text to generate a summary. Choose your preferred summary length: short, medium, or long.
      </p>

      {message && (
        <div
          className={`mb-6 max-w-6xl w-full rounded-md p-4 text-center font-semibold ${
            message.type === "warning" ? "bg-yellow-200 text-yellow-900" : "bg-green-200 text-green-900"
          }`}
          role="alert"
        >
          {message.text}
        </div>
      )}

      <div className="max-w-6xl w-full bg-white rounded-lg shadow-lg p-4 sm:p-6 md:p-8 flex flex-col md:flex-row gap-4 md:gap-8">
        <div
          ref={leftSectionRef}
          className="flex-1 border-2 border-dashed border-gray-300 rounded-lg p-6 flex flex-col justify-center items-center cursor-pointer hover:border-blue-500 transition-colors"
          onClick={() => fileInputRef.current?.click()}
        >
          <input
            type="file"
            className="hidden"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".pdf,.docx,.jpg,.jpeg,.png"
            disabled={isUploading || isTyping}
          />
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-16 w-16 text-blue-400 mb-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={1.5}
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M12 12v8m0 0l-3-3m3 3l3-3m-3-9v6m0-6l-3 3m3-3l3 3" />
          </svg>
          <p className="text-gray-600 text-center">
            {fileName
              ? `Selected file: ${fileName}`
              : "Click here or drag and drop a file (PDF, DOCX, JPG, PNG)"}
          </p>
        </div>

        <div className="flex-1 flex flex-col">
          {/* Loader */}
          {isUploading && (
            <div className="flex justify-center items-center space-x-2 mb-4">
              <svg
                className="animate-spin h-5 w-5 text-blue-500"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                />
              </svg>
              <span className="text-blue-600 font-semibold">Loading summary...</span>
            </div>
          )}

          <textarea
            className="resize-none border border-gray-300 rounded-md p-4 mb-4 flex-grow text-gray-900"
            style={{ height: containerHeight || 300 }}
            placeholder=""
            value={displayedText}
            onChange={(e) => setDisplayedText(e.target.value)}
            spellCheck={false}
            disabled={isUploading || isTyping}
          />

          <div className="flex gap-4 justify-center">
            {(["short", "medium", "long"] as SummaryLength[]).map((length) => (
              <button
                key={length}
                onClick={() => !isTyping && !isUploading && setSummaryLength(length)}
                disabled={isTyping || isUploading}
                className={`px-4 py-2 rounded-md font-semibold transition-colors
                  ${
                    summaryLength === length
                      ? "bg-blue-500 text-white shadow-md"
                      : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                  }
                  ${(isTyping || isUploading) ? "opacity-50 cursor-not-allowed hover:bg-gray-200" : ""}
                `}
              >
                {length.charAt(0).toUpperCase() + length.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
