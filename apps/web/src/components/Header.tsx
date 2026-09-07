import { MapPinned } from "lucide-react";
import Link from "next/link";
import { Show, UserButton } from "@clerk/nextjs";

export function Header() {
  return (
    <header className="flex min-h-13 items-center justify-between border-b border-[#e5e5e0] pb-5">
      <Link
        className="flex items-center gap-2 text-[19px] font-extrabold tracking-[-0.055em] text-[#1b1c1a] no-underline"
        href="/"
      >
        <MapPinned size={22} className="text-[#146a58]" />
        <span>Dubway</span>
      </Link>

      <div className="flex items-center gap-2">
        <Show when="signed-in">
          <UserButton />
        </Show>
      </div>
    </header>
  );
}
