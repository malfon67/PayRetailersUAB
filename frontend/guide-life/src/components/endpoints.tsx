export interface FormData {
    username: string;
    birthday: string;
    country: string;
    city: string;
    sex: string;
    has_sons: boolean;
    num_sons: number;
    civil_state: string;
    employment_status: string; // Afegit camp per a l'estat laboral

  }
  
  const generateRandomUserId = (): string => {
    const randomId = Math.floor(1000 + Math.random() * 9000); // Genera un número aleatori de 4 dígits
    return `user_${randomId}`;
  };
  
  const formatBirthday = (birthday: string): string => {
    const date = new Date(birthday);
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0"); // Els mesos comencen en 0
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  };

  export const submitFormData = async (formData: FormData): Promise<any> => {
    const requestBody = {
      type: "start",
      user_id: generateRandomUserId(), // Genera una user_id aleatòria
      user_data: {
        name: formData.username,
        age: new Date().getFullYear() - new Date(formData.birthday).getFullYear(), // Calcula l'edat
        birthday: formatBirthday(formData.birthday), // Converteix la data al format dd/MM/yyyy
        country: formData.country,
        city: formData.city,
        sex: formData.sex,
        has_sons: formData.has_sons,
        num_sons: formData.num_sons,
        civil_state: formData.civil_state,
        employment_status: formData.employment_status, // Afegit estat laboral
      },
    };
  
    try {
      const response = await fetch("https://f7ae-158-109-94-92.ngrok-free.app/process-input", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });
  
      if (!response.ok) {
        throw new Error("Error en enviar les dades");
      }
  
      const result = await response.json();
      return result;
    } catch (error) {
      console.error("Error:", error);
      throw error;
    }
  };