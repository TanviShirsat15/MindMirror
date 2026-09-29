import { Navigate, Route, Routes } from 'react-router-dom'

import AppLayout from '../layouts/AppLayout'
import AuthLayout from '../layouts/AuthLayout'

import LoginPage from '../pages/auth/LoginPage'
import SignUpPage from '../pages/auth/SignUpPage'
import DashboardPage from '../pages/dashboard/DashboardPage'
import JournalPage from '../pages/journal/JournalPage'
import HabitsPage from '../pages/habits/HabitsPage'
import WellBeingAnalysisPage from '../pages/wellbeing/WellBeingAnalysisPage'
import AnalyticsHistoryPage from '../pages/analytics/AnalyticsHistoryPage'
import InsightsPage from '../pages/insights/InsightsPage'
import ProfileSettingsPage from '../pages/settings/ProfileSettingsPage'

export default function AppRoutes() {
  return (
    <Routes>
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignUpPage />} />
      </Route>

      <Route element={<AppLayout />}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/journal" element={<JournalPage />} />
        <Route path="/habits" element={<HabitsPage />} />
        <Route path="/wellbeing" element={<WellBeingAnalysisPage />} />
        <Route path="/analytics" element={<AnalyticsHistoryPage />} />
        <Route path="/insights" element={<InsightsPage />} />
        <Route path="/settings" element={<ProfileSettingsPage />} />
      </Route>
    </Routes>
  )
}