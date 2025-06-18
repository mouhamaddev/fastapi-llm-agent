"use client";
import { useState, useRef, useEffect } from "react";

type SummaryLength = "short" | "medium" | "long";

const ALLOWED_EXTENSIONS = [".pdf", ".docx", ".jpg", ".jpeg", ".png"];

const STORAGE_KEY = "myAppAuth";

interface AuthData {
  uuid: string;
  username: string;
  token: string;
  expiry: number;
}

export default function Home() {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [authUsername, setAuthUsername] = useState("");
  const [authPassword, setAuthPassword] = useState("");
  const [user, setUser] = useState<{ uuid: string; username: string } | null>(null);
  const [token, setToken] = useState<string | null>(null);

  const [summaryLength, setSummaryLength] = useState<SummaryLength>("medium");
  const [fileName, setFileName] = useState<string | null>(null);
  const [fullSummary, setFullSummary] = useState("");
  const [displayedText, setDisplayedText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [registerLoading, setRegisterLoading] = useState(false);
  const [loginLoading, setLoginLoading] = useState(false);

  const [containerHeight, setContainerHeight] = useState(0);
  const leftSectionRef = useRef<HTMLDivElement>(null);

  const [message, setMessage] = useState<{ type: "warning" | "success"; text: string } | null>(null);

  const registerRef = useRef(null);
  const loginRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (showRegister && registerRef.current && !(registerRef.current as HTMLElement).contains(event.target as Node)) {
        setShowRegister(false);
      }
      if (showLogin && loginRef.current && !(loginRef.current as HTMLElement).contains(event.target as Node)) {
        setShowLogin(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showRegister, showLogin]);
  
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const data: AuthData = JSON.parse(saved);
        if (data.expiry > Date.now()) {
          setUser({ uuid: data.uuid, username: data.username });
          setToken(data.token);
          setMessage({ type: "success", text: `Welcome back, ${data.username}!` });
        } else {
          localStorage.removeItem(STORAGE_KEY);
        }
      } catch {
        localStorage.removeItem(STORAGE_KEY);
      }
    }
  }, []);

  async function handleRegister() {
    if (!authUsername || !authPassword) {
      setMessage({ type: "warning", text: "Please fill username and password." });
      return;
    }
  
    setRegisterLoading(true);
  
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: authUsername, password: authPassword }),
      });
  
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Registration failed");
      }
  
      await res.json();
      setMessage({ type: "success", text: "Registered successfully!" });
      await handleLogin(false);
      setShowRegister(false);
    } catch (err: any) {
      setMessage({ type: "warning", text: err.message || "Registration error" });
    } finally {
      setRegisterLoading(false);
    }
  }

  async function handleLogin(showText: boolean = true) {
    if (!authUsername || !authPassword) {
      setMessage({ type: "warning", text: "Please fill username and password." });
      return;
    }

    setLoginLoading(true);

    try {
      const params = new URLSearchParams();
      params.append("username", authUsername);
      params.append("password", authPassword);

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: params.toString(),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Login failed");
      }
      const data = await res.json();
      const authData: AuthData = {
        uuid: "unknown-uuid",
        username: authUsername,
        token: data.access_token,
        expiry: Date.now() + 24 * 60 * 60 * 1000,
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(authData));
      setUser({ uuid: authData.uuid, username: authData.username });
      setToken(authData.token);
      if (showText) {
        setMessage({ type: "success", text: `Logged in successfully.` });
      }
      setShowLogin(false);
      setAuthPassword("");
      // reloadAfterSeconds(1.5);
    } catch (err: any) {
      setMessage({ type: "warning", text: err.message || "Login error" });
    } finally {
      setLoginLoading(false);
    }
  }

  function handleLogout() {
    localStorage.removeItem(STORAGE_KEY);
    setUser(null);
    setToken(null);
    setMessage({ type: "success", text: "Logged out successfully." });
    reloadAfterSeconds(1.5);
  }

  function reloadAfterSeconds(seconds: number) {
    setTimeout(() => {
      window.location.reload();
    }, seconds * 1000);
  }

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
          `${process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"}/documents/upload/?summary_length=${summaryLength}`,
          {
            method: "POST",
            headers: {
              ...(token ? { Authorization: `Bearer ${token}` } : {}),
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
        setMessage({ type: "warning", text: "Something went wrong." });
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
      <div className="relative w-full mb-8 flex flex-col items-center">
        <div className="text-center flex flex-col items-center flex-1">
          <h1 className="text-4xl font-bold mb-4 text-gray-900">
            FastAPI Microservice
          </h1>
          <p className="text-gray-600 mb-8 max-w-3xl">
            Upload a document (PDF, DOCX, or Image) to generate a summary.
          </p>
        </div>
        <div className="absolute top-0 right-0 flex items-center space-x-3">
          {user ? (
            <>
              <button
          className="px-4 py-2 bg-red-400 text-white rounded-md hover:bg-red-500 transition cursor-pointer"
          onClick={handleLogout}
              >
          Logout
              </button>
            </>
          ) : (
            <>
              <button
                className="px-4 py-2 bg-blue-500 text-white text-white rounded-lg shadow-md hover:brightness-110 hover:from-indigo-500 hover:to-blue-700 transition mr-3 cursor-pointer"
                onClick={() => setShowLogin(true)}
              >
                Login
              </button>
              <button
                className="px-4 py-2 bg-blue-500 text-white text-white rounded-lg shadow-md hover:from-green-600 hover:to-teal-700 transition cursor-pointer"
                onClick={() => setShowRegister(true)}
              >
                Register
              </button>
            </>
          )}
        </div>
      </div>

      {showRegister && (
        <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
          <div
            ref={registerRef}
            className="bg-white rounded-md p-6 w-96 space-y-4 relative shadow-2xl transform transition-all duration-300 scale-95 opacity-0 animate-modal"
          >
            <input
              type="text"
              name="new-user-random"
              autoComplete="off"
              placeholder="Username"
              value={authUsername}
              onChange={(e) => setAuthUsername(e.target.value)}
              readOnly
              onFocus={(e) => e.target.removeAttribute("readOnly")}
              className="w-full border border-gray-300 rounded-md p-2 placeholder-gray-500 text-gray-900"
            />
            <input
              type="password"
              name="new-user-random-password"
              autoComplete="off"
              placeholder="Password"
              value={authPassword}
              onChange={(e) => setAuthPassword(e.target.value)}
              readOnly
              onFocus={(e) => e.target.removeAttribute("readOnly")}
              className="w-full border border-gray-300 rounded-md p-2 placeholder-gray-500 text-gray-900"
            />
            <div className="flex justify-end space-x-2">
              <button
                onClick={() => {
                  setShowRegister(false);
                  setAuthPassword("");
                }}
                className="px-4 py-2 text-gray-700 rounded-md bg-gray-200 hover:bg-gray-300 cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={handleRegister}
                disabled={registerLoading}
                className="px-4 py-2 rounded-md bg-blue-500 text-white hover:bg-blue-600 transition cursor-pointer flex items-center justify-center min-w-[100px]"
              >
                {registerLoading ? (
                  <svg
                    className="animate-spin h-5 w-5 text-white"
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
                ) : (
                  "Register"
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {showLogin && (
        <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
          <div
            ref={loginRef}
            className="bg-white rounded-md p-6 w-96 space-y-4 relative shadow-2xl transform transition-all duration-300 scale-95 opacity-0 animate-modal"
          >
            <input
              type="text"
              name="user-random"
              autoComplete="off"
              placeholder="Username"
              value={authUsername}
              onChange={(e) => setAuthUsername(e.target.value)}
              readOnly
              onFocus={(e) => e.target.removeAttribute("readOnly")}
              className="w-full border border-gray-300 rounded-md p-2 placeholder-gray-500 text-gray-900"
            />
            <input
              type="password"
              name="user-random-password"
              autoComplete="off"
              placeholder="Password"
              value={authPassword}
              onChange={(e) => setAuthPassword(e.target.value)}
              readOnly
              onFocus={(e) => e.target.removeAttribute("readOnly")}
              className="w-full border border-gray-300 rounded-md p-2 placeholder-gray-500 text-gray-900"
            />
            <div className="flex justify-end space-x-2">
              <button
                onClick={() => {
                  setShowLogin(false);
                  setAuthPassword("");
                }}
                className="px-4 py-2 text-gray-700 rounded-md bg-gray-200 hover:bg-gray-300 transition cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={handleLogin}
                disabled={loginLoading}
                className="px-4 py-2 rounded-md bg-blue-500 text-white hover:bg-blue-600 transition cursor-pointer flex items-center justify-center min-w-[100px]"
              >
                {loginLoading ? (
                  <svg
                    className="animate-spin h-5 w-5 text-white"
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
                ) : (
                  "Login"
                )}
              </button>
            </div>
          </div>
        </div>
      )}

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
            style={{ height: containerHeight || 250 }}
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
                className={`px-4 py-2 rounded-md font-semibold transition-colors cursor-pointer
                  ${
                    summaryLength === length
                      ? "bg-blue-500 text-white shadow-md"
                      : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                  }
                  ${(isTyping || isUploading) ? "opacity-50 cursor-not-allowed hover:bg-gray-200" : ""}
                `}
              >
                {length.charAt(0).toUpperCase() + length.slice(1.5)}
              </button>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
