import Link from "next/link";
import { User } from "@auth0/nextjs-auth0/types";
export default function FormHeader({ user }: User) {
  return (
    <header className="sshadow-sm z-10 min-h-[10vh] bg-neutral">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-start items-center py-4 md:justify-start md:space-x-10">
          <div className="flex justify-start items-center lg:w-0 lg:flex-1">
            <Link href="/">
              <div className="flex flex-row items-center justify-center">
                <img
                  src={"stonks.png"}
                  alt="Stonks"
                  className="h-12 w-auto sm:h-12 mr-2"
                />
                <span className="font-bold">StonkSensei</span>
              </div>
            </Link>
          </div>

          <div className="hidden md:flex items-center justify-end md:flex-1 lg:w-0">
            {user ? (
              <a
                className="ml-8 whitespace-nowrap inline-flex items-center justify-center px-4 py-2 rounded-full shadow-sm text-base font-medium bg-neutral border border-white hover:outline"
                href="/auth/logout"
              >
                Logout
              </a>
            ) : (
              <a
                href="auth/login"
                className="ml-8 whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-full shadow-sm text-base font-medium text-neutral bg-positive"
              >
                Sign in
              </a>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
