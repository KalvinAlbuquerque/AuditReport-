import React from 'react';

// Props que o modal vai receber
interface MissingVulnerabilitiesModalProps {
  isOpen: boolean; // Indica se o modal está aberto ou fechado
  onClose: () => void; // Função para fechar o modal
  title: string; // Título do modal (ex: "Vulnerabilidades Ausentes - Sites")
  content: string[]; // Array de strings com o conteúdo das vulnerabilidades
}

const MissingVulnerabilitiesModal: React.FC<MissingVulnerabilitiesModalProps> = ({
  isOpen,
  onClose,
  title,
  content,
}) => {
  if (!isOpen) return null; // Não renderiza nada se o modal não estiver aberto

  // Função para copiar o conteúdo para a área de transferência
  const handleCopy = () => {
    // Converte o array de strings em uma única string com quebras de linha
    const textToCopy = content.join('\n');
    navigator.clipboard.writeText(textToCopy)
      .then(() => {
        alert('Conteúdo copiado para a área de transferência!'); // Mensagem de sucesso
      })
      .catch((err) => {
        console.error('Falha ao copiar o conteúdo:', err);
        alert('Erro ao copiar o conteúdo.'); // Mensagem de erro
      });
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-xl max-w-lg w-full m-4">
        <h2 className="text-xl font-bold text-gray-800 mb-4">{title}</h2>
        <div className="max-h-60 overflow-y-auto border border-gray-300 p-3 rounded-md bg-gray-50 text-gray-700 text-sm mb-4">
          {content.length > 0 ? (
            content.map((line, index) => (
              <p key={index} className="mb-1">
                {line}
              </p>
            ))
          ) : (
            <p>Nenhuma vulnerabilidade ausente encontrada.</p>
          )}
        </div>
        <div className="flex justify-end space-x-3">
          <button
            onClick={handleCopy}
            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition duration-300"
          >
            Copiar
          </button>
          <button
            onClick={onClose}
            className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded transition duration-300"
          >
            Fechar
          </button>
        </div>
      </div>
    </div>
  );
};

export default MissingVulnerabilitiesModal;