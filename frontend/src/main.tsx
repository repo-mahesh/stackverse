// import React from "react";
// import ReactDOM from "react-dom/client";
// import { BrowserRouter } from "react-router-dom";
// import { GoogleOAuthProvider } from "@react-oauth/google";
// import App from "./App";
// import { UserProvider } from "./UserContext";

// ReactDOM.createRoot(document.getElementById("root")!).render(
//   <React.StrictMode>
//     <BrowserRouter>
//       <GoogleOAuthProvider clientId="234041048530-dmqnkij4n6irdbmdlt6givpl2obid77q.apps.googleusercontent.com">
//         <UserProvider>
//           <App />
//         </UserProvider>
//       </GoogleOAuthProvider>
//     </BrowserRouter>
//   </React.StrictMode>
// );


import React from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router-dom";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { UserProvider } from "./UserContext";
import router from "./router"; // Import the router
import { AuthProvider } from "./auth/AuthContext";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId="234041048530-dmqnkij4n6irdbmdlt6givpl2obid77q.apps.googleusercontent.com">
      <AuthProvider>
      <UserProvider>
        <RouterProvider router={router} />
      </UserProvider>
      </AuthProvider>
    </GoogleOAuthProvider>
  </React.StrictMode>
);
