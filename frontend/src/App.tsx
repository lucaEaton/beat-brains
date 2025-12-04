import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card.tsx";
import "./App.css";
import { FileUploader } from "./components/FileUploader.tsx";

function App() {
  return (
    <div className="terminal-bg min-h-screen">

      {/*header*/}
      <div className="w-full border-b border-green-500/50 bg-black/80 px-4 py-5 flex items-center justify-between fixed top-0 left-0 right-0 z-50 shadow-md shadow-green-500/20">
        <div className="flex items-center space-x-2">
          <span className="ml-3 text-green-400 font-mono text-sm tracking-tight">
            Beat Brains Terminal v1.0
          </span>
        </div>
        <div className="flex items-center space-x-6 font-mono text-green-300 text-sm">
          <a
            href="https://github.com/lucaEaton/beat-brains"
            target="_blank"
            className="hover:text-green-200 transition-colors"
          >
            GitHub Repo
          </a>
          <a
            href="https://www.linkedin.com/in/luca-eaton/"
            target="_blank"
            className="hover:text-green-200 transition-colors"
          >
            LinkedIn
          </a>
        </div>
      </div>

      <div className="flex items-center justify-center p-4 pt-36">
        <Card className="terminal-glow w-full max-w-4xl border border-green-500/60 bg-black/80 text-green-300">
          <CardHeader className="border-b border-green-500/40 pb-4">
            <CardTitle className="flex items-center justify-between text-xl sm:text-2xl font-mono tracking-tight">
              <span>&gt; Beat Brains Terminal</span>
              <span className="text-[0.65rem] sm:text-xs text-green-500/80">
                STATUS: <span className="text-emerald-300">IDLE</span>
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-4">
            <FileUploader />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}


export default App;
