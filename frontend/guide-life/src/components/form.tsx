import React, { useState } from "react";
import Dropdown from "./dropdown";

interface FormProps {
  onSubmit: (formData: FormData) => void;
}

export interface FormData {
  username: string;
  birthday: string;
  country: string;
  city: string;
  sex: string;
  has_sons: boolean;
  num_sons: number;
  civil_state: string;
  employment_status: string; // Nou camp per a l'estat laboral
}

// Mapeo de estado civil según el género
const civilStateMapping: { [key: string]: string[] } = {
  Default: ["Soltero/a", "Casado/a", "Viudo/a", "Con pareja"],
  Male: ["Soltero", "Casado", "Viudo", "Con pareja"],
  Female: ["Soltera", "Casada", "Viuda", "Con pareja"],
};

// Mapeo de equivalencias entre masculino, femenino y genérico
const civilStateEquivalences: { [key: string]: { Male: string; Female: string; Default: string } } = {
  "Soltero/a": { Male: "Soltero", Female: "Soltera", Default: "Soltero/a" },
  Soltero: { Male: "Soltero", Female: "Soltera", Default: "Soltero/a" },
  Soltera: { Male: "Soltero", Female: "Soltera", Default: "Soltero/a" },
  "Casado/a": { Male: "Casado", Female: "Casada", Default: "Casado/a" },
  Casado: { Male: "Casado", Female: "Casada", Default: "Casado/a" },
  Casada: { Male: "Casado", Female: "Casada", Default: "Casado/a" },
  "Viudo/a": { Male: "Viudo", Female: "Viuda", Default: "Viudo/a" },
  Viudo: { Male: "Viudo", Female: "Viuda", Default: "Viudo/a" },
  Viuda: { Male: "Viudo", Female: "Viuda", Default: "Viudo/a" },
  "Con pareja": { Male: "Con pareja", Female: "Con pareja", Default: "Con pareja" },
};

