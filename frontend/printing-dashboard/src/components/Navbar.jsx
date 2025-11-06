"use client";

export default function Navbar() {
    return (
        <div className="bg-white shadow px-6 py-3 flex justify-between items-center">
            <h1 className="font-semibold text-lg text-gray-700">Printing Dashboard</h1>
            <button
                onClick={() => {
                    localStorage.removeItem("token");
                    window.location.href = "/login";
                }}
                className="text-sm bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
            >
                Logout
            </button>
        </div>
    );
}
