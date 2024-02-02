import React, { useState } from "react";

export type User = {
    username: string;
    uri: string;
}

type UserProviderProps = {
    children: React.ReactNode;
};

export const UserContext = React.createContext<{
    user: User | null;
    setUser: React.Dispatch<React.SetStateAction<User | null>>;
}>({ user: null, setUser: () => { } });

export const UserProvider: React.FC<UserProviderProps> = ({
    children,
}: {
    children: React.ReactNode
}) => {
    const [user, setUser] = useState<User | null>(null);

    return (
        <UserContext.Provider value={{ user, setUser }}>
            {children}
        </UserContext.Provider>
    );
}