"use client";

import { useUser } from "@auth0/nextjs-auth0";
import { useEffect } from "react";
import FormHeader from "@/components/FormHeader";

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, error, isLoading } = useUser();

  useEffect(() => {
    if (user) {
      fetch(`/api/user?email=${user.email}`)
        .then((response) => response.json())
        .then((data) => {
          if (!data) {
            fetch("/api/user", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ email: user.email }),
            });
          }
        });
    }
  }, [user]);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>{error.message}</div>;

  if (!user) {
    return <div>Access Denied</div>;
  }

  return (
    <>
      <FormHeader user={user} sub={""} />
      {children}
    </>
  );
}
