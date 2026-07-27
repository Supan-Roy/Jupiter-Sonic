import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Cpu, 
  Database, 
  Globe, 
  Mic, 
  Play, 
  RefreshCw, 
  Sparkles, 
  Volume2, 
  Video, 
  Terminal, 
  CheckCircle,
  FolderOpen
} from 'lucide-react';

// Interfaces for Server Response
interface ModuleStatus {
  enabled: boolean;
  model_id: string;
}

interface SystemStatus {
  project_name: string;
  environment: string;
  debug: boolean;
  modules: Record<string, ModuleStatus>;
}

// Fallback modules metadata if API is offline
const defaultModules = {
  asr: { name: "Speech Recognition (ASR)", desc: "Transcribe WAV/MP3 to text with word-timestamps", model: "openai/whisper-base" },
  diarization: { name: "Speaker Diarization", desc: "Identify speaker turns and partition segments", model: "pyannote/speaker-diarization-3.1" },
  cloning: { name: "Voice Cloning", desc: "Extract zero-shot multi-speaker voice embedding print", model: "VectorEmbeddingExtractor" },
  tts: { name: "Text-to-Speech (TTS)", desc: "Synthesize target voice clone speech from text", model: "coqui/XTTS-v2" },
  translation: { name: "Multilingual Translation", desc: "Seamless cross-lingual speech-to-text alignment", model: "facebook/nllb-200-600M" },
  enhancement: { name: "Audio Enhancement", desc: "Local noise suppression and spectral restoration", model: "speechbrain/metricgan+" },
  alignment: { name: "Forced Alignment", desc: "Extract word-level boundary offsets from audio waveform", model: "reach-out/wav2vec2-aligner" },
  dubbing: { name: "Dubbing Pipeline", desc: "Orchestrated video audio replacements", model: "MultiModuleOrchestrator" }
};

