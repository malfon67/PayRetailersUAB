import Form from '../components/form';
import { submitFormData, FormData } from '../components/endpoints';
import { useNavigate } from "react-router-dom"; // Importa useNavigate

const FormPage = () => {
  const navigate = useNavigate(); // Inicialitza useNavigate

  const handleFormSubmit = async (formData: FormData) => {
    console.log('Form Data:', formData);

    try {
      navigate("/chat"); // Redirigeix a la pàgina de confirmació
      const result = await submitFormData(formData);
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