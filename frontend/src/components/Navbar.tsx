
import { Bell, User} from "lucide-react";

{/* dummy navbar for now */}
export default function Navbar(){
    return (
    <nav className="flex absolute top-0 gap-16 justify-end w-full p-4">

        <div>
            <Bell/>
        </div>

        <div>
            <User/>
        </div>


    </nav>
    )

}