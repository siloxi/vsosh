"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { API_ENDPOINTS } from "@/lib/api";

export default function RedirectToRoot() {
  const router = useRouter();

  useEffect(() => {
    let mounted = true;

    async function sendRequestAndRedirect() {
      try {
        await fetch(API_ENDPOINTS.AUTH.LOGOUT, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ example: "data" }),
        });
      } catch (err) {
        // optional: handle error
        console.error(err);
      } finally {
        if (mounted) router.replace("/");
      }
    }

    sendRequestAndRedirect();

    return () => {
      mounted = false;
    };
  }, [router]);

  return null;
}
