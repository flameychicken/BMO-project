import { Routes, Route } from 'react-router-dom'
import BMO from './pages/BMO';
import './App.css'

function App() {
  return (
    <Routes>
      <Route path="/" element={<BMO />} />
    </Routes>
  )
}

export default App
