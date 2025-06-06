import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

type Lista = {
  idLista: string;
  nomeLista: string;
};

const GerarRelatorio = () => {
  const [listas, setListas] = useState<Lista[]>([]);
  const [listaSelecionada, setListaSelecionada] = useState<Lista | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchListas = async () => {
      try {
        const response = await fetch("http://localhost:5000/listas/getTodasAsListas/");
        if (!response.ok) throw new Error("Erro ao buscar listas");

        const data = await response.json();

        console.log("Listas:", data);
        setListas(data);
      } catch (error) {
        console.error("Erro ao buscar listas:", error);
      }
    };

    fetchListas();
  }, []);

  const handleSelecionar = (lista: Lista) => {
    setListaSelecionada(lista);
  };

  const handleAvancar = () => {
    if (listaSelecionada) {
      navigate(`/gerar-relatorio/${listaSelecionada.idLista}`);
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex"
      style={{ backgroundImage: "url('/assets/fundo.png')" }}
    >
      <div className="w-1/5 bg-white-800 text-white flex items-center justify-center p-4">
        <Link to="/">
          <img
            src="/assets/logocogel.jpg"
            alt="COGEL Logo"
            className="w-32 h-auto"
          />
        </Link>
      </div>

      <div className="w-4/5 p-8 bg-white rounded-l-lg shadow-md">
        <h1 className="text-xl font-bold text-black mb-4">Gerar Relatório</h1>
        <p className="text-black mb-4">Selecione uma lista</p>

        <div className="bg-gray-100 h-60 overflow-y-auto rounded-md p-4 mb-6">
          {listas.length > 0 ? (
            <ul className="space-y-2">
              {listas.map((lista) => (
                <li
                  key={lista.idLista}
                  className={`p-3 rounded cursor-pointer border ${
                    listaSelecionada?.idLista === lista.idLista
                      ? "bg-[#007BB4] text-white"
                      : "bg-white hover:bg-gray-200 text-black"
                  }`}
                  onClick={() => handleSelecionar(lista)}
                >
                  {lista.nomeLista}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500">Nenhuma lista disponível.</p>
          )}
        </div>

        <div className="flex justify-end">
          <button
            className={`px-6 py-2 rounded text-white font-medium cursor-pointer ${
              listaSelecionada
                ? "bg-[#007BB4] hover:bg-[#009BE2]"
                : "bg-gray-400 cursor-not-allowed"
            }`}
            disabled={!listaSelecionada}
            onClick={handleAvancar}
          >
            Avançar
          </button>
        </div>
      </div>
    </div>
  );
};

export default GerarRelatorio;
