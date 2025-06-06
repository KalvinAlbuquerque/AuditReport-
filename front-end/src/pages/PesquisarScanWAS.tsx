import { useState } from "react";
import { Link } from "react-router-dom";

type Scan = {
  config_id: string;
  name: string;
  description: string;
  created_at: string;
  last_scan: {
    status: string;
    application_uri: string;
  };
};

const AlertModal = ({ message, onClose }: { message: string; onClose: () => void }) => {
  return (
    <div className="absolute top-1/3 left-1/2 transform -translate-x-1/2 w-1/3 bg-white p-6 rounded-lg shadow-md z-50">
      <h2 className="text-lg font-semibold mb-4">Alerta</h2>
      <p className="mb-4">{message}</p>
      <div className="flex justify-end">
        <button
          onClick={onClose}
          className="bg-[#007BB4] text-white px-4 py-2 rounded hover:bg-[#009BE2] cursor-pointer"
        >
          OK
        </button>
      </div>
    </div>
  );
};

const PesquisarScanWAS = () => {
  const [nomeUsuario, setNomeUsuario] = useState("");
  const [nomePasta, setNomePasta] = useState("");
  const [scans, setScans] = useState<Scan[]>([]);
  const [allscans, setAllscans] = useState<any>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [nomeLista, setNomeLista] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [alertMessage, setAlertMessage] = useState<string | null>(null); // Estado para mensagem do alerta

  const handlePesquisa = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:5000/scans/webapp/scansfromfolderofuser/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ nomeUsuario, nomePasta }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        setAlertMessage(`ERRO AO BUSCAR SCANS: ${errorText}`);
        throw new Error("Failed to fetch scans");
      }

      const data = await response.json();
      console.log("Scans:", data);
      setAllscans(data);
      setScans(data.items);
    } catch (err: unknown) {
      if (err instanceof Error) console.error("Error:", err.message);
      else console.error("An unknown error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setNomeLista("");
  };

  const handleAddToList = async () => {
    if (!nomeLista) {
      setAlertMessage("Por favor, insira um nome para a lista.");
      return;
    }

    if (scans.length === 0) {
      setAlertMessage("Nenhum scan disponível para adicionar.");
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:5000/listas/adicionarWAPPScanALista/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          nomeLista: nomeLista,
          scans: allscans,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Erro ao adicionar à lista: ${errorText}`);
      }

      setAlertMessage("Scans adicionados com sucesso!");
      closeModal();
    } catch (error: any) {
      setAlertMessage(error.message || "Erro desconhecido");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex"
      style={{
        backgroundImage: "url('/assets/fundo.png')",
        cursor: isLoading ? "wait" : "default",
      }}
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
        <h1 className="text-2xl font-bold mb-6">Pesquisar Scans - Web App</h1>

        <div className="flex flex-col space-y-4 max-w-sm">
          <div>
            <label className="block font-semibold mb-1 text-black">Nome Usuário</label>
            <input
              type="text"
              className="w-full p-2 border border-gray-300 rounded"
              id="nome-usuario"
              value={nomeUsuario}
              onChange={(e) => setNomeUsuario(e.target.value)}
            />
          </div>

          <div>
            <label className="block font-semibold mb-1 text-black">Nome Pasta</label>
            <input
              type="text"
              className="w-full p-2 border border-gray-300 rounded"
              id="nome-pasta"
              value={nomePasta}
              onChange={(e) => setNomePasta(e.target.value)}
            />
          </div>

          <button
            onClick={handlePesquisa}
            className="bg-[#007BB4] text-white px-4 py-2 rounded hover:bg-[#009BE2] w-fit cursor-pointer"
            disabled={isLoading}
          >
            {isLoading ? "Carregando..." : "Pesquisar"}
          </button>
        </div>

        <div className="flex flex-col items-end mt-6 space-y-2">
          <button
            onClick={openModal}
            className="bg-[#007BB4] text-white px-4 py-2 rounded hover:bg-[#009BE2] text-sm cursor-pointer"
          >
            + Adicionar à lista
          </button>
          <span className="text-sm text-gray-700">
            Total de scans: {scans.length}
          </span>
        </div>

        <div className="mt-4 h-80 bg-gray-100 rounded-lg overflow-y-auto">
          {scans.length > 0 ? (
            <ul className="space-y-4">
              {scans.map((scan) => (
                <li key={scan.config_id} className="p-4 bg-white rounded shadow-md">
                  <h3 className="text-lg font-semibold">{scan.name}</h3>
                  <p className="text-gray-600">{scan.description}</p>
                  <p className="text-sm text-gray-500">Created At: {new Date(scan.created_at).toLocaleString()}</p>
                  <p className="text-sm text-gray-500">Last Scan Status: {scan.last_scan.status}</p>
                </li>
              ))}
            </ul>
          ) : (
            <div className="flex items-center justify-center h-full">
              <p className="text-center text-gray-500">Lista Vazia</p>
            </div>
          )}
        </div>
      </div>

      {isModalOpen && (
        <div className="absolute top-1/3 left-1/2 transform -translate-x-1/2 w-1/3 bg-white p-6 rounded-lg shadow-md z-50">
          <h2 className="text-xl font-semibold mb-4">Nome da Lista</h2>
          <input
            type="text"
            className="w-full p-2 border border-gray-300 rounded mb-4"
            placeholder="Digite o nome da lista"
            value={nomeLista}
            onChange={(e) => setNomeLista(e.target.value)}
          />
          <div className="flex justify-end space-x-4">
            <button
              onClick={closeModal}
              className="bg-gray-300 text-black px-4 py-2 rounded hover:bg-gray-400 cursor-pointer"
            >
              Cancelar
            </button>
            <button
              onClick={handleAddToList}
              className="bg-[#007BB4] text-white px-4 py-2 rounded hover:bg-[#009BE2] cursor-pointer"
              disabled={isLoading}
            >
              {isLoading ? "Adicionando..." : "Adicionar"}
            </button>
          </div>
        </div>
      )}

      {alertMessage && (
        <AlertModal
          message={alertMessage}
          onClose={() => setAlertMessage(null)}
        />
      )}
    </div>
  );
};

export default PesquisarScanWAS;
