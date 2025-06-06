import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

type Lista = {
  idLista: string;
  nomeLista: string;
};

const ListaDeScans = () => {
  const [listas, setListas] = useState<Lista[]>([]);
  const [listaSelecionada, setListaSelecionada] = useState<Lista | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchListas = async () => {
      try {
        const response = await fetch("http://localhost:5000/listas/getTodasAsListas/");
        if (!response.ok) throw new Error("Erro ao buscar listas");

        const data = await response.json();
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

  const handleRemoverLista = async () => {
    if (!listaSelecionada) return;

    const confirmacao = window.confirm(`Tem certeza que deseja remover a lista "${listaSelecionada.nomeLista}"?`);
    if (!confirmacao) return;

    try {
      const response = await fetch("http://localhost:5000/listas/excluirLista/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ idLista: listaSelecionada.idLista }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Erro ao remover lista: ${errorText}`);
      }

      // Atualiza a lista após remover
      setListas((prevListas) => prevListas.filter(l => l.idLista !== listaSelecionada.idLista));
      setListaSelecionada(null);
      alert("Lista removida com sucesso!");
    } catch (error) {
      console.error("Erro ao remover lista:", error);
      alert("Ocorreu um erro ao remover a lista.");
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex"
      style={{ backgroundImage: "url('/assets/fundo.png')" }}
    >
      {/* Sidebar azul à esquerda */}
      <div className="w-1/5 bg-white-800 text-white flex items-center justify-center p-4">
        <Link to="/">
          <img
            src="/assets/logocogel.jpg"
            alt="COGEL Logo"
            className="w-32 h-auto"
          />
        </Link>
      </div>

      {/* Conteúdo principal */}
      <div className="w-4/5 p-8 bg-[#F9FCFD] rounded-l-lg shadow-md flex flex-col">
        {/* Título */}
        <h1 className="text-2xl font-bold text-black mb-4">Listas de Scans</h1>

        {/* Botões alinhados à direita */}
        <div className="flex justify-end space-x-4 mb-4">
          
          <button
            onClick={() => navigate("/criar-lista")}
            className="bg-[#007BB4] text-white px-4 py-2 rounded hover:bg-[#005f87] transition cursor-pointer"
          >
            + Adicionar Lista
          </button>

          <button
            disabled={!listaSelecionada}
            onClick={() => {
              if (listaSelecionada) {
                navigate(`/editar-lista`, {
                  state: {
                    nome: listaSelecionada.nomeLista,
                    id: listaSelecionada.idLista,
                  },
                });
              }
            }}
            className={`px-4 py-2 rounded transition ${
              listaSelecionada
                ? "bg-[#007BB4] text-white hover:bg-[#005f87] cursor-pointer"
                : "bg-gray-400 text-white cursor-not-allowed"
            }`}
          >
            Editar Lista
          </button>

          <button
            disabled={!listaSelecionada}
            onClick={handleRemoverLista}
            className={`px-4 py-2 rounded transition ${
              listaSelecionada
                ? "bg-[#007BB4] text-white hover:bg-[#005f87] cursor-pointer ring-2 ring-white"
                : "bg-gray-400 text-white cursor-not-allowed"
            }`}
          >
            Remover Lista
          </button>
        </div>

        {/* Área da lista */}
        <div className="bg-gray-100 flex-1 rounded-md p-4 overflow-y-auto">
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
            <div className="flex items-center justify-center h-full">
              <p className="text-gray-500 text-center">Nenhuma lista disponível.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ListaDeScans;
