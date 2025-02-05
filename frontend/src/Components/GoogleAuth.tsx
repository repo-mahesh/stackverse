import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { useUser } from "../UserContext";
import { GoogleLogin } from "@react-oauth/google";
// import jwtDecode from "jwt-decode";

const GoogleAuth = () => {
  const [error, setError] = useState<string | null>(null);
  const { loginUser } = useUser();
  const navigate = useNavigate();

  const handleLoginSuccess = async (credentialResponse: any) => {
    try {
      console.log("Google token response:", credentialResponse); // Debug log

      // Send token to Django backend
      const response = await fetch("http://127.0.0.1:8000/api/auth/google/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          credential: credentialResponse.credential, // Use credential from Google response
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.log("Login error:", errorData);
        throw new Error(errorData.error || "Login failed");
      }

      const data = await response.json();
      console.log("Login response:", data);

      if (data.user) {
        loginUser({
          email: data.user.email,
          name: data.user.name,
          is_premium: data.user.is_premium || false,
          picture: data.user.picture || null,
        });

        navigate("/dashboard");
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : "Login failed");
      console.error("Error during Google login:", error);
    }
  };

  return (
    <div>
      <GoogleLogin
        onSuccess={handleLoginSuccess}
        onError={() => setError("Google login failed")}
      />
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default GoogleAuth;
