import {
  Activity,
  Cpu,
  Github,
  Layers,
  Lock,
  Mail,
} from "lucide-react";

export default function App() {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col font-sans relative overflow-hidden select-none">
      {/* Background ambient glows */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-primary/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-indigo-500/10 rounded-full blur-[120px] pointer-events-none" />

      {/* Header */}
      <header className="px-6 py-4 flex justify-between items-center z-10">
        <div className="flex items-center gap-3">
          <img src="/logo.svg" className="w-8 h-8" alt="Jupiter Sonic Logo" />
          <h1 className="text-base font-semibold tracking-tight text-white font-sans antialiased">
            Jupiter Sonic
          </h1>
        </div>

        <div className="flex items-center gap-3">
          <a
            href="https://github.com/Supan-Roy/Jupiter-Sonic"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#0c1221] border border-border text-xs text-gray-400 hover:text-white hover:border-primary/50 transition-all duration-200"
          >
            <Github size={14} />
            <span>GitHub</span>
          </a>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col justify-center items-center px-6 py-12 z-10 text-center max-w-4xl mx-auto w-full">
        {/* Animated Glow Orb */}
        <div className="relative mb-6">
          <div className="absolute inset-0 bg-gradient-to-tr from-primary to-indigo-600 rounded-full blur-3xl opacity-30 animate-pulse" />
          <img src="/logo.svg" className="relative w-36 h-36 animate-bounce" alt="Jupiter Sonic Logo" style={{ animationDuration: '3s' }} />
        </div>

        {/* Big Coming Soon Text */}
        <h2 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-4">
          <span className="bg-gradient-to-b from-white via-gray-100 to-gray-500 bg-clip-text text-transparent">
            COMING
          </span>{" "}
          <span className="bg-gradient-to-r from-primary via-primary-glow to-indigo-400 bg-clip-text text-transparent drop-shadow-[0_0_20px_rgba(139,92,246,0.3)]">
            SOON
          </span>
        </h2>

        <p className="text-sm md:text-base text-gray-400 max-w-2xl mb-12 leading-relaxed">
          Open-source speech intelligence platform for voice cloning, dubbing, and AI audio pipelines.
        </p>

        <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-6">
          Topics
        </h3>

        {/* Feature Highlights Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 w-full mb-12">
          <div className="glass-card rounded-2xl p-5 text-left flex flex-col gap-3">
            <div className="text-primary-glow bg-primary/10 w-8 h-8 rounded-lg flex items-center justify-center border border-primary/20">
              <Cpu size={16} />
            </div>
            <div>
              <h3 className="text-xs font-bold text-gray-200">Local Inference</h3>
              <p className="text-[11px] text-gray-500 mt-1">
                Zero cloud dependencies. Completely offline, secure execution.
              </p>
            </div>
          </div>

          <div className="glass-card rounded-2xl p-5 text-left flex flex-col gap-3">
            <div className="text-primary-glow bg-primary/10 w-8 h-8 rounded-lg flex items-center justify-center border border-primary/20">
              <Layers size={16} />
            </div>
            <div>
              <h3 className="text-xs font-bold text-gray-200">Modular Pipelines</h3>
              <p className="text-[11px] text-gray-500 mt-1">
                Easily swap model backends (Whisper, XTTS) via standard
                interfaces.
              </p>
            </div>
          </div>

          <div className="glass-card rounded-2xl p-5 text-left flex flex-col gap-3">
            <div className="text-primary-glow bg-primary/10 w-8 h-8 rounded-lg flex items-center justify-center border border-primary/20">
              <Lock size={16} />
            </div>
            <div>
              <h3 className="text-xs font-bold text-gray-200">Privacy First</h3>
              <p className="text-[11px] text-gray-500 mt-1">
                Your data never leaves your system. Enterprise-ready security.
              </p>
            </div>
          </div>

          <div className="glass-card rounded-2xl p-5 text-left flex flex-col gap-3">
            <div className="text-primary-glow bg-primary/10 w-8 h-8 rounded-lg flex items-center justify-center border border-primary/20">
              <Activity size={16} />
            </div>
            <div>
              <h3 className="text-xs font-bold text-gray-200">AI Dubbing Engine</h3>
              <p className="text-[11px] text-gray-500 mt-1">
                Orchestrated forced-alignment, diarization, and TTS synthesis.
              </p>
            </div>
          </div>
        </div>


      </main>

      {/* Footer */}
      <footer className="px-6 py-6 border-t border-border/60 bg-[#040810]/50 backdrop-blur-md flex flex-col sm:flex-row justify-between items-center gap-4 text-xs text-gray-500 font-medium z-10 w-full mt-auto">
        <div className="flex items-center gap-2">
          <span>© {new Date().getFullYear()} Jupiter Sonic Lab</span>
        </div>
        <div className="flex items-center gap-4 flex-wrap justify-center">
          <span className="flex items-center gap-1">
            Developed by <strong className="text-gray-400">Supan Roy</strong>
          </span>
          <span className="text-gray-600">|</span>
          <a
            href="mailto:contact@supanroy.com"
            className="hover:text-primary-glow transition-colors flex items-center gap-1"
          >
            <Mail size={12} /> contact@supanroy.com
          </a>
        </div>
      </footer>
    </div>
  );
}
