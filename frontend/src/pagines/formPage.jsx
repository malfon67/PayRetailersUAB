import React from 'react';
import Form from '../components/form';

const FormPage = () => {
  const handleFormSubmit = async (formData) => {
    console.log('Form Data:', formData);

    // Envia les dades a una API
    try {
      const response = await fetch('https://api.example.com/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Error en enviar les dades');
      }

      const result = await response.json();
      console.log('Resposta de l\'API:', result);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <Form onSubmit={handleFormSubmit} />
    </div>
  );
};

export default FormPage;