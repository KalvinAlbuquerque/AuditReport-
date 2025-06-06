import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import ConfirmDeleteModal from './ConfirmDeleteModal'; // Importe o modal de confirmação

const RelatoriosGerados = () => {
  const [dias, setDias] = useState("");
  const [relatorios, setRelatorios] = useState<Array<{ nome: string; id: string }>>([]);
  const [isLoading, setIsLoading] = useState(false);

  // --- ESTADOS PARA O MODAL DE CONFIRMAÇÃO ---
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [reportToDelete, setReportToDelete] = useState<{ id: string; nome: string } | null>(null);
  const [confirmAllDelete, setConfirmAllDelete] = useState(false); // Novo estado para diferenciar "excluir tudo"
  // ------------------------------------------

  const fetchRelatorios = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(
        "http://localhost:5000/relatorios/getRelatoriosGerados/"
      );

      if (response.ok) {
        const data = await response.json();
        setRelatorios(data);
      } else {
        console.error("Erro ao carregar relatórios:", await response.text());
        alert("Erro ao carregar relatórios.");
      }
    } catch (error) {
      console.error("Erro de rede:", error);
      alert("Erro de rede ao carregar relatórios.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchRelatorios();
  }, []);

  const handleAtualizar = () => {
    fetchRelatorios();
  };

  const downloadPDF = (idRelatorio: string, nomeRelatorio: string) => {
    const fileUrl = `/downloads/${idRelatorio}/main.pdf`;
    const link = document.createElement("a");
    link.href = fileUrl;
    link.setAttribute("download", `${nomeRelatorio}.pdf`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // --- FUNÇÕES PARA EXCLUSÃO INDIVIDUAL ---
  const handleDeleteClick = (id: string, nome: string) => {
    setReportToDelete({ id, nome });
    setConfirmAllDelete(false); // Garante que não é uma exclusão "tudo"
    setShowConfirmModal(true);
  };

  // --- FUNÇÃO PARA EXCLUIR TUDO (ABRIR MODAL) ---
  const handleDeleteAllClick = () => {
    setReportToDelete(null); // Limpa o relatório individual
    setConfirmAllDelete(true); // Indica que é uma exclusão "tudo"
    setShowConfirmModal(true);
  };

  const confirmDelete = async () => {
    setShowConfirmModal(false);
    setIsLoading(true);

    try {
      let response;
      let successMessage = "";
      let errorMessage = "";

      if (confirmAllDelete) { // Lógica para excluir tudo
        response = await fetch("http://localhost:5000/relatorios/deleteAllRelatorios/", {
          method: 'DELETE',
        });
        successMessage = "Todos os relatórios foram excluídos com sucesso!";
        errorMessage = "Erro ao excluir todos os relatórios.";
      } else if (reportToDelete) { // Lógica para excluir individualmente
        response = await fetch(
          `http://localhost:5000/relatorios/deleteRelatorio/${reportToDelete.id}`,
          {
            method: 'DELETE',
          }
        );
        successMessage = `Relatório "${reportToDelete.nome}" excluído com sucesso!`;
        errorMessage = `Erro ao excluir relatório "${reportToDelete.nome}".`;
      } else {
        // Isso não deveria acontecer se a lógica de estado estiver correta
        console.error("Nenhum relatório selecionado para exclusão.");
        alert("Nenhum relatório selecionado para exclusão.");
        return;
      }

      if (response.ok) {
        alert(successMessage);
        fetchRelatorios(); // Recarrega a lista
      } else {
        const errorText = await response.text();
        console.error(errorMessage, errorText);
        alert(`${errorMessage}: ${errorText}`);
      }
    } catch (error) {
      console.error("Erro de rede na exclusão:", error);
      alert(`Erro de rede: ${confirmAllDelete ? "ao excluir todos os relatórios" : "ao excluir o relatório"}.`);
    } finally {
      setIsLoading(false);
      setReportToDelete(null); // Limpa o estado
      setConfirmAllDelete(false); // Reseta a flag
    }
  };

  const cancelDelete = () => {
    setShowConfirmModal(false);
    setReportToDelete(null);
    setConfirmAllDelete(false);
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

      <div className="w-4/5 bg-[#f9fcfd] rounded-l-lg shadow-md p-8 flex flex-col">
        <h1 className="text-2xl font-bold mb-6 text-black">
          Relatórios Gerados
        </h1>

        <div className="flex items-center space-x-2 mb-4">
          <span className="text-black">Últimos</span>
          <input
            type="number"
            value={dias}
            onChange={(e) => setDias(e.target.value)}
            className="border border-gray-300 rounded px-2 py-1 w-20 focus:outline-none"
            placeholder="0"
          />
          <span className="text-black">dias</span>
          <button
            onClick={handleAtualizar}
            className="bg-[#007bb4] text-white px-4 py-2 rounded hover:bg-[#005f87] transition cursor-pointer ml-4"
            disabled={isLoading}
          >
            Atualizar
          </button>
          {/* --- BOTÃO DE EXCLUIR TUDO --- */}
          <button
            onClick={handleDeleteAllClick}
            className="bg-red-700 hover:bg-red-800 text-white px-4 py-2 rounded transition cursor-pointer ml-auto"
            disabled={isLoading || relatorios.length === 0} // Desabilita se estiver carregando ou não houver relatórios
          >
            Excluir Tudo
          </button>
          {/* ------------------------------ */}
        </div>

        <div className="flex-1 bg-gray-100 border border-blue-500 rounded-md p-4 overflow-y-auto">
          {isLoading ? (
            <div className="text-gray-500 text-center mt-20">
              Carregando relatórios...
            </div>
          ) : relatorios.length === 0 ? (
            <div className="text-gray-500 text-center mt-20">
              Nenhum relatório encontrado.
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {relatorios.map((relatorio) => (
                <div
                  key={relatorio.id}
                  className="bg-white p-4 rounded-lg shadow-md flex justify-between items-center transition-all duration-300"
                >
                  <button
                    onClick={() => downloadPDF(relatorio.id, relatorio.nome)}
                    className="text-blue-600 hover:underline cursor-pointer text-lg font-semibold bg-transparent border-none p-0 m-0"
                  >
                    {relatorio.nome}
                  </button>
                  <button
                    onClick={() => handleDeleteClick(relatorio.id, relatorio.nome)}
                    className="bg-red-500 hover:bg-red-600 text-white font-bold py-1 px-3 rounded text-sm transition duration-300"
                  >
                    Excluir
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* --- RENDERIZAÇÃO DO MODAL DE CONFIRMAÇÃO --- */}
      {(reportToDelete || confirmAllDelete) && (
        <ConfirmDeleteModal
          isOpen={showConfirmModal}
          onClose={cancelDelete}
          onConfirm={confirmDelete}
          message={
            confirmAllDelete
              ? "Tem certeza que deseja excluir TODOS os relatórios? Esta ação é irreversível e apagará todos os dados e arquivos."
              : `Tem certeza que deseja excluir o relatório "${reportToDelete?.nome}"? Esta ação é irreversível.`
          }
        />
      )}
      {/* ------------------------------------------- */}
    </div>
  );
};

export default RelatoriosGerados;