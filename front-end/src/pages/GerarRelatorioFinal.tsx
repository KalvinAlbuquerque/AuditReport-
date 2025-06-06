import { useParams, useNavigate, Link } from "react-router-dom";
import { useState } from "react";
import MissingVulnerabilitiesModal from './MissingVulnerabilitiesModal'; // Certifique-se de que o caminho está correto

const AlertModal = ({ message, onClose }: { message: string; onClose: () => void }) => {
  return (
    <div className="fixed top-1/3 left-1/2 transform -translate-x-1/2 w-1/3 bg-white p-6 rounded-lg shadow-md z-50 border border-gray-300">
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

const RelatorioFinal = () => {
  const { idLista } = useParams();
  const navigate = useNavigate();

  const [alertMessage, setAlertMessage] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    secretaria: "",
    sigla: "",
    dataInicio: "",
    dataFinal: "",
    mesConclusao: "",
    anoConclusao: "",
    linkGoogleDrive: ""
  });

  // --- ESTADOS PARA GERENCIAR O MODAL ---
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalTitle, setModalTitle] = useState('');
  const [modalContent, setModalContent] = useState<string[]>([]);
  // ------------------------------------

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const downloadPDF = (idRelatorio: string) => {
    const fileUrl = `/downloads/${idRelatorio}/main.pdf`;
    const link = document.createElement("a");
    link.href = fileUrl;
    link.setAttribute("download", `Relatorio_${formData.secretaria}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  // FUNÇÃO ATUALIZADA: Agora, esta função APENAS OBTÉM o conteúdo
  // Ela não abre o modal diretamente.
  const getMissingVulnerabilitiesContent = async (idRelatorio: string, reportType: 'sites' | 'servers'): Promise<string[] | null> => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/listas/getRelatorioMissingVulnerabilities/?relatorioId=${idRelatorio}&type=${reportType}`
      );
      const data = await response.json();

      if (response.ok) {
        if (data.content && Array.isArray(data.content) && data.content.length > 0) {
          return data.content; // Retorna o array de linhas de conteúdo
        } else {
          console.log(`Nenhuma vulnerabilidade ausente encontrada para ${reportType} ou arquivo vazio.`);
          return null; // Retorna null se não houver conteúdo ou o arquivo estiver vazio
        }
      } else if (response.status === 404) {
        console.log(`Arquivo de vulnerabilidades ausentes para ${reportType} não encontrado.`);
        return null; // Retorna null se o arquivo não for encontrado (404)
      } else {
        console.error(`Erro ao verificar vulnerabilidades ausentes (${reportType}, ${response.status}): ${data.error || 'Erro desconhecido.'}`);
        return null; // Retorna null para outros erros
      }
    } catch (error) {
      console.error(`Erro de conexão com o servidor ao verificar vulnerabilidades para ${reportType}.`, error);
      return null; // Retorna null em caso de erro de rede
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      idLista,
      nomeSecretaria: formData.secretaria,
      siglaSecretaria: formData.sigla,
      dataInicio: formData.dataInicio,
      dataFim: formData.dataFinal,
      mes: formData.mesConclusao,
      ano: formData.anoConclusao,
      linkGoogleDrive: formData.linkGoogleDrive
    };

    try {

      const response = await fetch("http://127.0.0.1:5000/listas/gerarRelatorioDeLista/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const text = await response.text();

      if (response.ok) {
        const idRelatorioGerado = text;
        // downloadPDF(idRelatorioGerado);

        const sitesContent = await getMissingVulnerabilitiesContent(idRelatorioGerado, 'sites');
        const serversContent = await getMissingVulnerabilitiesContent(idRelatorioGerado, 'servers');

        let combinedContent: string[] = [];
        let modalDisplayTitle = "Vulnerabilidades Ausentes no Relatório"; // Título padrão

        if (sitesContent && sitesContent.length > 0) {
          combinedContent.push("--- VULNERABILIDADES DE SITES ---");
          combinedContent = combinedContent.concat(sitesContent);
        }

        if (serversContent && serversContent.length > 0) {
          if (sitesContent && sitesContent.length > 0) {
            combinedContent.push(""); // Adiciona uma linha em branco para separar se ambos existirem
          }
          combinedContent.push("--- VULNERABILIDADES DE SERVIDORES ---");
          combinedContent = combinedContent.concat(serversContent);
        }

        // Somente abra o modal se houver algum conteúdo combinado
        if (combinedContent.length > 0) {
          setModalTitle(modalDisplayTitle); // Define o título unificado
          setModalContent(combinedContent);
          setIsModalOpen(true);
        } else {
          setAlertMessage("Nenhuma vulnerabilidade ausente (sites ou servidores) foi encontrada com dados.");
          setIsModalOpen(true);
          console.log("Nenhuma vulnerabilidade ausente (sites ou servidores) foi encontrada com dados.");
          // Opcional: Se quiser dar um feedback para o usuário mesmo que nada seja encontrado
          // alert("Nenhuma vulnerabilidade ausente foi encontrada para este relatório.");
        }
        // --------------------------------------------------------------------

      } else {
        setAlertMessage(`Erro ao gerar relatório (${response.status}): ${text}`);
        setIsModalOpen(true);
      }
    } catch (error) {
      setAlertMessage("Erro ao conectar com o servidor.");
      setIsModalOpen(true);
      console.error(error);
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

      <div className="w-4/5 p-10 bg-white rounded-l-lg shadow-md">
        <h1 className="text-2xl font-bold text-black mb-8">Gerar Relatório</h1>

        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-6">
          <div>
            <label className="block text-black mb-1">Nome da Secretaria</label>
            <input
              type="text"
              name="secretaria"
              value={formData.secretaria}
              onChange={handleChange}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-black mb-1">Sigla</label>
            <input
              type="text"
              name="sigla"
              value={formData.sigla}
              onChange={handleChange}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-black mb-1">Data de Início</label>
            <input
              type="text"
              name="dataInicio"
              value={formData.dataInicio}
              onChange={handleChange}
              placeholder="Exemplo: 01 de Janeiro de 2023"
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-black mb-1">Mês de Conclusão</label>
            <input
              type="text"
              name="mesConclusao"
              value={formData.mesConclusao}
              onChange={handleChange}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-black mb-1">Data Final</label>
            <input
              type="text"
              name="dataFinal"
              value={formData.dataFinal}
              onChange={handleChange}
              placeholder="Exemplo: 01 de Janeiro de 2023"
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-black mb-1">Ano de Conclusão</label>
            <input
              type="text"
              name="anoConclusao"
              value={formData.anoConclusao}
              onChange={handleChange}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-black mb-1">Link da pasta do Google Drive</label>
            <input
              type="text"
              name="linkGoogleDrive"
              value={formData.linkGoogleDrive}
              onChange={handleChange}
              className="w-full p-2 border rounded"
            />
          </div>

          <div className="col-span-2 flex justify-end mt-4">
            <button
              type="submit"
              className="bg-[#007BB4] text-white px-6 py-2 rounded hover:bg-[#009BE2] cursor-pointer"
            >
              Concluir
            </button>
          </div>
        </form>
      </div>

      {/* --- RENDERIZAÇÃO DO MODAL --- */}
      <MissingVulnerabilitiesModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)} // Função para fechar o modal
        title={modalTitle}
        content={modalContent}
      />
      {/* ---------------------------- */}

      {isModalOpen && alertMessage && (
        <AlertModal
          message={alertMessage}
          onClose={() => {
            setIsModalOpen(false);
            setAlertMessage(null);
          }}
        />
      )}
    </div>
  );
};

export default RelatorioFinal;