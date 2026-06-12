import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { motion, AnimatePresence } from 'motion/react';
import { CheckCircle2, AlertTriangle, X } from 'lucide-react';

interface WSNotification {
  id: string;
  type: string;
  message: string;
  status: string;
  timestamp: Date;
}

export default function NotificationListener() {
  const { user, isAuthenticated } = useAuth();
  const [notifications, setNotifications] = useState<WSNotification[]>([]);

  useEffect(() => {
    if (!isAuthenticated || !user) {
      setNotifications([]);
      return;
    }

    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/api/ws/${user.id}`;

    let socket: WebSocket;
    let reconnectTimeout: any;

    const connectWebSocket = () => {
      console.log(`[WS] Connecting to ${wsUrl}`);
      socket = new WebSocket(wsUrl);

      socket.onopen = () => {
        console.log('[WS] Connection established');
      };

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('[WS] Received data:', data);

          if (data.type === 'form_status_update') {
            const newNotif: WSNotification = {
              id: Math.random().toString(36).substr(2, 9),
              type: data.type,
              message: data.message,
              status: data.status,
              timestamp: new Date()
            };
            setNotifications(prev => [newNotif, ...prev]);

            // Auto close after 10 seconds
            setTimeout(() => {
              setNotifications(prev => prev.filter(n => n.id !== newNotif.id));
            }, 10000);
          }
        } catch (err) {
          console.error('[WS] Error processing message:', err);
        }
      };

      socket.onclose = () => {
        console.log('[WS] Connection closed, retrying in 3s...');
        reconnectTimeout = setTimeout(connectWebSocket, 3000);
      };

      socket.onerror = (err) => {
        console.error('[WS] Socket error:', err);
        socket.close();
      };
    };

    connectWebSocket();

    return () => {
      if (socket) socket.close();
      clearTimeout(reconnectTimeout);
    };
  }, [user, isAuthenticated]);

  const removeNotification = (id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-4 max-w-sm w-full pointer-events-none">
      <AnimatePresence>
        {notifications.map((notif) => (
          <motion.div
            key={notif.id}
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9, y: -20 }}
            className="pointer-events-auto w-full bg-[#181a1f]/95 backdrop-blur-md border border-white/10 rounded-2xl p-5 shadow-2.5xl flex gap-4"
          >
            <div className={`w-10 h-10 rounded-xl shrink-0 flex items-center justify-center ${
              notif.status === 'approved'
                ? 'bg-emerald-500/15 text-emerald-400'
                : 'bg-rose-500/15 text-rose-400'
            }`}>
              {notif.status === 'approved' ? (
                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              ) : (
                <AlertTriangle className="w-5 h-5 text-rose-405" />
              )}
            </div>
            <div className="flex-1 space-y-1">
              <div className="flex justify-between items-start">
                <span className="text-[10px] uppercase font-black tracking-wider text-slate-500">
                  Form Review Updated
                </span>
                <span className="text-[9px] text-slate-500">
                  {notif.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              <p className="text-sm font-bold text-white leading-snug">
                {notif.status === 'approved' ? 'Form Approved!' : 'Form Rejected'}
              </p>
              <p className="text-xs text-slate-400 leading-relaxed">
                {notif.message}
              </p>
            </div>
            <button
              onClick={() => removeNotification(notif.id)}
              className="text-slate-500 hover:text-white transition-colors self-start p-1 cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
