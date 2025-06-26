import React from "react";
import { PopupProps } from "../../common/types";
import "./Popup.scss";

const Popup: React.FC<PopupProps> = ({ open, message, onClose, actions }) => {
  if (!open) return null;
  return (
    <div className="popup-overlay">
      <div className="popup-box">
        <div className="popup-message">{message}</div>
        {actions && <div className="popup-actions">{actions}</div>}
        <button className="popup-close" onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default Popup; 