import Link from "next/link";
import { User } from "@auth0/nextjs-auth0/types";
export default function FormHeader({ user }: User) {
  return (
    <header className="sshadow-sm z-10 bg-neutral">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-start items-center py-4 md:justify-start md:space-x-10">
          <div className="flex justify-start items-center lg:w-0 lg:flex-1">
            <Link href="/">
              <span className="sr-only">StonkSensei</span>
              <svg
                className="h-8 w-auto sm:h-10"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M13.5 6L10 18.5M6.5 8.5L3 12L6.5 15.5M17.5 8.5L21 12L17.5 15.5"
                  stroke="#FFFFFF"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
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
