import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

// Reaproveitando seu AlertModal
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

const CriarLista = () => {
  const [nomeLista, setNomeLista] = useState("");
  const [alertMessage, setAlertMessage] = useState<string | null>(null);
  const [redirectAfterAlert, setRedirectAfterAlert] = useState<boolean>(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!nomeLista.trim()) {
      setAlertMessage("Por favor, insira o nome da lista.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/listas/criarLista/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ nomeLista }),
      });

      if (response.status === 200) {
        setAlertMessage("Lista criada com sucesso!");
        setRedirectAfterAlert(true);
      } else if (response.status === 409) {
        const error = await response.text();
        setAlertMessage(error);
      } else {
        const error = await response.text();
        setAlertMessage(`Erro ao criar lista (${response.status}): ${error}`);
      }
    } catch (error) {
      console.error(error);
      setAlertMessage("Erro ao conectar com o servidor.");
    }
  };

  const handleCloseAlert = () => {
    setAlertMessage(null);
    if (redirectAfterAlert) {
      navigate("/lista-de-scans");
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

      {/* Formulário central */}
      <div className="w-4/5 flex items-center">
        <div className="bg-white rounded-lg shadow-md p-10 w-full max-w-2xl">
          <h1 className="text-2xl font-bold text-black mb-8">Criar Lista</h1>

          <form onSubmit={handleSubmit} className="flex items-center gap-4">
            <div className="flex-1">
              <label className="block text-black mb-1">Nome da Lista</label>
              <input
                type="text"
                value={nomeLista}
                onChange={(e) => setNomeLista(e.target.value)}
                className="w-full p-2 border rounded"
              />
            </div>

            <button
              type="submit"
              className="bg-[#007BB4] text-white px-6 py-2 rounded hover:bg-[#009BE2] cursor-pointer mt-6"
            >
              Criar
            </button>
          </form>
        </div>
      </div>

      {/* Modal de alerta */}
      {alertMessage && (
        <AlertModal
          message={alertMessage}
          onClose={handleCloseAlert}
        />
      )}
    </div>
  );
};

export default CriarLista;
