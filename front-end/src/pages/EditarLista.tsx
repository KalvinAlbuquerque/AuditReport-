import { useState, useEffect } from "react";
import { useLocation, Link } from "react-router-dom";

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

const EditarLista = () => {
  const { state } = useLocation();
  const { nome, id } = state || {};

  const [nomeLista, setNomeLista] = useState("");
  const [alertMessage, setAlertMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [scans, setScans] = useState<string[]>([]);
  const [vmScanInfo, setVmScanInfo] = useState<string[] | null>(null);

  const showAlert = (message: string) => {
    setAlertMessage(message);
  };

  const closeAlert = () => {
    setAlertMessage(null);
  };

  useEffect(() => {
    if (nome) {
      setNomeLista(nome);
    }
  }, [nome]);

  useEffect(() => {
    const fetchScans = async () => {
      if (!nome) return;

      try {
        const response = await fetch("http://localhost:5000/listas/getScansDeLista/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ nomeLista: nome }),
        });

        if (response.ok) {
          const data = await response.json();
          setScans(data);
        } else {
          const errorText = await response.text();
          console.error("Erro ao buscar scans:", errorText);
        }
      } catch (error) {
        console.error("Erro de rede:", error);
      }
    };

    const fetchVMScanInfo = async () => {
      if (!nome) return;

      try {
        const response = await fetch("http://localhost:5000/listas/getVMScansDeLista/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ nomeLista: nome }),
        });

        if (response.ok) {
          const data = await response.json();
          setVmScanInfo(data);
        } else {
          const errorText = await response.text();
          console.error("Erro ao buscar info de VM Scan:", errorText);
        }
      } catch (error) {
        console.error("Erro de rede:", error);
      }
    };

    fetchScans();
    fetchVMScanInfo();
  }, [nome]);

  const handleAtualizar = async () => {
    setIsLoading(true);
    if (!nomeLista || !id) {
      showAlert("Nome da lista ou ID não encontrado.");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/listas/editarNomeLista/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id: id,
          novoNome: nomeLista,
        }),
      });

      if (response.ok) {
        showAlert("Nome da lista atualizado com sucesso!");
      } else {
        const errorText = await response.text();
        showAlert(`Erro ao atualizar lista: ${errorText}`);
      }
    } catch (error) {
      showAlert("Erro na requisição: " + error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRemover = async () => {
    if (!nomeLista) {
      showAlert("Nome da lista não disponível.");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/listas/limparScansDeLista/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ nomeLista }),
      });

      if (response.ok) {
        setScans([]); // Limpa os scans do estado local
        showAlert("Lista de scans limpa com sucesso!");
      } else {
        const errorText = await response.text();
        showAlert(`Erro ao limpar lista: ${errorText}`);
      }
    } catch (error) {
      showAlert("Erro na requisição: " + error);
    }
  };

  const handleRemoverVM = async () => {
    if (!nomeLista) {
      showAlert("Nome da lista não disponível.");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/listas/limparVMScansDeLista/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ nomeLista }),
      });

      if (response.ok) {
        setVmScanInfo(null); // Limpa os scans do estado local
        showAlert("Lista de scans limpa com sucesso!");
      } else {
        const errorText = await response.text();
        showAlert(`Erro ao limpar lista: ${errorText}`);
      }
    } catch (error) {
      showAlert("Erro na requisição: " + error);
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

      <div className="w-4/5 bg-[#F9FCFD] rounded-l-lg shadow-md p-8 flex flex-col">
        <h1 className="text-2xl font-bold mb-6 text-black">Editar Lista</h1>

        <div className="flex items-end mb-6 space-x-4">
          <div>
            <label className="block text-black font-medium mb-1">Nome da Lista</label>
            <input
              type="text"
              value={nomeLista}
              onChange={(e) => setNomeLista(e.target.value)}
              className="border border-gray-300 rounded px-4 py-2 w-72 focus:outline-none"
            />
          </div>

          <button
            onClick={handleAtualizar}
            className="bg-[#007BB4] text-white px-6 py-2 rounded hover:bg-[#005f87] transition cursor-pointer"
            disabled={isLoading}
          >
            Atualizar
          </button>
        </div>

        <div className="flex justify-end mb-4">
          <button
            onClick={handleRemover}
            className="bg-[#007BB4] text-white px-6 py-2 rounded hover:bg-[#005f87] transition cursor-pointer"
            disabled={isLoading}
          >
            Limpar Lista de WAS
          </button>
        </div>

        {/* Bloco de Scans */}
        <div className="bg-gray-100 border border-blue-500 rounded-md flex-1 p-4">
          {scans.length === 0 ? (
            <div className="text-gray-500 mt-4 text-center flex items-center justify-center h-full">
              Sem scans na lista.
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {scans.map((scan, index) => (
                <div key={index} className="bg-white p-4 rounded-lg shadow-md transition-all duration-300">
                  <p className="text-black">{scan}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="flex justify-end mt-4">
          <button
            onClick={handleRemoverVM}
            className="bg-[#007BB4] text-white px-6 py-2 rounded hover:bg-[#005f87] transition cursor-pointer"
            disabled={isLoading}
          >
            Limpar Lista de VM
          </button>
        </div>

        {/* Novo bloco de VM Scan Info */}
        <div className="bg-gray-100 border border-blue-500 rounded-md p-4 mt-6">
          {vmScanInfo ? (
            <div className="bg-white p-4 rounded-lg shadow-md transition-all duration-300">
              <p className="text-black font-semibold">Nome do Scan:</p>
              <p className="text-black">{vmScanInfo[0]}</p>
              <p className="text-black font-semibold mt-2">Criado Por:</p>
              <p className="text-black">{vmScanInfo[1]}</p>
            </div>
          ) : (
            <div className="text-gray-500 flex items-center justify-center h-full">
              Sem informações de VM Scan disponíveis.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EditarLista;
