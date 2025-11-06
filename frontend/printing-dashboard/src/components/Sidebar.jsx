"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { FaBox, FaUsers, FaCog, FaHome } from "react-icons/fa";

export default function Sidebar() {
    const path = usePathname();

    const menus = [
        { name: "Dashboard", path: "/dashboard", icon: <FaHome /> },
        { name: "Produk", path: "/dashboard/products", icon: <FaBox /> },
        { name: "Pengguna", path: "/dashboard/users", icon: <FaUsers /> },
        { name: "Pengaturan", path: "/dashboard/settings", icon: <FaCog /> },
    ];

    return (
        <div className="w-64 bg-blue-700 text-white min-h-screen p-5">
            <h2 className="text-xl font-bold mb-8 text-center">📇 Printing</h2>
            <ul>
                {menus.map((menu) => (
                    <li key={menu.path} className="mb-3">
                        <Link
                            href={menu.path}
                            className={`flex items-center gap-3 px-3 py-2 rounded-md ${path === menu.path ? "bg-blue-500" : "hover:bg-blue-600"
                                }`}
                        >
                            {menu.icon}
                            {menu.name}
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}
