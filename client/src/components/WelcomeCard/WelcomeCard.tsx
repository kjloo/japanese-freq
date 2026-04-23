import { FunctionComponent } from "react";
import { useNavigate } from "react-router-dom";

const WelcomeCard: FunctionComponent = () => {
  const navigate = useNavigate();

  const handleMineClick = () => {
    navigate("/mine");
  };

  const handleChatClick = () => {
    navigate("/chat");
  };

  return (
    <div className="card">
      <h1 className="title">Welcome</h1>
      <p className="text">Get started by clicking the button below</p>

      <button className="start-button" onClick={handleMineClick}>
        Mine
      </button>

      <button className="start-button" onClick={handleChatClick}>
        Chat
      </button>
    </div>
  );
};

export default WelcomeCard;
