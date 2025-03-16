import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { LoadingSpinner } from "./loadingSpinner";

export const Summary = () => {
  const location = useLocation();
  const [htmlData, setHtmlData] = useState(null);
  const htmlReport = location.state?.report || "Error";

  console.log(`Report ${htmlReport}`);

  /*useEffect(() => {
    if (location.state?.data) {
      setTimeout(() => setHtmlData(location.state.data), 1000); 
      console.log()
    }
  }, [location.state]);*/

  return (
    <div className="h-full flex flex-col justify-start items-center space-y-10">
      <p className="text-2xl mt-2 font-bold">Informe final</p>
      {htmlReport ? (
        <div dangerouslySetInnerHTML={{ __html: htmlReport }}></div>
      ) : (
        <LoadingSpinner />
      )}
    </div>
  );
};
