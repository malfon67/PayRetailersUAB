import Form from '../components/form';
import { submitFormData, FormData } from '../components/endpoints';
import { useNavigate } from "react-router-dom"; // Importa useNavigate

const FormPage = () => {
  const navigate = useNavigate(); // Inicialitza useNavigate

  const handleFormSubmit = async (formData: FormData) => {

    try {
      const result = await submitFormData(formData);

      const data = result?.data || "Soy Antonia, pregúntame lo que quiras";
      const user_id = result?.user_id || "DEF-10";

      navigate("/chat", { state: { responseAI: data, userID: user_id } });

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