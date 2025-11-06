"use client";
import { useState } from "react";
import api from "@/lib/api";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";

export default function LoginPage() {
    const router = useRouter();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            const params = new URLSearchParams();
            params.append("username", username);
            params.append("password", password);

            const res = await api.post("/auth/login", params, {
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
            });

            localStorage.setItem("token", res.data.access_token);
            router.push("/dashboard");
        } catch (err) {
            console.error(err.response?.data || err.message);
            setError("Login gagal. Periksa username atau password kamu.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-screen items-center justify-center bg-gradient-to-br from-blue-100 to-blue-300">
            <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="bg-white p-10 rounded-2xl shadow-2xl w-96"
            >
                <div className="text-center mb-6">
                    <div className="text-4xl font-extrabold text-blue-600 mb-2">
                        🖨️ Printing App
                    </div>
                    <p className="text-gray-500 text-sm">Masuk ke akun Anda</p>
                </div>

                {error && (
                    <p className="text-red-500 text-sm bg-red-100 py-2 px-3 rounded mb-4 text-center">
                        {error}
                    </p>
                )}

                <form onSubmit={handleLogin}>
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-600 mb-1">
                            Username
                        </label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="w-full border border-gray-300 p-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-600"
                            placeholder="Masukkan username"
                            required
                        />
                    </div>

                    <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-600 mb-1">
                            Password
                        </label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full border border-gray-300 p-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-600"
                            placeholder="Masukkan password"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className={`w-full py-2 rounded-lg text-white font-semibold transition-all ${loading
                            ? "bg-blue-300 cursor-not-allowed"
                            : "bg-blue-600 hover:bg-blue-700"
                            }`}
                    >
                        {loading ? "Memproses..." : "Masuk"}
                    </button>
                </form>
            </motion.div>
        </div>
    );
}
