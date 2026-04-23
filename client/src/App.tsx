import { lazy, Suspense } from "react";
import { Routes } from "react-router";
import { BrowserRouter as Router, Route } from "react-router-dom";
import WelcomeCard from "./components/WelcomeCard/WelcomeCard";

const MineMenu = lazy(() => import("./components/MineMenu/MineMenu"));
const Chat = lazy(() => import("./components/Chat/Chat"));

function App() {
  return (
    <div className="app-container">
      <Router>
        <Suspense fallback={<div>Loading...</div>}>
          <div className="content">
            <Routes>
              <Route path="/" element={<WelcomeCard />} />
              <Route path="/anki" element={<div>Settings coming soon!</div>} />
              <Route path="/mine" element={<MineMenu />} />
              <Route path="/chat" element={<Chat />} />
              <Route path="*" element={<div>Page not found</div>} />
            </Routes>
          </div>
        </Suspense>
      </Router>
    </div>
  );
}

export default App;
