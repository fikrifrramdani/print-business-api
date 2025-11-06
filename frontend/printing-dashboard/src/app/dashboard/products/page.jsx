"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";

export default function ProductsPage() {
    const [products, setProducts] = useState([]);
    const [name, setName] = useState("");
    const [code, setCode] = useState("");
    const [type, setType] = useState("barang");
    const [cost, setCost] = useState("");
    const [sell, setSell] = useState("");
    const [stock, setStock] = useState(0);

    const fetchProducts = async () => {
        const res = await api.get("/products/");
        setProducts(res.data);
    };

    const handleAdd = async (e) => {
        e.preventDefault();
        await api.post("/products/", {
            code,
            name,
            type,
            cost_price: parseFloat(cost),
            sell_price: parseFloat(sell),
            category_id: 1, // sementara default kategori 1
            stock: parseInt(stock),
        });
        setCode("");
        setName("");
        setCost("");
        setSell("");
        setStock(0);
        fetchProducts();
    };

    useEffect(() => {
        fetchProducts();
    }, []);

    return (
        <div>
            <h2 className="text-xl font-semibold mb-4">Daftar Produk</h2>

            <form onSubmit={handleAdd} className="bg-white p-4 rounded shadow mb-6">
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    <input
                        placeholder="Kode Produk"
                        value={code}
                        onChange={(e) => setCode(e.target.value)}
                        className="border p-2 rounded"
                    />
                    <input
                        placeholder="Nama Produk"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className="border p-2 rounded"
                    />
                    <select value={type} onChange={(e) => setType(e.target.value)} className="border p-2 rounded">
                        <option value="barang">Barang</option>
                        <option value="jasa">Jasa</option>
                    </select>
                    <input
                        placeholder="Harga Modal"
                        value={cost}
                        onChange={(e) => setCost(e.target.value)}
                        className="border p-2 rounded"
                    />
                    <input
                        placeholder="Harga Jual"
                        value={sell}
                        onChange={(e) => setSell(e.target.value)}
                        className="border p-2 rounded"
                    />
                    <input
                        placeholder="Stok"
                        value={stock}
                        onChange={(e) => setStock(e.target.value)}
                        className="border p-2 rounded"
                    />
                </div>
                <button
                    type="submit"
                    className="mt-4 bg-blue-600 text-gray px-4 py-2 rounded hover:bg-blue-700"
                >
                    Tambah Produk
                </button>
            </form>

            <table className="w-full bg-white rounded shadow text-sm">
                <thead>
                    <tr className="bg-gray-100 text-left">
                        <th className="p-2">Kode</th>
                        <th className="p-2">Nama</th>
                        <th className="p-2">Tipe</th>
                        <th className="p-2">Modal</th>
                        <th className="p-2">Jual</th>
                        <th className="p-2">Stok</th>
                    </tr>
                </thead>
                <tbody>
                    {products.map((p) => (
                        <tr key={p.id} className="border-t hover:bg-gray-50">
                            <td className="p-2">{p.code}</td>
                            <td className="p-2">{p.name}</td>
                            <td className="p-2">{p.type}</td>
                            <td className="p-2">{p.cost_price}</td>
                            <td className="p-2">{p.sell_price}</td>
                            <td className="p-2">{p.stock}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
