import React from "react";
import clsx from "clsx";

export const Button = ({ children, onClick, variant = "default", className = "" }) => {
  const baseStyles = "px-4 py-2 rounded-xl text-sm font-medium transition-all";
  const variants = {
    default: "bg-blue-600 text-white hover:bg-blue-700",
    outline: "border border-blue-600 text-blue-600 hover:bg-blue-50",
  };

  return (
    <button
      onClick={onClick}
      className={clsx(baseStyles, variants[variant], className)}
    >
      {children}
    </button>
  );
};
