// Hover

// import React, { useState, useRef } from 'react';

// const Dropdown = ({ title, icon, children, position = "bottom" }) => {
//   const [isOpen, setIsOpen] = useState(false);
//   const timeoutRef = useRef(null); 

//   const toggleDropdown = () => {
//     setIsOpen(!isOpen);
//   };

//   const handleMouseEnter = () => {
//     clearTimeout(timeoutRef.current); 
//     setIsOpen(true);
//   };

//   const handleMouseLeave = () => {
//     clearTimeout(timeoutRef.current); 
//     timeoutRef.current = setTimeout(() => {
//       setIsOpen(false);
//     }, 300); 
//   };

//   const handleItemClick = () => {
//     setIsOpen(false);
//   };

//   const dropdownPositionClass = position === 'right' ? 'left-full ml-2 top-0' : 'left-0 mt-2';

//   return (
//     <div className="relative">
//       <button 
//         className="px-4 py-2 flex items-center hover:bg-gray-700 transition duration-300"
//         onMouseEnter={handleMouseEnter} 
//         onMouseLeave={handleMouseLeave} 
//       >
//         {title}
//         <span className="ml-2">{icon}</span>
//       </button>
//       {isOpen && (
//         <div 
//           className={`absolute ${dropdownPositionClass} w-48 bg-gray-800 text-white shadow-lg rounded-md z-50`}
//           onMouseEnter={handleMouseEnter} 
//           onMouseLeave={handleMouseLeave} 
//         >
//           {React.Children.map(children, (child) =>
//             React.cloneElement(child, {
//               onClick: () => {
//                 handleItemClick();
//                 if (child.props.onClick) {
//                   child.props.onClick();
//                 }
//               }
//             })
//           )}
//         </div>
//       )}
//     </div>
//   );
// };

// export default Dropdown;


// buttonn

// import React, { useState } from 'react';

// const Dropdown = ({ title, icon, children, position = "bottom" }) => {
//   const [isOpen, setIsOpen] = useState(false);

//   const toggleDropdown = () => {
//     setIsOpen(!isOpen);
//   };

//   const dropdownPositionClass = position === 'right' ? 'left-full ml-2 top-0' : 'left-0 mt-2';

//   return (
//     <div className="relative">
//       <button 
//         className="px-4 py-2 flex items-center hover:bg-gray-700 transition duration-300"
//         onClick={toggleDropdown} // Toggle dropdown on button click for mobile view
//       >
//         {title}
//         <span className="ml-2">{icon}</span>
//       </button>
//       {isOpen && (
//         <div 
//           className={`absolute ${dropdownPositionClass} w-48 bg-gray-800 text-white shadow-lg rounded-md z-50`}
//           onMouseEnter={() => setIsOpen(true)} // Keep dropdown open on hover for desktop view
//           onMouseLeave={() => setIsOpen(false)}
//         >
//           {children}
//         </div>
//       )}
//     </div>
//   );
// };

// export default Dropdown;


//Click And Hide 

import React, { useState, useRef } from 'react';

const Dropdown = ({ title, icon, children, position = "bottom" ,setOpenStatus=()=>{},subMenu=false}) => {
  const [isOpen, setIsOpen] = useState(false);
  const timeoutRef = useRef(null); // Reference to store timeout

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleMouseEnter = () => {
    clearTimeout(timeoutRef.current); // Clear any existing timeout
     setIsOpen(true);

     !subMenu && setOpenStatus(title)
  };

  const handleMouseLeave = () => {
    clearTimeout(timeoutRef.current); // Clear any existing timeout
    timeoutRef.current = setTimeout(() => {
      setIsOpen(false);
    }, 300); // Delay in milliseconds before hiding dropdown
  };

  const handleItemClick = () => {
    setIsOpen(false); // Close dropdown when an item is clicked
  };

  const dropdownPositionClass = position === 'right' ? 'left-full ml-2 top-0' : 'left-0 mt-2';

  return (
    <div className="relative">
      <button style={{ justifyContent:"space-between" ,width:"100%"}}
        className="px-4 py-2 flex items-center  hover:bg-gray-700 transition duration-300"
        onMouseEnter={handleMouseEnter} // Open dropdown on hover
        onMouseLeave={handleMouseLeave} // Close dropdown with delay when mouse leaves
      >
        {title}
        <span className="ml-2">{icon}</span>
      </button>
      {isOpen && (
        <div 
          className={`absolute ${dropdownPositionClass} w-48 bg-gray-800 text-white shadow-lg rounded-md z-50`}
          onMouseEnter={handleMouseEnter} // Keep dropdown open on hover within dropdown area
          onMouseLeave={handleMouseLeave} // Close dropdown with delay when mouse leaves dropdown area
        >
          {React.Children.map(children, (child) =>
            React.cloneElement(child, {
              onClick: () => {
                handleItemClick();
                setOpenStatus();
                if (child.props.onClick) {
                  child.props.onClick();
                }
              }
            })
          )}
        </div>
      )}
    </div>
  );
};

export default Dropdown;