const Form: React.FC<FormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState<FormData>({
    username: "",
    birthday: "",
    country: "",
    city: "",
    sex: "Default", // Estado inicial: "Selecciona tu sexo"
    has_sons: false,
    num_sons: 0,
    civil_state: "",
    employment_status: "", // Estat laboral inicial buit
  });

  const [errors, setErrors] = useState<{ [key: string]: string }>({}); // Track validation errors

  const handleChange = (id: string, value: string | boolean) => {
    setFormData((prevData) => {
      const updatedData = { ...prevData, [id]: value };

      // Actualitzar dinàmicament l'estat civil segons el sexe
      if (id === "sex") {
        const validCivilStates = civilStateMapping[value as string] || [];

        // Si l'estat civil actual té una equivalència, actualitzem-lo
        if (prevData.civil_state in civilStateEquivalences) {
          const equivalentState = civilStateEquivalences[prevData.civil_state][value as 'Male' | 'Female' | 'Default'];
          if (validCivilStates.includes(equivalentState)) {
            updatedData.civil_state = equivalentState; // Assignem l'equivalent
          } else {
            updatedData.civil_state = ""; // Restableix si no és vàlid
          }
        }
      }

      return updatedData;
    });
  };

  const validateForm = () => {
    const newErrors: { [key: string]: string } = {};

    // Check required fields
    if (!formData.username.trim()) newErrors.username = "El nombre y apellido es obligatorio.";
    if (!formData.birthday.trim()) newErrors.birthday = "La fecha de nacimiento es obligatoria.";
    if (!formData.country.trim()) newErrors.country = "El país es obligatorio.";
    if (!formData.city.trim()) newErrors.city = "La ciudad es obligatoria.";
    if (!formData.sex.trim() || formData.sex === "Default")
      newErrors.sex = "El sexo es obligatorio.";
    if (!formData.civil_state.trim()) newErrors.civil_state = "El estado civil es obligatorio.";
    if (!formData.employment_status.trim())
      newErrors.employment_status = "El estado laboral es obligatorio.";

    setErrors(newErrors);

    // Return true if there are no errors
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (validateForm()) {
      onSubmit(formData); // Submit the form if validation passes
    }
  };

  return (
    <form
      className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 w-full max-w-md"
      onSubmit={handleSubmit}
    >
      <h2 className="text-2xl font-bold mb-6 text-gray-800 text-center">Formulario de Usuario</h2>

      {/* Nombre y Apellido */}
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
          Nombre y Apellido
        </label>
        <input
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="username"
          type="text"
          placeholder="Introduce tu nombre y apellido"
          value={formData.username}
          onChange={(e) => handleChange(e.target.id, e.target.value)}
        />
        {errors.username && <p className="text-red-500 text-xs italic">{errors.username}</p>}
      </div>

      {/* Fecha de Nacimiento */}
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="birthday">
          Fecha de Nacimiento
        </label>
        <input
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="birthday"
          type="date"
          value={formData.birthday}
          onChange={(e) => handleChange(e.target.id, e.target.value)}
        />
        {errors.birthday && <p className="text-red-500 text-xs italic">{errors.birthday}</p>}
      </div>

      {/* Estado Laboral */}
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="employment_status">
          Estado Laboral
        </label>
        <input
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="employment_status"
          type="text"
          placeholder="Introduce tu estado laboral"
          value={formData.employment_status}
          onChange={(e) => handleChange(e.target.id, e.target.value)}
        />
        {errors.employment_status && (
          <p className="text-red-500 text-xs italic">{errors.employment_status}</p>
        )}
      </div>

      {/* Dropdown per a Països */}
      <Dropdown
        id="country"
        label="País"
        value={formData.country}
        onChange={(id, value) => handleChange(id, value)}
        type="country"
      />
      {errors.country && <p className="text-red-500 text-xs italic">{errors.country}</p>}

      {/* Dropdown per a Ciutats */}
      <Dropdown
        id="city"
        label="Ciudad"
        value={formData.city}
        onChange={(id, value) => handleChange(id, value)}
        type="city"
        selectedCountry={formData.country} // Nom del país seleccionat
      />
      {errors.city && <p className="text-red-500 text-xs italic">{errors.city}</p>}

      {/* Sexo */}
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="sex">
          Sexo
        </label>
        <select
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="sex"
          value={formData.sex}
          onChange={(e) => handleChange(e.target.id, e.target.value)}
        >
          <option value="Default">Selecciona tu sexo</option>
          <option value="Male">Masculino</option>
          <option value="Female">Femenino</option>
        </select>
        {errors.sex && <p className="text-red-500 text-xs italic">{errors.sex}</p>}
      </div>

      {/* Estado Civil */}
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="civil_state">
          Estado Civil
        </label>
        <select
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="civil_state"
          value={formData.civil_state}
          onChange={(e) => handleChange(e.target.id, e.target.value)}
        >
          <option value="">Selecciona tu estado civil</option>
          {civilStateMapping[formData.sex]?.map((state) => (
            <option key={state} value={state}>
              {state}
            </option>
          ))}
        </select>
        {errors.civil_state && <p className="text-red-500 text-xs italic">{errors.civil_state}</p>}
      </div>

      {/* ¿Tienes Hijos? */}
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="has_sons">
          ¿Tienes hijos?
        </label>
        <input
          id="has_sons"
          type="checkbox"
          checked={formData.has_sons}
          onChange={(e) => handleChange(e.target.id, e.target.checked)}
        />
      </div>

      {/* Número de Hijos */}
      {formData.has_sons && (
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="num_sons">
            Número de Hijos
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="num_sons"
            type="number"
            placeholder="Introduce el número de hijos"
            value={formData.num_sons}
            onChange={(e) => handleChange(e.target.id, e.target.value)}
          />
        </div>
      )}

      {/* Botón de Enviar */}
      <div className="flex items-center justify-between">
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit"
        >
          Enviar
        </button>
      </div>
    </form>
  );
};

export default Form;