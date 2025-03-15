import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import FormPage from '../pagines/formPage';
import Chat from '../pagines/chat';
const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/form" element={<FormPage />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="*" element={<Navigate to="/form" replace />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;