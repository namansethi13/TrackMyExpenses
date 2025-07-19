import {AppSidebar} from "@/components/AppSidebar";
import { Home, Plus, ChartLineIcon, MessageSquareIcon } from "lucide-react";
import { useState, useEffect } from "react";
import { AddExpense, ChatWithAI, Dashboard, Visualize, Fallback } from "./components/home-screens";

type NavItem = {
  name: string;
  icon: React.ReactElement<any>;
  key: string;
};
export default function App() {
    const [selectedKey, setSelectedKey] = useState("dashboard")
    const [sidebarOpen, setSidebarOpen] = useState(false)
    const [smallScreen, setSmallScreen] = useState(false)

    const navItems : NavItem[] = [
      { name: "Dashboard", icon: <Home />, key: "dashboard" },
      { name: "Add New Expense", icon: <Plus />, key: "expense" },
      { name: "Visualize", icon: <ChartLineIcon />, key: "chart" },
      { name: "Chat with ai", icon: <MessageSquareIcon />, key: "chat" },
    ];
  
  const onItemSelect = (key: string) => {
    setSelectedKey(key)
  }

  useEffect(() => {
  const handleResize = () => {
    if (window.outerWidth >= 768) {
      setSidebarOpen(true);
      setSmallScreen(false);
    } else {
      setSidebarOpen(false);
      setSmallScreen(true);
    }
  };
  handleResize();

  window.addEventListener("resize", handleResize);

  return () => window.removeEventListener("resize", handleResize);
  }, []);

  const onSideBarToggle = () => {
    setSidebarOpen(prev => !prev)
  }
  return (
    <div className="flex w-full h-full">
      <div className={`transition-all ease-in-out duration-300 ${sidebarOpen ? 'w-64' : 'w-0'} ${smallScreen ? "absolute" : ""}`}>
        <AppSidebar
          onItemSelect={onItemSelect}
          navItems={navItems}
          sidebarOpen={sidebarOpen}
          onSideBarToggle={onSideBarToggle}
        />
      </div>
    <div className="flex-1 overflow-auto p-4">
    {
      selectedKey === "dashboard" ? <Dashboard />
      : selectedKey === "expense" ? <AddExpense />
      : selectedKey === "settings" ? <ChatWithAI />
      : selectedKey === "chart" ? <Visualize />
      : selectedKey === "chat" ? <ChatWithAI />
      : <Fallback />
    }
  </div>
    </div>
  );
}