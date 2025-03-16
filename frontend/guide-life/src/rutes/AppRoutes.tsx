import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import FormPage from '../pagines/formPage';
import Chat from '../pagines/chat';
import '../index.css';
import { Summary } from '../pagines/summary';

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/form" element={<FormPage />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/summary" element={<Summary />} />
        <Route path="*" element={<Navigate to="/chat" replace />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;