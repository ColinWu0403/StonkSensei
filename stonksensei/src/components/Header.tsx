import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Header() {
  return (
    <header className="sshadow-sm z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-start items-center py-4 md:justify-start md:space-x-10">
          <div className="flex justify-start items-center lg:w-0 lg:flex-1">
            <Link href="/">
              <span className="sr-only">StreamLine</span>
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
            <a
              className="ml-8 whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-full shadow-sm text-base font-medium bg-neutral hover:outline"
              href="/auth/login"
            >
              Sign in
            </a>
            <a
              href="auth/login"
              className="ml-8 whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-full shadow-sm text-base font-medium text-neutral bg-positive"
            >
              Sign up
            </a>
          </div>
        </div>
      </div>
    </header>
  );
}
