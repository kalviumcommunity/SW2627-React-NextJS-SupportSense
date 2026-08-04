import React from 'react';
import { Search, Bell, Sparkles } from 'lucide-react';

interface HeaderProps {
  title: string;
  subtitle: string;
}

export const Header: React.FC<HeaderProps> = ({ title, subtitle }) => {
  return (
    <header style={{
      height: '64px',
      padding: '0 32px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      background: 'rgba(250, 249, 244, 0.85)',
      backdropFilter: 'blur(12px)',
      WebkitBackdropFilter: 'blur(12px)',
      borderBottom: '1px solid var(--outline-variant)',
      position: 'sticky',
      top: 0,
      zIndex: 40
    }}>
      {/* Search Bar matching Stitch Design System */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        background: 'var(--surface-container)',
        border: '1px solid var(--outline-variant)',
        padding: '6px 14px',
        borderRadius: '9999px',
        width: '280px'
      }}>
        <Search size={14} color="var(--on-surface-variant)" />
        <input 
          type="text" 
          placeholder="Search accounts..."
          style={{
            background: 'transparent',
            border: 'none',
            outline: 'none',
            color: 'var(--on-surface)',
            fontSize: '0.85rem',
            width: '100%'
          }}
        />
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        {/* Live AI Status Pill */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          background: 'var(--secondary-container)',
          border: '1px solid var(--secondary)',
          padding: '4px 10px',
          borderRadius: '9999px',
          fontSize: '0.75rem',
          color: 'var(--secondary)',
          fontWeight: 600
        }}>
          <Sparkles size={12} /> Model Active (93.5%)
        </div>

        {/* Notification Bell */}
        <button style={{
          background: 'transparent',
          border: 'none',
          color: 'var(--on-surface-variant)',
          cursor: 'pointer',
          padding: '6px',
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <Bell size={18} />
        </button>

        {/* User Profile Avatar matching Stitch */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', paddingLeft: '8px', borderLeft: '1px solid var(--outline-variant)' }}>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            background: 'var(--primary-container)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--on-primary-container)',
            fontWeight: 700,
            fontSize: '0.85rem'
          }}>
            AI
          </div>
          <div>
            <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--on-surface)' }}>Admin Lead</div>
            <div style={{ fontSize: '0.7rem', color: 'var(--on-surface-variant)' }}>ChurnShield Admin</div>
          </div>
        </div>
      </div>
    </header>
  );
};
