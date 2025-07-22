import { ReceiptIndianRupee,LogOut, ChevronLeft, ChevronRight} from "lucide-react";
import React, { useEffect, useState } from "react";

type NavItem = {
  name: string;
  icon: React.ReactElement<any>;
  key: string;
};

type AppSidebarProps = {
  onItemSelect: (key: string) => void;
  navItems: NavItem[];
  onSideBarToggle : () => void;
  sidebarOpen: boolean;
};
export function AppSidebar({onItemSelect, navItems, onSideBarToggle, sidebarOpen } : AppSidebarProps) {

  const [selectedOption, setSelectedOption] = useState("dashboard")
  

  const selectOption = (key: string) => {
    setSelectedOption(key);
  };

  const toggleSideBar = () =>{
    onSideBarToggle();
  }

  useEffect(() => {
    onItemSelect(selectedOption);
  }, [selectedOption, onItemSelect]);


  return (
    <div className={`h-screen fixed z-50 w-64 duration-300 bg-gray-100 dark:bg-gray-900 p-4 shadow-md flex flex-col justify-between transition-all ${sidebarOpen ? "" : "-translate-x-full" } ease-in-out`}>
      <div id="logo-container" className="flex gap-2 justify-center items-center">
        <ReceiptIndianRupee/>
        <h2 className="text-lg font-bold text-gray-800 dark:text-white">TrackMyExpenses</h2>
      </div>
        <ul id="mainLinks" className="flex justify-between flex-col h-1/4">
        {navItems.map(item => {
            const isSelected = item.key === selectedOption;
            return (
              <li
                className={`flex gap-2 justify-start items-center p-2 transition-all rounded-lg cursor-pointer ${
                  isSelected ? "bg-blue-500 text-white" : "hover:bg-gray-200 dark:hover:bg-gray-700"
                }`}
                key={item.key}
                onClick={() => selectOption(item.key)}
              >
                {React.cloneElement(item.icon, {
                  className: `w-5 h-5 ${isSelected ? "text-white" : "text-gray-600 dark:text-gray-300"}`,
                })}
                <h3 className={`font-medium ${isSelected ? "text-white" : ""}`}>{item.name}</h3>
              </li>
            );
          })}
        </ul>

        <div id="logout-button" className="flex gap-2 justify-start items-center p-2 transition-all rounded-lg cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-700">
            <LogOut/>
            <h3>Logout</h3>
        </div>

        <div className="absolute top-[50%] -right-8 bg-gray-100 w-10 rounded-r-xl">
          <button>
          {sidebarOpen ?
          <ChevronRight size={50} strokeWidth="0.8" onClick={toggleSideBar}/>
          :
          <ChevronLeft size={50} strokeWidth="0.8" onClick={toggleSideBar}/>

        }
          </button>
        </div>
    </div>
  );  
}