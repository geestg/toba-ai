import { useEffect, useState } from "react";

export default function useTheme() {
  const [themeMode, setThemeMode] = useState(() => {
    return localStorage.getItem("theme") || "siang";
  });

  useEffect(() => {
    document.body.dataset.theme = themeMode;
    localStorage.setItem("theme", themeMode);
  }, [themeMode]);

  const toggleTheme = () => {
    setThemeMode((prev) =>
      prev === "siang" ? "malam" : "siang"
    );
  };

  return {
    themeMode,
    setThemeMode,
    toggleTheme,
  };
}