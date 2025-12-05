import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClientProvider, QueryClient } from '@tanstack/react-query'
import AppLayout from './components/layout/AppLayout'
import Dashboard from './pages/Dashboard'
import AppPage from './pages/AppPage'
import ReviewsPage from './pages/ReviewsPage'
import './App.css'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AppLayout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/apps" element={<AppPage />} />
            <Route path="/reviews" element={<ReviewsPage />} />
          </Routes>
        </AppLayout>
      </Router>
    </QueryClientProvider>
  )
}

export default App