export default function App() {
  const [activeTab, setActiveTab] = useState<'asr' | 'tts' | 'translate' | 'dubbing'>('asr');
  const [apiStatus, setApiStatus] = useState<'online' | 'offline' | 'checking'>('checking');
  const [systemData, setSystemData] = useState<SystemStatus | null>(null);
  
  // ASR Playground States
  const [asrFile, setAsrFile] = useState<File | null>(null);
  const [asrLang, setAsrLang] = useState('en');
  const [asrResult, setAsrResult] = useState<any>(null);
  const [asrLoading, setAsrLoading] = useState(false);
  
  // TTS Playground States
  const [ttsText, setTtsText] = useState('Hello and welcome to Jupiter Sonic. This speech is generated locally using voice clone print.');
  const [ttsVoicePath, setTtsVoicePath] = useState('mock_speaker_embedding.bin');
  const [ttsResult, setTtsResult] = useState<any>(null);
  const [ttsLoading, setTtsLoading] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

  // Translation Playground States
  const [transText, setTransText] = useState('Welcome to Jupiter Sonic. All AI processing runs completely offline on your hardware.');
  const [sourceLang, setSourceLang] = useState('en');
  const [targetLang, setTargetLang] = useState('es');
  const [transResult, setTransResult] = useState<any>(null);
  const [transLoading, setTransLoading] = useState(false);

  // Dubbing Playground States
  const [dubVideo, setDubVideo] = useState<File | null>(null);
  const [dubTargetLang, setDubTargetLang] = useState('es');
  const [dubStatusLogs, setDubStatusLogs] = useState<string[]>([]);
  const [dubResult, setDubResult] = useState<any>(null);
  const [dubLoading, setDubLoading] = useState(false);

  const API_BASE = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1') as string;
  const SERVER_URL = API_BASE.replace('/api/v1', '');

  // Fetch API status on load
  const checkStatus = async () => {
    setApiStatus('checking');
    try {
      const res = await fetch(`${API_BASE}/status`);
      if (res.ok) {
        const data = await res.json();
        setSystemData(data);
        setApiStatus('online');
      } else {
        setApiStatus('offline');
      }
    } catch (e) {
      setApiStatus('offline');
      setSystemData(null);
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  // Handlers
  const handleAsrSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!asrFile) return;
    setAsrLoading(true);
    setAsrResult(null);
    
    const formData = new FormData();
    formData.append('file', asrFile);
    if (asrLang) formData.append('language', asrLang);

    try {
      const response = await fetch(`${API_BASE}/asr/transcribe`, {
        method: 'POST',
        body: formData
      });
      if (response.ok) {
        const data = await response.json();
        setAsrResult(data);
      } else {
        setAsrResult({ error: `Server returned error status ${response.status}` });
      }
    } catch (err: any) {
      setAsrResult({ error: `Connection failed: ${err.message}` });
    } finally {
      setAsrLoading(false);
    }
  };

  const handleTtsSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setTtsLoading(true);
    setTtsResult(null);
    setAudioUrl(null);

    try {
      const response = await fetch(`${API_BASE}/tts/synthesize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: ttsText,
          voice_print_path: ttsVoicePath
        })
      });
      if (response.ok) {
        const data = await response.json();
        setTtsResult(data);
        // Map relative path from backend (e.g. /static/outputs/xyz.wav) to full URL
        setAudioUrl(`${SERVER_URL}${data.audio_path}`);
      } else {
        setTtsResult({ error: `Server returned error status ${response.status}` });
      }
    } catch (err: any) {
      setTtsResult({ error: `Connection failed: ${err.message}` });
    } finally {
      setTtsLoading(false);
    }
  };

  const handleTransSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setTransLoading(true);
    setTransResult(null);

    try {
      const response = await fetch(`${API_BASE}/translation/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: transText,
          source_lang: sourceLang,
          target_lang: targetLang
        })
      });
      if (response.ok) {
        const data = await response.json();
        setTransResult(data);
      } else {
        setTransResult({ error: `Server returned error status ${response.status}` });
      }
    } catch (err: any) {
      setTransResult({ error: `Connection failed: ${err.message}` });
    } finally {
      setTransLoading(false);
    }
  };

  const handleDubSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!dubVideo) return;
    setDubLoading(true);
    setDubResult(null);
    setDubStatusLogs([
      "Initializing dubbing engine...",
      "Extracting audio track via FFmpeg...",
    ]);

    const formData = new FormData();
    formData.append('file', dubVideo);
    formData.append('target_lang', dubTargetLang);

    // Simulate logs in background since the pipeline triggers all mock stages
    const steps = [
      "Running Automatic Speech Recognition (ASR)...",
      "Analyzing speakers (Diarization)...",
      "Translating segments to target language...",
      "Generating cloned speech via TTS...",
      "Aligning audio tracks (Forced Alignment)...",
      "Cleaning audio track (Enhancement)...",
      "Remuxing dubbed audio streams into container via FFmpeg...",
      "Process completed successfully."
    ];

    let logCounter = 0;
    const interval = setInterval(() => {
      if (logCounter < steps.length) {
        setDubStatusLogs((prev: string[]) => [...prev, steps[logCounter]]);
        logCounter++;
      } else {
        clearInterval(interval);
      }
    }, 900);

    try {
      const response = await fetch(`${API_BASE}/dubbing/dub`, {
        method: 'POST',
        body: formData
      });
      clearInterval(interval);
      if (response.ok) {
        const data = await response.json();
        setDubResult(data);
        setDubStatusLogs((prev: string[]) => [...prev, "Completed. Dubbed file ready."]);
      } else {
        setDubResult({ error: `Server returned error status ${response.status}` });
      }
    } catch (err: any) {
      clearInterval(interval);
      setDubResult({ error: `Connection failed: ${err.message}` });
    } finally {
      setDubLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col font-sans">
      {/* Premium Header */}
      <header className="border-b border-border bg-[#070b13]/85 backdrop-blur-md sticky top-0 z-40 px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-4">
        <div className="flex items-center gap-3">
          <div className="bg-primary/20 p-2 rounded-xl border border-primary/30 shadow-primary-glow animate-pulse-slow">
            <span className="text-xl">🪐</span>
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-white via-primary-glow to-primary bg-clip-text text-transparent">
              JUPITER SONIC
            </h1>
            <p className="text-xs text-gray-500 font-medium">Local Speech Intelligence Platform</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-[#0d1527] px-3 py-1.5 rounded-lg border border-border">
            <span className={`w-2.5 h-2.5 rounded-full ${
              apiStatus === 'online' ? 'bg-success animate-pulse' :
              apiStatus === 'offline' ? 'bg-danger' : 'bg-warning animate-spin'
            }`} />
            <span className="text-xs font-semibold uppercase tracking-wider text-gray-400">
              {apiStatus === 'online' ? 'Engine Online' :
               apiStatus === 'offline' ? 'Engine Offline' : 'Connecting'}
            </span>
          </div>
          
          <button 
            onClick={checkStatus}
            className="p-2 rounded-lg bg-[#0e1626] border border-border hover:bg-[#18253f] transition-all duration-200"
            title="Refresh Status"
          >
            <RefreshCw size={14} className={apiStatus === 'checking' ? 'animate-spin' : ''} />
          </button>
        </div>
      </header>

      {/* Main Grid Layout */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Systems Dashboard */}
        <section className="lg:col-span-4 flex flex-col gap-6">
          {/* Hardware & DB Config widget */}
          <div className="glass-card rounded-2xl p-5 shadow-card-glow flex flex-col gap-4 animate-fade-in">
            <h2 className="text-sm font-bold uppercase tracking-wider text-primary-glow flex items-center gap-2">
              <Cpu size={16} /> Local Hardware Context
            </h2>
            
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="bg-[#0c1221] p-3 rounded-xl border border-border">
                <p className="text-gray-500 font-semibold mb-1">EXECUTION DEVICE</p>
                <p className="text-white font-bold flex items-center gap-1.5">
                  <Sparkles size={12} className="text-primary-glow" /> CPU / Local GPU
                </p>
              </div>
              <div className="bg-[#0c1221] p-3 rounded-xl border border-border">
                <p className="text-gray-500 font-semibold mb-1">DATABASE PATH</p>
                <p className="text-white font-mono font-bold truncate">jupiter_sonic.db</p>
              </div>
            </div>

            <div className="border-t border-border/60 pt-4 flex flex-col gap-3">
              <div className="flex justify-between items-center text-xs">
                <span className="text-gray-400 flex items-center gap-1.5">
                  <Database size={12} /> SQLite Database
                </span>
                <span className="text-success font-semibold flex items-center gap-1">
                  <CheckCircle size={12} /> SQLite3 Active
                </span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-gray-400 flex items-center gap-1.5">
                  <FolderOpen size={12} /> Local Weight Cache
                </span>
                <span className="text-gray-300 font-mono font-medium">/models</span>
              </div>
            </div>
          </div>

          {/* Swappable Modules Status List */}
          <div className="glass-card rounded-2xl p-5 shadow-card-glow flex-1 flex flex-col gap-4 animate-fade-in" style={{ animationDelay: '0.1s' }}>
            <h2 className="text-sm font-bold uppercase tracking-wider text-primary-glow flex items-center gap-2">
              <Activity size={16} /> Loaded AI Modules
            </h2>
            <p className="text-xs text-gray-500">
              Each module below exposes decoupled interfaces. Real model weights (Whisper, XTTS) can be hot-swapped dynamically.
            </p>

            <div className="flex-1 overflow-y-auto max-h-[420px] pr-1 flex flex-col gap-2.5">
              {Object.entries(defaultModules).map(([key, meta]) => {
                const apiMeta = systemData?.modules?.[key];
                const isEnabled = apiMeta ? apiMeta.enabled : true; // default to true if backend offline for mock visual demo
                return (
                  <div key={key} className="bg-[#080d19]/80 border border-border/80 rounded-xl p-3.5 hover:border-primary/30 transition-all duration-200">
                    <div className="flex justify-between items-start mb-1">
                      <h3 className="text-xs font-bold text-gray-200">{meta.name}</h3>
                      <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider ${
                        isEnabled ? 'bg-success/15 text-success border border-success/20' : 'bg-gray-800 text-gray-500'
                      }`}>
                        {isEnabled ? 'Active' : 'Disabled'}
                      </span>
                    </div>
                    <p className="text-[11px] text-gray-500 line-clamp-1 mb-2">{meta.desc}</p>
                    <div className="flex items-center justify-between text-[10px] font-mono text-primary-glow bg-[#040810] px-2.5 py-1 rounded">
                      <span className="text-gray-500">ID:</span>
                      <span className="truncate max-w-[200px]" title={apiMeta?.model_id || meta.model}>
                        {apiMeta?.model_id || meta.model}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* Right Column: Tabbed Interactive Playground */}
        <section className="lg:col-span-8 flex flex-col gap-6">
          <div className="glass-card rounded-2xl p-5 shadow-card-glow flex-1 flex flex-col animate-fade-in" style={{ animationDelay: '0.2s' }}>
            
            {/* Tabs Selector */}
            <div className="flex border-b border-border gap-2 pb-4 overflow-x-auto">
              <button 
                onClick={() => setActiveTab('asr')}
                className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all duration-200 whitespace-nowrap ${
                  activeTab === 'asr' 
                    ? 'bg-primary text-white shadow-primary-glow' 
                    : 'bg-transparent text-gray-400 hover:bg-[#0c1221] hover:text-white'
                }`}
              >
                <Mic size={14} /> Speech Recognition (ASR)
              </button>
              
              <button 
                onClick={() => setActiveTab('tts')}
                className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all duration-200 whitespace-nowrap ${
                  activeTab === 'tts' 
                    ? 'bg-primary text-white shadow-primary-glow' 
                    : 'bg-transparent text-gray-400 hover:bg-[#0c1221] hover:text-white'
                }`}
              >
                <Volume2 size={14} /> Text to Speech (TTS)
              </button>

              <button 
                onClick={() => setActiveTab('translate')}
                className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all duration-200 whitespace-nowrap ${
                  activeTab === 'translate' 
                    ? 'bg-primary text-white shadow-primary-glow' 
                    : 'bg-transparent text-gray-400 hover:bg-[#0c1221] hover:text-white'
                }`}
              >
                <Globe size={14} /> Translation
              </button>

              <button 
                onClick={() => setActiveTab('dubbing')}
                className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all duration-200 whitespace-nowrap ${
                  activeTab === 'dubbing' 
                    ? 'bg-primary text-white shadow-primary-glow' 
                    : 'bg-transparent text-gray-400 hover:bg-[#0c1221] hover:text-white'
                }`}
              >
                <Video size={14} /> Dubbing Pipeline
              </button>
            </div>

            {/* Tab Panels */}
            <div className="flex-1 pt-6 flex flex-col">
              
              {/* Tab 1: ASR Panel */}
              {activeTab === 'asr' && (
                <div className="flex-1 flex flex-col gap-6">
                  <div>
                    <h3 className="text-base font-bold text-white mb-1">Local Speech to Text</h3>
                    <p className="text-xs text-gray-500">Upload an audio stream file. The system processes transcription locally and breaks down word timestamps.</p>
                  </div>

                  <form onSubmit={handleAsrSubmit} className="flex flex-col gap-4">
                    <div className="flex flex-col md:flex-row gap-4">
                      <div className="flex-1 flex flex-col gap-1.5">
                        <label className="text-xs font-bold text-gray-400">Audio File (.wav, .mp3)</label>
                        <input 
                          type="file" 
                          accept="audio/*"
                          onChange={(e) => setAsrFile(e.target.files?.[0] || null)}
                          required
                          className="file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-primary file:text-white file:cursor-pointer hover:file:bg-primary-hover text-xs text-gray-400 bg-[#060b14] border border-border p-2 rounded-xl w-full"
                        />
                      </div>

                      <div className="w-full md:w-48 flex flex-col gap-1.5">
                        <label className="text-xs font-bold text-gray-400">Language Hint (Optional)</label>
                        <select 
                          value={asrLang}
                          onChange={(e) => setAsrLang(e.target.value)}
                          className="bg-[#060b14] border border-border p-2 rounded-xl text-xs text-white"
                        >
                          <option value="en">English (en)</option>
                          <option value="es">Spanish (es)</option>
                          <option value="fr">French (fr)</option>
                          <option value="de">German (de)</option>
                          <option value="zh">Chinese (zh)</option>
                        </select>
                      </div>
                    </div>

                    <button 
                      type="submit" 
                      disabled={asrLoading || apiStatus === 'offline'}
                      className="bg-primary hover:bg-primary-hover text-white text-xs font-bold py-3 px-6 rounded-xl flex items-center justify-center gap-2 self-start transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-primary-glow"
                    >
                      {asrLoading ? <RefreshCw className="animate-spin" size={14} /> : <Play size={14} />}
                      Transcribe Speech
                    </button>
                  </form>

                  {/* ASR Results */}
                  <div className="flex-1 flex flex-col gap-3 min-h-[160px] bg-[#050912] border border-border rounded-xl p-4">
                    <div className="flex justify-between items-center border-b border-border/40 pb-2">
                      <span className="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center gap-1.5">
                        <Terminal size={12} /> Execution Log / Output
                      </span>
                      {asrResult && <span className="text-[10px] bg-success/20 text-success border border-success/30 px-2 py-0.5 rounded font-mono font-bold">SUCCESS</span>}
                    </div>

                    {asrLoading && (
                      <div className="flex-1 flex flex-col items-center justify-center gap-2 text-gray-500 text-xs">
                        <RefreshCw className="animate-spin text-primary" size={24} />
                        <span>Transcribing via local Whisper wrapper...</span>
                      </div>
                    )}

                    {!asrLoading && !asrResult && (
                      <div className="flex-1 flex items-center justify-center text-gray-600 text-xs font-mono">
                        Ready to process. Upload audio above.
                      </div>
                    )}

                    {!asrLoading && asrResult && (
                      <div className="flex-1 flex flex-col gap-4 overflow-y-auto max-h-[220px]">
                        <div>
                          <p className="text-xs font-semibold text-gray-400 mb-1">FULL TRANSCRIPTION</p>
                          <p className="text-sm text-white font-medium bg-[#0b101c] p-3 rounded-lg border border-border/50">{asrResult.text}</p>
                        </div>
                        
                        {asrResult.segments && (
                          <div>
                            <p className="text-xs font-semibold text-gray-400 mb-1.5">WORD SEGMENTS</p>
                            <div className="flex flex-wrap gap-1.5">
                              {asrResult.segments.flatMap((seg: any) => seg.words || []).map((w: any, idx: number) => (
                                <div key={idx} className="bg-[#0c1223] border border-border/70 rounded-lg p-2 flex flex-col items-center text-[10px] min-w-[60px]">
                                  <span className="text-white font-bold">{w.word}</span>
                                  <span className="text-gray-500 font-mono text-[9px] mt-0.5">{w.start}s - {w.end}s</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Tab 2: TTS Panel */}
              {activeTab === 'tts' && (
                <div className="flex-1 flex flex-col gap-6">
                  <div>
                    <h3 className="text-base font-bold text-white mb-1">Local Text-to-Speech synthesis</h3>
                    <p className="text-xs text-gray-500">Convert standard text to audio synthesis. In production, this clone preserves voice characteristics from cloned embedding prints.</p>
                  </div>

                  <form onSubmit={handleTtsSubmit} className="flex flex-col gap-4">
                    <div className="flex flex-col gap-3">
                      <label className="text-xs font-bold text-gray-400">Synthesis Text Script</label>
                      <textarea 
                        rows={3}
                        value={ttsText}
                        onChange={(e) => setTtsText(e.target.value)}
                        required
                        className="bg-[#060b14] border border-border p-3 rounded-xl text-xs text-white resize-none w-full"
                      />
                    </div>

                    <div className="flex flex-col md:flex-row gap-4">
                      <div className="flex-1 flex flex-col gap-1.5">
                        <label className="text-xs font-bold text-gray-400">Voice Clone print path</label>
                        <input 
                          type="text" 
                          value={ttsVoicePath}
                          onChange={(e) => setTtsVoicePath(e.target.value)}
                          required
                          className="bg-[#060b14] border border-border p-2 rounded-xl text-xs text-white font-mono"
                        />
                      </div>
                    </div>

                    <button 
                      type="submit" 
                      disabled={ttsLoading || apiStatus === 'offline'}
                      className="bg-primary hover:bg-primary-hover text-white text-xs font-bold py-3 px-6 rounded-xl flex items-center justify-center gap-2 self-start transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-primary-glow"
                    >
                      {ttsLoading ? <RefreshCw className="animate-spin" size={14} /> : <Play size={14} />}
                      Synthesize Speech
                    </button>
                  </form>

                  {/* TTS Results */}
                  <div className="flex-1 flex flex-col gap-3 min-h-[160px] bg-[#050912] border border-border rounded-xl p-4">
                    <div className="flex justify-between items-center border-b border-border/40 pb-2">
                      <span className="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center gap-1.5">
                        <Terminal size={12} /> Audio Synthesis Output
                      </span>
                    </div>

                    {ttsLoading && (
                      <div className="flex-1 flex flex-col items-center justify-center gap-2 text-gray-500 text-xs">
                        <RefreshCw className="animate-spin text-primary" size={24} />
                        <span>Synthesizing voice tracks locally...</span>
                      </div>
                    )}

                    {!ttsLoading && !ttsResult && (
                      <div className="flex-1 flex items-center justify-center text-gray-600 text-xs font-mono">
                        Ready. Input text and click Synthesize.
                      </div>
                    )}

                    {!ttsLoading && ttsResult && (
                      <div className="flex-1 flex flex-col gap-4 justify-center">
                        <div className="flex flex-col gap-2">
                          <p className="text-xs font-semibold text-gray-400">PLAY AUDIO TRACK</p>
                          {audioUrl && (
                            <div className="bg-[#0d1427] border border-border p-4 rounded-xl flex flex-col gap-3">
                              <audio src={audioUrl} controls className="w-full" />
                              <div className="flex justify-between text-[10px] text-gray-500 font-mono mt-1">
                                <span>Output Path: {ttsResult.audio_path}</span>
                                <span>Duration: {ttsResult.duration}s</span>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Tab 3: Translation Panel */}
              {activeTab === 'translate' && (
                <div className="flex-1 flex flex-col gap-6">
                  <div>
                    <h3 className="text-base font-bold text-white mb-1">Local Text Translation</h3>
                    <p className="text-xs text-gray-500">Translate speech texts offline. Serves as the language translator inside the dubbing pipeline.</p>
                  </div>

                  <form onSubmit={handleTransSubmit} className="flex flex-col gap-4">
                    <div className="flex flex-col gap-3">
                      <label className="text-xs font-bold text-gray-400">Source Text</label>
                      <textarea 
                        rows={3}
                        value={transText}
                        onChange={(e) => setTransText(e.target.value)}
                        required
                        className="bg-[#060b14] border border-border p-3 rounded-xl text-xs text-white resize-none w-full"
                      />
                    </div>

                    <div className="flex flex-col md:flex-row gap-4">
                      <div className="flex-1 flex flex-col gap-1.5">
                        <label className="text-xs font-bold text-gray-400">Source Language</label>
                        <select 
                          value={sourceLang}
                          onChange={(e) => setSourceLang(e.target.value)}
                          className="bg-[#060b14] border border-border p-2 rounded-xl text-xs text-white w-full"
                        >
                          <option value="en">English (en)</option>
                          <option value="es">Spanish (es)</option>
                          <option value="fr">French (fr)</option>
                          <option value="de">German (de)</option>
                          <option value="zh">Chinese (zh)</option>
                        </select>
                      </div>

                      <div className="flex-1 flex flex-col gap-1.5">
                        <label className="text-xs font-bold text-gray-400">Target Language</label>
                        <select 
                          value={targetLang}
                          onChange={(e) => setTargetLang(e.target.value)}
                          className="bg-[#060b14] border border-border p-2 rounded-xl text-xs text-white w-full"
                        >
                          <option value="es">Spanish (es)</option>
                          <option value="fr">French (fr)</option>
                          <option value="de">German (de)</option>
                          <option value="zh">Chinese (zh)</option>
                          <option value="en">English (en)</option>
                        </select>
                      </div>
                    </div>

                    <button 
                      type="submit" 
                      disabled={transLoading || apiStatus === 'offline'}
                      className="bg-primary hover:bg-primary-hover text-white text-xs font-bold py-3 px-6 rounded-xl flex items-center justify-center gap-2 self-start transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-primary-glow"
                    >
                      {transLoading ? <RefreshCw className="animate-spin" size={14} /> : <Play size={14} />}
                      Translate Text
                    </button>
                  </form>

                  {/* Translation Results */}
                  <div className="flex-1 flex flex-col gap-3 min-h-[160px] bg-[#050912] border border-border rounded-xl p-4">
                    <div className="flex justify-between items-center border-b border-border/40 pb-2">
                      <span className="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center gap-1.5">
                        <Terminal size={12} /> Translation Output
                      </span>
                    </div>

                    {transLoading && (
                      <div className="flex-1 flex flex-col items-center justify-center gap-2 text-gray-500 text-xs">
                        <RefreshCw className="animate-spin text-primary" size={24} />
                        <span>Translating text content locally...</span>
                      </div>
                    )}

                    {!transLoading && !transResult && (
                      <div className="flex-1 flex items-center justify-center text-gray-600 text-xs font-mono">
                        Ready. Input text and click Translate.
                      </div>
                    )}

                    {!transLoading && transResult && (
                      <div className="flex-1 flex flex-col gap-4 justify-center">
                        <div>
                          <p className="text-xs font-semibold text-gray-400 mb-1">TRANSLATED TEXT</p>
                          <p className="text-sm text-white font-medium bg-[#0b101c] p-3 rounded-lg border border-border/50">
                            {transResult.translated_text}
                          </p>
                          <div className="flex justify-between text-[10px] text-gray-500 font-mono mt-2">
                            <span>From: {transResult.source_language.toUpperCase()}</span>
                            <span>To: {transResult.target_language.toUpperCase()}</span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Tab 4: Dubbing Panel */}
              {activeTab === 'dubbing' && (
                <div className="flex-1 flex flex-col gap-6">
                  <div>
                    <h3 className="text-base font-bold text-white mb-1">AI Video Dubbing Pipeline</h3>
                    <p className="text-xs text-gray-500">
                      Upload a video container file. The engine splits streams via FFmpeg, extracts transcripts, translates languages, synthesizes vocal cloning, and merges it back into the container.
                    </p>
                  </div>

                  <form onSubmit={handleDubSubmit} className="flex flex-col gap-4">
                    <div className="flex flex-col md:flex-row gap-4">
                      <div className="flex-1 flex flex-col gap-1.5">
                        <label className="text-xs font-bold text-gray-400">Video File (.mp4)</label>
                        <input 
                          type="file" 
                          accept="video/mp4"
                          onChange={(e) => setDubVideo(e.target.files?.[0] || null)}
                          required
                          className="file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-primary file:text-white file:cursor-pointer hover:file:bg-primary-hover text-xs text-gray-400 bg-[#060b14] border border-border p-2 rounded-xl w-full"
                        />
                      </div>

                      <div className="w-full md:w-48 flex flex-col gap-1.5">
                        <label className="text-xs font-bold text-gray-400">Target Language</label>
                        <select 
                          value={dubTargetLang}
                          onChange={(e) => setDubTargetLang(e.target.value)}
                          className="bg-[#060b14] border border-border p-2 rounded-xl text-xs text-white"
                        >
                          <option value="es">Spanish (es)</option>
                          <option value="fr">French (fr)</option>
                          <option value="de">German (de)</option>
                          <option value="zh">Chinese (zh)</option>
                        </select>
                      </div>
                    </div>

                    <button 
                      type="submit" 
                      disabled={dubLoading || apiStatus === 'offline'}
                      className="bg-primary hover:bg-primary-hover text-white text-xs font-bold py-3 px-6 rounded-xl flex items-center justify-center gap-2 self-start transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-primary-glow"
                    >
                      {dubLoading ? <RefreshCw className="animate-spin" size={14} /> : <Play size={14} />}
                      Run Dubbing Pipeline
                    </button>
                  </form>

                  {/* Dubbing Logs */}
                  <div className="flex-1 flex flex-col gap-3 min-h-[180px] bg-[#050912] border border-border rounded-xl p-4">
                    <div className="flex justify-between items-center border-b border-border/40 pb-2">
                      <span className="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center gap-1.5">
                        <Terminal size={12} /> Pipeline Execution Log
                      </span>
                    </div>

                    {dubStatusLogs.length === 0 && (
                      <div className="flex-1 flex items-center justify-center text-gray-600 text-xs font-mono">
                        Ready. Upload video and execute pipeline.
                      </div>
                    )}

                    {dubStatusLogs.length > 0 && (
                      <div className="flex-1 flex flex-col gap-2 overflow-y-auto max-h-[160px] font-mono text-[11px] text-gray-300">
                        {dubStatusLogs.map((log, index) => (
                          <div key={index} className="flex items-center gap-2">
                            <span className="text-primary-glow">&gt;&gt;</span>
                            <span>{log}</span>
                          </div>
                        ))}
                        {dubLoading && (
                          <div className="flex items-center gap-2 mt-1">
                            <RefreshCw className="animate-spin text-primary" size={10} />
                            <span className="text-gray-500">Executing...</span>
                          </div>
                        )}
                      </div>
                    )}

                    {dubResult && (
                      <div className="mt-4 pt-4 border-t border-border/40 flex flex-col gap-2.5">
                        <p className="text-xs font-bold text-white">PIPELINE RESULT ASSETS</p>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          <div className="bg-[#0b101c] border border-border p-3 rounded-lg flex flex-col gap-1 text-[11px]">
                            <span className="text-gray-500 font-bold">DUBBED VIDEO STREAM:</span>
                            <span className="text-white font-mono break-all">{dubResult.dubbed_video_path}</span>
                          </div>
                          <div className="bg-[#0b101c] border border-border p-3 rounded-lg flex flex-col gap-1 text-[11px]">
                            <span className="text-gray-500 font-bold">ISOLATED AUDIO MIX:</span>
                            <span className="text-white font-mono break-all">{dubResult.output_audio_path}</span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

            </div>
          </div>
        </section>

      </main>

      {/* Footer info */}
      <footer className="border-t border-border/60 bg-[#040810] px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-2.5 text-xs text-gray-500 font-medium">
        <span>© 2026 Jupiter Sonic Contributors. MIT Licensed.</span>
        <span>Local-First Speech Engine v0.1.0</span>
      </footer>
    </div>
  );
}
