// import './index.css';
import { ThemeProvider } from './context/ThemeContext';
import AppRoutes from './Routes/Index'; // Import the central routes

function App() {
  console.log("Dental Report loaded");
  return (
    <ThemeProvider>
      {/* Render the AppRoutes component which handles all routing */}
      <AppRoutes />
    </ThemeProvider>
  );
}

export default App;
