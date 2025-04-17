import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import Home from './components/Pages/Home';
import Questions from './components/Pages/Questions';
import Navbar from './components/Main/Navbar';
import { ThemeProvider } from './context/ThemeContext';

function App() {
  console.log("App.jsx loaded");
  return (
    <ThemeProvider>
      <Router>
        <div className="min-h-screen flex flex-col">

          <Navbar />
          <div className="flex-grow">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/questions" element={<Questions />} />
              {/* Add other routes here as needed */}
            </Routes>
          </div>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
