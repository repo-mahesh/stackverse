// import { createContext, useState, useEffect, ReactNode } from "react";
// import axiosInstance from "../api/AxiosInstance";  // Use the configured axios instance

// // Define User type
// interface User {
//     id: number;
//     username: string;
//     email: string;
//     is_premium: boolean;
// }

// // Define context type
// interface AuthContextType {
//     user: User | null;
//     setUser: (user: User | null) => void;
//     loading: boolean;
// }

// // Create AuthContext with a default value
// export const AuthContext = createContext<AuthContextType | undefined>(undefined);

// // Define props type for AuthProvider
// interface AuthProviderProps {
//     children: ReactNode;
// }

// export const AuthProvider = ({ children }: AuthProviderProps) => {
//     const [user, setUser] = useState<User | null>(null);
//     const [loading, setLoading] = useState(true);

//     // Fetch user only once when the app loads
//     useEffect(() => {
//         const fetchUser = async () => {
//             try {
//                 const response = await axiosInstance.get<User>("/api/auth/user_info/");
//                 setUser(response.data);
//             } catch (error) {
//                 setUser(null);
//             }
//             setLoading(false);
//         };
//         fetchUser();
//     }, []);

//     return (
//         <AuthContext.Provider value={{ user, setUser, loading }}>
//             {children}
//         </AuthContext.Provider>
//     );
// };


import { createContext, useState, useEffect, ReactNode } from "react";
import axiosInstance from "../api/AxiosInstance";

interface User {
    id: number;
    username: string;
    email: string;
    is_premium: boolean;
}

interface AuthContextType {
    user: User | null;
    setUser: (user: User | null) => void;
    loading: boolean;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
    const [user, setUser] = useState<User | null>(() => {
        // Initialize user from localStorage if available
        const savedUser = localStorage.getItem('user');
        return savedUser ? JSON.parse(savedUser) : null;
    });
    const [loading, setLoading] = useState(true);

    // Update localStorage whenever user state changes
    useEffect(() => {
        if (user) {
            localStorage.setItem('user', JSON.stringify(user));
        } else {
            localStorage.removeItem('user');
        }
    }, [user]);

    // Fetch user info and validate session
    useEffect(() => {
        const validateSession = async () => {
            try {
                const response = await axiosInstance.get<User>("/api/auth/user_info/");
                setUser(response.data);
            } catch (error) {
                // Clear user data if validation fails
                setUser(null);
                localStorage.removeItem('user');
            } finally {
                setLoading(false);
            }
        };

        validateSession();
    }, []);

    return (
        <AuthContext.Provider value={{ user, setUser, loading }}>
            {children}
        </AuthContext.Provider>
    );
};
