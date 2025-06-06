import { Link } from "react-router-dom";  

const ScansPage = () => {
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

      {/* Conteúdo central */}
      <div className="w-4/5 flex items-center justify-center bg-white">
        <div className="grid grid-cols-3 gap-10 text-center">
          {/* Item 1 */}
          <Link to="/webapp-scans">
          <div className="hover:scale-105 transition">
            <img src="/assets/web.png" alt="Web Application Scans" className="mx-auto h-25 mb-4 cursor-pointer" />
            <p className="text-black font-medium !font-black">Web Application Scans</p>
          </div>
          </Link>

          {/* Item 2 */}
          <Link to="/vm-scans">
          <div className="hover:scale-105 transition">
            <img src="/assets/vm.png" alt="Vulnerability Management Scans" className="mx-auto h-25 mb-4 cursor-pointer" />
            <p className="text-black font-medium !font-black">Vulnerability Management Scans</p>
          </div>
          </Link>

          {/* Item 3 */}
          <Link to='/lista-de-scans'>
          <div className="hover:scale-105 transition">
            <img src="/assets/listas.png" alt="Listas de Scans" className="mx-auto h-25 mb-4 cursor-pointer" />
            <p className="text-black font-medium !font-black">Listas de Scans</p>
          </div>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ScansPage;