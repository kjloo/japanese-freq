import { lazy, Suspense } from 'react'
import { Routes } from 'react-router'
import { BrowserRouter as Router, Route } from 'react-router-dom'

const Start = lazy(() => import('./components/Start'));

function App() {

  return (
    <div className='app-container'>
      <Router>
        <Suspense fallback={<div>Loading...</div>}>
          <div className='content'>
            <Routes>
              <Route path="/" element={<Start />} />
              <Route path="*" element={<div>Page not found</div>} />
            </Routes>
          </div>
        </Suspense>
      </Router>
    </div>
  )
}

export default App