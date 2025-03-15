import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import FormPage from '../pagines/formPage';
import Chat from '../pagines/chat';
import '../index.css';

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/form" element={<FormPage />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="*" element={<Navigate to="/chat" replace />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;