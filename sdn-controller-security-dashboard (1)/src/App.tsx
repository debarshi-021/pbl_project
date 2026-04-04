import React, { useState, useEffect, useCallback } from 'react';
import { 
  ShieldCheck, 
  ShieldAlert, 
  Usb, 
  Activity, 
  Database, 
  Lock, 
  AlertCircle,
  Clock,
  Terminal,
  X,
  Minus,
  Square
} from 'lucide-react';

// Types for our simulation
interface Device {
  id: string;
  path: string;
  status: 'AUTHENTICATED' | 'REJECTED';
  reason: string;
  verifyTime: number;
}

export default function App() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [status, setStatus] = useState("System Status: Monitoring Active...");

  const simulatePlug = (type: 'TRUSTED' | 'FAKE') => {
    const driveLetter = String.fromCharCode(68 + Math.floor(Math.random() * 5)) + ':';
    if (devices.find(d => d.path === driveLetter)) return;

    setTimeout(() => {
      const newDevice: Device = type === 'TRUSTED' 
        ? { id: 'SW-CORE-001', path: driveLetter, status: 'AUTHENTICATED', reason: 'Signature Valid', verifyTime: 45 }
        : { id: 'SW-CORE-001', path: driveLetter, status: 'REJECTED', reason: 'Signature Invalid', verifyTime: 38 };
      
      setDevices(prev => [...prev, newDevice]);
      setStatus(`System Status: ${devices.length + 1} device(s) monitored.`);
      
      if (type === 'FAKE') {
        alert(`SECURITY ALERT: Unauthorized device detected at ${driveLetter}!\nReason: Signature Invalid`);
      }
    }, 500);
  };

  const simulateUnplug = (path: string) => {
    setDevices(prev => prev.filter(d => d.path !== path));
    setStatus(devices.length <= 1 ? "System Status: No devices connected." : `System Status: ${devices.length - 1} device(s) monitored.`);
  };

  return (
    <div className="h-screen bg-[#d4d0c8] p-4 font-['Tahoma',sans-serif] text-sm select-none">
      {/* Classic Windows Window */}
      <div className="w-full h-full bg-[#d4d0c8] border-2 border-white border-r-[#808080] border-b-[#808080] flex flex-col shadow-[1px_1px_0_0_#000]">
        
        {/* Title Bar */}
        <div className="bg-[#000080] p-1 flex justify-between items-center text-white font-bold">
          <div className="flex items-center gap-2">
            <Usb className="w-4 h-4" />
            <span>SDN Controller Security Dashboard v1.0</span>
          </div>
          <div className="flex gap-1">
            <button className="w-5 h-5 bg-[#d4d0c8] border border-white border-r-[#808080] border-b-[#808080] text-black flex items-center justify-center text-xs font-bold"><Minus className="w-3 h-3" /></button>
            <button className="w-5 h-5 bg-[#d4d0c8] border border-white border-r-[#808080] border-b-[#808080] text-black flex items-center justify-center text-xs font-bold"><Square className="w-3 h-3" /></button>
            <button className="w-5 h-5 bg-[#d4d0c8] border border-white border-r-[#808080] border-b-[#808080] text-black flex items-center justify-center text-xs font-bold"><X className="w-3 h-3" /></button>
          </div>
        </div>

        {/* Menu Bar */}
        <div className="flex gap-4 px-2 py-1 border-b border-[#808080] text-xs">
          <span className="hover:bg-[#000080] hover:text-white px-1 cursor-default">File</span>
          <span className="hover:bg-[#000080] hover:text-white px-1 cursor-default">View</span>
          <span className="hover:bg-[#000080] hover:text-white px-1 cursor-default">Tools</span>
          <span className="hover:bg-[#000080] hover:text-white px-1 cursor-default">Help</span>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-4 flex flex-col gap-4 overflow-hidden">
          <div>
            <h1 className="text-xl font-bold">SDN Controller Security Dashboard</h1>
            <p className="text-xs">TPM-Inspired USB Authentication System</p>
          </div>

          {/* Table Area */}
          <div className="flex-1 bg-white border-2 border-[#808080] border-r-white border-b-white overflow-auto">
            <table className="w-full text-left border-collapse">
              <thead className="sticky top-0 bg-[#d4d0c8] border-b border-[#808080]">
                <tr>
                  <th className="p-1 border-r border-[#808080] font-normal">Device ID</th>
                  <th className="p-1 border-r border-[#808080] font-normal">Drive Path</th>
                  <th className="p-1 border-r border-[#808080] font-normal">Status</th>
                  <th className="p-1 border-r border-[#808080] font-normal">Reason</th>
                  <th className="p-1 font-normal">Verify Time</th>
                </tr>
              </thead>
              <tbody>
                {devices.map((d, i) => (
                  <tr key={i} className="hover:bg-[#000080] hover:text-white group">
                    <td className="p-1 border-r border-[#d4d0c8]">{d.id}</td>
                    <td className="p-1 border-r border-[#d4d0c8]">{d.path}</td>
                    <td className={`p-1 border-r border-[#d4d0c8] font-bold ${d.status === 'AUTHENTICATED' ? 'text-green-700 group-hover:text-green-300' : 'text-red-700 group-hover:text-red-300'}`}>
                      {d.status}
                    </td>
                    <td className="p-1 border-r border-[#d4d0c8]">{d.reason}</td>
                    <td className="p-1 flex justify-between">
                      <span>{d.verifyTime}ms</span>
                      <button onClick={() => simulateUnplug(d.path)} className="text-[10px] text-blue-800 underline group-hover:text-white">Eject</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Simulation Controls (Hidden in real app) */}
          <div className="p-2 border border-[#808080] flex gap-4 items-center bg-[#e4e0d8]">
            <span className="text-[10px] font-bold uppercase text-[#808080]">Hardware Simulation:</span>
            <button onClick={() => simulatePlug('TRUSTED')} className="px-4 py-1 bg-[#d4d0c8] border-2 border-white border-r-[#808080] border-b-[#808080] active:border-[#808080] active:border-r-white active:border-b-white">Plug Trusted USB</button>
            <button onClick={() => simulatePlug('FAKE')} className="px-4 py-1 bg-[#d4d0c8] border-2 border-white border-r-[#808080] border-b-[#808080] active:border-[#808080] active:border-r-white active:border-b-white">Plug Fake USB</button>
          </div>
        </div>

        {/* Status Bar */}
        <div className="bg-[#d4d0c8] border-t border-[#808080] p-1 text-xs flex justify-between">
          <div className="border border-[#808080] border-r-white border-b-white px-2 flex-1">{status}</div>
          <div className="border border-[#808080] border-r-white border-b-white px-4">CAPS</div>
          <div className="border border-[#808080] border-r-white border-b-white px-4">NUM</div>
        </div>
      </div>
    </div>
  );
}
