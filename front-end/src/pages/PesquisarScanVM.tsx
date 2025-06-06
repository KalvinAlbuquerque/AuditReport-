import { useState } from "react";
import { Link } from "react-router-dom";

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


const PesquisarScanVM = () => {
  const [nomeScan, setNomeScan] = useState("");
  const [resultado, setResultado] = useState<{ name: string; owner: string, id: string, id_scan: string } | null>(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [nomeLista, setNomeLista] = useState("");
  const [alertMessage, setAlertMessage] = useState<string | null>(null); // Estado para mensagem do alerta
  const [isLoading, setIsLoading] = useState(false);

  const handleAddToList = async () => {
    if (!nomeLista) {
      setAlertMessage("Por favor, insira um nome para a lista.");
      return;
    }

    if (resultado === null) {
      setAlertMessage("Nenhum scan disponível para adicionar.");
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:5000/listas/adicionarVMScanALista/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          nomeLista: nomeLista,
          nomeScan: resultado?.name,
          idScan: resultado?.id,
          criadoPor: resultado?.owner,
          idNmr: resultado?.id_scan,
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

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setNomeLista("");
  };

  const handlePesquisa = async () => {
    if (!nomeScan.trim()) {
      setErro("Por favor, insira o nome do scan.");
      setResultado(null);
      return;
    }

    setCarregando(true);
    setErro(null);
    setResultado(null);

    try {
      const response = await fetch("http://localhost:5000/scansvm/getScanByName/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: nomeScan,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText);
      }

      const data = await response.json();

      // Pega só name e owner do retorno
      const id = data.uuid ?? "Não informado";
      const name = data.name ?? "Não informado";
      const owner = data.owner ?? "Não informado";
      const id_scan = data.id ?? "Não informado";

      setResultado({ name, owner, id, id_scan });
    } catch (error: any) {
      setErro(error.message || "Erro ao conectar com o servidor.");
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex"
      style={{
        backgroundImage: "url('/assets/fundo.png')",
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

      <div className="w-4/5 bg-white rounded-l-lg p-8">
        <h1 className="text-2xl font-bold mb-6">
          Pesquisar Scans - Vulnerability Management
        </h1>

        <div className="flex flex-col space-y-2 max-w-md mx-auto mt-10">
          <label className="block font-semibold text-black">Nome do Scan</label>
          <input
            type="text"
            className="w-full p-2 border border-gray-300 rounded"
            placeholder="Digite o nome do scan"
            value={nomeScan}
            onChange={(e) => setNomeScan(e.target.value)}
          />
          <div className="flex justify-center">
            <button
              onClick={handlePesquisa}
              className="bg-[#007BB4] text-white px-6 py-2 rounded hover:bg-[#009BE2] cursor-pointer"
            >
              Pesquisar
            </button>
          </div>
        </div>

        <div className="flex justify-end mt-6">
          <button onClick={openModal} className="bg-[#007BB4] text-white px-4 py-2 rounded hover:bg-[#009BE2] text-sm cursor-pointer">
            + Adicionar à lista
          </button>
        </div>

        <div className="mt-4 h-[400px] bg-gray-100 rounded-lg overflow-y-auto p-4">
            {carregando && (
            <div className="flex items-center justify-center h-full">
              <p className="text-gray-500 text-center">Carregando...</p>
            </div>
            )}
          {erro && <div className="flex items-center justify-center h-full">
            <p className="text-red-500 text-center">{erro}</p>
          </div>}
          {resultado && (
            <div className="space-y-2 text-gray-800">
              <p><strong>Nome do Scan:</strong> {resultado.name}</p>
              <p><strong>Criado por:</strong> {resultado.owner}</p>
            </div>
          )}
          {!carregando && !erro && !resultado && (
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

export default PesquisarScanVM;
