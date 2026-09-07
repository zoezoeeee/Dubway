"use client";
import { Sparkles } from "lucide-react";
import { SignInButton, Show, useUser } from "@clerk/nextjs";
import { formatDublinDate } from "@/util/data";

export function WelcomePanel() {
  const { user } = useUser();

  return (
    <>
      <Show when="signed-out">
        <section className="mx-auto w-[min(500px,100%)] py-[18vh]">
          <div className="mb-5 grid h-9 w-9 place-items-center rounded-lg border border-[#cde3da] bg-[#e4f0eb] text-[#146a58]">
            <Sparkles size={22} />
          </div>

          <p className="mb-2.5 text-[11px] font-bold uppercase tracking-[0.08em] text-[#969791]">
            Dublin, organised
          </p>

          <h1 className="m-0 text-[clamp(34px,5vw,52px)] font-[750] tracking-[-0.07em] text-[#1b1c1a] leading-[0.98]">
            Your everyday Dublin.
          </h1>

          <p className="mt-2.75 max-w-110 text-[15px] text-[#686963]">
            Keep regular routes, places, and everyday routines in one calm
            dashboard.
          </p>

          <SignInButton mode="modal">
            <button className="primary-button mt-6">Get started</button>
          </SignInButton>
        </section>
      </Show>

      <Show when="signed-in">
        <section className="flex justify-between gap-8 py-11.5">
          <div>
            <p className="mb-2.5 text-[11px] font-bold uppercase tracking-[0.08em] text-[#969791]">
              {formatDublinDate()}
            </p>
            <h1 className="m-0 text-[clamp(34px,5vw,52px)] font-[750] tracking-[-0.07em] text-[#1b1c1a] leading-[0.98]">
              Your everyday Dublin
            </h1>
            <p className="mt-2.75 max-w-110 text-[15px] text-[#686963]">
              {user?.firstName
                ? `Ready when you are, ${user.firstName}.`
                : "Routes, regular places, and the routines that keep your week moving."}
            </p>
          </div>
        </section>
      </Show>
    </>
  );
}
