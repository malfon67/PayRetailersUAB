import React from "react";

export const AudioSpinner = () => {
  return (
    <div className="flex flex-col justify-center items-center space-y-2">
      <div className="w-6 h-6 bg-red-500 rounded-full animate-ping"></div>
    </div>
  );
};
