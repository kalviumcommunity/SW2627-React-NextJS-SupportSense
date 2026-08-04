import { useState } from 'react';
import { Sidebar, navItems } from './components/Sidebar';
import { Header } from './components/Header';
import { DashboardView } from './components/DashboardView';
import { CustomersView } from './components/CustomersView';
import { TicketsView } from './components/TicketsView';
import { AIPredictionView } from './components/AIPredictionView';
import { CustomerHealthView } from './components/CustomerHealthView';
import { RecommendationsView } from './components/RecommendationsView';
import { AnalyticsView } from './components/AnalyticsView';
import { NotificationsView } from './components/NotificationsView';

export function App() {
  const [currentTab, setCurrentTab] = useState('dashboard');

  const currentNav = navItems.find(item => item.id === currentTab) || navItems[0];

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <Sidebar currentTab={currentTab} setCurrentTab={setCurrentTab} />

      {/* Main Viewport */}
      <div className="main-viewport">
        {/* Top Header */}
        <Header 
          title={currentNav.label} 
          subtitle={`Stitch Project 12479333125364553402 • ChurnShield Enterprise System`} 
        />

        {/* Dynamic Screen View Content */}
        <main className="content-area">
          {currentTab === 'dashboard' && <DashboardView />}
          {currentTab === 'customers' && <CustomersView />}
          {currentTab === 'tickets' && <TicketsView />}
          {currentTab === 'prediction' && <AIPredictionView />}
          {currentTab === 'health' && <CustomerHealthView />}
          {currentTab === 'recommendations' && <RecommendationsView />}
          {currentTab === 'analytics' && <AnalyticsView />}
          {currentTab === 'notifications' && <NotificationsView />}
        </main>
      </div>
    </div>
  );
}

export default App;
