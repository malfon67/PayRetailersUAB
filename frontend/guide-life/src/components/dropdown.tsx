import React, { useState, useEffect, useRef } from "react";

interface Country {
  name: string;
  code: string;
  subregion: string;
  region: string;
  cities?: { toponymName: string }[];
}

interface DropdownProps {
  id: string;
  label: string;
  value: string;
  onChange: (id: string, value: string) => void;
  type: "country" | "city"; // Determines if it's for countries or cities
  selectedCountry?: string; // Selected country name (required for cities)
}

const Dropdown: React.FC<DropdownProps> = ({ id, label, value, onChange, type, selectedCountry }) => {
  const [options, setOptions] = useState<string[]>([]);
  const [filteredOptions, setFilteredOptions] = useState<string[]>([]); // Filtered options based on input
  const [inputValue, setInputValue] = useState(value);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false); // Controls whether the dropdown is open
  const [hasInteracted, setHasInteracted] = useState(false); // Tracks if the user has interacted with the input
  const isSelectingOption = useRef(false); // Tracks if an option is being selected
  const dropdownRef = useRef<HTMLDivElement>(null); // Ref for the dropdown container

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        if (type === "country") {
          // Fetch countries from latinoAmericanCountries.json
          const response = await fetch("/lib/latinoAmericanCountries.json");
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data: Country[] = await response.json();
          const countryNames = data.map((country) => country.name);
          setOptions(countryNames);
          setFilteredOptions(countryNames); // Initialize filtered options
        } else if (type === "city" && selectedCountry) {
          // Fetch cities from countriesWithCities.json
          const response = await fetch("/lib/countriesWithCities.json");
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data: Country[] = await response.json();
          const country = data.find((country) => country.name === selectedCountry);
          const cityNames = country?.cities?.map((city) => city.toponymName) || [];
          setOptions(cityNames);
          setFilteredOptions(cityNames); // Initialize filtered options
        }
      } catch (error) {
        console.error(`Error loading ${type} options:`, error);
      }
    };

    fetchOptions();
  }, [type, selectedCountry]);

  useEffect(() => {
    // Update the input value when the external `value` changes
    setInputValue(value);

    // Filter options based on the new value
    const filtered = options.filter((option) =>
      option.toLowerCase().includes(value.toLowerCase())
    );
    setFilteredOptions(filtered);

    // Open the dropdown only if the user has interacted with the input
    if (hasInteracted && !isSelectingOption.current && filtered.length > 0) {
      setIsDropdownOpen(true);
    } else {
      setIsDropdownOpen(false);
    }
  }, [value, options, hasInteracted]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setInputValue(newValue);
    setHasInteracted(true); // Mark that the user has interacted with the input

    // Filter options based on the input value
    const filtered = options.filter((option) =>
      option.toLowerCase().includes(newValue.toLowerCase())
    );
    setFilteredOptions(filtered);

    // Open the dropdown if there are matching options
    setIsDropdownOpen(filtered.length > 0);

    // Notify the parent component of the change
    onChange(id, newValue);
  };

  const handleOptionClick = (option: string) => {
    isSelectingOption.current = true; // Mark that an option is being selected
    setInputValue(option); // Update the input value
    setIsDropdownOpen(false); // Close the dropdown

    // Only notify the parent if the value actually changed
    if (option !== value) {
      onChange(id, option);
    }

    // Reset the selection flag after a short delay
    setTimeout(() => {
      isSelectingOption.current = false;
    }, 100);
  };

  const handleInputFocus = () => {
    setHasInteracted(true); // Mark that the user has interacted with the input
    // Open the dropdown only if there are filtered options available
    if (filteredOptions.length > 0) {
      setIsDropdownOpen(true);
    }
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
      setIsDropdownOpen(false); // Close the dropdown if the click is outside
    }
  };

  useEffect(() => {
    // Add event listener for clicks outside the dropdown
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      // Clean up the event listener
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="mb-4 relative" ref={dropdownRef}>
      <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor={id}>
        {label}
      </label>
      <input
        id={id}
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        onFocus={handleInputFocus} // Open the dropdown when the input gains focus
        placeholder={`Escribe o selecciona ${label.toLowerCase()}`}
        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
      />
      {isDropdownOpen && filteredOptions.length > 0 && (
        <ul className="absolute z-10 bg-white border border-gray-300 rounded w-full mt-1 max-h-40 overflow-y-auto">
          {filteredOptions.map((option, index) => (
            <li
              key={index}
              onClick={() => handleOptionClick(option)}
              className="px-4 py-2 cursor-pointer hover:bg-gray-100"
            >
              {option}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Dropdown;