import { BrowserRouter as Router } from 'react-router-dom';
import AppRoutes from './Routes/Index';

const App = () => {
  console.log("Hello World");
  return (
    <Router>
      <AppRoutes />
    </Router>
  );
};

export default App;
