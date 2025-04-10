import { useState } from 'react';

const BurgerMenu = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative">
      <button onClick={() => setIsOpen(!isOpen)} className="px-4 py-2 hover:bg-gray-700">
        ☰
      </button>
      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-gray-800 shadow-lg p-4">
          <p>Contact Number: (123) 456-7890</p>
          <p>Email: contact@example.com</p>
        </div>
      )}
    </div>
  );
};

export default BurgerMenu;
