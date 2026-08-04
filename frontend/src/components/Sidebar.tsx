import React from 'react';
import { 
  LayoutDashboard, 
  Users, 
  Ticket, 
  BrainCircuit, 
  HeartPulse, 
  Sparkles, 
  BarChart3, 
  Bell,
  FileText,
  Settings
} from 'lucide-react';

interface SidebarProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
}

export const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'customers', label: 'Customers', icon: Users },
  { id: 'tickets', label: 'Support Tickets', icon: Ticket },
  { id: 'prediction', label: 'AI Predictions', icon: BrainCircuit },
  { id: 'health', label: 'Customer Health', icon: HeartPulse },
  { id: 'recommendations', label: 'Recommendations', icon: Sparkles },
  { id: 'analytics', label: 'Analytics', icon: BarChart3 },
  { id: 'notifications', label: 'Notifications', icon: Bell },
];

export const Sidebar: React.FC<SidebarProps> = ({ currentTab, setCurrentTab }) => {
  return (
    <aside style={{
      width: '240px',
      background: 'var(--surface)',
      borderRight: '1px solid var(--outline-variant)',
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      position: 'fixed',
      left: 0,
      top: 0,
      zIndex: 50,
      padding: '32px 0'
    }}>
      {/* Brand Header */}
      <div style={{
        padding: '0 24px',
        marginBottom: '40px',
        display: 'flex',
        alignItems: 'center',
        gap: '12px'
      }}>
        <div style={{
          width: '32px',
          height: '32px',
          borderRadius: '6px',
          background: 'var(--primary-container)',
          color: 'var(--on-primary-container)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: 700,
          fontSize: '1rem'
        }}>
          C
        </div>
        <div>
          <h1 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--primary)', letterSpacing: '-0.02em', lineHeight: 1.2 }}>
            ChurnShield
          </h1>
          <span style={{ fontSize: '0.65rem', color: 'var(--on-surface-variant)', textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 600 }}>
            Enterprise AI
          </span>
        </div>
      </div>

      {/* Navigation List */}
      <nav style={{ padding: '0 12px', flex: 1, display: 'flex', flexDirection: 'column', gap: '4px' }}>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentTab(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                width: '100%',
                padding: '10px 16px',
                borderTopRightRadius: '8px',
                borderBottomRightRadius: '8px',
                background: isActive ? 'rgba(197, 163, 88, 0.15)' : 'transparent',
                color: isActive ? 'var(--primary)' : 'var(--on-surface-variant)',
                borderLeft: isActive ? '3px solid var(--primary)' : '3px solid transparent',
                fontWeight: isActive ? 700 : 400,
                fontSize: '0.875rem',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'all 0.15s ease'
              }}
            >
              <Icon size={18} color={isActive ? 'var(--primary)' : 'var(--on-surface-variant)'} />
              {item.label}
            </button>
          );
        })}
      </nav>

      {/* Settings Footer */}
      <div style={{
        padding: '16px 12px 0 12px',
        borderTop: '1px solid var(--outline-variant)'
      }}>
        <button style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          width: '100%',
          padding: '10px 16px',
          borderRadius: '8px',
          background: 'transparent',
          color: 'var(--on-surface-variant)',
          border: 'none',
          fontSize: '0.875rem',
          cursor: 'pointer'
        }}>
          <Settings size={18} color="var(--on-surface-variant)" />
          Settings
        </button>
      </div>
    </aside>
  );
};
