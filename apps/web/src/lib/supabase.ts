import { createClient } from "@supabase/supabase-js";

export function createSupabaseClient(
  accessToken: () => Promise<string | null>,
) {
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
    {
      accessToken,
    },
  );
}
